import unittest
from src.spotipy_manager import *


class TestSpotipyManager(unittest.TestCase):
    def setUp(self):
        self.spm = SpotipyManager()

    def test_find_song_in_playlists(self):
        playlists = self.spm.find_song_in_playlists('spotify:track:0K8ML5cB3rGmNe1oOVTXPo')
        correct_set = set()
        correct_set.add('6zNdYuhJeOZYRTMiZ0T9DR')
        correct_set.add('14FwYXlO5PH4dqaQYdomp6')
        correct_set.add('37i9dQZF1Etq2nOAOxQGnV')

        self.assertEqual(playlists, correct_set)


if __name__ == '__main__':
    unittest.main()