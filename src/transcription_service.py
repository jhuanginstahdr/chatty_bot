from threading import Thread, Event
from queue import Queue, Empty, Full
from logging import debug, error

from transcription import AudioTranscription

def CreateAudioTranscriptionService(
    transcript : AudioTranscription, 
    audio_q : Queue, 
    text_q : Queue, 
    stop_event : Event) -> Thread:

    # retrive an audio data from audio_q
    def get_from_audio_queue():
        try:
            return audio_q.get(timeout=0.5)
        except Empty:
            debug('did not receive any audio data')
    
    # store the transcript in text_q
    def put_in_text_queue(text):
        if not text:
            return
        debug(f'putting {text} in text_q')
        try:
            text_q.put(text)
        except Full:
            error('cannot place item in queue')

    return Thread(target=lambda: transcript.Transcribe(get_from_audio_queue, put_in_text_queue, stop_event))