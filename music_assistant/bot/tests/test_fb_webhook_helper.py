# Tests
from unittest import TestCase
from mock import Mock, patch

# Helpers
from music_assistant.bot.helpers import FbWebhookAPI
from music_assistant.bot.helpers import Handlers

from music_assistant.bot.constants import *
#from music_assistant.bot.fixtures import *


class FbWebhookAPITest(TestCase):
    """ Test module for FbWebhook helper """

    def setUp(self):
        pass

    def test_successful_fb_messenger_registration(self):
        # Send  request to the webhook, check that receve
        # Arrange
        hub_challenge_code = 2021531252
        request = {
                'hub.challenge': str(hub_challenge_code), 
                'hub.verify_token': FB_VERIFY_TOKEN, 
                'hub.mode': ['subscribe']
            }
        # Act
        (data, status) = FbWebhookAPI.verify_token(request)
        # Assert
        self.assertEqual(data, hub_challenge_code)

    def test_failed_fb_messenger_registration(self):
        # Arrange
        hub_challenge_code = 2021531252
        request = {
                'hub.challenge': str(hub_challenge_code), 
                'hub.verify_token': 'AnyOtherToken', 
                'hub.mode': ['subscribe']
            }
            
        # Act
        (data, status) = FbWebhookAPI.verify_token(request)
        
        # Assert
        self.assertIn('error',data)

    @patch('music_assistant.bot.helpers.fb_webhook.Handlers.facebook_message', autospec=True)
    def test_fb_message_processing(self,mock_handler_fb_msg):
        # Arrange
        message_content = ['hola']
        request = {"entry": [
                    {"messaging": message_content},
                    ]}
        # Act
        data = FbWebhookAPI.process_message(request)
        # Assert
        self.assertEqual(
                mock_handler_fb_msg.call_count, 
                len(message_content)
            )
        mock_handler_fb_msg.assert_called_once_with(message_content[0])
