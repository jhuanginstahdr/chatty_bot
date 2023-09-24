from abc import ABC, abstractmethod
from threading import Event

class AudioCapture(ABC):
    @abstractmethod
    def Capture(self, stop_event : Event, **kwargs) -> None:
        pass