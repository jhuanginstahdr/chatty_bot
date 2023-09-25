from threading import Thread, Event
from queue import Queue, Empty, Full
from logging import info, debug, error
from src.model.large_language_model.response import ResponseGenerator

def CreateResponseService(
    response : ResponseGenerator, 
    query_q : Queue, 
    response_q : Queue,
    stop_event : Event) -> Thread:

    if not isinstance(response, ResponseGenerator):
        raise Exception(f'{response} is not of type {ResponseGenerator}')

    # retrieve all texts from text_q and join them to form a prompt
    def create_prompt_from_text_queue() -> str:
        if query_q.empty():
            return None
        debug(f'constructing prompt from text_q')
        list = []
        while True:
            try:
                list.append(query_q.get(timeout=0.5))
            except Empty:
                break
        if not list:
            return None
        return " ".join(list)

    # store the response from llm in text_q
    def put_in_response_queue(text):
        if not text:
            return
        info(f'response:\n{text}')
        try:
            response_q.put(text)
        except Full:
            error(f'cannot place item in {response_q}')

    # thread for feeding prompt and getting responses via OpenAI's API
    return Thread(target=lambda: response.Query(stop_event, 
                                                get_prompt = create_prompt_from_text_queue, 
                                                process_response = put_in_response_queue))