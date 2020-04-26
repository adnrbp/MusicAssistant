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
        """ Build a simple text message for a user """
        response_msg = {
                "recipient": {"id": self.sender_id}, 
                "message": {"text": user_name +", "+ content}
            }
        self.send_message(response_msg)

    #def initial_instructions_message(self, sender_id, content): #content includes text w/ user_name
    def initial_instructions_message(self, user_name):
        """ Build an initial default message with custom user name"""
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


    def result_songs_template(self,content):
        """Given a list of songs, build its format with Payloads"""
        elements = []
        for (index, track) in enumerate(content):
            element = {
                "title": "{}. {}".format(index+1,track["track_name"]),
                "subtitle": track["artist_name"],
                "buttons": [
                    {
                        "type": "postback",
                        "title" : "Favorita",
                        "payload": "FAVORITE_{}_PAYLOAD".format(track["id"])
                    }
                ]
            }
            elements.append(element)
        return elements

    def lyrics_result_template(self, content, user_name):
        """ Build an interactive list template based on result songs """
        response_text = "Encontré {} canciones, espero esté la que buscabas".format(len(content))
        self.text_message(response_text, user_name)
        elements = self.result_songs_template(content)

        response_msg = {
                "recipient": {"id": self.sender_id}, 
                "message": {
                    "attachment": {
                        "type": "template",
                        "payload": {
                            "template_type": "generic",
                            "elements": elements,
                        }
                    }
                }
            }
        self.send_message(response_msg)


