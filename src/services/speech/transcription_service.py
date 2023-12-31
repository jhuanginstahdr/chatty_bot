from threading import Thread, Event
from queue import Queue, Empty, Full
from logging import debug, error, info
from src.model.speech.audio_transcription.transcription import AudioTranscription

def CreateAudioTranscriptionService(
    transcript : AudioTranscription, 
    audio_q : Queue, 
    text_q : Queue, 
    stop_event : Event) -> Thread:

    if not isinstance(transcript, AudioTranscription):
        raise Exception(f'{transcript} is not of type {AudioTranscription}')

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
        info(f'transcript: {text}')
        try:
            text_q.put(text)
        except Full:
            error('cannot place item in queue')

    return Thread(target=lambda: transcript.Transcribe(stop_event, 
                                                       get_audio_data = get_from_audio_queue, 
                                                       process_transcript = put_in_text_queue))