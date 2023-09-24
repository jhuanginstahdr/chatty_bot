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
        self.mock_recognizer = Mock(spec=Recognizer)
        self.mock_audio_source = Mock(spec=AudioSource)
        self.mock_audio_source.__enter__ = Mock(return_value=self.mock_audio_source)
        self.capture_service = AudioCaptureBySpeechRecognition(self.mock_recognizer, self.mock_audio_source)

    def test_init(self):
        """
        Test __init__ that raises exceptions on invalid args
        """
        with self.assertRaises(Exception):
            # Test invalid recognizer
            invalid_recognizer = Mock()
            AudioCaptureBySpeechRecognition(invalid_recognizer, self.mock_audio_source)

        with self.assertRaises(Exception):
            # Test invalid audio_source
            invalid_audio_source = Mock()
            AudioCaptureBySpeechRecognition(self.mock_recognizer, invalid_audio_source)

    def test_capture_once(self):
        """
        Test CaptureOnce with valid args
        """
        # Configure mock Recognizer and AudioSource
        audio_data_mock = Mock()
        self.mock_recognizer.listen.return_value = audio_data_mock

        captured_audio = AudioCaptureBySpeechRecognition.CaptureOnce(self.mock_recognizer, self.mock_audio_source)

        self.assertEqual(captured_audio, audio_data_mock)
        self.mock_recognizer.listen.assert_called_with(self.mock_audio_source, phrase_time_limit=10)

    def test_capture_once_with_invalid_inputs(self):
        """
        Test CaptureOnce with invalid inputs
        """
        with self.assertRaises(Exception):
            # Mock an invalid Recognizer
            invalid_recognizer = Mock()
            AudioCaptureBySpeechRecognition.CaptureOnce(invalid_recognizer, self.mock_audio_source)

        with self.assertRaises(Exception):
            # Mock an invalid AudioSource
            invalid_source = Mock()
            AudioCaptureBySpeechRecognition.CaptureOnce(self.mock_recognizer, invalid_source)

    def test_capture_once_with_caught_errors(self):
        """
        Test CaptureOnce with errors raised by listen
        """
        with self.assertLogs(level='ERROR'):
            self.mock_recognizer.listen.side_effect = WaitTimeoutError("Wait timeout")
            audio_data = AudioCaptureBySpeechRecognition.CaptureOnce(self.mock_recognizer, self.mock_audio_source)
            self.assertIsNone(audio_data)

        with self.assertLogs(level='ERROR'):
            self.mock_recognizer.listen.side_effect = Exception("Unknown error")
            audio_data = AudioCaptureBySpeechRecognition.CaptureOnce(self.mock_recognizer, self.mock_audio_source)
            self.assertIsNone(audio_data)

    @patch('src.model.speech.audio_capture.capture_by_speech_recognition.AudioCaptureBySpeechRecognition.CaptureOnce')
    def test_capture(self, _):
        """
        Test Capture with valid args and ensure that process_audio is called
        """
        process_audio_mock = Mock()
        stop_event_mock = Mock(spec=Event)
        stop_event_mock.is_set.side_effect = [False, True]  

        self.capture_service.Capture(stop_event_mock, process_audio = process_audio_mock)

        # Ensure the process_audio method was called
        process_audio_mock.assert_called()

    def test_capture_with_invalid_inputs(self):
        """
        Test Capture with invalid inputs
        """
        process_audio_mock = Mock()
        stop_event_mock = Mock(spec=Event)

        with self.assertRaises(Exception):
            # Mock uncallable process_audio method
            invalid_process_audio = 123
            self.capture_service.Capture(stop_event_mock, process_audio = invalid_process_audio)

        with self.assertRaises(Exception):
            # Mock uncallable process_audio method
            invalid_process_audio = 123
            self.capture_service.Capture(stop_event_mock, invalid_kwarg = process_audio_mock)

        with self.assertRaises(Exception):
            # Mock invalid stop_event 
            invalid_stop_event = Mock()
            self.capture_service.Capture(invalid_stop_event, process_audio = process_audio_mock)


