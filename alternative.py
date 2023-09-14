import speech_recognition as sr
import threading
import time
import queue
import openai
from capture import audio_capture
from transcribe import audio_transcription
from response import generate_response

OPENAI_API_KEY = ''

#mechanism to stop the threads
stop_event = threading.Event()

def continuous_speech_capture(recognizer : sr.Recognizer, audio_q : queue):
    if not isinstance(audio_q, queue.Queue):
        raise Exception(f'{audio_q} is not of type {queue.Queue}')
    
    microphone = sr.Microphone()
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        while not stop_event.is_set():
            audio = audio_capture(recognizer, source, audio_q)
            if audio is not None:
                audio_q.put(audio)
            time.sleep(0.3)

def continuous_speech_processing(recognizer : sr.Recognizer, audio_q : queue, text_q : queue):
    if not isinstance(audio_q, queue.Queue):
        raise Exception(f'{audio_q} is not type of {queue.Queue}')
    if not isinstance(text_q, queue.Queue):
        raise Exception(f'{text_q} is not type of {queue.Queue}')
    
    while not stop_event.is_set():
        if audio_q.empty():
            continue
        audio = audio_q.get()
        if not isinstance(audio, sr.AudioData):
            raise Exception(f'{audio} is not type of {sr.AudioData}')
        transcript = audio_transcription(recognizer, audio)
        if transcript:
            text_q.put(transcript)
            print(f"Transcript: {transcript}")
        time.sleep(0.5)

def continuous_llm_response(text_q : queue.Queue):
    if not isinstance(text_q, queue.Queue):
        raise Exception(f'{text_q} is not type of {queue.Queue}')
    
    openai.api_key = OPENAI_API_KEY
    while not stop_event.is_set():
        if text_q.empty():
            continue
        print(f'aggregating {text_q.qsize()} number of messages')
        texts = []
        while not text_q.empty():
            texts.append(text_q.get())
        prompt = " ".join(texts)
        if not prompt:
            return
        generate_response(text_q)
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