from unittest import TestCase
from unittest.mock import Mock
from pyttsx3 import Engine
from src.model.speech.text_to_speech.speech_generator_by_pyttsx3 import SpeechGeneratorByPyttsx3
from threading import Event

class TestSpeechGenerationByPyttsx3(TestCase):

    def setUp(self):
        """
        Initial setup for the tests for ResponseByLLM
        """
        self.mock_engine = Mock(spec=Engine)
        self.speech_generator = SpeechGeneratorByPyttsx3(self.mock_engine)

    def test_init(self):
        """
        Test with invalid engine as arguments
        """
        with self.assertRaises(Exception) :
            invalid_engine = Mock()
            SpeechGeneratorByPyttsx3(invalid_engine)

    def test_test_generate_speech_once(self):
        """
        Test GenerateSpeechOnce with a non empty str and ensure the engine calls are invoked
        """
        self.speech_generator.GenerateSpeechOnce("Test speech")
        self.mock_engine.say.assert_called_once()
        self.mock_engine.startLoop.assert_called_once()
        self.mock_engine.iterate.assert_called_once()
        self.mock_engine.endLoop.assert_called_once()

    def test_test_generate_speech_once_with_empty_text(self):
        """
        Test GenerateSpeechOnce with an empty str and ensure that the engine calls are not invoked
        """
        self.speech_generator.GenerateSpeechOnce('')
        self.mock_engine.say.assert_not_called()
        self.mock_engine.startLoop.assert_not_called()
        self.mock_engine.iterate.assert_not_called()
        self.mock_engine.endLoop.assert_not_called()

    def test_generate_speech_once_with_error(self):
        """
        Test GenerateSpeechOnce with an empty str and ensure that the engine calls are not invoked
        """
        with self.assertLogs(level='ERROR'):
            self.mock_engine.say.side_effect = Exception()
            self.speech_generator.GenerateSpeechOnce('Test speech')

        with self.assertLogs(level='ERROR'):
            self.mock_engine.startLoop.side_effect = Exception()
            self.speech_generator.GenerateSpeechOnce('Test speech')

        with self.assertLogs(level='ERROR'):
            self.mock_engine.iterate.side_effect = Exception()
            self.speech_generator.GenerateSpeechOnce('Test speech')

        with self.assertLogs(level='ERROR'):
            self.mock_engine.endLoop.side_effect = Exception()
            self.speech_generator.GenerateSpeechOnce('Test speech')

    def test_generate_speech(self):
        """
        Test GenerateSpeech method with valid get_text callback and stop_event
        """
        mock_get_text = Mock()
        mock_get_text.return_value = 'Test speech'

        mock_stop_event = Mock(spec=Event)
        mock_stop_event.is_set.side_effect = [False, True]

        self.speech_generator.GenerateSpeech(mock_stop_event, get_text = mock_get_text)

        mock_get_text.assert_called_once()

    def test_generate_speech_invalid_args(self):
        """
        Test GenerateSpeech with invalid get_text callback and stop_event
        """
        mock_get_text = Mock()
        mock_get_text.return_value = ''

        mock_stop_event = Mock(spec=Event)
        mock_stop_event.is_set.side_effect = [False, True]

        #provided a not callable get_text method
        with self.assertRaises(Exception):
            invalid_get_text = 123
            self.speech_generator.GenerateSpeech(mock_stop_event, get_text = invalid_get_text)

        #provided a valid get_text method but did not specify its key
        with self.assertRaises(Exception):
            invalid_get_text = 123
            self.speech_generator.GenerateSpeech(mock_stop_event, mock_get_text)

        #provided an invalid stop event
        with self.assertRaises(Exception):
            invalid_stop_event = Mock()
            self.speech_generator.GenerateSpeech(invalid_stop_event, get_text = mock_get_text)

        mock_get_text.assert_not_called()
