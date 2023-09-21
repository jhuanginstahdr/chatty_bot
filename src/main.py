from speech_recognition import Recognizer, Microphone
from threading import Event
from queue import Queue
from time import sleep
from logging import info

from model.speech.audio_capture.capture_by_speech_recognition import AudioCaptureBySpeechRecognition
from model.speech.audio_transcription.transcription_by_speech_recognition import AudioTranscriptionBySpeechRecognition
from model.large_language_model.response_by_llm import ResponseByLLM
from model.large_language_model.LLM_OpenAI import LLM_OpenAI

from services.speech.capture_service import CreateAudioCaptureService
from services.speech.transcription_service import CreateAudioTranscriptionService
from services.large_language_model.response_service import CreateResponseService

"""
A demo on how the three services: capture, transcription and response work together
to feed speech (in English) as prompt to a Large-Language-Model like OpenAI's GPT
"""
def demo_direct_speech_to_text_to_llm() -> None:

    recognizer = Recognizer()
    stop_event = Event()

    audio_q = Queue(100)
    text_q = Queue(1000)

    capture = AudioCaptureBySpeechRecognition(recognizer, Microphone())
    capture_thread = CreateAudioCaptureService(capture, audio_q, stop_event)
    capture_thread.start()

    transcription = AudioTranscriptionBySpeechRecognition(recognizer)
    transcription_thread = CreateAudioTranscriptionService(transcription, audio_q, text_q, stop_event)
    transcription_thread.start()

    import os
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    openai_llm = LLM_OpenAI(openai_api_key)
    response = ResponseByLLM(openai_llm)
    response_thread = CreateResponseService(response, text_q, stop_event)
    response_thread.start()

    try:
        while True:
            sleep(10)
            pass
    except KeyboardInterrupt:
        stop_event.set()

    capture_thread.join()
    transcription_thread.join()
    response_thread.join()

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    demo_direct_speech_to_text_to_llm()
    info('App has exited')