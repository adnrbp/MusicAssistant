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

    @patch('music_assistant.bot.helpers.message_handlers.Conversation.get_last_message',
        autospec=True)
    @patch('music_assistant.bot.helpers.message_handlers.Message.save_text',
        autospec=True)
    @patch('music_assistant.bot.helpers.message_handlers.MusixMatchAPI.search_lyrics',
        autospec=True)
    def test_initial_text_gives_default_message_back(self, 
                    mock_search_lyrics,
                    mock_save_text, 
                    mock_get_last_message):
        # Arrange
        conversation_id = 1
        needs_follow_up = False
        payload = ""
        mock_get_last_message.return_value = (conversation_id,needs_follow_up, payload)

        # Act
        (response_data, response_type) = self.handler.process_text("hola")

        # Assert
        self.assertEqual(response_type, ResponseType.default)
        mock_save_text.assert_called_with(conversation_id,"hola")
        self.assertEqual(mock_search_lyrics.call_count,0)


    @patch('music_assistant.bot.helpers.message_handlers.Conversation.get_last_message',
        autospec=True)
    @patch('music_assistant.bot.helpers.message_handlers.Message.save_text',
        autospec=True)
    @patch('music_assistant.bot.helpers.message_handlers.MusixMatchAPI.search_lyrics',
        autospec=True)
    def test_lyrics_payload_search_lyrics_on_musix_match(self, 
                    mock_search_lyrics,
                    mock_save_text, 
                    mock_get_last_message):
        # Arrange
        conversation_id = 1
        needs_follow_up = True
        payload = "LYRICS_PAYLOAD"
        found_songs_data = [{"name":"Sample_song"}]
        mock_get_last_message.return_value = (conversation_id,needs_follow_up, payload)
        mock_search_lyrics.return_value = found_songs_data

        # Act
        (response_data, response_type) = self.handler.process_text("Sample Lyrics")

        # Assert
        self.assertEqual(response_type, ResponseType.results)
        self.assertEqual(len(response_data["data"]),len(found_songs_data))
        #self.assertTrue(response_data["text"].startswith("Encontré"))

        mock_save_text.assert_called_with(conversation_id,"Sample Lyrics")
        self.assertEqual(mock_search_lyrics.call_count,1)

    @patch('music_assistant.bot.helpers.message_handlers.Conversation.get_last_message',
        autospec=True)
    @patch('music_assistant.bot.helpers.message_handlers.Message.save_text',
        autospec=True)
    @patch('music_assistant.bot.helpers.message_handlers.MusixMatchAPI.search_lyrics',
        autospec=True)
    def test_lyrics_payload_search_with_empty_result_send_sorry(self, 
                    mock_search_lyrics,
                    mock_save_text, 
                    mock_get_last_message):
        # Arrange
        conversation_id = 1
        needs_follow_up = True
        payload = "LYRICS_PAYLOAD"
        found_songs_data = []
        mock_get_last_message.return_value = (conversation_id,needs_follow_up, payload)
        mock_search_lyrics.return_value = found_songs_data

        # Act
        (response_data, response_type) = self.handler.process_text("Sample Lyrics2")

        # Assert
        self.assertEqual(response_type, ResponseType.text)
        self.assertTrue(response_data.startswith("Lo siento"))

        mock_save_text.assert_called_with(conversation_id,"Sample Lyrics2")
        self.assertEqual(mock_search_lyrics.call_count,1)


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


class HandlersOptionsTest(TestCase):
    """ OPTIONS proc: search lyrics, save to favorites"""

    def setUp(self):
        self.mock_record_message_and_payload = patch(
            'music_assistant.bot.helpers.message_handlers.Handlers.record_message_and_payload',autospec=True).start()
        self.mock_search_track_by_id = patch(
            'music_assistant.bot.helpers.message_handlers.Handlers.search_track_by_id',autospec=True).start()
        # User and Conversation Models
        self.mock_users_quantity = patch(
            'music_assistant.bot.helpers.message_handlers.User.users_quantity',autospec=True).start()
        self.mock_quantity_by_day = patch(
            'music_assistant.bot.helpers.message_handlers.Conversation.quantity_by_day',autospec=True).start()
        # Song Model
        self.mock_favorites_by_user = patch(
            'music_assistant.bot.helpers.message_handlers.Song.favorites_by_user',autospec=True).start()
        self.mock_get_top_songs = patch(
            'music_assistant.bot.helpers.message_handlers.Song.get_top_songs',autospec=True).start()
        self.addCleanup(patch.stopall)

    def test_on_search_lyrics_option_selected_saves_postback_mark_to_wait_for_lyrics(self):
        pass

    def test_on_favorite_option_selected_saves_track_in_users_favorites(self):
        pass