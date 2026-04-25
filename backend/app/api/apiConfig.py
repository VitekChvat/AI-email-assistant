# Imports
from fastapi import APIRouter, HTTPException
from pathlib import Path
import json
import logging

# Setting up logger for this module
logger = logging.getLogger(f"app.{__name__}")

# Creating API router
router = APIRouter(prefix="/config", tags=["Config"])

# Finding json with config data
currentDir = Path(__file__).resolve().parent
appDir = currentDir.parent
configJson = appDir / "applicationSettings" / "config.json"

@router.get("/configJson")
def send_config_json():
    try:
        # Checking if config file exists
        if not configJson.exists():
            logger.error(f"Config file not found: {configJson}")
            raise HTTPException(status_code=500, detail="Config file not found")

        # Returning config data to frontend
        with open(configJson, "r", encoding="utf-8") as f:
            data = json.load(f)

        logger.info("Config data loaded successfully")
        return data
    
    # Handling potential errors with detailed logging
    except json.JSONDecodeError as e:
        logger.error(f"Error in JSON format: {e}")
        raise HTTPException(status_code=500, detail="Invalid JSON format")
    except PermissionError as e:
        logger.error(f"Permission error when reading file: {e}")
        raise HTTPException(status_code=500, detail="Permission denied")
    except Exception:
        # tohle je důležité → uloží celý traceback
        logger.exception("Unexpected error occurred while loading config")
        raise HTTPException(status_code=500, detail="Internal server error")
