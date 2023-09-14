import speech_recognition as sr
import logging
import queue

"""
transcribe the audio captured and stored in the queue and have the result placed in the text queue
problem: need to figure out how to exit app asap (text is queued so this isn't processed immediately)
"""
def audio_transcription(recognizer : sr.Recognizer, audio : sr.AudioData):
    if not isinstance(recognizer, sr.Recognizer):
        raise Exception(f'{recognizer} is not type of {sr.Recognizer}')
    
    try:
        return recognizer.recognize_google(audio, language="en-US")
    except sr.UnknownValueError:
        logging.error("Google Web Speech API could not understand the audio")
    except sr.RequestError as e:
        logging.error("Could not request results from Google Web Speech API; {0}".format(e))
    except KeyboardInterrupt:
        logging.info("Stopping the speech recognition.")