from speech_recognition import Recognizer, Microphone
from threading import Thread, Event, main_thread, enumerate as thread_enumerate
from queue import Queue, Empty
import time, os, logging

from capture import AudioCapture
from transcription import AudioTranscription
from response import ResponseFromOpenAI

"""
A demo on how the three services: capture, transcription and response work together
to feed speech (in English) as prompt to a Large-Language-Model like OpenAI's GPT
"""
def direct_speech_to_text_to_llm() -> None:

    recognizer = Recognizer()
    stop_event = Event()

    audio_q = Queue(100)
    text_q = Queue(1000)

    # store the captured audio data in audio_q
    def put_in_audio_queue(audio):
        if audio is None:
            return
        logging.debug('putting audio in audio_q')
        audio_q.put(audio)

    # retrive an audio data from audio_q
    def get_from_audio_queue():
        try:
            return audio_q.get(timeout=0.5)
        except Empty:
            logging.debug('did not receive any audio data')
    
    # store the transcript in text_q
    def put_in_text_queue(text):
        if not text:
            return
        logging.debug(f'putting {text} in text_q')
        text_q.put(text)

    # retrieve all texts from text_q and join them to form a prompt
    def create_prompt_from_text_queue() -> str:
        if text_q.empty():
            return None
        logging.debug(f'constructing prompt from text_q')
        list = []
        while True:
            try:
                list.append(text_q.get(timeout=1))
            except Empty:
                break
        if not list:
            return None
        prompt = " ".join(list)
        logging.info(f'prompt: {prompt}')
        return prompt
    
    # print out the response
    def print_response(text : str):
        if text:
            logging.info(f'response: {text}')

    #a thread for audio capture
    capture = AudioCapture(recognizer, Microphone())
    Thread(target=lambda: capture.Capture(put_in_audio_queue, stop_event)).start()

    #thread for audio trancription
    transcript = AudioTranscription(recognizer)
    Thread(target=lambda: transcript.Transcribe(get_from_audio_queue, put_in_text_queue, stop_event)).start()

    #thread for feeding prompt and getting responses via OpenAI's API
    response = ResponseFromOpenAI(os.environ.get('OPENAI_API_KEY'))
    Thread(target=lambda: response.Query(create_prompt_from_text_queue, print_response, stop_event)).start()

    try:
        while True:
            time.sleep(10)
            pass
    except KeyboardInterrupt:
        stop_event.set()

    for thread in thread_enumerate():
        if thread == main_thread():
            continue
        thread.join()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    direct_speech_to_text_to_llm()
    print('App has exited')