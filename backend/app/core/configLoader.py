# Imports
import json
from pathlib import Path
import logging

logger = logging.getLogger(f"app.{__name__}")

# Configuration class to load settings from JSON file
class Config:

    # Static method to load configuration
    @staticmethod
    def load(targetFile=None):
        # The main config.json file will not load if the test is running
        if targetFile is None:
            currentFile = Path(__file__).resolve()
            appFolder = currentFile.parent.parent
            targetFile = appFolder / "applicationSettings" / "config.json"

        # Error handling for missing config file and JSON parsing issues
        if not Path(targetFile).exists():
            logger.error(f"Config file not found: {targetFile}")
            raise FileNotFoundError(f"Config file not found: {targetFile}")

        try: 
            with open(targetFile, "r", encoding="utf-8") as f:
                return json.load(f)
            
        except json.JSONDecodeError as err:
            logger.error(f"Error parsing config file: {err}", exc_info=True)
            raise ValueError(f"Error parsing config file: {err}") from err
        except Exception as err:
            logger.exception("Unexpected error while loading config")
            raise RuntimeError("An unexpected error occurred while loading config") from err
