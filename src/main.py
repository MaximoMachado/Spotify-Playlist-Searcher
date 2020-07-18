from src.spotipy_manager import *
import tkinter as tk


class Application(tk.Frame):
    # TODO Documentation
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.main_frame = tk.Frame(master)
        self.main_frame.grid(row=0, column=0, columnspan=2, padx=10)
        self.spm = SpotipyManager()

        self.create_base_widgets()

    def create_base_widgets(self):
        # GUI widgets
        self.header = tk.Label(self.main_frame, text="Spotify Playlist Searcher", width=50)
        self.header.grid(row=0, column=0, columnspan=2, pady=10)

        self.settings_btn = tk.Button(self.main_frame, text="Settings")
        self.settings_btn.grid(row=0, column=1, sticky=tk.E)

        # Song Search
        self.create_song_widgets()

        # Playlist Search
        self.create_playlist_widgets()

    def create_song_widgets(self):
        self.song_search = tk.Frame(self.main_frame)
        self.song_search.grid(row=1, column=0, columnspan=2, rowspan=3)

        self.search_bar = tk.Entry(self.song_search, width=50)
        self.search_bar.grid(row=0, column=0)
        self.search_bar.focus()
        self.search_bar.bind('<Return>', lambda x: self.search_submit())

        self.search_bar_submit = tk.Button(self.song_search, text="Search for Song", command=self.search_submit)
        self.search_bar_submit.grid(row=0, column=1)

        self.search_results_label = tk.Label(self.song_search, text='Song Results')
        self.search_results_label.grid(row=1, column=0, columnspan=2)

        self.search_results = tk.Listbox(self.song_search, width=50)
        self.search_results.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        self.search_results.bind('<<ListboxSelect>>', lambda x: self.check_song_selection())
        self.search_results.bind('<Return>', lambda x: self.search_playlists())

    def create_playlist_widgets(self):
        self.playlist_search = tk.Frame(self.main_frame)
        self.playlist_search.grid(row=4, column=0, columnspan=2, rowspan=3, pady=(0, 10))

        self.playlist_search_btn = tk.Button(self.playlist_search, text="Search Playlists For Song", command=self.search_playlists, state=tk.DISABLED)
        self.playlist_search_btn.grid(row=0, column=0, columnspan=2, pady=5)

        # Will be displayed at later point
        self.playlist_label = tk.Label(self.playlist_search, text='Playlist Results')
        self.playlist_results = tk.Listbox(self.playlist_search, width=50)

    def search_submit(self):
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
        if self.search_results.curselection():
            self.playlist_search_btn['state'] = tk.NORMAL
        else:
            self.playlist_search_btn['state'] = tk.DISABLED

    def search_playlists(self):
        # If nothing is selected, selection_get() throws an error
        try:
            song_selected = self.search_results.selection_get()
        except:
            return

        song_uri = self.song_dict[song_selected]
        playlist_uris = self.spm.find_song_in_playlists(song_uri)
        playlist_names = [self.spm.get_name_from_uri(uri) for uri in playlist_uris]

        # Displaying playlist listbox and then inserting playlists
        self.playlist_label.grid(row=1, column=0, columnspan=2, pady=(10, 5))
        self.playlist_results.grid(row=2, column=0, columnspan=2, padx=5)
        self.playlist_results.delete(0, tk.END)
        if playlist_names:
            for name in playlist_names:
                self.playlist_results.insert(tk.END, name)
        else:
            self.playlist_results.insert(tk.END, 'The selected song is not found in any of your playlists.')


root = tk.Tk()
root.title('Spotify Playlist Searcher')
app = Application(master=root)
app.mainloop()

