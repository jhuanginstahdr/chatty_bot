from abc import ABC, abstractmethod
from threading import Event

class ResponseGenerator(ABC):
    @abstractmethod
    def Query(self, stop_event : Event, **kwargs) -> None:
        pass