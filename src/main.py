from src.spotipy_manager import *
import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.main_frame = tk.Frame(master)
        self.main_frame.grid(row=0, column=0, columnspan=2, padx=10)
        self.spm = SpotipyManager()
        self.create_base_widgets()

    def create_base_widgets(self):
        self.header = tk.Label(self.main_frame, text="Spotify Playlist Searcher", width=50)
        self.header.grid(row=0, column=0, columnspan=2, pady=10)

        self.settings_btn = tk.Button(self.main_frame, text="Settings")
        self.settings_btn.grid(row=0, column=1, sticky=tk.E)

        self.search_bar = tk.Entry(self.main_frame, width=50)
        self.search_bar.grid(row=1, column=0)
        self.search_bar.focus()

        self.search_bar_submit = tk.Button(self.main_frame, text="Search for Song", command=self.search_submit)
        self.search_bar_submit.grid(row=1, column=1)

        self.search_results = tk.Listbox(width=50)
        self.search_results.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

    def search_submit(self):
        # TODO Bind function to enter key, either while in focus of search bar or anytime at all.
        self.search_results.delete(0, tk.END)

        search = self.search_bar.get()
        paging_object = self.spm.get_spotipy_client().search(search)
        tracks = paging_object['tracks']['items']

        for track in tracks:
            artists = track['artists']
            artists_str = ''
            for i, artist in enumerate(artists):
                artists_str += f'{artist["name"]}'
                if not i == len(artists) - 1:
                    artists_str += ', '

            self.search_results.insert(tk.END, f"{track['name']}    -   {artists_str}")


root = tk.Tk()
root.title('Spotify Playlist Searcher')
app = Application(master=root)
app.mainloop()

