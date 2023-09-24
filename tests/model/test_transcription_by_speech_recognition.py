from unittest import TestCase
from unittest.mock import Mock
from speech_recognition import AudioData, Recognizer, UnknownValueError, RequestError
from src.model.speech.audio_transcription.transcription_by_speech_recognition import AudioTranscriptionBySpeechRecognition
from threading import Event


class TestAudioTranscriptionBySpeechRecognition(TestCase):

    def setUp(self):
        """
        Initial setup for the tests designed using AudioTranscriptionBySpeechRecognition package for audio transcription
        """
        self.mock_recognizer = Mock(spec=Recognizer)
        self.mock_audio_data = Mock(spec=AudioData)
        self.transcription_service = AudioTranscriptionBySpeechRecognition(self.mock_recognizer)

    def test_init(self):
        """
        Test __init__ that raises exceptions on invalid args
        """
        with self.assertRaises(Exception):
            # Mock an invalid recognizer
            invalid_recognizer = Mock()
            AudioTranscriptionBySpeechRecognition(invalid_recognizer)

    def test_transcribe_once(self):
        """
        Test TranscribeOnce with valid input and compare the returned transcript
        """
        expected_transcript = "This is a test transcript"
        self.mock_recognizer.recognize_google.return_value = expected_transcript

        # Call the TranscribeOnce method
        result = AudioTranscriptionBySpeechRecognition.TranscribeOnce(self.mock_recognizer, self.mock_audio_data)

        # Check if the correct transcript is returned
        self.assertEqual(result, expected_transcript)
        
    def test_transcribe_once_with_invalid_inputs(self):
        """
        Test TranscribeOnce with invalid inputs
        """
        with self.assertRaises(Exception):
            # Mock an invalid recognizer
            invalid_recognizer = Mock()
            AudioTranscriptionBySpeechRecognition.TranscribeOnce(invalid_recognizer, self.mock_audio_data)

        with self.assertRaises(Exception):
            # Mock an invalid audio data
            invalid_audio_data = Mock()
            AudioTranscriptionBySpeechRecognition.TranscribeOnce(self.mock_recognizer, invalid_audio_data)

    def test_transcribe_once_with_caught_errors(self):
        """
        Test TranscribeOnce with errors raised from transcription
        """
        with self.assertLogs(level='DEBUG'):
            self.mock_recognizer.recognize_google.side_effect = UnknownValueError('Unknown Value')
            result = AudioTranscriptionBySpeechRecognition.TranscribeOnce(self.mock_recognizer, self.mock_audio_data)
            self.assertIsNone(result)

        with self.assertLogs(level='ERROR'):
            self.mock_recognizer.recognize_google.side_effect = RequestError('Request Error')
            result = AudioTranscriptionBySpeechRecognition.TranscribeOnce(self.mock_recognizer, self.mock_audio_data)
            self.assertIsNone(result)

    def test_transcribe(self):
        """
        Test Transcribe with valid audio data and get_audio_data and process_transcript methods and ensure that they are called
        """
        # Mock get_audio_data and process_transcript functions
        mock_get_audio_data = Mock(return_value=self.mock_audio_data)
        mock_process_transcript = Mock()

        # Mock stop_event
        mock_stop_event = Mock(spec=Event)
        mock_stop_event.is_set.side_effect = [False, True]  

        # Mock audio transcription
        self.transcription_service.Transcribe(mock_stop_event, 
                                              get_audio_data = mock_get_audio_data, 
                                              process_transcript = mock_process_transcript)

        # Check if mock_get_audio_data and mock_process_transcript were called
        mock_get_audio_data.assert_called_once()
        mock_process_transcript.assert_called_once()

    def test_transcribe_with_invalid_inputs(self):
        """
        Test Transcribe with invalid inputs
        """
        mock_get_audio_data = Mock(return_value=self.mock_audio_data)
        mock_process_transcript = Mock()
        mock_stop_event = Mock(spec=Event)
        mock_stop_event.is_set.side_effect = [False, True]  

        with self.assertRaises(Exception):
            # Mock uncallable get_audio_data
            invalid_get_audio_data = 123
            self.transcription_service.Transcribe(mock_stop_event, 
                                                  get_audio_data = invalid_get_audio_data, 
                                                  process_transcript = mock_process_transcript)
            
        with self.assertRaises(Exception):
            # Mock uncallable get_audio_data
            invalid_get_audio_data = 123
            self.transcription_service.Transcribe(mock_stop_event, 
                                                  invalid_kwarg = mock_get_audio_data, 
                                                  process_transcript = mock_process_transcript)

        with self.assertRaises(Exception):
            # Mock uncallable process_transcript
            invalid_process_transcript = 123
            self.transcription_service.Transcribe(mock_stop_event, 
                                                  get_audio_data = mock_get_audio_data, 
                                                  process_transcript = invalid_process_transcript)
            
        with self.assertRaises(Exception):
            # Mock uncallable process_transcript
            invalid_process_transcript = 123
            self.transcription_service.Transcribe(mock_stop_event, 
                                                  get_audio_data = mock_get_audio_data, 
                                                  invalid_kwarg = mock_process_transcript)

        with self.assertRaises(Exception):
            # Mock invalid stop_event
            invalid_stop_event = Mock()
            self.transcription_service.Transcribe(invalid_stop_event, 
                                                  get_audio_data = mock_get_audio_data, 
                                                  process_transcript = mock_process_transcript)

    def test_transcribe_invalid_audio_data(self):
        """
        Test Transcribe with invalid audio data from get_audio_data
        """
        # get_audio_data returns a Mock that is not of type AudioData
        mock_get_audio_data = Mock(return_value=Mock())
        mock_process_transcript = Mock()
        mock_stop_event = Mock(spec=Event)
        mock_stop_event.is_set.side_effect = [False, True]  

        with self.assertRaises(Exception):
            self.transcription_service.Transcribe(mock_stop_event, 
                                                  get_audio_data = mock_get_audio_data, 
                                                  process_transcript = mock_process_transcript)