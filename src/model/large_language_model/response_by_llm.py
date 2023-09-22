from threading import Event
from .LLM_adaptor import LLM_Adaptor
from .response import ResponseGenerator
from logging import info

class ResponseByLLM(ResponseGenerator):

    def __init__(self, llm_adaptor : LLM_Adaptor):
        """
        Cosntructs an object of ResponseGenerator that sends a prompt for response from the provided large language model (LLM)

        Args:
            llm_adaptor (LLM_Adaptor) : an instance of LLM_Adaptor that contains a specific large language model (e.g. openai, llama etc)
        """
        if not isinstance(llm_adaptor, LLM_Adaptor):
            raise Exception(f'{llm_adaptor} is not of type {LLM_Adaptor}')
        
        self.llm_adaptor = llm_adaptor

    def QueryOnce(self, prompt: str) -> str:
        """
        Gets a response from self.llm_adaptor based on the given prompt
        
        Args:
            prompt (str) : query to be consumed by self.llm_adaptor

        Returns:
            response from self.llm_adaptor
        """
        if not prompt:
            return None
        
        if not isinstance(prompt, str):
            raise Exception(f'{prompt} is not of type {str}')
        
        info(f'Prompt: {prompt}')
        #except exceptions to be handled within ConsumePrompt and ParseResponse
        self.llm_adaptor.ConsumePrompt(prompt)
        return self.llm_adaptor.ParseResponse()
    
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