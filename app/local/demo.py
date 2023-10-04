from speech_recognition import Recognizer, Microphone
from threading import Event
from queue import Queue
from time import sleep

from src.model.speech.audio_capture.capture_by_speech_recognition import AudioCaptureBySpeechRecognition
from src.model.speech.audio_transcription.transcription_by_speech_recognition import AudioTranscriptionBySpeechRecognition
from src.model.large_language_model.response_by_llm import ResponseByLLM
from src.model.large_language_model.LLM_OpenAI import LLM_OpenAI
from src.model.speech.text_to_speech.speech_generator_by_pyttsx3 import SpeechGeneratorByPyttsx3

from src.services.speech.capture_service import CreateAudioCaptureService
from src.services.speech.transcription_service import CreateAudioTranscriptionService
from src.services.large_language_model.response_service import CreateResponseService
from src.services.speech.speech_generation_service import CreateSpeechGenerationService

"""
A demo on how the three services: speech capture, transcription, response-by-llm and text-to-speech
functions work together.
1. capture audio speech
2. transcribe speech to text
3. feed text as prompt to retrieve response from a language-model
4. generate audio speech from the response of the language-model
"""
def multithreaded_demo() -> None:

    # object responsible for audio capture and transcription
    recognizer = Recognizer()

    # event that stops all worker threads
    stop_event = Event()

    # store captured audio data
    audio_q = Queue(100)
    # store transcribed texts as queries to language-model
    query_q = Queue(1000)
    # store the response from language model
    response_q = Queue(1000)

    # setup for continuous audio capture
    capture = AudioCaptureBySpeechRecognition(recognizer, Microphone())
    capture_thread = CreateAudioCaptureService(capture, audio_q, stop_event)
    capture_thread.start()

    # setup for continuous speech transcription
    transcription = AudioTranscriptionBySpeechRecognition(recognizer)
    transcription_thread = CreateAudioTranscriptionService(transcription, audio_q, query_q, response_q, stop_event)
    transcription_thread.start()

    # setup for continuous process with a language-model that provides responses to the queries
    import os
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    openai_llm = LLM_OpenAI(openai_api_key)
    response = ResponseByLLM(openai_llm)
    response_thread = CreateResponseService(response, query_q, response_q, stop_event)
    response_thread.start()

    # setup for speech generation
    import pyttsx3
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    pttsx3_generator = SpeechGeneratorByPyttsx3(engine)
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