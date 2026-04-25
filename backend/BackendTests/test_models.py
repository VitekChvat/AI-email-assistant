# Imports
from app.models.modelsEmail import EmailRequest, EmailResponse
from app.models.modelsLogs import LogDataInput, LogResponse
import pytest
from pydantic import ValidationError

# MODELS_EMAIL.PY TESTS
# Test EmailRequest model with valid input
def test_email_request():
    testRequest = EmailRequest(email_text="Hello, how are you?")

    assert testRequest.email_text == "Hello, how are you?"

# Test EmailRequest model with invalid input
def test_email_request_invalid():
    with pytest.raises(ValidationError):
        EmailRequest(email_text=None)

# Test EmailRequest model with missing input
def test_email_request_missing():
    with pytest.raises(ValidationError):
        EmailRequest()


# Test EmailResponse model with valid input
def test_email_response():
    testResponse = EmailResponse(
        original_email="Hello, how are you?",
        reply="I'm good, thank you!",
        model="qwen3:8b"
    )

    assert testResponse.original_email == "Hello, how are you?"
    assert testResponse.reply == "I'm good, thank you!"
    assert testResponse.model == "qwen3:8b"

# Test EmailResponse model with invalid input
def test_email_response_invalid():
    with pytest.raises(ValidationError):
        EmailResponse(
            original_email=None,
            reply=None,
            model=None
        )

# Test EmailResponse model with missing input
def test_email_response_missing():
    with pytest.raises(ValidationError):
        EmailResponse()



# MODELS_LOGS.PY TESTS
# Test LogDataInput model with valid input
def test_log_data_input():
    testLogData = LogDataInput(
        message="Hello",
        extraField="something",
        url="http://example.com",
        userAgent="Chrome",
        timestamp="2024-06-01T12:00:00Z"
    )

    assert testLogData.message == "Hello"
    assert testLogData.url == "http://example.com"
    assert testLogData.userAgent == "Chrome"
    assert testLogData.timestamp == "2024-06-01T12:00:00Z"
    assert testLogData.extraField == "something"

# Test LogDataInput model with invalid input
def test_log_data_input_message_too_short():
    with pytest.raises(ValidationError):
        LogDataInput(
            message="",
            url="http://example.com",
            userAgent="Chrome",
            timestamp="2024-06-01T12:00:00Z"
        )
def test_log_data_input_message_too_long():
    with pytest.raises(ValidationError):
        LogDataInput(
            message="x" * 1010,
            url="http://example.com",
            userAgent="Chrome",
            timestamp="2024-06-01T12:00:00Z"
        )

# Test LogDataInput model with missing input
def test_log_data_input_missing():
    with pytest.raises(ValidationError):
        LogDataInput(
            url="http://example.com",
            userAgent="Chrome",
            timestamp="2024-06-01T12:00:00Z"
        )


# Test LogResponse model with valid input
def test_log_response():
    testLogResponse = LogResponse(message="Log received successfully")

    assert testLogResponse.message == "Log received successfully"

# Test LogResponse model with invalid input
def test_log_response_invalid():
    with pytest.raises(ValidationError):
        LogResponse(message=None)

# Test LogResponse model with missing input
def test_log_response_missing():
    with pytest.raises(ValidationError):
        LogResponse()
