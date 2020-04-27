""" Musix Match API Service """
# Networking
import requests

# Constants
from music_assistant.songs.constants import *

# Models
from songs.models import Song
# Debug
from pprint import pprint


base_url='http://api.musixmatch.com/ws/1.1/'

class MusixMatchAPI():

    @classmethod
    def search_lyrics(cls, lyrics):
        """Query API for track by given lyrics"""
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

        result_tracks = cls.get_tracks_data(response)
        return result_tracks

    # @classmethod
    # def send_request(cls, api_method, param_field, param_data):
    #     # multiple fields? = decompose key-value + add to params
    #     params = {
    #         'format': 'json', 
    #         param_field: param_data,
    #         'apikey': MUSIX_MATCH_KEY
    #         }

    #     response = requests.get(
    #             base_url + api_method, 
    #             params=params
    #         ).json()
    #     return response


    @classmethod
    def get_tracks_data(cls,response):
        """ Parse api results to data required """
        track_list = response["message"]["body"]["track_list"]
        result_tracks = []
        result_ids = []
        for track_obj in track_list:
            track = track_obj["track"] 
            track_id = int(track["track_id"])
            one_track = {}
            if track_id not in result_ids:
                one_track["remote_id"] = track_id
                one_track["name"] = track["track_name"]
                one_track["artist_name"] = track["artist_name"]
                result_tracks.append(one_track)
                result_ids.append(track_id)
        pprint(result_ids)
        pprint(result_tracks)
        return result_tracks

    @classmethod
    def get_one_track_data(cls,response):
        """ Parse api result to data required """
        track = response["message"]["body"]["track"]
        one_track = {}
        one_track["remote_id"] = int(track["track_id"]) 
        one_track["name"] = track["track_name"]
        one_track["artist_name"] = track["artist_name"]
        pprint(one_track)
        return one_track



    @classmethod
    def search_by_id(cls,track_id):
        """Query API for track with given id"""
        api_method = "track.get"
        params = {
            'format': 'json', 
            'track_id': track_id,
            'apikey': MUSIX_MATCH_KEY
            }
        response = requests.get(
                base_url + api_method, 
                params=params
            ).json()

        result_track = cls.get_one_track_data(response)

        track_name = result_track["name"]
        artist_name = result_track["artist_name"]

        return (track_name, artist_name)

    @classmethod
    def search_and_store_track(cls,track_id):
        """
        Get track from storage, or from API if doesnt exists.
        """
        track_result = Song.get_track(track_id)
        if track_result is None:
            (track_name, artist_name) = cls.search_by_id(track_id)

            track_result = Song.save_track(
                    name = track_name,
                    artist = artist_name,
                    track_id = track_id
                )
        return track_result


