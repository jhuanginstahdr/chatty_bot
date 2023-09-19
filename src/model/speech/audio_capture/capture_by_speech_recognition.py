from speech_recognition import Recognizer, AudioData, AudioSource, WaitTimeoutError
from threading import Event
from logging import info, error
from .capture import AudioCapture

class AudioCaptureBySpeechRecognition(AudioCapture):

    def __init__(self, recognizer : Recognizer, audio_source : AudioSource):
        """
        Cosntructs an AudioCapture object for capturing audio data using speech_recognition package

        Args:
            recognizer (Recognizer) : object required for capturing audio data
            audio_source (AudioSource) : source of audio data (e.g. microphone or file)
        """
        if not isinstance(recognizer, Recognizer):
            raise Exception(f'{recognizer} is not type of {Recognizer}')
        if not isinstance(audio_source, AudioSource):
            raise Exception(f'{audio_source} is not type of {AudioSource}')
        
        self.recognizer = recognizer
        self.audio_source = audio_source

    def Capture(self, process_audio : callable, stop_event : Event) -> None:
        """
        Continuous audio capture that feeds audio data to process_audio in a loop. The
        loop ends when the stop_event is set. 

        Args:
            process_audio (method) : provided process on top of the captured audio data
            stop_event (Event) : mechanism that stops the continuous capture

        Returns:
            None
        """
        if not callable(process_audio):
            raise Exception(f'{process_audio} is not callable')
        if not isinstance(stop_event, Event):
            raise Exception(f'{stop_event} is not of type {Event}')
        
        info('Listening for speech...')
        source = self.audio_source.__enter__()
        self.recognizer.adjust_for_ambient_noise(source)
        while not stop_event.is_set():
            audio = AudioCaptureBySpeechRecognition.CaptureOnce(self.recognizer, source)
            process_audio(audio)

        info(f'exited audio capturing loop')

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
            raise Exception(f'{recognizer} is not type of {Recognizer}')
        if not isinstance(source, AudioSource):
            raise Exception(f'{source} is not type of {AudioSource}')
        
        try:
            return recognizer.listen(source, phrase_time_limit=10)
        except WaitTimeoutError:
            error('Wait timeout')
        except Exception:
            error('Unknown error with audio capturing')