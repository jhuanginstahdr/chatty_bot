import speech_recognition as sr
import threading
import time
import logging

exit_phrase = 'exit app'

def recognition(recognizer, source) -> str:
    if not isinstance(recognizer, sr.Recognizer):
        raise Exception(f'incorrect type of {recognizer}')
    if not isinstance(source, sr.AudioSource):
        raise Exception(f'incorrect type of {source}')
    
    try:
        audio = recognizer.listen(source)
        transcript = recognizer.recognize_google(audio, language="en-US")
        logging.info(f"Transcript: {transcript}")
    except sr.UnknownValueError:
        logging.error("Google Web Speech API could not understand the audio")
    except sr.RequestError as e:
        logging.error("Could not request results from Google Web Speech API; {0}".format(e))
    except KeyboardInterrupt:
        logging.info("Stopping the speech recognition.")
        
    return transcript

def continuous_speech_recognition(recognizer, microphone):
    #stopping the recognition by capturing the key phrase
    def capture_exit_app_phrase(transcript):
        return transcript == exit_phrase
    
    transcript = ''
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        while not capture_exit_app_phrase(transcript):
            print('Listening for speech...')
            time.sleep(1)
            transcript = recognition(recognizer, source)

def transcribe_continuous_speech():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # Create and start the recognition thread
    thread = threading.Thread(target=continuous_speech_recognition(recognizer, microphone))
    thread.daemon = True  # The thread will exit when the main program exits
    return thread

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    recognition_thread = transcribe_continuous_speech()
    recognition_thread.start()
    recognition_thread.join()
    print('App exiting phrase captured')