from src.spotipy_manager import *
import tkinter as tk

root = tk.Tk()
root.title('Spotify Playlist Searcher')

header = tk.Label(root, text="Spotify Playlist Searcher")
header.grid(row=0, column=0, columnspan=2)


settings_btn = tk.Button(root, text="Settings")
settings_btn.grid(row=0, column=1, sticky=tk.E)

search_bar = tk.Entry(root, width=50)
search_bar.grid(row=1, column=0)

search_bar_submit = tk.Button(root, text="Search for Song")
search_bar_submit.grid(row=1, column=1)

root.mainloop()

