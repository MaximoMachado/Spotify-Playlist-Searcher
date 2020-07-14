from src.spotipy_manager import *
import tkinter as tk
import os


def login_spotify():
    spm = SpotipyManager()
    load_widgets()
    login_btn.grid_forget()


def search_submit():
    pass


def load_widgets():
    search_bar = tk.Entry(root, width=50)
    search_bar.grid(row=1, column=0)

    search_bar_submit = tk.Button(root, text="Search for Song", command=search_submit)
    search_bar_submit.grid(row=1, column=1)


root = tk.Tk()
root.title('Spotify Playlist Searcher')

header = tk.Label(root, text="Spotify Playlist Searcher", width=50)
header.grid(row=0, column=0, columnspan=2, pady=10)

settings_btn = tk.Button(root, text="Settings")
settings_btn.grid(row=0, column=1, sticky=tk.E)

spm = None
if os.path.exists("./data/.cache-user"):
    spm = SpotipyManager()
    load_widgets()
else:
    login_btn = tk.Button(root, text="Login to Spotify", command=login_spotify, width=50)
    login_btn.grid(row=1, column=0)


root.mainloop()

