""" Messages Logic """

# Helpers
from .fb_messages import FbMessageAPI
from enum import Enum

# Services
from songs.services import MusixMatchAPI

# Models
from bot.models import Conversation
from bot.models import Message
from songs.models import Favorite
from songs.models import Song
from users.models import User

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

    def __init__(self,sender_id, user_name,conversation_id):
        self.sender_id = sender_id
        self.user_name = user_name
        self.conversation = conversation_id

    def facebook_message(self, message):
        """ 
        Create an instance of FB Message Response Builder and handle its response
        """
        (sender_id, content, event_type) = self.process_type(message)
        
        self.generate_response(sender_id, content, event_type)

    # INPUT 
    def process_type(self, message):
        """ Determine/Define the type of message and call the handler."""
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

            if 'attachments' in message['message']:
                sender_id = message['sender']['id']
                #message_text = message['message']['attachments']
                response_data = ":)"
                response_type = ResponseType.default

                return (sender_id, response_data, response_type)

        if 'postback' in message:
            sender_id = message['sender']['id']
            postback_payload = message['postback']['payload']
            #event_type = MessageType.action
            
            (response_data, response_type) = self.process_postback(postback_payload)
            return (sender_id, response_data, response_type)

    def process_text(self, message_text):
        """ 
        Understand text, process something and create response
        random text: outputs Default Options
        lyrics text (with previous Postback) : process request text
        """
        # check session from request
        print("\n\n Processing text")
        (conversation, needs_follow_up, payload) = Conversation.get_last_message(self.conversation)
        Message.save_text(conversation, message_text)
        if needs_follow_up:
            if payload=="LYRICS_PAYLOAD":
                found_songs_data = MusixMatchAPI.search_lyrics(message_text)
                if len(found_songs_data) < 1 :
                    sorry_message = "No pudimos encontrar la canción :("
                    return (sorry_message, ResponseType.text)
                else:
                    response_message = "Encontré {} canciones, espero esté la que buscabas".format(len(found_songs_data))
                    response_data = {
                        "text": response_message,
                        "data": found_songs_data,
                        "buttons":{
                            "title": "Favorita",
                            "payload": "FAVORITE_{}_PAYLOAD",
                        }
                    }
                    return (response_data, ResponseType.results) #.results
            # if "FAVORITE_" in payload:
            #     return (message_text, ResponseType.default)

        return (message_text, ResponseType.default)

    def process_postback(self, postback_payload):
        """ 
        Understand payload-type(switch), process something and create response
        """
        if postback_payload == "GET_STARTED_BOT":
            response_data = "Soy un bot de busqueda musical por letras/lyrics"
            self.record_message_and_payload(response_data, postback_payload)
            return (response_data, ResponseType.default)

        if postback_payload == "LYRICS_PAYLOAD":
            response_data = "escribe la letra que quieres buscar :)"
            self.record_message_and_payload(response_data, postback_payload, with_follow_up=True)
            return (response_data, ResponseType.text)

        if "FAVORITE_" in postback_payload:
            track_id = postback_payload.split("_")[1]
            (track, was_saved) = self.search_track_by_id(track_id)

            if was_saved:
                response_data = "se guardó la canción {} en tu lista de favoritos".format(track.name)
            else:
                response_data = "la canción {} ya estaba en tu lista de favoritos".format(track.name)
            self.record_message_and_payload(response_data, postback_payload)

            return (response_data, ResponseType.text)


        if "REMOVE_" in postback_payload:
            track_id = postback_payload.split("_")[1]
            #removed = self.remove_track_by_id(track_id)
            removed = True

            if removed:
                response_data = "Se Borró la canción seleccionada"
            else:
                response_data = "La canción no existe en tu lista de canciones"
            self.record_message_and_payload(response_data, postback_payload)

            return (response_data, ResponseType.text)
            
        if postback_payload == "FAVORITES_PAYLOAD":
            # query user favorite songs songs
            favorite_songs = Song.favorites_by_user(self.sender_id)

            response_message = "tienes {} cancion(es) en tu lista de favoritos, estas son:".format(len(favorite_songs))
            self.record_message_and_payload(response_message, postback_payload)
            response_data = {
                "text": response_message,
                "data": favorite_songs,
                "buttons":{
                    "title": "Eliminar",
                    "payload": "REMOVE_{}_PAYLOAD",
                }
            }
            # crear template de ResponseType.favorites
            return (response_data, ResponseType.results)

        if postback_payload == "COUNT_USERS":
            users_quantity = User.users_quantity()
            response_data = "Aproximadamente {} usuario(s) utilizan el bot".format(users_quantity)
            self.record_message_and_payload(response_data, postback_payload)
            return (response_data, ResponseType.text)

        if postback_payload == "CHAT_DAYS":
            #query
            chats_daily_quantity = 1
            response_data = "Aproximadamente hay {} chat(s) en el día".format(chats_daily_quantity)
            self.record_message_and_payload(response_data, postback_payload)
            return (response_data, ResponseType.text)

        if postback_payload == "TOP_FAVORITES":
            top_songs = Song.get_top_songs()

            response_message = "estos son las top 5 canciones:"
            self.record_message_and_payload(response_message, postback_payload)
            response_data = {
                "text": response_message,
                "data": top_songs,
                "buttons":{
                    "title": "Favorita",
                    "payload": "FAVORITE_{}_PAYLOAD",
                }
            }
            # crear template de ResponseType.favorites
            return (response_data, ResponseType.results)



    # OUTPUT
    def generate_response(self, sender_id, received_message, response_type):
        """ 
        Create an instance of FB Message Response Builder and handle its response
        """
        fb = FbMessageAPI(sender_id)
        if response_type == ResponseType.default:
            fb.initial_instructions_message(self.user_name)
        elif response_type == ResponseType.text:
            fb.text_message(received_message, self.user_name)
        elif response_type == ResponseType.results:
            fb.lyrics_result_template(received_message, self.user_name)
       

    # services
    def record_message_and_payload(self,message, payload, with_follow_up=False):
        """Save conversation Message and Mark message to followup """
        conversation = Conversation.set_postback(self.conversation, payload)
        Message.save_text(conversation, message, with_follow_up=with_follow_up)


    def search_track_by_id(self,track_id):
        """ Query track remotely + save in db """
        track = MusixMatchAPI.search_and_store_track(track_id)
        user = User.get_user_by_sender_id(self.sender_id)
        was_saved = Favorite.save_track(user, track)
        return (track, was_saved)

    # def remove_track_by_id(self,track_id):
    #     """ Remove favorite track saved """
    #     pass
