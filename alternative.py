import speech_recognition as sr
import threading
import time
import logging
import queue

exit_phrase = 'exit app'

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

def continuous_speech_capture(recognizer : sr.Recognizer, audio_q : queue):
    microphone = sr.Microphone()
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            audio_capture(recognizer, source, audio_q)
            time.sleep(0.3)

def continuous_speech_processing(recognizer : sr.Recognizer, audio_q : queue, text_q : queue):
    while True:
        audio_transcription(recognizer, audio_q, text_q)
        time.sleep(0.5)

def capture_exit_app_phrase(transcript) -> bool:
    return transcript == exit_phrase

def transcribe_continuous_speech():
    recognizer = sr.Recognizer()
    audio_q = queue.Queue()
    text_q = queue.Queue()

    # Create and start the recognition thread
    capture_thread = threading.Thread(target=lambda: continuous_speech_capture(recognizer, audio_q))
    capture_thread.daemon = True  # The thread will exit when the main program exits
    process_thread = threading.Thread(target=lambda: continuous_speech_processing(recognizer, audio_q, text_q))
    process_thread.daemon = True  # The thread will exit when the main program exits

    capture_thread.start()
    process_thread.start()

    capture_thread.join()
    process_thread.join()

if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG)
    transcribe_continuous_speech()
    print('App exiting phrase captured')