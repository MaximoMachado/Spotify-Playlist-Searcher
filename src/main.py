import spotipy
import spotipy.util as util

# TODO Make git repository and start thinking how to format this
# First make command line program, then expand to application
# Allow choice of permissions to read private playlists or not
# Function to format search query correctly and allow advanced searching
# Figure out playlist formatting
# Some songs don't have an id, if that happens resort to name matching


def find_song_in_playlists(song_uri):
    # TODO Make it so all playlists gone through, method has limit to how many shown at a time
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        # print(playlist['name'])
        tracks = sp.playlist_tracks(playlist['id'])

        if is_track_in_tracks(song_uri, tracks):
            print(f"Found in Playlist {playlist['name']}")
        while tracks['next']:
            tracks = sp.next(tracks)
            if is_track_in_tracks(song_uri, tracks):
                print(f"Found in Playlist {playlist['name']}")


def is_track_in_tracks(song_uri, tracks):
    """
    Checks whether song is within a list of songs
    :param song_uri: ID of target song
    :param tracks: Page object of list of tracks
    :return: @hether or a not a song is within a list of tracks
    """
    for track in tracks['items']:
        if song_uri == track['track']['uri']:
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
