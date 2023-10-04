from speech_recognition import Recognizer, AudioData, AudioSource, WaitTimeoutError
from ...Events.custom_event import CustomEvent, CustomEventBus, EventDecorator, GetEventName
from threading import Event
from logging import info, error
from .capture import AudioCapture
from time import sleep

class AudioCaptureBySpeechRecognition(AudioCapture):

    def __init__(self, event_bus : CustomEventBus, recognizer : Recognizer, audio_source : AudioSource):
        """
        Cosntructs an AudioCapture object for capturing audio data using speech_recognition package

        Args:
            recognizer (Recognizer) : object required for capturing audio data
            audio_source (AudioSource) : source of audio data (e.g. microphone or file)
        """
        if not isinstance(recognizer, Recognizer):
            raise TypeError(f'{recognizer} is not type of {Recognizer}')
        if not isinstance(audio_source, AudioSource):
            raise TypeError(f'{audio_source} is not type of {AudioSource}')
        
        self.recognizer = recognizer
        self.audio_source = audio_source
        self.event_bus = event_bus

    @EventDecorator('AudioCapturedEvent')
    def AudioCapturedEvent(self, audio : AudioData) -> None:
        self.event_bus.publish(CustomEvent(GetEventName(self.AudioCapturedEvent), audio))

    def EventLoop(self, stop_event : Event):
        if not isinstance(stop_event, Event):
            raise TypeError(f'{stop_event} is not of type {Event}')
        
        info('Listening for speech...')
        source = self.audio_source.__enter__()
        self.recognizer.adjust_for_ambient_noise(source)
        while not stop_event.is_set():
            audio = AudioCaptureBySpeechRecognition.CaptureOnce(self.recognizer, source)
            self.AudioCapturedEvent(audio)

        info(f'exited audio capturing loop')

    def Capture(self, stop_event : Event, **kwargs) -> None:
        pass

    @staticmethod
    def CaptureOnce(recognizer : Recognizer, source : AudioSource) -> AudioData:
        """
        Return the captured segment of some audio data

        Args:
            recognizer (Recognizer) : object that captures audio data from source
            source (AudioSource) : the source of audio data

        Returns:
            The captured audio data given recognizer and audio source
        """
        if not isinstance(recognizer, Recognizer):
            raise TypeError(f'{recognizer} is not type of {Recognizer}')
        if not isinstance(source, AudioSource):
            raise TypeError(f'{source} is not type of {AudioSource}')
        
        try:
            return recognizer.listen(source, phrase_time_limit=10)
        except WaitTimeoutError as wait_e:
            error(f'Wait timeout {wait_e}')
        except Exception as unknown_e:
            error(f'Unknown error with audio capturing {unknown_e}')