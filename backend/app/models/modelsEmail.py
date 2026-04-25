# Imports
from pydantic import BaseModel

# Structure of user input
class EmailRequest(BaseModel):
    email_text: str

# Structure of AI response
class EmailResponse(BaseModel):
    original_email: str
    reply: str
    model: str
