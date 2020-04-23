""" WebHook views. """

# Django Rest Framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.conf import settings

from .constants import *

class WebhookAPIView(APIView):
    """
    Webhook communications
    """
    def get(self, request, *args, **kwargs):
        """ Register webhook with Facebook Messenger """
        if request.GET.get('hub.verify_token', '') == settings.FACEBOOK_VERIFY_TOKEN:
            data=int(request.GET.get('hub.challenge'))
            return Response(data,status=status.HTTP_200_OK)
        return Response(
            {'error': 'bad parameter'},
            status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        """ Receive messages from user entries in a request"""
        for entry in request.data['entry']:
            for message in entry['messaging']:
                print(message)
                return Response({'success': True})