# Django
from django.test import TestCase

# Services
from music_assistant.songs.services import MusixMatchAPI

from music_assistant.songs.constants import *

class MusixMatchAPITest(TestCase):
    def setUp(self):
        pass

    def test_get_tracks_for_lyrics(self):
        # Arrange/Given
        lyrics = "Black leather gloves, no sequins"

        # Act/When
        track_len = MusixMatchAPI.search_lyrics(lyrics)

        # Assert/Then
        self.assertEqual(track_len, 1)