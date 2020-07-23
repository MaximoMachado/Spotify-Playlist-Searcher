import re
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
        Gets Name of Song/Album/Playlist/Artist from its uri
        :param uri: Unique id of object
        :return: Name of object from uri
        """
        matched_uri = re.search('spotify:(track|playlist|album|artist):.*', uri)
        if matched_uri:
            # Format of uri is spotify:type:id
            uri_type = matched_uri.group(1)
            get_obj_from_uri = getattr(self.sp, uri_type)

            return get_obj_from_uri(uri)['name']
        else:
            raise ValueError('uri string not in spotify uri format or is uri of a user')

    def find_song_in_playlists(self, song_uri, playlists_to_exclude=()):
        """
        For a particular song, search all user playlists and return matched playlists
        :param song_uri: Unique ID of song on Spotify
        :param playlists_to_exclude: Set of playlist uri's to not search through
        :return: Set of Playlist URIs that song is found within
        """
        found_playlist_ids = set()

        playlists = self.sp.current_user_playlists()

        self._find_song_helper(song_uri, playlists, found_playlist_ids, playlists_to_exclude)
        while playlists['next']:
            playlists = self.sp.next(playlists)
            self._find_song_helper(song_uri, playlists, found_playlist_ids, playlists_to_exclude)

        return found_playlist_ids

    def _find_song_helper(self, song_uri, playlists, set_to_modify, playlists_to_exclude):
        """
        Adds to a set playlists that contain the song specified
        :param song_uri: Unique ID of song on Spotify to find
        :param playlists: Page Object of Playlists to search through
        :param set_to_modify: Set that playlists are added to
        :param playlists_to_exclude: Set of playlist uri's to not search through
        """
        for playlist in playlists['items']:
            if playlist['uri'] not in playlists_to_exclude:
                tracks = self.sp.playlist_tracks(playlist['uri'])

                if is_track_in_tracks(song_uri, tracks):
                    set_to_modify.add(playlist['uri'])
                while tracks['next']:
                    tracks = self.sp.next(tracks)
                    if is_track_in_tracks(song_uri, tracks):
                        set_to_modify.add(playlist['uri'])
