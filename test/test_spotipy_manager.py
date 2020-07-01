import unittest
from src.spotipy_manager import *


class TestSpotipyManager(unittest.TestCase):
    def setUp(self):
        self.spm = SpotipyManager()

    def test_is_track_in_tracks(self):
        sp = self.spm.get_spotipy_client()
        song_uri = 'spotify:track:0K8ML5cB3rGmNe1oOVTXPo'  # Melancolia by Caravan Palace
        album = sp.album('spotify:album:5Pnctsm9Mi4D6W3DzWckA6')  # Album song is in
        self.assertTrue(is_track_in_tracks(song_uri, album['tracks']))

        playlist = sp.playlist('spotify:playlist:37i9dQZF1DWYkaDif7Ztbp')  # African Heat Playlist
        self.assertFalse(is_track_in_tracks(song_uri, sp.playlist_tracks(playlist['id'])))


    def test_find_song_in_playlists(self):
        playlists = self.spm.find_song_in_playlists('spotify:track:0K8ML5cB3rGmNe1oOVTXPo')
        correct_set = set()
        correct_set.add('6zNdYuhJeOZYRTMiZ0T9DR')
        correct_set.add('14FwYXlO5PH4dqaQYdomp6')
        correct_set.add('37i9dQZF1Etq2nOAOxQGnV')

        self.assertEqual(playlists, correct_set)


if __name__ == '__main__':
    unittest.main()