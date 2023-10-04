from speech_recognition import Recognizer, AudioData, UnknownValueError, RequestError
from ...Events.custom_event import CustomEvent, CustomEventBus, EventDecorator, GetEventName
from threading import Event
from logging import debug, error, info
from .transcription import AudioTranscription
from time import sleep

class AudioTranscriptionBySpeechRecognition(AudioTranscription):

    def __init__(self, event_bus : CustomEventBus, recognizer : Recognizer):
        """
        Constructs an object of AudioTranscription that transcribes audio data by
        functions provided in speech_recognition package

        Args:
            recognizer (Recognizer) : object required for transcribing audio data
        """
        if not isinstance(recognizer, Recognizer):
            raise TypeError(f'{recognizer} is not type of {Recognizer}')
        
        self.recognizer = recognizer
        self.event_bus = event_bus
    
    @EventDecorator('AudioTranscribedEvent')
    def AudioTranscribedEvent(self, transcript : str) -> None:
        self.event_bus.publish(CustomEvent(GetEventName(self.AudioTranscribedEvent), transcript))

    def AudioReceivedHandler(self, event : CustomEvent):
        if not isinstance(event, CustomEvent):
            raise TypeError(f'{event} is not type of {CustomEvent}')
        audio = event.data
        if not isinstance(audio, AudioData):
            raise TypeError(f'{audio} is not type of {AudioData}')
        transcript = AudioTranscriptionBySpeechRecognition.TranscribeOnce(self.recognizer, audio)
        self.AudioTranscribedEvent(transcript)

    def EventLoop(self, stop_event : Event):

        if not isinstance(stop_event, Event):
            raise TypeError(f'{stop_event} is not type of {Event}')
        
        while not stop_event.is_set():
            # looping to capture events
            sleep(0.5)

        info(f'exited audio transcription loop')

    def Transcribe(self, stop_event : Event, **kwargs) -> None:
        pass

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
            raise TypeError(f'{recognizer} is not type of {Recognizer}')
        if not isinstance(audio, AudioData):
            raise TypeError(f'{audio} is not of type {AudioData}')
        
        try:
            return recognizer.recognize_google(audio, language="en-US")
        except UnknownValueError as unknown_value_e:
            debug(f"Google Web Speech API could not understand the audio {unknown_value_e}")
        except RequestError as request_e:
            error(f"Could not request results from Google Web Speech API {request_e}")
        except Exception as unknown_e:
            error(f"Unknown error {unknown_e}")