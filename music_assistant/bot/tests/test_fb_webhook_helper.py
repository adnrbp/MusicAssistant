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
        
    @patch('music_assistant.bot.helpers.fb_webhook.FbWebhookAPI.get_user_data', autospec=True)
    @patch('music_assistant.bot.helpers.fb_webhook.Handlers', autospec=True)
    def test_fb_message_processing(self,Handlers_mock, mock_get_user_data):
        # Arrange
        mock_handler = Handlers_mock.return_value
        sender_id = 2345435
        mock_get_user_data.return_value = (sender_id, "user1", 2)
        message_content = [{'sender': sender_id}]
        request = {"entry": [
                    {"messaging": message_content},
                    ]}
        session = {}
        # Act
        data = FbWebhookAPI.process_message(request,session)
        # Assert
        self.assertEqual(
                mock_handler.facebook_message.call_count,
                len(message_content)
            )
        mock_handler.facebook_message.assert_called_once_with(message_content[0])
