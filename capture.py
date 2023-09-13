import speech_recognition as sr
import logging
import queue

"""
capture audio and buffer them in a queue
"""
def audio_capture(recognizer : sr.Recognizer, source : sr.AudioSource, audio_q : queue) -> sr.AudioData:
    if not isinstance(recognizer, sr.Recognizer):
        raise Exception(f'{recognizer} is not type of {sr.Recognizer}')
    if not isinstance(source, sr.AudioSource):
        raise Exception(f'{source} is not type of {sr.AudioSource}')
    if not isinstance(audio_q, queue.Queue):
        raise Exception(f'{audio_q} is not type of {queue.Queue}')
    
    #to do: put a limit on the queue, and dequeue the oldest audio when the size of queue reaches that limit
    #perhaps this should be done with a custom queue object that manages the queue by size etc.
    print('Listening for speech...')
    audio = None
    try:
        audio = recognizer.listen(source)
        #audio = process_audio(audio)
        audio_q.put(audio)
    except Exception:
        logging.error('Unknown error with audio capturing')