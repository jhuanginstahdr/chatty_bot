from threading import Thread, Event
from queue import Queue, Empty
from logging import debug
from model.speech.text_to_speech.speech_generator import SpeechGenerator

def CreateSpeechGenerationService(
    generator : SpeechGenerator, 
    text_q : Queue, 
    stop_event : Event) -> Thread:

    if not isinstance(generator, SpeechGenerator):
        raise Exception(f'{generator} is not of type {SpeechGenerator}')

    # retrive an audio data from audio_q
    def get_from_text_queue():
        try:
            return text_q.get(timeout=0.5)
        except Empty:
            debug('there was no text for speech generation')

    return Thread(target=lambda: generator.GenerateSpeech(get_from_text_queue, None, stop_event))