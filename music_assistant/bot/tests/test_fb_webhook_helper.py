
# Django
from django.test import TestCase

# Helpers
from music_assistant.bot.helpers import FbWebhookAPI

from music_assistant.bot.constants import *
#from music_assistant.bot.fixtures import *

class FbWebhookAPITest(TestCase):
    """ Test module for FbWebhook helper """

    def setUp(self):
        pass

    def test_successful_fb_messenger_registration():
        # Send  request to the webhook, check that receve
        request = {
                'hub.challenge': ['2021531252'], 
                'hub.verify_token': [FB_VERIFY_TOKEN], 
                'hub.mode': ['subscribe']
            }
        (data, status) = FbWebhookAPI.verify_token(request)

        pass
    def test_failed_fb_messenger_registration():
        pass

    def test_fb_message_processing():
        # A user sends a message to the webhook, 
        # check that called Handlers.facebook_message(sender_id, message_text)
        request = {
                "entry": [
                    {"messaging": [
                        {"message": {"text": "nuevo"},
                        "recipient": {"id": "111257337224637"},
                        "sender": {"id": "3274432302589797"},
                        "timestamp": 1587665033710
                        }],]}
        pass
