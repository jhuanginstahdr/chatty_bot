from LLM_adaptor import LLM
from openai import ChatCompletion
from logging import error

class LLM_OpenAI(LLM):
    def __init__(self, key : str):
        if not isinstance(key, str):
            raise Exception(f'{key} is not of type {str}')
        self.key = key

    def Setup(self):
        import openai
        openai.api_key = self.key

    #TO DO: template for response to be further refactored
    def ConsumePrompt(self, prompt : str):
        try:
            self.reply = ChatCompletion.create(
                model="gpt-3.5-turbo", 
                messages=[{"role": "user", "content": prompt}])
        except Exception as e:
            #possible causes include invalid API key
            error(f'Error has been raised {e}')
        
    #TO DO: template or additional logic for interpreting the resposne from LLM to be further refactored
    def ParseResponse(self) -> str:
        if self.reply is None:
            return None
        #process the reply and set it back to None (not caching the responses)
        res = self.reply["choices"][0]["message"]["content"]
        self.reply = None
        return res