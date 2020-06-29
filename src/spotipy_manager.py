import spotipy
import spotipy.util as util


class SpotipyManager:
    def __init__(self, username):
        token = util.prompt_for_user_token(username=username, scope='user-library-read playlist-read-private')
        self.sp = spotipy.Spotify(auth=token)

    def find_song_in_playlists(self, song_uri):
        
        found_playlist_ids = set()

        playlists = self.sp.current_user_playlists()

        self.find_song_helper(song_uri, playlists, found_playlist_ids)
        while playlists['next']:
            playlists = self.sp.next(playlists)
            self.find_song_helper(song_uri, playlists, found_playlist_ids)

        return found_playlist_ids

    def find_song_helper(self, song_uri, playlists, set_to_modify):
        for playlist in playlists['items']:
            tracks = self.sp.playlist_tracks(playlist['id'])

            if self.is_track_in_tracks(song_uri, tracks):
                set_to_modify.add(playlist['id'])
            while tracks['next']:
                tracks = self.sp.next(tracks)
                if self.is_track_in_tracks(song_uri, tracks):
                    set_to_modify.add(playlist['id'])

    def is_track_in_tracks(self, song_uri, tracks):
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
