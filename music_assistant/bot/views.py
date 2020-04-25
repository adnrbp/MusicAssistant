""" WebHook views. """

# Django Rest Framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Helpers
from .helpers import Handlers
from .helpers import FbWebhookAPI

# Constants
from .constants import *

class WebhookAPIView(APIView):
    """
    Webhook communications
    """
    def get(self, request, *args, **kwargs):
        """ Register webhook with Facebook Messenger """
        (data, response_status) = FbWebhookAPI.verify_token(request.GET)
        return Response(data,status=response_status)

    def post(self, request, *args, **kwargs):
        """ Receive messages from user entries in a request"""
        data = FbWebhookAPI.process_message(request.data,request.session)
        return Response(data)