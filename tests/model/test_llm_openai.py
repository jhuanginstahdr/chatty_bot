from unittest import TestCase
from unittest.mock import Mock, patch
from src.model.large_language_model.LLM_OpenAI import LLM_OpenAI

class TestResponseByLLM(TestCase):

    def setUp(self):
        """
        Initial setup for the tests for ResponseByLLM
        """
        key = Mock(spec=str)
        self.llm_adaptor = LLM_OpenAI(key)

    def test_init(self):
        """
        Test __init__ that raises exceptions on invalid args
        """
        with self.assertRaises(Exception):
            # Mock an invalid api key
            invalid_key = Mock()
            LLM_OpenAI(invalid_key)

    @patch('openai.ChatCompletion.create')
    def test_consume_prompt(self, mock_create):
        """
        Test ConsumePrompt with mocked prompt and make sure llm_adaptor.reply is assigned mock_response
        """
        mock_prompt = 'Test Prompt'
        mock_response = 'Test Response'
        mock_create.return_value = mock_response
 
        self.llm_adaptor.ConsumePrompt(mock_prompt)
        self.assertEqual(mock_response, self.llm_adaptor.reply)

        mock_create.assert_called_with(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": mock_prompt}]
        )

    @patch('openai.ChatCompletion.create')
    def test_consume_prompt_error(self, mock_create):
        """
        Test ConsumePrompt with mocked prompt which raises error and make sure llm_adaptor.reply is None
        """
        mock_prompt = 'Test Prompt'

        with self.assertRaises(Exception):
            # raising an error while creating a response
            mock_create.return_value = Exception('Error querying')
            self.llm_adaptor.ConsumePrompt(mock_prompt)
            self.assertEqual(None, self.llm_adaptor.reply)

        mock_create.assert_called_with(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": mock_prompt}]
        )

    def test_parse_response(self):
        """
        Test ParseResponse when llm_adaptor.reply is valid
        """
        mock_response = {
            "choices": [{"message": {"content": "Test response"}}]
        }
        self.llm_adaptor.reply = mock_response
        self.assertEqual('Test response', self.llm_adaptor.ParseResponse())
        #make sure llm_adaptor.reply is cleared
        self.assertEqual(None, self.llm_adaptor.reply)
        
    def test_parse_response_none(self):
        """
        Test ParseResponse when llm_adaptor.reply is None
        """
        self.llm_adaptor.reply = None
        self.assertEqual(None, self.llm_adaptor.ParseResponse())
        
    def test_parse_response_invalid_reply(self):
        """
        Test ParseResponse when llm_adaptor.reply is invalid
        """
        with self.assertRaises(Exception):
            self.llm_adaptor.reply = ''
            self.llm_adaptor.ParseResponse()