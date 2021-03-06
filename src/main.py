from src.spotipy_manager import *
import tkinter as tk
from tkinter.ttk import Progressbar, Style
import threading
import pickle
from datetime import datetime, timezone


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.resizable(0, 0)
        self.master.protocol("WM_DELETE_WINDOW", self.save_and_exit)

        self.main_frame = tk.Frame(master)
        self.main_frame.grid(row=0, column=0, columnspan=2, padx=10)
        self.spm = SpotipyManager()

        # Set default settings
        self.settings = {'cache': True, 'playlists_exclude': []}
        # Load settings from file
        try:
            with open('./data/settings.pickle', 'rb') as file:
                self.settings = pickle.load(file)
        except FileNotFoundError:
            pass

        self.cache = {'date_modified': datetime.now(timezone.utc), 'data': None}
        # Load cache from file
        try:
            with open('./data/cache-playlists.pickle', 'rb') as file:
                self.cache = pickle.load(file)
        except FileNotFoundError:
            pass

        # Thread created even if settings disable cache in case setting is changed later on.
        cache_thread = threading.Thread(target=self.cache_playlists_helper)
        cache_thread.daemon = True
        cache_thread.start()

        self.create_base_widgets()

    def save_and_exit(self):
        """
        Saves self.settings to a file and exits
        """
        with open('./data/settings.pickle', 'wb+') as file:
            pickle.dump(self.settings, file)
        with open('./data/cache-playlists.pickle', 'wb+') as file:
            pickle.dump(self.cache, file)
        self.master.destroy()

    def cache_playlists_helper(self):
        """
        Sets cache data to correct format of playlists. Function should only called in a thread.
        """
        playlists = self.spm.get_spotipy_client().current_user_playlists()
        self.cache['data'] = self.spm.cache_songs_in_playlists(playlists)

    def create_base_widgets(self):
        """
        Initialises all widgets and puts onto the grid the widgets that appear at the start of the application.
        """
        # GUI widgets
        header = tk.Label(self.main_frame, text="Spotify Playlist Searcher", width=50)
        header.grid(row=0, column=0, columnspan=2, pady=10)

        settings_btn = tk.Button(self.main_frame, text="Settings", command=lambda: self.create_settings_widgets())
        settings_btn.grid(row=0, column=1, sticky=tk.E)

        # Song Search
        self.create_song_widgets()

        # Playlist Search
        self.create_playlist_widgets()

    def create_song_widgets(self):
        """
        Initialises widgets related to searching for songs on Spotify
        """
        song_search = tk.Frame(self.main_frame)
        song_search.grid(row=1, column=0, columnspan=2, rowspan=3)

        self.search_bar = tk.Entry(song_search, width=50)
        self.search_bar.grid(row=0, column=0)
        self.search_bar.focus()
        # Lambda expression is necessary because of self arg
        self.search_bar.bind('<Return>', lambda x: self.search_submit())

        search_bar_submit = tk.Button(song_search, text="Search for Song", command=self.search_submit)
        search_bar_submit.grid(row=0, column=1)

        search_results_label = tk.Label(song_search, text='Song Results')
        search_results_label.grid(row=1, column=0, columnspan=2)

        self.search_results = tk.Listbox(song_search, width=50)
        self.search_results.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        self.search_results.bind('<<ListboxSelect>>', lambda x: self.check_song_selection())
        self.search_results.bind('<Return>', lambda x: self.search_playlists())

    def create_playlist_widgets(self):
        """
        Initialises widgets related to searching through playlists for a song. Does not display the playlist results listbox and label.
        """
        playlist_search = tk.Frame(self.main_frame)
        playlist_search.grid(row=4, column=0, columnspan=2, rowspan=3, pady=(0, 10))

        self.playlist_search_btn = tk.Button(playlist_search, text="Search Playlists For Song", command=self.search_playlists, state=tk.DISABLED)
        self.playlist_search_btn.grid(row=0, column=0, columnspan=2, pady=5)

        # Will be displayed at later point
        self.playlist_label = tk.Label(playlist_search, text='Playlist Results')
        self.playlist_results = tk.Listbox(playlist_search, width=50)

        # Loading Bar
        loading_style = Style()
        loading_style.theme_use('alt')
        loading_style.configure('TProgressbar', thickness=10)
        self.playlist_loading = Progressbar(self.main_frame, style='TProgressbar', mode='indeterminate', length=150, maximum=50)

    def search_submit(self):
        """
        Takes search entered and displays the songs in the listbox. Also, initialises a dict mapping the song names to their Spotify uri.
        """
        # Disables playlist button and clears search results
        self.search_results.delete(0, tk.END)
        self.playlist_search_btn['state'] = tk.DISABLED

        self.song_dict = {}  # Maps how song appears in listbox to the song's uri for playlist searching
        search = self.search_bar.get()
        if search:
            paging_object = self.spm.get_spotipy_client().search(search)
            tracks = paging_object['tracks']['items']

            for track in tracks:

                artists = track['artists']
                artists_str = ''
                for i, artist in enumerate(artists):
                    artists_str += f'{artist["name"]}'
                    if not i == len(artists) - 1:
                        artists_str += ', '

                output_str = f"{track['name']}    -    {artists_str}"
                self.search_results.insert(tk.END, output_str)
                self.song_dict[output_str] = track['uri']

    def check_song_selection(self):
        """
        If a song has been selected in the song listbox, then the button to search through the playlists can be pressed.
        """
        if self.search_results.curselection():
            self.playlist_search_btn['state'] = tk.NORMAL
        else:
            self.playlist_search_btn['state'] = tk.DISABLED

    def search_playlists(self):
        """
        Searches through the playlists for the selected song and displays the results in a new listbox.
        """
        def threaded_search():
            # If nothing is selected, selection_get() throws an error
            try:
                song_selected = self.search_results.selection_get()
            except:
                return

            song_uri = self.song_dict[song_selected]
            # If caching is enabled and the cache has data, use cached data
            if self.settings['cache'] and not self.cache['data'] is None:
                playlist_uris = set()
                for playlist_uri in self.cache['data']:
                    if song_uri in self.cache['data'][playlist_uri] and playlist_uri not in self.settings['playlists_exclude']:
                        playlist_uris.add(playlist_uri)
            else:
                playlist_uris = self.spm.find_song_in_playlists(song_uri, self.settings['playlists_exclude'])
            playlist_names = [self.spm.get_name_from_uri(uri) for uri in playlist_uris]

            # Displaying playlist listbox and then inserting playlists
            self.playlist_label.grid(row=1, column=0, columnspan=2, pady=(10, 5))
            self.playlist_results.grid(row=2, column=0, columnspan=2, padx=5)
            self.playlist_results.delete(0, tk.END)
            if playlist_names:
                playlist_names.sort()
                for name in playlist_names:
                    self.playlist_results.insert(tk.END, name)
            else:
                self.playlist_results.insert(tk.END, 'The selected song is not found in any of your playlists.')
            # Remove Loading Bar
            self.playlist_loading.stop()
            self.playlist_loading.grid_forget()

        # Start and draw Loading Bar
        self.playlist_loading.grid(row=8, column=0, columnspan=2, sticky=tk.E, pady=(0, 10))
        self.playlist_loading.start()

        # Initialize thread
        thread = threading.Thread(target=lambda: threaded_search())
        thread.daemon = True  # Prevents thread from running after application closes
        thread.start()

    def create_settings_widgets(self):
        """
        Creates a new window for settings related to the application
        """
        self.settings_window = tk.Toplevel(self.master)
        self.settings_window.resizable(0, 0)
        self.settings_window.title('Settings')
        self.settings_window.protocol("WM_DELETE_WINDOW", self.exit_settings)

        settings_frame = tk.Frame(self.settings_window)
        settings_frame.grid(row=0, column=0)

        settings_header = tk.Label(settings_frame, text='Settings')
        settings_header.grid(row=0, column=0, columnspan=2)

        # TODO Implement caching
        self.cache_toggle_val = tk.BooleanVar()
        self.cache_toggle_val.set(self.settings['cache'])
        cache_toggle = tk.Checkbutton(settings_frame, variable=self.cache_toggle_val,
                                      text='Enable Caching (Inaccurate results if the playlist have been modified recently)')
        cache_toggle.grid(row=1, column=0, sticky=tk.W)

        playlist_options_frame = tk.LabelFrame(settings_frame, text='Playlists Searched')
        playlist_options_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10))

        self.options_toggle_val = tk.BooleanVar()
        self.options_toggle_val.set(True)
        playlist_options_toggle = tk.Checkbutton(playlist_options_frame, text='Toggle all playlists', variable=self.options_toggle_val, command=self.playlists_toggle)
        playlist_options_toggle.grid(row=0, column=0, columnspan=2, sticky=tk.W)

        # TODO Add scrollbar if too many playlist options
        playlists = self.spm.get_spotipy_client().current_user_playlists()
        self.playlist_exclude_data = []  # List of Tuple (Playlist_URI, BooleanVar)
        # Generates checkboxes for each user playlist
        for i, playlist in enumerate(playlists['items']):
            playlist_name = f'{playlist["name"]}'

            is_playlist_excluded = tk.BooleanVar()
            if playlist['uri'] in self.settings['playlists_exclude']:
                is_playlist_excluded.set(False)
            else:
                is_playlist_excluded.set(True)
            self.playlist_exclude_data.append((playlist["uri"], is_playlist_excluded))
            option = tk.Checkbutton(playlist_options_frame, text=playlist_name, variable=self.playlist_exclude_data[i][1])
            option.grid(row=i+1, column=0, columnspan=2, sticky=tk.W)

        reset_btn = tk.Button(settings_frame, text='Reset Settings', command=self.reset_settings)
        reset_btn.grid(row=4, column=0, columnspan=2, pady=(0, 10))

    def exit_settings(self):
        """
        Saves settings to self.settings before exiting.
        """
        self.settings['cache'] = self.cache_toggle_val.get()
        self.settings['playlists_exclude'] = [check_val[0] for check_val in self.playlist_exclude_data if not check_val[1].get()]
        self.settings_window.destroy()

    def reset_settings(self):
        """
        Resets settings to default values.
        """
        self.settings = {'cache': True, 'playlists_exclude': []}
        self.cache_toggle_val.set(True)
        for val in self.playlist_exclude_data:
            val[1].set(True)

    def playlists_toggle(self):
        """
        Toggles all of the playlist checkboxes on or off
        """
        toggle_val = self.options_toggle_val.get()
        for check_val in self.playlist_exclude_data:
            check_val[1].set(toggle_val)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Spotify Playlist Searcher')
    app = Application(master=root)
    app.mainloop()

