# Logging setup
from logs.loggingSetUp import logging_set_up
logging_set_up()

# Other Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import apiEmail
from logs import apiLogs
from app.api import apiConfig
import logging

# Setting up logger for this module
logger = logging.getLogger(f"app.{__name__}")

# Creating FastAPI app instance with router
app = FastAPI(title="AI Task Assistant")
app.include_router(apiEmail.router)
app.include_router(apiLogs.router)
app.include_router(apiConfig.router)

# CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)
