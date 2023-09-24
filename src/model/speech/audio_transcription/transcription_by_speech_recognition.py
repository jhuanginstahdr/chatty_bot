from speech_recognition import Recognizer, AudioData, UnknownValueError, RequestError
from threading import Event
from logging import debug, error, info
from .transcription import AudioTranscription

class AudioTranscriptionBySpeechRecognition(AudioTranscription):

    def __init__(self, recognizer : Recognizer):
        """
        Constructs an object of AudioTranscription that transcribes audio data by
        functions provided in speech_recognition package

        Args:
            recognizer (Recognizer) : object required for transcribing audio data
        """
        if not isinstance(recognizer, Recognizer):
            raise Exception(f'{recognizer} is not type of {Recognizer}')
        
        self.recognizer = recognizer

    def Transcribe(self, stop_event : Event, **kwargs) -> None:
        """
        Continuous audio transcription in a loop where the loop ends when the stop_event is set.
        The audio data for transcription is consumed from get_audio_data function and the result
        of the transcription is consumed by process_transcript method

        Args:
            get_audio_data (function) : responsible for returning audio data for transcription
            process_transcript (method) : responsible for consuming transcript
            stop_event (Event) : mechanism that stops the continuous transcription

        Returns:
            None
        """
        get_audio_data = kwargs.get('get_audio_data', None)
        process_transcript = kwargs.get('process_transcript', None)
        if not callable(get_audio_data):
            raise Exception(f'{get_audio_data} is not callable')
        if not callable(process_transcript):
            raise Exception(f'{process_transcript} is not callable')
        if not isinstance(stop_event, Event):
            raise Exception(f'{stop_event} is not type of {Event}')
        
        while not stop_event.is_set():
            audio = get_audio_data()
            if (audio is None):
                continue
            if not isinstance(audio, AudioData):
                raise Exception(f'{audio} is not type of {AudioData}')
            transcript = AudioTranscriptionBySpeechRecognition.TranscribeOnce(self.recognizer, audio)
            process_transcript(transcript)

        info(f'exited audio transcription loop')


    @staticmethod
    def TranscribeOnce(recognizer : Recognizer, audio : AudioData) -> str:
        """
        Return text (transcript) given a segment of audio data

        Args:
            recognizer (Recognizer) : object required for transcribing audio data
            audio (AudioData) : audio data for transcription

        Returns:
            text transcribed from audio data
        """
        if not isinstance(recognizer, Recognizer):
            raise Exception(f'{recognizer} is not type of {Recognizer}')
        if not isinstance(audio, AudioData):
            raise Exception(f'{audio} is not of type {AudioData}')
        
        try:
            return recognizer.recognize_google(audio, language="en-US")
        except UnknownValueError:
            debug("Google Web Speech API could not understand the audio")
        except RequestError as e:
            error(f"Could not request results from Google Web Speech API {e}")