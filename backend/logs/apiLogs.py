# Imports
from fastapi import APIRouter, HTTPException
from pathlib import Path
from app.models.modelsLogs import LogDataInput, LogResponse
import json
import logging

# Setting up logger for this module
logger = logging.getLogger(f"app.{__name__}")

# Creating API router
router = APIRouter(prefix="/log", tags=["Log"])

# Defining POST endpoint for Logs
@router.post("/js_error", response_model=LogResponse)
def capture_js_error(payload: LogDataInput):
    try:
        logPath = Path("logs/app.log")
        
        if not logPath.parent.exists():
            raise RuntimeError("Log directory does not exist")

        with open(logPath, "a", encoding="utf-8") as f:
            f.write(f"JavaScript Error: {json.dumps(payload.model_dump())}\n")
        
        logger.info("JS error logged successfully")

        return {"message": "Error logged successfully"}
    
    # Error handling for file writing issues and unexpected exceptions
    except PermissionError as e:
        logger.error(f"Permission error writing log: {e}")
        raise HTTPException(status_code=500, detail="Cannot write log file")
    except Exception:
        logger.exception("Unexpected error while logging JS error")
        raise HTTPException(status_code=500, detail="Internal server error")
