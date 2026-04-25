# Imports
from fastapi import APIRouter, HTTPException
from app.models.modelsEmail import EmailRequest, EmailResponse
from app.services.emailAnalyzer import EmailAnalyzer
import logging

# Setting up logger for this module
logger = logging.getLogger(f"app.{__name__}")

# Creating API router and analyzer instance
router = APIRouter(prefix="/email", tags=["Email"])
analyzer = EmailAnalyzer()

# Defining POST endpoint for email reply
@router.post("/reply", response_model=EmailResponse)
def reply_to_email(data: EmailRequest):
    try:
        # Generating reply
        response = analyzer.generate_reply(data.email_text)
        logger.info("Response generated successfully")
        return response
    
    # Handling potential exceptions during reply generation
    except ValueError as e:
        logger.error(f"Value error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except TimeoutError as e:
        logger.error(f"Timeout error: {e}")
        raise HTTPException(status_code=504, detail="Generation timeout")
    except Exception:
        logger.exception("Unexpected error occurred while generating reply.")
        raise HTTPException(status_code=500, detail="Internal server error")
