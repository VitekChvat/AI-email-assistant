# Imports
from unittest.mock import patch, MagicMock
import pytest
from app.ai.ollamaQwen3 import QwenProvider
import requests


# Test of missing ai model
def test_missing_model_in_config():
    with patch("app.ai.ollamaQwen3.Config.load", return_value={}):
        with pytest.raises(ValueError):
            QwenProvider()

# Test of succes response
def test_reply_success():
    fake_response = MagicMock()
    fake_response.json.return_value = {"response": "Hello back!"}
    fake_response.raise_for_status.return_value = None

    with patch("app.ai.ollamaQwen3.Config.load", return_value={"aiModel": "test-model"}):
        with patch("app.ai.ollamaQwen3.requests.post", return_value=fake_response):

            provider = QwenProvider()
            result = provider.reply_to_email("Hello")

            assert result == "Hello back!"

# Test of missing "response"
def test_missing_response_field():
    fake_response = MagicMock()
    fake_response.json.return_value = {}
    fake_response.raise_for_status.return_value = None

    with patch("app.ai.ollamaQwen3.Config.load", return_value={"aiModel": "test-model"}):
        with patch("app.ai.ollamaQwen3.requests.post", return_value=fake_response):

            provider = QwenProvider()

            result = provider.reply_to_email("Hello")

            assert "unexpected error" in result.lower()

# Testing HTTP error handling
def test_http_error():
    fake_response = MagicMock()
    fake_response.raise_for_status.side_effect = requests.HTTPError()

    with patch("app.ai.ollamaQwen3.Config.load", return_value={"aiModel": "test-model"}):
        with patch("app.ai.ollamaQwen3.requests.post", return_value=fake_response):

            provider = QwenProvider()
            result = provider.reply_to_email("Hello")

            assert "http error" in result.lower()

# Testing network error handling
def test_network_error():
    with patch("app.ai.ollamaQwen3.Config.load", return_value={"aiModel": "test-model"}):
        with patch("app.ai.ollamaQwen3.requests.post", side_effect=requests.RequestException()):

            provider = QwenProvider()
            result = provider.reply_to_email("Hello")

            assert "network error" in result.lower()
