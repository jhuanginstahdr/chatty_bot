from speech_recognition import Recognizer, Microphone
from threading import Thread, Event, enumerate as thread_enumerate
from queue import Queue
import time
import os

from capture import AudioCapture
from transcription import AudioTranscript
from response import ResponseFromOpenAI

"""
A demo on how the three services: capture, transcription and response work together
to feed speech (in English) as prompt to a Large-Language-Model like OpenAI's GPT
"""
def direct_speech_to_text_to_llm() -> None:

    recognizer = Recognizer()
    stop_event = Event()

    audio_q = Queue()
    text_q = Queue()

    # store the captured audio data in audio_q
    def queue_audio(audio):
        if audio is not None:
            audio_q.put(audio)

    # retrive an audio data from audio_q
    def dequeue_audio():
        return None if audio_q.empty() else audio_q.get(timeout=1)
    
    # store the transcript in text_q
    def queue_text(text):
        if text:
            text_q.put(text)
            print(text)

    # retrieve all texts from text_q and join them to form a prompt
    def dequeue_text_for_prompt():
        if text_q.empty():
            return None
        list = []
        while not text_q.empty():
            list.append(text_q.get(timeout=1))
        return " ".join(list)
    
    # print out the response
    def print_response(text : str):
        if text:
            print(f'response: {text}')

    #a thread for audio capture
    capture = AudioCapture(recognizer, Microphone())
    capture_thread = Thread(target=lambda: capture.ContinuousCapture(queue_audio, stop_event, 0.1))
    capture_thread.daemon = True
    capture_thread.start()

    #thread for audio trancription
    transcript = AudioTranscript(recognizer)
    transcript_thread = Thread(target=lambda: transcript.ContinuousAudioDataTranscription(dequeue_audio, queue_text, stop_event, 0.1))
    transcript_thread.daemon = True
    transcript_thread.start()

    #thread for feeding prompt and getting responses via OpenAI's API
    response = ResponseFromOpenAI(os.environ.get('OPENAI_API_KEY'))
    response_thread = Thread(target=lambda: response.ContinousResponse(dequeue_text_for_prompt, print_response, stop_event, 0.1))
    response_thread.daemon = True
    response_thread.start()

    try:
        while True:
            time.sleep(10)
            pass
    except KeyboardInterrupt:
        stop_event.set()

    for thread in thread_enumerate():
        thread.join()

if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG)
    direct_speech_to_text_to_llm()
    print('App has exited')