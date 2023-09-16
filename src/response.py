from abc import ABC, abstractmethod
from threading import Event

class ResponseGenerator(ABC):
    @abstractmethod
    def Query(self, get_prompt : callable, process_response : callable, stop_event : Event) -> None:
        pass