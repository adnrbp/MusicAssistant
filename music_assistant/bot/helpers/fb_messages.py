""" Facebook Messages Helper """
# Networking
import requests

# Debug
from pprint import pprint

# Constants
from music_assistant.bot.constants import *

fb_base_url = 'https://graph.facebook.com/v6.0/'
fb_messages_url = fb_base_url + 'me/messages'

class FbMessageAPI:
    """
    Build and Send Response messages to users
    """
    def __init__(self, sender_id):
        self.sender_id = sender_id
        self.get_user_details()

    def get_user_details(self):
        """ Request user information to create a personalized response message"""
        user_details_url = fb_base_url + self.sender_id

        user_details_params = {
                'fields': 'first_name,last_name,profile_pic', 
                'access_token': FB_ACCESS_TOKEN
            }
        user_details = requests.get(
            user_details_url, 
            params = user_details_params
        ).json()
        pprint(user_details)
        self.user_name = user_details['first_name']
        self.user_last_name = user_details['last_name']
        

    def send_message(self, response_msg):
        """ Send a response Message to facebook """
        status = requests.post(
            fb_messages_url,
            params=FB_ACCESS_TOKEN_PARAM,
            json=response_msg
        )
        pprint(status.json())

    def text_message(self, content):
        """ Structure message payload """
        response_msg = {
                "recipient": {"id": self.sender_id}, 
                "message": {"text": self.user_name +", "+ content}
            }
        self.send_message(response_msg)

