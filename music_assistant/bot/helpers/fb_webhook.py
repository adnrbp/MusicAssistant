
# Django Rest Framework
from rest_framework import status

# Helpers
from .fb_messages import FbMessageAPI
from .message_handlers import Handlers

# Models
from users.models import User
from bot.models import Conversation

# Constants
from music_assistant.bot.constants import *

from pprint import pprint

class FbWebhookAPI():
    """ Manage Facebook initial connection and message reception."""

    @classmethod
    def verify_token(cls, request):
        """ Register webhook with Facebook Messenger """
        # print(request)
        if request.get('hub.verify_token', '') == FB_VERIFY_TOKEN:
            data= int(request.get('hub.challenge'))
            result = status.HTTP_200_OK
        else:
            data = {'error': 'bad parameter'}
            result = status.HTTP_400_BAD_REQUEST
        return (data, result)

    @classmethod
    def process_message(cls, entries, session):    
        """ Receive messages from user entries in a request"""
        print("\n ENTRIES!!!!")
        pprint(entries)
        
        for entry in entries['entry']:
            for message in entry['messaging']:
                (sender_id, name, conversation_id ) = cls.get_user_data(message['sender'])
                handler = Handlers(session, sender_id, name, conversation_id ) #,sender_id)
                handler.facebook_message(message)
        return {'success': True}

    #service
    @classmethod
    def get_user_data(cls,sender):
        if 'id' in sender:
            sender_id = sender['id']
            user = User.get_user_by_sender_id(sender_id)
            
            if user is None:
                fb = FbMessageAPI(sender_id)
                (user_name, last_name) = fb.get_user_details()

                user = User.register_new_user(sender_id, user_name, last_name)
            conversation_id = Conversation.register_new_conversation(user)
            return (sender_id, user.first_name, conversation_id)
    
    