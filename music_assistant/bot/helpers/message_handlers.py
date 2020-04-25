""" Messages Logic """

# Helpers
from .fb_messages import FbMessageAPI
from enum import Enum

# Services
from music_assistant.songs.services import MusixMatchAPI

from pprint import pprint


class MessageType(Enum):
    text = 1
    action = 2
    attachment = 3

class ResponseType(Enum):
    default = 1
    text = 2 # as a complement message
    results = 3 # from lyrics result
    favorites = 4



class Handlers():
    """ Handle messages and Build Responders"""

    def __init__(self,session):
        self.session = session

    def facebook_message(self, message):
        """ 
        Create an instance of FB Message Response Builder and handle its response
        """
        (sender_id, content, event_type) = self.process_type(message)
        
        self.generate_response(sender_id, content, event_type)

    def process_type(self, message):
        """ Determine/Define the type of message and call the handler."""
        # print("\n\n MENSAJEEEEE TYPE")
        # pprint(message)
        if 'message' in message:
            if 'quick_reply' in message['message']:
                sender_id = message['sender']['id']
                postback_payload = message['message']['quick_reply']['payload']

                (response_data, response_type) = self.process_postback(postback_payload)
                return (sender_id, response_data, response_type)


            if 'text' in message['message']:
                sender_id = message['sender']['id']
                message_text = message['message']['text']
                #event_type = MessageType.text

                # response_data should be a dictionary of results/etc
                (response_data, response_type) = self.process_text(message_text)
                return (sender_id, response_data, response_type)

        if 'postback' in message:
            sender_id = message['sender']['id']
            postback_payload = message['postback']['payload']
            #event_type = MessageType.action
            
            (response_data, response_type) = self.process_postback(postback_payload)
            return (sender_id, response_data, response_type)

    def generate_response(self, sender_id, received_message, response_type):
        """ 
        Create an instance of FB Message Response Builder and handle its response
        """
        fb = FbMessageAPI(sender_id)
        if response_type == ResponseType.default:
            fb.initial_instructions_message()
        elif response_type == ResponseType.text:
            fb.text_message(received_message)

    def process_text(self, message_text):
        """ 
        Understand text, process something and create response
        """
        # check session from request
        print("\n\n Processing text")
        if 'last_message' in self.session.keys():
            print("GOT the KEY")
        if self.session.get("last_message", "") == "LYRICS_PAYLOAD":
            #response_data = MusixMatchAPI.search_lyrics(message_text)
            response_data = "yourSong is from me"
            return (response_data, ResponseType.text) #.results
        # else

        return (message_text, ResponseType.default)

    def process_postback(self, postback_payload):
        """ 
        Understand payload-type(switch), process something and create response
        """
        if postback_payload == "LYRICS_PAYLOAD":
            response_data = "escribe la letra que quieres buscar :)"
            self.session["last_message"] = "LYRICS_PAYLOAD"
            print("\n SAVING KEY")
            print(self.session["last_message"])
            return (response_data, ResponseType.text)
       