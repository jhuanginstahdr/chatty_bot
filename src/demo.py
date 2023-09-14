import speech_recognition as sr
import threading
import time
import queue
import os
from capture import AudioCapture
from transcribe import AudioTranscript
from response import ResponseFromOpenAI

if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG)
    recognizer = sr.Recognizer()
    stop_event = threading.Event()

    audio_q = queue.Queue()
    text_q = queue.Queue()

    def queue_audio(audio):
        if audio is not None:
            audio_q.put(audio)

    def dequeue_audio():
        return None if audio_q.empty() else audio_q.get(timeout=1)
    
    def queue_text(text):
        if text:
            text_q.put(text)
            print(text)

    def text_queue_to_prompt():
        if text_q.empty():
            return None
        list = []
        while not text_q.empty():
            list.append(text_q.get(timeout=1))
        return " ".join(list)
    
    def print_response(text : str):
        if text:
            print(f'response: {text}')

    capture = AudioCapture(recognizer, sr.Microphone())
    capture_thread = threading.Thread(target=lambda: capture.ContinuousCapture(queue_audio, stop_event, 0.1))
    capture_thread.daemon = True
    capture_thread.start()

    transcript = AudioTranscript(recognizer)
    transcript_thread = threading.Thread(target=lambda: transcript.ContinuousAudioDataTranscription(dequeue_audio, queue_text, stop_event, 0.1))
    transcript_thread.daemon = True
    transcript_thread.start()

    response = ResponseFromOpenAI(os.environ.get('OPENAI_API_KEY'))
    response_thread = threading.Thread(target=lambda: response.ContinousResponse(text_queue_to_prompt, print_response, stop_event, 0.1))
    response_thread.daemon = True
    response_thread.start()

    try:
        while True:
            time.sleep(10)
            pass
    except KeyboardInterrupt:
        stop_event.set()

    capture_thread.join()
    transcript_thread.join()
    response_thread.join()

    print('App has exited')