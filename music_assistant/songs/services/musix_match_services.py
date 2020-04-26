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
        result_tracks = []
        result_ids = []
        for track_obj in track_list:
            track = track_obj["track"] 
            track_id = int(track["track_id"])
            one_track = {}
            if track_id not in result_ids:
                type(track_id)
                one_track["id"] = track_id
                one_track["track_name"] = track["track_name"]
                one_track["artist_name"] = track["artist_name"]
                result_tracks.append(one_track)
                result_ids.append(track_id)
        pprint(result_ids)
        pprint(result_tracks)
        return result_tracks
    @classmethod
    def search_by_id(cls,track_id):
        pass