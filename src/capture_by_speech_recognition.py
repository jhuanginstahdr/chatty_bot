from speech_recognition import Recognizer, Microphone, AudioData, AudioSource, WaitTimeoutError
from threading import Event
from logging import info, error
from capture import AudioCapture

class AudioCaptureBySpeechRecognition(AudioCapture):

    """
    Cosntructor

    Args:
        recognizer (Recognizer) : object required for capturing audio data
        microphone (Microphone) : device for capturing audio data
    """
    def __init__(self, recognizer : Recognizer, microphone : Microphone):
        if not isinstance(recognizer, Recognizer):
            raise Exception(f'{recognizer} is not type of {Recognizer}')
        if not isinstance(microphone, Microphone):
            raise Exception(f'{microphone} is not type of {Microphone}')
        
        self.recognizer = recognizer
        self.microphone = microphone

    """
    Continuous audio capture

    Args:
        process_audio (method) : provided process on top of the captured audio data
        stop_event (Event) : mechanism that stops the continuous capture

    Returns:
        None
    """
    def Capture(self, process_audio : callable, stop_event : Event) -> None:
        if not callable(process_audio):
            raise Exception(f'{process_audio} is not callable')
        if not isinstance(stop_event, Event):
            raise Exception(f'{stop_event} is not of type {Event}')
        
        info('Listening for speech...')
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while not stop_event.is_set():
                audio = AudioCaptureBySpeechRecognition.CaptureOnce(self.recognizer, source)
                process_audio(audio)

    """
    Captured one segment of audio data

    Args:
        recognizer (Recognizer) : object that captures audio data from source
        source (AudioSource) : the source of audio data

    Returns:
        The captured audio data given recognizer and audio source
    """
    @staticmethod
    def CaptureOnce(recognizer : Recognizer, source : AudioSource) -> AudioData:
        if not isinstance(recognizer, Recognizer):
            raise Exception(f'{recognizer} is not type of {Recognizer}')
        if not isinstance(source, AudioSource):
            raise Exception(f'{source} is not type of {AudioSource}')
        
        try:
            return recognizer.listen(source)
        except WaitTimeoutError:
            error('Wait timeout')
        except Exception:
            error('Unknown error with audio capturing')