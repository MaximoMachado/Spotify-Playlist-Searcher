from src.spotipy_manager import *
import tkinter as tk
import os.path

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_base_widgets()

    def create_base_widgets(self):
        self.header = tk.Label(root, text="Spotify Playlist Searcher", width=50)
        self.header.grid(row=0, column=0, columnspan=2, pady=10)

        self.settings_btn = tk.Button(root, text="Settings")
        self.settings_btn.grid(row=0, column=1, sticky=tk.E)

        if os.path.exists("./data/.cache-user"):
            self.spm = SpotipyManager()
            self.load_widgets()
        else:
            self.login_btn = tk.Button(root, text="Login to Spotify", command=self.login_spotify)
            self.login_btn.grid(row=1, column=0, columnspan=2)

    def login_spotify(self):
        self.spm = SpotipyManager()
        self.load_widgets()
        self.login_btn.grid_forget()

    def load_widgets(self):
        self.search_bar = tk.Entry(root, width=50)
        self.search_bar.grid(row=1, column=0)
        self.search_bar.focus()

        self.search_bar_submit = tk.Button(root, text="Search for Song", command=self.search_submit)
        self.search_bar_submit.grid(row=1, column=1)

    def search_submit(self):
        search = self.search_bar.get()
        print(self.spm.get_spotipy_client().search(search))


root = tk.Tk()
root.title('Spotify Playlist Searcher')
app = Application(master=root)
app.mainloop()

