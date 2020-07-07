import spotipy
from spotipy.oauth2 import SpotifyOAuth


def is_track_in_tracks(song_uri, tracks):
    """
    Checks whether song is within a list of songs
    :param song_uri: ID of target song
    :param tracks: Page object of track or playlist track objects
    :return: Whether or a not a song is within a list of tracks
    """
    for track in tracks['items']:
        try:
            # If playlist track it contains the track object within the key 'track'
            if song_uri == track['track']['uri']:
                return True
        except KeyError:
            if song_uri == track['uri']:
                return True
    return False


class SpotipyManager:
    """
    Manages Spotipy functions and implements additional functions useful to interacting with Spotipy
    """
    def __init__(self):
        """
        Initializes spotipy client with a prompted token from username
        :param username: Username of Spotify Account
        """
        scope = 'user-library-read playlist-read-private'
        auth = SpotifyOAuth(scope=scope, cache_path='./data/.cache-user')
        self.sp = spotipy.Spotify(auth_manager=auth)

    def get_spotipy_client(self):
        """
        Allows access to Spotipy to use its functions
        :return: Spotipy client
        """
        return self.sp

    def get_name_from_uri(self, uri):
        """
        Gets Name of Song/Album/Playlist from its uri
        :param uri: Unique id of object
        :return: Name of object from uri
        """
        if 'spotify:' in uri:
            # Format of uri is spotify
            uri_type = uri.split(':')[1]
            get_obj_from_id = getattr(self.sp, uri_type)

            return get_obj_from_id(uri)['name']
        else:
            raise ValueError('uri string not in spotify uri format')

    def get_playlist_name(self, playlist_id):
        """
        Gets name of a playlist from the id or uri
        :param playlist_id: ID of playlist
        :return: str Playlist Name
        """
        return self.sp.playlist(playlist_id)['name']

    def find_song_in_playlists(self, song_uri):
        """
        For a particular song, search all user playlists and return matched playlists
        :param song_uri: Unique ID of song on Spotify
        :return: Set of Playlist IDs that song is found within
        """
        found_playlist_ids = set()

        playlists = self.sp.current_user_playlists()

        self._find_song_helper(song_uri, playlists, found_playlist_ids)
        while playlists['next']:
            playlists = self.sp.next(playlists)
            self._find_song_helper(song_uri, playlists, found_playlist_ids)

        return found_playlist_ids

    def _find_song_helper(self, song_uri, playlists, set_to_modify):
        """
        Adds to a set playlists that contain the song specified
        :param song_uri: Unique ID of song on Spotify to find
        :param playlists: Page Object of Playlists to search through
        :param set_to_modify: Set that playlists are added to
        """
        for playlist in playlists['items']:
            tracks = self.sp.playlist_tracks(playlist['id'])

            if is_track_in_tracks(song_uri, tracks):
                set_to_modify.add(playlist['id'])
            while tracks['next']:
                tracks = self.sp.next(tracks)
                if is_track_in_tracks(song_uri, tracks):
                    set_to_modify.add(playlist['id'])
