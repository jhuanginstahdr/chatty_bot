from threading import Thread, Event
from queue import Queue, Empty
from logging import info, debug
from model.large_language_model.response import ResponseGenerator

def CreateResponseService(
    response : ResponseGenerator, 
    text_q : Queue, 
    stop_event : Event) -> Thread:

    if not isinstance(response, ResponseGenerator):
        raise Exception(f'{response} is not of type {ResponseGenerator}')

    # retrieve all texts from text_q and join them to form a prompt
    def create_prompt_from_text_queue() -> str:
        if text_q.empty():
            return None
        debug(f'constructing prompt from text_q')
        list = []
        while True:
            try:
                list.append(text_q.get(timeout=0.5))
            except Empty:
                break
        if not list:
            return None
        return " ".join(list)
    
    # print out the response
    def print_response(text : str):
        if text:
            info(f'response: {text}')

    # thread for feeding prompt and getting responses via OpenAI's API
    return Thread(target=lambda: response.Query(create_prompt_from_text_queue, print_response, stop_event))