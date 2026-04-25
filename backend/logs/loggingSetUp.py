# Imports
import logging
from pathlib import Path
from concurrent_log_handler import ConcurrentRotatingFileHandler
import logging

# Setting up logger for this module
logger = logging.getLogger(f"app.{__name__}")

def logging_set_up():
    try:
        # Setting up log directories and files
        logDir = Path("logs")
        logDir.mkdir(exist_ok=True)

        appLog = logDir / "app.log"
        serverLog = logDir / "server.log"

        formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )

        # Function for adding rotating file handlers and duplicity check
        def add_file_handler(logger, log_file, level=logging.INFO, propagateState=False):
            try:
                if not any(
                    isinstance(h, ConcurrentRotatingFileHandler) and h.baseFilename == str(log_file)
                    for h in logger.handlers):
                    
                    handler = ConcurrentRotatingFileHandler(str(log_file), encoding="utf-8", maxBytes=1024*1024, backupCount=2)
                    handler.setLevel(level)
                    handler.setFormatter(formatter)
                    logger.addHandler(handler)
                logger.propagate = propagateState
            
            # Handling potential permission errors and other exceptions
            except Exception as e:
                logger.exception(f"Handler setup failed")
                raise RuntimeError(f"Cannot attach log handler") from e

        try:
            # App logger
            appLogger = logging.getLogger("app")
            appLogger.setLevel(logging.DEBUG)

            # Duplicity check and adding file handler
            add_file_handler(appLogger, appLog, level=logging.DEBUG, propagateState=False)

        # Handling potential exceptions during logger setup
        except Exception as e:
            logging.exception("App logger setup failed")
            raise RuntimeError("App logging setup failed") from e

        try:
            # Server logger
            for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
                    serverLogger = logging.getLogger(name)
                    serverLogger.setLevel(logging.INFO)

                    # Duplicity check and adding file handler
                    add_file_handler(serverLogger, serverLog, level=logging.INFO, propagateState=False)

        # Handling potential exceptions during logger setup
        except Exception as e:
            logging.exception("Server logger setup failed")
            raise RuntimeError("Server logging setup failed") from e
    
    # Handling any unexpected exceptions during the entire logging setup process
    except Exception as e:
        logging.exception("Critical logging system failure")
        raise RuntimeError("Logging system completely failed") from e
