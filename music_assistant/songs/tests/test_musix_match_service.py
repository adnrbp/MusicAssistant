# Django
from unittest import TestCase

# Services
from music_assistant.songs.services import MusixMatchAPI

from music_assistant.songs.constants import *

class MusixMatchAPITest(TestCase):
    def setUp(self):
        # Arrange/Given
        self.lyrics = "Black leather gloves, no sequins"
        # Act/When
        self.tracks = MusixMatchAPI.search_lyrics(self.lyrics)

    def test_get_tracks_for_lyrics(self):
        # Assert/Then
        self.assertEqual(len(self.tracks), 1)

    def test_get_tracks_name_and_artist(self):
        # Act/When
        track = self.tracks[0]
        number_keys = len(track.keys()) # with id
        has_name = 'name' in track
        has_track_artist = 'artist_name' in track
        
        # Assert/Then
        self.assertTrue(has_name)
        self.assertTrue(has_track_artist)
        self.assertEqual(number_keys, 3)
