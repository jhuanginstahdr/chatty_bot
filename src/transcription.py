from abc import ABC, abstractmethod
from threading import Event

class AudioTranscription(ABC):
    @abstractmethod
    def Transcribe(self, get_audio_data : callable, process_transcript : callable, stop_event : Event) -> None:
        pass