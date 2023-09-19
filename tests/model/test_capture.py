from unittest import TestCase
from unittest.mock import Mock, patch
from speech_recognition import Recognizer, AudioSource, WaitTimeoutError
from src.model.speech.audio_capture.capture_by_speech_recognition import AudioCaptureBySpeechRecognition
from threading import Event

class TestAudioCaptureBySpeechRecognition(TestCase):

    def setUp(self):
        """
        Initial setup for the tests designed using AudioCaptureBySpeechRecognition package for audio capture
        """
        # Mock Recognizer and AudioSource
        self.mock_recognizer = Mock(spec=Recognizer)
        self.mock_audio_source = Mock(spec=AudioSource)

        # Patch the context manager to return another mock object
        self.mock_audio_source.__enter__ = Mock(return_value=self.mock_audio_source)

        self.capture_service = AudioCaptureBySpeechRecognition(self.mock_recognizer, self.mock_audio_source)

    def test_init(self):
        """
        Test __init__ that raises exceptions on invalid args
        """
        with self.assertRaises(Exception):
            # Test invalid recognizer
            AudioCaptureBySpeechRecognition(None, self.mock_audio_source)

        with self.assertRaises(Exception):
            # Test invalid audio_source
            AudioCaptureBySpeechRecognition(self.mock_recognizer, None)

    def test_capture_once(self):
        """
        Test AudioCaptureBySpeechRecognition.CaptureOnce with valid args
        """
        # Configure mock Recognizer and AudioSource
        audio_data_mock = Mock()
        self.mock_recognizer.listen.return_value = audio_data_mock

        captured_audio = AudioCaptureBySpeechRecognition.CaptureOnce(self.mock_recognizer, self.mock_audio_source)

        self.assertEqual(captured_audio, audio_data_mock)
        self.mock_recognizer.listen.assert_called_with(self.mock_audio_source, phrase_time_limit=10)

    def test_invalid_recognizer(self):
        """
        Test AudioCaptureBySpeechRecognition.CaptureOnce with invalid recognizer
        """
        # Mock an invalid Recognizer
        invalid_recognizer = Mock()
        invalid_recognizer.side_effect = Exception("Invalid recognizer")

        with self.assertRaises(Exception):
            AudioCaptureBySpeechRecognition.CaptureOnce(invalid_recognizer, self.mock_audio_source)

    def test_invalid_source(self):
        """
        Test AudioCaptureBySpeechRecognition.CaptureOnce with invalid recognizer
        """
        # Mock an invalid AudioSource
        invalid_source = Mock()
        invalid_source.side_effect = Exception("Invalid source")

        with self.assertRaises(Exception):
            AudioCaptureBySpeechRecognition.CaptureOnce(self.mock_recognizer, invalid_source)

    def test_wait_timeout_error(self):
        """
        Test AudioCaptureBySpeechRecognition.CaptureOnce with time out error
        """
        # Mock WaitTimeoutError
        self.mock_recognizer.listen.side_effect = WaitTimeoutError("Wait timeout")

        with self.assertLogs(level='ERROR'):
            audio_data = AudioCaptureBySpeechRecognition.CaptureOnce(self.mock_recognizer, self.mock_audio_source)
            self.assertIsNone(audio_data)

    def test_unknown_error(self):
        """
        Test AudioCaptureBySpeechRecognition.CaptureOnce with unknown error
        """
        # Mock an unknown error during capturing
        self.mock_recognizer.listen.side_effect = Exception("Unknown error")

        with self.assertLogs(level='ERROR'):
            audio_data = AudioCaptureBySpeechRecognition.CaptureOnce(self.mock_recognizer, self.mock_audio_source)
            self.assertIsNone(audio_data)

    @patch('src.model.speech.audio_capture.capture_by_speech_recognition.AudioCaptureBySpeechRecognition.CaptureOnce')
    def test_capture(self, _):
        """
        Test AudioCaptureBySpeechRecognition.Capture with valid args
        """
        # Mock process_audio method
        process_audio_mock = Mock()

        # Mock the stop event
        stop_event_mock = Mock(spec=Event)
        # Exit loop on the second iteration
        stop_event_mock.is_set.side_effect = [False, True]  

        self.capture_service.Capture(process_audio_mock, stop_event_mock)

        # Ensure the process_audio method was called
        process_audio_mock.assert_called()

    def test_capture_process_audio_not_callable(self):
        """
        Test AudioCaptureBySpeechRecognition.Capture with process_audio_mock not being callable
        """
        # Mock process_audio method
        invalid_process = 123

        # Mock the stop event
        stop_event_mock = Mock(spec=Event)

        with self.assertRaises(Exception):
            self.capture_service.Capture(invalid_process, stop_event_mock)

    def test_capture_invalid_stop_event(self):
        """
        Test AudioCaptureBySpeechRecognition.Capture with invalid stop_event
        """
        # Mock process_audio method
        process_audio_mock = Mock()

        # Mock the stop event 
        invalid_stop_event = Mock()

        with self.assertRaises(Exception):
            self.capture_service.Capture(process_audio_mock, invalid_stop_event)

