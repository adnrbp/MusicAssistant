""" Musix Match API Service """
# Networking
import requests

# Debug
from pprint import pprint

# Constants
from music_assistant.songs.constants import *

base_url='http://api.musixmatch.com/ws/1.1/'

class MusixMatchAPI():

    @classmethod
    def search_lyrics(cls, lyrics):
        api_method = "track.search"
        params = {
            'format': 'json', 
            'q_lyrics': lyrics,
            'apikey': MUSIX_MATCH_KEY
            }

        response = requests.get(
                base_url + api_method, 
                params=params
            ).json()
        track_list = response["message"]["body"]["track_list"]
        print(len(track_list))
        return len(track_list)