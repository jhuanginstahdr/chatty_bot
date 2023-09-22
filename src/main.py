from speech_recognition import Recognizer, Microphone
from threading import Event
from queue import Queue
from time import sleep
from logging import info

from model.speech.audio_capture.capture_by_speech_recognition import AudioCaptureBySpeechRecognition
from model.speech.audio_transcription.transcription_by_speech_recognition import AudioTranscriptionBySpeechRecognition
from model.large_language_model.response_by_llm import ResponseByLLM
from model.large_language_model.LLM_OpenAI import LLM_OpenAI
from model.speech.text_to_speech.speech_generator_by_pyttsx3 import SpeechGeneratorByPyttsx3

from services.speech.capture_service import CreateAudioCaptureService
from services.speech.transcription_service import CreateAudioTranscriptionService
from services.large_language_model.response_service import CreateResponseService
from services.speech.speech_generation_service import CreateSpeechGenerationService

"""
A demo on how the three services: capture, transcription and response work together
to feed speech (in English) as prompt to a Large-Language-Model like OpenAI's GPT
"""
def demo_direct_speech_to_text_to_llm() -> None:

    recognizer = Recognizer()
    stop_event = Event()

    audio_q = Queue(100)
    query_q = Queue(1000)
    response_q = Queue(1000)

    capture = AudioCaptureBySpeechRecognition(recognizer, Microphone())
    capture_thread = CreateAudioCaptureService(capture, audio_q, stop_event)
    capture_thread.start()

    transcription = AudioTranscriptionBySpeechRecognition(recognizer)
    transcription_thread = CreateAudioTranscriptionService(transcription, audio_q, query_q, stop_event)
    transcription_thread.start()

    import os
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    openai_llm = LLM_OpenAI(openai_api_key)
    response = ResponseByLLM(openai_llm)
    response_thread = CreateResponseService(response, query_q, response_q, stop_event)
    response_thread.start()

    pttsx3_generator = SpeechGeneratorByPyttsx3()
    speech_generator_thread = CreateSpeechGenerationService(pttsx3_generator, response_q, stop_event)
    speech_generator_thread.start()

    try:
        while True:
            sleep(10)
            pass
    except KeyboardInterrupt:
        stop_event.set()

    capture_thread.join()
    transcription_thread.join()
    response_thread.join()
    speech_generator_thread.join()

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    demo_direct_speech_to_text_to_llm()
    info('App has exited')