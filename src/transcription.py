from speech_recognition import Recognizer, AudioData, UnknownValueError, RequestError
from threading import Event
import logging
import time

class AudioTranscription:

    """
    Cosntructor of AudioTranscript

    Args:
        recognizer (Recognizer) : object required for transcribing audio data
    """
    def __init__(self, recognizer : Recognizer):
        if not isinstance(recognizer, Recognizer):
            raise Exception(f'{recognizer} is not type of {Recognizer}')
        
        self.recognizer = recognizer

    """
    Continuous audio transcription

    Args:
        get_audio_data (function) : responsible for returning audio data for transcription
        process_transcript (method) : responsible for consuming transcript
        stop_event (Event) : mechanism that stops the continuous transcription

    Returns:
        None
    """
    def Transcribe(self, get_audio_data : callable, process_transcript : callable, stop_event : Event, sleep = 1) -> None:
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
            transcript = AudioTranscription.TranscribeOnce(self.recognizer, audio)
            process_transcript(transcript)
            time.sleep(sleep)

    """
    Transcribe the audio captured

    Args:
        recognizer (Recognizer) : object required for transcribing audio data
        audio (AudioData) : audio data for transcription

    Returns:
        text recognized from audio data
    """
    @staticmethod
    def TranscribeOnce(recognizer : Recognizer, audio : AudioData) -> str:
        if not isinstance(recognizer, Recognizer):
            raise Exception(f'{recognizer} is not type of {Recognizer}')
        if not isinstance(audio, AudioData):
            raise Exception(f'{audio} is not of type {AudioData}')
        
        try:
            return recognizer.recognize_google(audio, language="en-US")
        except UnknownValueError:
            logging.error("Google Web Speech API could not understand the audio")
        except RequestError as e:
            logging.error(f"Could not request results from Google Web Speech API {e}")
        except KeyboardInterrupt:
            logging.info("Stopping the speech recognition.")