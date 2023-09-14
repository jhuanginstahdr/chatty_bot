import speech_recognition as sr
import logging
import time
import threading

class AudioTranscript:

    """
    Cosntructor of AudioTranscript

    Args:
        recognizer (sr.Recognizer) : object required for transcribing audio data
    """
    def __init__(self, recognizer : sr.Recognizer):
        if not isinstance(recognizer, sr.Recognizer):
            raise Exception(f'{recognizer} is not type of {sr.Recognizer}')
        self.recognizer = recognizer

    """
    Continuous audio transcription

    Args:
        get_audio_data (method) : responsible for returning audio data for transcription
        process_transcript (method) : responsible for consuming transcript
        stop_event (threading.Event) : mechanism that stops the continuous transcription

    Returns:
        None
    """
    def ContinuousAudioDataTranscription(self, get_audio_data : callable, process_transcript : callable, stop_event : threading.Event, sleep = 1) -> None:
        if not callable(get_audio_data):
            raise Exception(f'{get_audio_data} is not callable')
        if not callable(process_transcript):
            raise Exception(f'{process_transcript} is not callable')
        if not isinstance(stop_event, threading.Event):
            raise Exception(f'{stop_event} is not type of {threading.Event}')
        
        while not stop_event.is_set():
            audio = get_audio_data()
            if (audio is None):
                continue
            if not isinstance(audio, sr.AudioData):
                raise Exception(f'{audio} is not type of {sr.AudioData}')
            transcript = AudioTranscript.TranscribeOnce(self.recognizer, audio)
            process_transcript(transcript)
            time.sleep(sleep)

    """
    Transcribe the audio captured

    Args:
        recognizer (sr.Recognizer) : object required for transcribing audio data
        audio (sr.AudioData) : audio data for transcription

    Returns:
        text recognized from audio data
    """
    @staticmethod
    def TranscribeOnce(recognizer : sr.Recognizer, audio : sr.AudioData) -> str:
        if not isinstance(recognizer, sr.Recognizer):
            raise Exception(f'{recognizer} is not type of {sr.Recognizer}')
        if not isinstance(audio, sr.AudioData):
            raise Exception(f'{audio} is not of type {sr.AudioData}')
        
        try:
            return recognizer.recognize_google(audio, language="en-US")
        except sr.UnknownValueError:
            logging.error("Google Web Speech API could not understand the audio")
        except sr.RequestError as e:
            logging.error(f"Could not request results from Google Web Speech API {e}")
        except KeyboardInterrupt:
            logging.info("Stopping the speech recognition.")