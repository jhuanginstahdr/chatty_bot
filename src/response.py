from abc import ABC, abstractmethod

class ResponseGenerator(ABC):
    @abstractmethod
    def GetResponse(prompt : str) -> str :
        pass

import openai
import threading
import time

class ResponseFromOpenAI(ResponseGenerator):

    """
    Cosntructor of ResponseFromOpenAI

    Args:
        api_key (str) : required for using OpenAI's API
    """
    def __init__(self, api_key : str):
        if not isinstance(api_key, str):
            raise Exception(f'{api_key} is not of type {str}')
        
        openai.api_key = api_key

    """
    Get response from OpenAI based on the given prompt
    
    Args:
        prompt (str) : query to OpenAI's LLM

    Returns:
        response from OpenAI's LLM
    """
    def GetResponse(self, prompt: str) -> str:
        if not prompt:
            return None
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[{"role": "user", "content": prompt}])
        return response["choices"][0]["message"]["content"]
    
    """
    Continuously consume prompts and provide response from OpenAI's LLM

    Args:
        get_prompt (function) : fetches the prompt
        process_response (method) : consume the response obtained

    Returns:
        None
    """
    def ContinousResponse(self, get_prompt : callable, process_response : callable, stop_event : threading.Event, sleep=1) -> None:
        if not callable(get_prompt):
            raise Exception(f'{get_prompt} is not callable')
        if not callable(process_response):
            raise Exception(f'{process_response} is not callable')
        if not isinstance(stop_event, threading.Event):
            raise Exception(f'{stop_event} is not of type {threading.Event}')
        
        while not stop_event.is_set():
            prompt = get_prompt()
            response = self.GetResponse(prompt)
            process_response(response)
            time.sleep(sleep)