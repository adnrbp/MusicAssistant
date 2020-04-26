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
    def __init__(self, sender_id, fb_url=fb_base_url):
        self.sender_id = sender_id # required for sending messages

        self.fb_base_url = fb_url
        self.fb_messages_url = self.fb_base_url + 'me/messages'
        
        self.access_token = FB_ACCESS_TOKEN
        self.access_token_param = {
            'access_token': self.access_token
        }

    def get_user_details(self):
        """ Request user information to create a personalized response message"""
        print("\n\nSENDER_ID")
        print(self.sender_id)
        print(self.fb_base_url)
        print(self.access_token)
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
        user_name = user_details['first_name']
        user_last_name = user_details['last_name']
        return (user_name, user_last_name)
    
    def save_user_id(self):
        """save sender id + store all his messages in db"""
        pass
        

    def send_message(self, response_msg):
        """ Send a response Message to facebook """
        status = requests.post(
            fb_messages_url,
            params=self.access_token_param,
            json=response_msg
        )
        print("\nSENDED MESSAGE:")
        pprint(response_msg)
        print("\nSENDED MESSAGE STATUS:")
        pprint(status.json())

    def text_message(self, content, user_name):
        """ Structure message payload """
        response_msg = {
                "recipient": {"id": self.sender_id}, 
                "message": {"text": user_name +", "+ content}
            }
        self.send_message(response_msg)

    #def initial_instructions_message(self, sender_id, content): #content includes text w/ user_name
    def initial_instructions_message(self, user_name):
        """ Structure message payload """
        response_msg = {
                "recipient": {"id": self.sender_id}, 
                "message": {
                    "text": "Hola " + user_name +", Soy un bot de busqueda musical por letras/lyrics",
                    "quick_replies": [
                        {
                            "content_type": "text",
                            "title": "Buscar Letra",
                            "payload": "LYRICS_PAYLOAD"
                        },
                        {
                            "content_type": "text",
                            "title": "Listar Favoritas",
                            "payload": "FAVORITES_PAYLOAD"
                        }
                    ]
                }
            }
        self.send_message(response_msg)
