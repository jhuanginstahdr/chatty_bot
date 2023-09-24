from abc import ABC, abstractmethod
from threading import Event

class AudioTranscription(ABC):
    @abstractmethod
    def Transcribe(self, stop_event : Event, **kwargs) -> None:
        pass