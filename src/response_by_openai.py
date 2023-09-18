from threading import Event
from openai import ChatCompletion
from response import ResponseGenerator
from logging import info

class ResponseFromOpenAI(ResponseGenerator):

    def __init__(self, key : str):
        """
        Cosntructs an object of ResponseGenerator that sends a prompt for response from OpenAI's large language model

        Args:
            key (str) : required for using OpenAI's API
        """
        if not isinstance(key, str):
            raise Exception(f'{key} is not of type {str}')
        
        import openai
        openai.api_key = key

    def QueryOnce(self, prompt: str) -> str:
        """
        Gets a response from OpenAI based on the given prompt
        
        Args:
            prompt (str) : query to OpenAI's LLM

        Returns:
            response from OpenAI's LLM
        """
        if not prompt:
            return None
        info(f'Prompt: {prompt}')
        response = ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[{"role": "user", "content": prompt}])
        return response["choices"][0]["message"]["content"]
    
    def Query(self, get_prompt : callable, process_response : callable, stop_event : Event) -> None:
        """
        Continuously consumes prompts in a loop and requests responses from OpenAI's large language model.
        The loop ends when the stop event is set.

        Args:
            get_prompt (function) : provides the prompts
            process_response (method) : consumes the response obtained

        Returns:
            None
        """
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