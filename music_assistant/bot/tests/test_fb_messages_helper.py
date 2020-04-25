# Tests
from unittest import TestCase
from mock import Mock, patch

# Helpers
from music_assistant.bot.helpers import FbMessageAPI
from music_assistant.bot.helpers import Handlers


class FbMessageAPITest(TestCase):
    """ Test module for FbMessage helper """

    def setUp(self):
        self.sender_id = "1234"
        with patch(
                'music_assistant.bot.helpers.fb_messages.FbMessageAPI.get_user_details'
            ) as mock_get_user_details:
            self.fb = FbMessageAPI(sender_id='1234')

    #@patch('music_assistant.bot.helpers.fb_messages.requests.get', autospec=True)
    def test_retrieve_user_details(self):#,mock_requests_get):
        pass

    @patch('music_assistant.bot.helpers.fb_messages.requests.post', autospec=True)
    def test_send_message(self,mock_requests_post):
        response_message = {"recipient":self.sender_id, "message": "hi"}
        self.fb.send_message(response_message)
        self.assertEqual(mock_requests_post.call_count,1)
        #mock_requests_post.assert_called_once_with(json=response_message)

    def test_build_text_message(self):
        pass

    def test_build_default_message(self):
        pass