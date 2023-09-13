import speech_recognition as sr
import threading
import time
import logging
import queue
import openai

#mechanism to stop the threads
stop_event = threading.Event()

class Bot:
    def __init__(self) -> None:
        openai.api_key = "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"

    def Generate(self, prompt):
        return openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", 
                    messages=[{"role": "user", "content": prompt}]
                )
    
    def Parse(self, response):
        return response["choices"][0]["message"]["content"]
    
    def ParsedMessage(self, prompt):
        return self.Parse(self.Generate(prompt))
    
    def SetupMessageQueue(self, q):
        self.q = q

    def SetupState(self, state):
        self.state = state

    def ShouldStop(self):
        return self.state.Stopped
    
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
        audio_q.put(audio)
    except Exception:
        logging.log('Unknown error with audio capturing')
        

"""
transcribe the audio captured and stored in the queue and have the result placed in the text queue
problem: need to figure out how to exit app asap (text is queued so this isn't processed immediately)
"""
def audio_transcription(recognizer : sr.Recognizer, audio_q : queue, text_q : queue):
    if not isinstance(recognizer, sr.Recognizer):
        raise Exception(f'{recognizer} is not type of {sr.Recognizer}')
    if not isinstance(audio_q, queue.Queue):
        raise Exception(f'{audio_q} is not type of {queue.Queue}')
    if not isinstance(text_q, queue.Queue):
        raise Exception(f'{text_q} is not type of {queue.Queue}')
    
    if audio_q.empty():
        return
    
    transcript = ''
    try:
        print(f'Transcribing... {audio_q.qsize()} remaining...')
        audio = audio_q.get()
        if not isinstance(audio, sr.AudioData):
            raise Exception(f'{audio} is not type of {sr.AudioData}')
        transcript = recognizer.recognize_google(audio, language="en-US")
        if transcript:
            text_q.put(transcript)
        print(f"Transcript: {transcript}")
    except sr.UnknownValueError:
        logging.error("Google Web Speech API could not understand the audio")
    except sr.RequestError as e:
        logging.error("Could not request results from Google Web Speech API; {0}".format(e))
    except KeyboardInterrupt:
        logging.info("Stopping the speech recognition.")

def consume_text(text_q : queue.Queue):
    if not isinstance(text_q, queue.Queue):
        raise Exception(f'{text_q} is not type of {queue.Queue}')

    texts = []
    while not text_q.empty():
        texts.append(text_q.get())
    
    prompt = " ".join(texts)
    if not prompt:
        return
    
    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", 
                messages=[{"role": "user", "content": prompt}])
    message = response["choices"][0]["message"]["content"]
    print(message)

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
    openai.api_key = "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"
    while not stop_event.is_set():
        consume_text(text_q)
        time.sleep(5)

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