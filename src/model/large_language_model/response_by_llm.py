from threading import Event
from LLM_adaptor import LLM
from .response import ResponseGenerator
from logging import info

class ResponseFromOpenAI(ResponseGenerator):

    def __init__(self, llm_model : LLM):
        """
        Cosntructs an object of ResponseGenerator that sends a prompt for response from the provided large language model (LLM)

        Args:
            llm_model (LLM) : an instance of LLM model
        """
        if not isinstance(llm_model, LLM):
            raise Exception(f'{llm_model} is not of type {LLM}')
        
        self.llm_model = llm_model

    def QueryOnce(self, prompt: str) -> str:
        """
        Gets a response from self.llm_model based on the given prompt
        
        Args:
            prompt (str) : query to self.llm_model

        Returns:
            response from self.llm_model
        """
        if not prompt:
            return None
        
        if not isinstance(prompt, str):
            raise Exception(f'{prompt} is not of type {str}')
        
        info(f'Prompt: {prompt}')
        self.llm_model.ConsumePrompt(prompt)
        return self.llm_model.ParseResponse()
    
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
        
        info('exited querying loop')