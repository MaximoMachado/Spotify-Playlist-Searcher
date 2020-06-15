import spotipy
import spotipy.util as util

# TODO Make git repository and start thinking how to format this
# First make command line program, then expand to application
# Allow choice of permissions to read private playlists or not
# Function to format search query correctly and allow advanced searching
# Figure out playlist formatting
# Some songs don't have an id, if that happens resort to name matching


def find_song_in_playlists(song_id):
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        print(playlist['name'])
        tracks = sp.playlist_tracks(playlist['id'])

        for track in tracks['items']:
            print(track)


def translate_search_query(query):
    pass


if __name__ == '__main__':
    username = 'Maximo Machado'  # input('Enter username: ')
    token = util.prompt_for_user_token(username=username, scope='user-library-read playlist-read-private')
    sp = spotipy.Spotify(auth=token)

    # search = input('Search Song: ')
    # print(sp.search(search))

    find_song_in_playlists('test')
