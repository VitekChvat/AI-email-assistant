# Imports
from app.ai.ollamaQwen3 import QwenProvider
from app.core.configLoader import Config
import logging

# Setting up logger for this module
logger = logging.getLogger(f"app.{__name__}")

# EmailAnalyzer service class
class EmailAnalyzer:

    def __init__(self):
        self.ai = QwenProvider()

    # Method to generate email reply
    def generate_reply(self, email_text: str) -> dict:
        try:
            reply = self.ai.reply_to_email(email_text)
            aiModel = Config.load()["aiModel"]

            logger.info("Email reply successfully generated")
        
            return {
                "original_email": email_text,
                "reply": reply,
                "model": aiModel
            }
        
        # Catching and logging any exceptions that occur during reply generation
        except Exception as e:
            logger.exception(f"Error in EmailAnalyzer.generate_reply: {e}")
            raise
