# Imports
from pydantic import BaseModel, ConfigDict, Field

# Structure of Log data sent from frontend
class LogDataInput(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
    url: str
    userAgent: str
    timestamp: str

    model_config = ConfigDict(extra="allow")

class LogResponse(BaseModel):
    message: str
