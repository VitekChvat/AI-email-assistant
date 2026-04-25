# Imports
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

# TEST /EMAIL/REPLY ENDPOINT
# Test valid request
def test_email_reply_success():
    response = client.post(
        "/email/reply",
        json={"email_text": "Test"}
    )

    assert response.status_code == 200
    data = response.json()

    assert "original_email" in data
    assert "reply" in data
    assert "model" in data

# Test invalid request
def test_email_reply_validation_error():
    response = client.post("/email/reply", json={})

    assert response.status_code == 422

# Test value error - 400 (mock)
def test_email_reply_value_error():
    with patch("app.services.emailAnalyzer.EmailAnalyzer.generate_reply", side_effect=ValueError("Test error")):

        response = client.post(
            "/email/reply",
            json={"email_text": "Test"}
        )

        assert response.status_code == 400

# Test timeout error - 504 (mock)
def test_email_reply_timeout_error():
    with patch("app.services.emailAnalyzer.EmailAnalyzer.generate_reply", side_effect=TimeoutError("Test timeout")):

        response = client.post(
            "/email/reply",
            json={"email_text": "Test"}
        )

        assert response.status_code == 504


# TEST /CONFIG/CONFIGJSON ENDPOINT
# Test valid request
def test_config_json_success():
    response = client.get("/config/configJson")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)

# Test invalid request (missing file)
def test_config_json_missing_file():
    with patch("pathlib.Path.exists", return_value=False):

        response = client.get("/config/configJson")

        assert response.status_code == 500


# TEST /LOG/JS_ERROR ENDPOINT
# Test valid request
def test_log_js_error_success():
    response = client.post(
        "/log/js_error",
        json={"message": "Test error", 
              "url": "http://example.com", 
              "userAgent": "pytest",
              "timestamp": "2026-01-01"
    })

    assert response.status_code == 200

# Test invalid request (missing file)
def test_log_js_error():
    with patch("pathlib.Path.exists", return_value=False):

        response = client.post(
            "/log/js_error",
            json={"message": "Test error", 
                  "url": "http://example.com", 
                  "userAgent": "pytest",
                  "timestamp": "2026-01-01"
        })

        assert response.status_code == 500
