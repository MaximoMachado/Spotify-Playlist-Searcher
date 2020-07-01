import spotipy
from spotipy.oauth2 import SpotifyOAuth


def is_track_in_tracks(song_uri, tracks):
    """
    Checks whether song is within a list of songs
    :param song_uri: ID of target song
    :param tracks: Page object of list of playlist tracks
    :return: Whether or a not a song is within a list of tracks
    """
    # TODO Make it applicable to both playlist tracks and tracks
    for playlist_track in tracks['items']:
        if song_uri == playlist_track['track']['uri']:
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
