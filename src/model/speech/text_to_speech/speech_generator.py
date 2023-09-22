from abc import ABC, abstractmethod
from threading import Event

class SpeechGenerator(ABC):
    @abstractmethod
    def GenerateSpeech(self, get_text : callable, process_speech : callable, stop_event : Event) -> None:
        pass