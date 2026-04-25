# Imports
import requests
import logging
from .base import BaseAIProvider
from app.core.configLoader import Config

# Setting up logger for this module
logger = logging.getLogger(f"app.{__name__}")

# QwenProvider class for interacting with Ollama models
class QwenProvider(BaseAIProvider):

    # Inicialization
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = Config.load().get("aiModel")

        if not self.model:
            logger.error("Missing 'aiModel' in configuration", exc_info=True)
            raise ValueError("Missing 'aiModel' in configuration")

    # Method to reply to email using the AI model
    def reply_to_email(self, email_text: str) -> str:
        prompt = f"""
        You are a professional email assistant that helps users write replies to emails.

        Your goal is to generate a natural, context-aware and accurate email response.

        ---

        CORE RULES:
        - Always reply in the SAME language as the incoming email
        - Be polite, professional, and human-like
        - Keep responses concise and relevant
        - Do NOT invent facts, data, or context not present in the email
        - If critical information is missing, ask a short clarifying question instead of guessing
        - Never mention that you are an AI
        - Never explain your reasoning
        - Do not add a subject line
        - Output only the email body

        ---

        BEHAVIOR RULES:
        - If the email is formal → respond formally
        - If the email is informal → respond naturally but still respectful
        - If the email is a request → confirm understanding + respond to request
        - If the email is unclear → ask a short clarification question
        - If the email contains multiple topics → address them separately but briefly

        ---

        STYLE:
        - Natural business communication
        - Simple, clear sentences
        - No unnecessary filler text
        - No bullet points unless explicitly needed

        ---

        EMAIL:
        {email_text}

        REPLY:
        """

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "top_p": 0.9,
            }
        }

        # Making POST request to Ollama API and handling response
        try:
            response = requests.post(self.url, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()

            reply = data.get("response")
            if not reply:
                logger.error("Missing 'response' field in AI response", exc_info=True)
                raise ValueError("Missing 'response' field in AI response")
            
            return reply.strip()
        
        except requests.HTTPError:
            logger.error("HTTP error occurred while calling Ollama API", exc_info=True)
            return "Sorry, I couldn't generate a reply due to an HTTP error."
        except requests.RequestException:
            logger.error("Network error occurred while calling Ollama API", exc_info=True)
            return "Sorry, I couldn't generate a reply due to a network error."
        except Exception as e:
            logger.exception(f"Unexpected error in QwenProvider: {e}")
            return "Sorry, I couldn't generate a reply due to an unexpected error."
