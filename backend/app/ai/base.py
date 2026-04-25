# Imports
from abc import ABC, abstractmethod

# Abstract class for basic sturcture of AI providers
class BaseAIProvider(ABC):
    @abstractmethod
    def reply_to_email(self, email_text: str) -> str:
        pass
