from abc import ABC, abstractmethod

class LLM_Adaptor(ABC):
    @abstractmethod
    def Setup(self) -> None:
        """
        Consider having the logic to set up the specific LLM model for use
        """
        pass

    @abstractmethod
    def ConsumePrompt(self, prompt : str) -> None:
        """
        Feeding the text prompt to the specific LLM for a response
        """
        pass

    @abstractmethod
    def ParseResponse(self) -> str:
        """
        Retrieve the parsed response
        """
        pass
