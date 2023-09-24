from abc import ABC, abstractmethod
from threading import Event

class SpeechGenerator(ABC):
    @abstractmethod
    def GenerateSpeech(self, stop_event : Event, **kwargs) -> None:
        pass