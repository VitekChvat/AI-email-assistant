# Imports
import uvicorn
import logging

# Setting up logger for this module
logger = logging.getLogger(f"app.{__name__}")

# Configurating uvicorn server
if __name__ == "__main__":
    try:
        uvicorn.run(
            "app.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
        )
    
    # Catching and logging any exceptions that occur during server startup
    except OSError as e:
        logger.error(f"OS error while starting server: {e}")
        raise RuntimeError("Server failed due to OS error") from e

    except Exception as e:
        logger.exception("Unexpected error while starting server")
        raise RuntimeError("Server startup failed") from e
    