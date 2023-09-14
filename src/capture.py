import speech_recognition as sr
import logging
import time
import threading

class AudioCapture:

    """
    Cosntructor of AudioCapture

    Args:
        recognizer (sr.Recognizer) : object required for capturing audio data
        microphone (sr.Microphone) : device for capturing audio data
    """
    def __init__(self, recognizer : sr.Recognizer, microphone : sr.Microphone):
        if not isinstance(recognizer, sr.Recognizer):
            raise Exception(f'{recognizer} is not type of {sr.Recognizer}')
        if not isinstance(microphone, sr.Microphone):
            raise Exception(f'{microphone} is not type of {sr.Microphone}')
        self.recognizer = recognizer
        self.microphone = microphone

    """
    Continuous audio capture

    Args:
        process_audio (method) : provided process on top of the captured audio data
        stop_event (threading.Event) : mechanism that stops the continuous capture

    Returns:
        None
    """
    def ContinuousCapture(self, process_audio : callable, stop_event : threading.Event, sleep = 1) -> None:
        if not callable(process_audio):
            raise Exception(f'{process_audio} is not callable')
        if not isinstance(stop_event, threading.Event):
            raise Exception(f'{stop_event} is not of type {threading.Event}')
        
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while not stop_event.is_set():
                audio = AudioCapture.CaptureOnce(self.recognizer, source)
                process_audio(audio)
                time.sleep(sleep)

    """
    Captured audio data

    Args:
        recognizer (sr.Recognizer) : object that captures audio data from source
        source (sr.AudioSource) : the source of audio data

    Returns:
        The captured audio data given recognizer and audio source
    """
    @staticmethod
    def CaptureOnce(recognizer : sr.Recognizer, source : sr.AudioSource) -> sr.AudioData:
        if not isinstance(recognizer, sr.Recognizer):
            raise Exception(f'{recognizer} is not type of {sr.Recognizer}')
        if not isinstance(source, sr.AudioSource):
            raise Exception(f'{source} is not type of {sr.AudioSource}')
        
        print('Listening for speech...')
        try:
            return recognizer.listen(source)
        except Exception:
            logging.error('Unknown error with audio capturing')