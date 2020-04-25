
# Django Rest Framework
from rest_framework import status

# Helpers
from .message_handlers import Handlers

# Constants
from music_assistant.bot.constants import *

from pprint import pprint

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
        print("\n ENTRIES!!!!")
        pprint(entries)
        for entry in entries['entry']:
            for message in entry['messaging']:
                Handlers.facebook_message(message)
        return {'success': True}