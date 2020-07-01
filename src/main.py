from src.spotipy_manager import *

# First make command line program, then expand to application
# Allow choice of permissions to read private playlists or not
# Function to format search query correctly and allow advanced searching
# Figure out playlist formatting
# Some songs don't have an id, if that happens resort to name matching

if __name__ == '__main__':

    spm = SpotipyManager()

    # Testing with song Melancolia by Caravan Palace
    playlists = spm.find_song_in_playlists('spotify:track:0K8ML5cB3rGmNe1oOVTXPo')
    print(playlists)
