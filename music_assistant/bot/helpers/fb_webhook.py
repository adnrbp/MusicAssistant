
# Django Rest Framework
from rest_framework import status

# Helpers
from .message_handlers import Handlers

# Constants
from music_assistant.bot.constants import *

class FbWebhookAPI():
    """ Manage Facebook initial connection and message reception."""

    @classmethod
    def verify_token(cls, request):
        """ Register webhook with Facebook Messenger """
        print(request)
        if request.get('hub.verify_token', '') == FB_VERIFY_TOKEN:
            data= int(request.get('hub.challenge'))
            result = status.HTTP_200_OK
        else:
            data = {'error': 'bad parameter'}
            result = status.HTTP_400_BAD_REQUEST
        return (data, result)

    @classmethod
    def process_message(cls, entries):    
        """ Receive messages from user entries in a request"""
        print(entries)
        for entry in entries['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    sender_id = message['sender']['id']
                    message_text = message['message']['text']

                    Handlers.facebook_message(sender_id, message_text)

                if 'postback' in message:
                    sender_id = message['sender']['id']
                    postback_payload = message['postback']['payload']

                    Handlers.facebook_message(sender_id, postback_payload )
        return {'success': True}