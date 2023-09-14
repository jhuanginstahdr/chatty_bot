import speech_recognition as sr
import threading
import time
import queue
import openai
import os
from capture import audio_capture
from transcribe import audio_transcription
from response import consume_text

api_key = os.environ.get('OPENAI_API_KEY')

#mechanism to stop the threads
stop_event = threading.Event()

def continuous_speech_capture(recognizer : sr.Recognizer, audio_q : queue):
    microphone = sr.Microphone()
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        while not stop_event.is_set():
            audio_capture(recognizer, source, audio_q)
            time.sleep(0.3)

def continuous_speech_processing(recognizer : sr.Recognizer, audio_q : queue, text_q : queue):
    while not stop_event.is_set():
        audio_transcription(recognizer, audio_q, text_q)
        time.sleep(0.5)

def continuous_llm_response(text_q : queue.Queue):
    openai.api_key = api_key
    while not stop_event.is_set():
        consume_text(text_q)
        time.sleep(0.7)

if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG)
    recognizer = sr.Recognizer()
    audio_q = queue.Queue()
    text_q = queue.Queue()

    # Create and start the recognition thread
    capture_thread = threading.Thread(target=lambda: continuous_speech_capture(recognizer, audio_q))
    capture_thread.daemon = True  # The thread will exit when the main program exits
    capture_thread.start()

    process_thread = threading.Thread(target=lambda: continuous_speech_processing(recognizer, audio_q, text_q))
    process_thread.daemon = True  # The thread will exit when the main program exits
    process_thread.start()

    response_thread = threading.Thread(target=lambda: continuous_llm_response(text_q))
    response_thread.daemon = True
    response_thread.start()

    try:
        while True:
            time.sleep(100)
            pass
    except KeyboardInterrupt:
        stop_event.set()

    capture_thread.join()
    process_thread.join()
    response_thread.join()

    print('App exiting phrase captured')