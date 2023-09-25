from logging import debug, error
from queue import Queue, Full
from threading import Thread, Event
from src.model.speech.audio_capture.capture import AudioCapture

def CreateAudioCaptureService(
    capture : AudioCapture, 
    audio_q : Queue, 
    stop_event : Event) -> Thread:

    if not isinstance(capture, AudioCapture):
        raise Exception(f'{capture} is not of type {AudioCapture}')

    # store the captured audio data in audio_q
    def put_in_audio_queue(audio):
        if audio is None:
            return
        debug('putting audio in audio_q')
        try:
            audio_q.put(audio, timeout=0.5)
        except Full:
            error('cannot place item in queue')

    return Thread(target=lambda: capture.Capture(stop_event, process_audio = put_in_audio_queue))