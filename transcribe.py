import speech_recognition as sr
import logging
import queue

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