import spotipy
import spotipy.util as util

# First make command line program, then expand to application
# Allow choice of permissions to read private playlists or not
# Function to format search query correctly and allow advanced searching
# Figure out playlist formatting
# Some songs don't have an id, if that happens resort to name matching


def find_song_in_playlists(song_uri):
    # TODO Make it so all playlists gone through, method has limit to how many shown at a time
    found_playlist_ids = set()

    playlists = sp.current_user_playlists()

    find_song_helper(song_uri, playlists, found_playlist_ids)
    while playlists['next']:
        playlists = sp.next(playlists)
        find_song_helper(song_uri, playlists, found_playlist_ids)

    return found_playlist_ids

def find_song_helper(song_uri, playlists, set_to_modify):
    for playlist in playlists['items']:
        tracks = sp.playlist_tracks(playlist['id'])

        if is_track_in_tracks(song_uri, tracks):
            set_to_modify.add(playlist['id'])
        while tracks['next']:
            tracks = sp.next(tracks)
            if is_track_in_tracks(song_uri, tracks):
                set_to_modify.add(playlist['id'])

def is_track_in_tracks(song_uri, tracks):
    """
    Checks whether song is within a list of songs
    :param song_uri: ID of target song
    :param tracks: Page object of list of tracks
    :return: Whether or a not a song is within a list of tracks
    """
    for playlist_track in tracks['items']:
        if song_uri == playlist_track['track']['uri']:
            return True
    return False


def translate_search_query(query):
    pass


if __name__ == '__main__':
    username = 'Maximo Machado'  # input('Enter username: ')
    token = util.prompt_for_user_token(username=username, scope='user-library-read playlist-read-private')
    sp = spotipy.Spotify(auth=token)

    # search = input('Search Song: ')
    # print(sp.search(search))

    find_song_in_playlists('spotify:track:0K8ML5cB3rGmNe1oOVTXPo')  # Testing with song Melancolia by Caravan Palace
