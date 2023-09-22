import pyttsx3
from threading import Event
from logging import error, info
from .speech_generator import SpeechGenerator

class SpeechGeneratorByPyttsx3(SpeechGenerator):
    def __init__(self):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        self.engine = engine

    @staticmethod
    def IsSpaceOnly(text : str) -> bool:
        if not text:
            return True
        return all(char.isspace() for char in text)

    def PlayGeneratedSpeechOnce(self, text : str) -> None:
        """
        Generate speech given the text and play the speech

        Args:
            text (str) : text to convert to audio speech

        Returns:
            None
        """
        if SpeechGeneratorByPyttsx3.IsSpaceOnly(text):
            return
        try:
            self.engine.say(text)
            self.engine.startLoop(False)
            self.engine.iterate()
            self.engine.endLoop()
        except Exception as e:
            error(f'Error generating and playing back the speech {e}')

    def GenerateSpeech(self, get_text : callable, abort_speech : callable, stop_event : Event):
        """
        Continuous text-to-speech-generation and playback in a loop where the loop ends when the stop_event is set.
        The texts for speech generation are consumed from get_audio_data function and the result

        Args:
            get_text (function) : responsible for returning text for speech generation
            stop_event (Event) : mechanism that stops the continuous text to speech generation

        Returns:
            None
        """
        if not callable(get_text):
            raise Exception(f'{get_text} is not callable')
        if not isinstance(stop_event, Event):
            raise Exception(f'{stop_event} is not type of {Event}')

        while not stop_event.is_set():
            text = get_text()
            self.PlayGeneratedSpeechOnce(text)
        
        info('exited speech generation loop')
        

