import unittest
from src.spotipy_manager import *


class TestSpotipyManager(unittest.TestCase):
    def setUp(self):
        self.spm = SpotipyManager()
        self.sp = self.spm.get_spotipy_client()

    def test_is_track_in_tracks(self):
        song_uri = 'spotify:track:0K8ML5cB3rGmNe1oOVTXPo'  # Melancolia by Caravan Palace
        album = self.sp.album('spotify:album:5Pnctsm9Mi4D6W3DzWckA6')  # Album song is in
        self.assertTrue(is_track_in_tracks(song_uri, album['tracks']))

        playlist = self.sp.playlist('spotify:playlist:37i9dQZF1DWYkaDif7Ztbp')  # African Heat Playlist
        self.assertFalse(is_track_in_tracks(song_uri, self.sp.playlist_tracks(playlist['id'])))

    def test_get_name_from_uri(self):
        self.assertEqual(self.spm.get_name_from_uri('spotify:track:5l08slmvFRUseHpq85neke'), 'NaNa', 'Track URI')
        self.assertEqual(self.spm.get_name_from_uri('spotify:album:4nlIXR3GjNDLvuV2nrgpkX'), 'Back Again', 'Album URI')
        self.assertEqual(self.spm.get_name_from_uri('spotify:playlist:37i9dQZF1DX3qCx5yEZkcJ'), 'Mellow Beats', 'Playlist URI')
        self.assertEqual(self.spm.get_name_from_uri('spotify:artist:4GcpBLY8g8NrmimWbssM26'), 'Mndsgn', 'Artist URI')

        with self.assertRaises(ValueError):
            self.spm.get_name_from_uri('test_str')

        with self.assertRaises(ValueError):
            self.spm.get_name_from_uri('spotify')

    def test_find_song_in_playlists(self):
        playlists = self.spm.find_song_in_playlists('spotify:track:0K8ML5cB3rGmNe1oOVTXPo')
        correct_set = set()
        correct_set.add('spotify:playlist:6zNdYuhJeOZYRTMiZ0T9DR')
        correct_set.add('spotify:playlist:14FwYXlO5PH4dqaQYdomp6')
        correct_set.add('spotify:playlist:37i9dQZF1Etq2nOAOxQGnV')

        self.assertEqual(playlists, correct_set)

        playlists = self.spm.find_song_in_playlists('spotify:track:0K8ML5cB3rGmNe1oOVTXPo', playlists_to_exclude=('spotify:playlist:6zNdYuhJeOZYRTMiZ0T9DR', 'spotify:playlist:14FwYXlO5PH4dqaQYdomp6'))
        correct_set = set()
        correct_set.add('spotify:playlist:37i9dQZF1Etq2nOAOxQGnV')

        self.assertEqual(playlists, correct_set)

    def test_cache_songs_in_playlists(self):
        playlists = self.sp.current_user_playlists()
        cached_playlists = self.spm.cache_songs_in_playlists(playlists)

        test_playlist_cached = cached_playlists['spotify:playlist:0YhxBIhx9BrFMrnAWL72PQ']
        correct_set = {'spotify:track:14dCt3xXZvmoqorYnxspSj',
                       'spotify:track:6WtiJthSHfbA5RIWcUU4TM',
                       'spotify:track:2ZltjIqztEpZtafc8w0I9t',
                       'spotify:track:5pS3GKYhlEAqSYM8JM27ki'}
        self.assertEqual(test_playlist_cached, correct_set, 'SPS_TEST Playlist')


if __name__ == '__main__':
    unittest.main()
