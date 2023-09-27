from .LLM_adaptor import LLM_Adaptor
from openai import ChatCompletion
from logging import error

class LLM_OpenAI(LLM_Adaptor):
    def __init__(self, key : str):
        if not isinstance(key, str):
            raise TypeError(f'{key} is not of type {str}')
        self.key = key

    def Setup(self):
        """
        Assign the API Key
        """
        import openai
        openai.api_key = self.key

    #TO DO: template for response to be further refactored
    def ConsumePrompt(self, prompt : str):
        """
        Store the response from OpenAI as reply to the given prompt
        Exception raised by queries to OpenAI should be handled here (e.g. invalid API key)
        """
        try:
            self.reply = ChatCompletion.create(
                model="gpt-3.5-turbo", 
                messages=[{"role": "user", "content": prompt}])
        except Exception as unknown_e:
            self.reply = None
            #possible causes such as invalid API key
            error(f'An unknown error has been raised {unknown_e}')
        
    #TO DO: template or additional logic for interpreting the resposne from LLM to be further refactored
    def ParseResponse(self) -> str:
        """
        Retrieve information from the structured response cached in self.reply
        """
        if self.reply is None:
            return None
        
        result = ''
        try:
            #process the reply and set it back to None (not caching the responses)
            result = self.reply["choices"][0]["message"]["content"]
        except KeyError as key_e:
            error(f'Error parsing the response {key_e}')
        except Exception as unknown_e:
            error(f'Unknown error {unknown_e}')
            
        #clear the cached response
        self.reply = None
        return result