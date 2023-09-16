from threading import Event
from openai import ChatCompletion
from response import ResponseGenerator

class ResponseFromOpenAI(ResponseGenerator):

    """
    Cosntructor

    Args:
        api_key (str) : required for using OpenAI's API
    """
    def __init__(self, key : str):
        if not isinstance(key, str):
            raise Exception(f'{key} is not of type {str}')
        
        import openai
        openai.api_key = key

    """
    Get response from OpenAI based on the given prompt
    
    Args:
        prompt (str) : query to OpenAI's LLM

    Returns:
        response from OpenAI's LLM
    """
    def QueryOnce(self, prompt: str) -> str:
        if not prompt:
            return None
        response = ChatCompletion.create(
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
    def Query(self, get_prompt : callable, process_response : callable, stop_event : Event) -> None:
        if not callable(get_prompt):
            raise Exception(f'{get_prompt} is not callable')
        if not callable(process_response):
            raise Exception(f'{process_response} is not callable')
        if not isinstance(stop_event, Event):
            raise Exception(f'{stop_event} is not of type {Event}')
        
        while not stop_event.is_set():
            prompt = get_prompt()
            response = self.QueryOnce(prompt)
            process_response(response)