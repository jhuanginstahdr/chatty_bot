from unittest import TestCase
from unittest.mock import Mock, patch
from src.model.large_language_model.response_by_llm import ResponseByLLM
from src.model.large_language_model.LLM_adaptor import LLM_Adaptor
from threading import Event

class TestResponseByLLM(TestCase):

    def setUp(self):
        """
        Initial setup for the tests for ResponseByLLM
        """
        self.response_llm_adaptor = Mock(spec=LLM_Adaptor)
        self.response_service = ResponseByLLM(self.response_llm_adaptor)

    def test_init(self):
        """
        Test __init__ that raises exceptions on invalid args
        """
        with self.assertRaises(Exception):
            # Mock an invalid llm adaptor
            invalid_llm_adaptor = Mock()
            ResponseByLLM(invalid_llm_adaptor)

    def test_query_once(self):
        """
        Test QueryOnce with mocked prompt and receive mocked response
        """
        mock_prompt = "Test Prompt"
        mock_response = 'Test Response'
        self.response_llm_adaptor.ParseResponse.return_value = mock_response

        # Prompt is not empty
        response = self.response_service.QueryOnce(mock_prompt)
        self.assertEqual(response, mock_response)
        
    # def test_transcribe_once_with_empty_prompt(self):
    #     """
    #     Test QueryOnce with empty prompt
    #     """
    #     response = self.response_service.QueryOnce('')
    #     self.assertEqual(response, None)

    # def test_transcribe_once_with_invalid_prompt(self):
    #     """
    #     Test QueryOnce with invalid prompt
    #     """
    #     with self.assertRaises(Exception):
    #         invalid_prompt = Mock()
    #         self.response_service.QueryOnce(invalid_prompt)

    # @patch('openai.ChatCompletion.create')
    # def test_query_once_with_invalid_api_key(self, mock_create):
    #     """
    #     Test QueryOnce with invalid API Key
    #     """
    #     prompt = "Test prompt"
    #     mock_create.side_effect = Exception('Invalid API Key')

    #     with self.assertRaises(Exception):
    #         # Prompt is not empty
    #         self.response_service.QueryOnce(prompt)

    # @patch('openai.ChatCompletion.create')
    # def test_query_once_with_undefined_response(self, mock_create):
    #     """
    #     Test QueryOnce with invalid API Key
    #     """
    #     prompt = "Test prompt"

    #     with self.assertRaises(Exception):
    #         invalid_response = Mock()
    #         mock_create.return_value = invalid_response
    #         self.response_service.QueryOnce(prompt)

    # @patch('openai.ChatCompletion.create')
    # def test_query(self, mock_create):
    #     """
    #     Test Query with valid get_prompt, process_response and stop_event
    #     """
    #     mock_get_prompt = Mock(return_value=Mock(spec=str))
    #     mock_process_response = Mock()

    #     # Mock stop_event
    #     mock_stop_event = Mock(spec=Event)
    #     mock_stop_event.is_set.side_effect = [False, True]  

    #     mock_response = {
    #         "choices": [{"message": {"content": "Test response"}}]
    #     }
    #     mock_create.return_value = mock_response

    #     # Mock audio transcription
    #     self.response_service.Query(mock_get_prompt, mock_process_response, mock_stop_event)

    #     # Check if mock_get_audio_data and mock_process_transcript were called
    #     mock_get_prompt.assert_called_once()
    #     mock_process_response.assert_called_once()

    # def test_query_with_invalid_inputs(self):
    #     """
    #     Test Qeury with invalid inputs
    #     """
    #     mock_get_prompt = Mock(return_value=Mock(spec=str))
    #     mock_process_response = Mock()
    #     mock_stop_event = Mock(spec=Event)
    #     mock_stop_event.is_set.side_effect = [False, True]  

    #     with self.assertRaises(Exception):
    #         # Mock uncallable get_prompt
    #         invalid_get_prompt = 123
    #         self.response_service.Query(invalid_get_prompt, mock_process_response, mock_stop_event)

    #     with self.assertRaises(Exception):
    #         # Mock uncallable process_response
    #         invalid_process_transcript = 123
    #         self.response_service.Query(mock_get_prompt, invalid_process_transcript, mock_stop_event)

    #     with self.assertRaises(Exception):
    #         # Mock invalid stop_event
    #         invalid_stop_event = Mock()
    #         self.response_service.Query(mock_get_prompt, mock_process_response, invalid_stop_event)