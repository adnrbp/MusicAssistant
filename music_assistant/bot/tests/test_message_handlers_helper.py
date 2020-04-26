# Tests
from unittest import TestCase
from mock import Mock, patch

# Helpers
from music_assistant.bot.helpers import Handlers
from music_assistant.bot.helpers.message_handlers import ResponseType

class HandlersTest(TestCase):
    """ Test module for Handlers helper """

    def setUp(self):
        self.handler = Handlers(
            sender_id=234234234,
            user_name="user1",
            conversation_id=2)

    @patch.object(
        Handlers,'process_text', 
        autospec=True,
        return_value=("data",1) # (response_data, response_type)
    )
    def test_define_message_of_type_text(self,mock_handlers_process_text):
        # Arrange
        message = {'message': {'text': 'hola'},'sender': {'id': '123'}}

        # Act
        self.handler.process_type(message)
        # Assert
        self.assertEqual(mock_handlers_process_text.call_count,1)


    @patch.object(
        Handlers,'process_postback', 
        autospec=True,
        return_value=("data",ResponseType.text) # (response_data, response_type)
    )
    def test_define_message_of_type_quick_reply(self,mock_handlers_process_postback):
        # Arrange
        message = { 'message': {
                        'quick_reply': {'payload': 'LYRICS_PAYLOAD'},
                        'text': 'Buscar Letra'
                        },
                    'sender': {'id': '123'}
                  }
        # Act
        self.handler.process_type(message)
        # Assert
        self.assertEqual(mock_handlers_process_postback.call_count,1)


    # REACTIVE proc: show options and search lyrics


    def test_initial_text_gives_default_message_back(self):
        pass

    def test_lyrics_payload_search_lyrics_on_musix_match(self):
        #also that sends .results
        pass

    def test_lyrics_payload_search_with_empty_result_send_sorry(self):
        pass


    #OPTIONS proc: search lyrics, save to favorites


    def test_on_search_lyrics_option_selected_saves_postback_mark_to_wait_for_lyrics(self):
        pass

    def test_on_favorite_option_selected_saves_track_in_users_favorites(self):
        pass


    # RESPONSE proc: render messages (default, simple text)

    @patch(
        'music_assistant.bot.helpers.message_handlers.FbMessageAPI', 
        autospec=True)
    def test_response_generation_request_default(self, FbMessageAPI_mock):
        # Arrange
        mock_fb = FbMessageAPI_mock.return_value

        sender_id= "123"
        received_message = {"content":"hola"}
        response_type = ResponseType.default

        # Act
        self.handler.generate_response(sender_id, received_message, response_type)

        # Assert
        FbMessageAPI_mock.assert_called_with(sender_id=sender_id)
        self.assertEqual(mock_fb.initial_instructions_message.call_count,1)
        self.assertEqual(mock_fb.text_message.call_count,0)

    @patch(
        'music_assistant.bot.helpers.message_handlers.FbMessageAPI', 
        autospec=True)
    def test_response_generation_request_text(self, FbMessageAPI_mock):
        # Arrange
        mock_fb = FbMessageAPI_mock.return_value

        sender_id= "123"
        received_message = {"content":"hola"}
        response_type = ResponseType.text

        # Act
        self.handler.generate_response(sender_id, received_message, response_type)

        # Assert
        FbMessageAPI_mock.assert_called_with(sender_id=sender_id)
        self.assertEqual(mock_fb.initial_instructions_message.call_count,0)
        self.assertEqual(mock_fb.text_message.call_count,1)
