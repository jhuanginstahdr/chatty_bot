from abc import ABC, abstractmethod
from threading import Event

class AudioCapture(ABC):
    @abstractmethod
    def Capture(self, process_audio : callable, stop_event : Event) -> None:
        pass