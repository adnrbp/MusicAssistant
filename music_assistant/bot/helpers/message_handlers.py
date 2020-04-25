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

    @classmethod
    def facebook_message(cls, message):
        """ 
        Create an instance of FB Message Response Builder and handle its response
        """
        (sender_id, content, event_type) = cls.process_type(message)
        
        cls.generate_response(sender_id, content, event_type)

    @classmethod
    def process_type(cls, message):
        """ Determine/Define the type of message and call the handler."""
        print("\n\n MENSAJEEEEE TYPE")
        pprint(message)
        if 'message' in message:
            if 'quick_reply' in message['message']:
                sender_id = message['sender']['id']
                postback_payload = message['message']['quick_reply']['payload']

                (response_data, response_type) = cls.process_postback(postback_payload)
                return (sender_id, response_data, response_type)


            if 'text' in message['message']:
                sender_id = message['sender']['id']
                message_text = message['message']['text']
                #event_type = MessageType.text

                # response_data should be a dictionary of results/etc
                (response_data, response_type) = cls.process_text(message_text)
                return (sender_id, response_data, response_type)

        if 'postback' in message:
            sender_id = message['sender']['id']
            postback_payload = message['postback']['payload']
            #event_type = MessageType.action
            
            (response_data, response_type) = cls.process_postback(postback_payload)
            return (sender_id, response_data, response_type)

    @classmethod
    def generate_response(cls, sender_id, received_message, response_type):
        """ 
        Create an instance of FB Message Response Builder and handle its response
        """
        fb = FbMessageAPI(sender_id)
        if response_type == ResponseType.default:
            fb.initial_instructions_message()
        elif response_type == ResponseType.text:
            fb.text_message(received_message)

    @classmethod
    def process_text(cls, message_text):
        """ 
        Understand text, process something and create response
        """
        # check session from request
        # if session["last_message"] == "LYRICS_PAYLOAD"
        #   MusixMatchAPI.search_lyrics(message_text)
        #   return (response_data, ResponseType.results)
        # else

        return (message_text, ResponseType.default)

    @classmethod
    def process_postback(cls, postback_payload):
        """ 
        Understand payload-type(switch), process something and create response
        """
        if postback_payload == "LYRICS_PAYLOAD":
            response_data = "escribe la letra que quieres buscar :)"
            # session["last_message"] = "LYRICS_PAYLOAD"
            return (response_data, ResponseType.text)
       