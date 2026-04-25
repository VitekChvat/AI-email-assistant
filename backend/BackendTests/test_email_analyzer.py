# Imports
import pytest
from unittest.mock import patch
from app.services.emailAnalyzer import EmailAnalyzer

# Testing successful email reply generation
def test_generate_reply_success():
    with patch("app.services.emailAnalyzer.QwenProvider") as MockProvider:
        mock_instance = MockProvider.return_value
        mock_instance.reply_to_email.return_value = "This is a test AI reply."

        with patch("app.core.configLoader.Config.load", return_value={"aiModel": "test-model"}):

            analyzer = EmailAnalyzer()
            result = analyzer.generate_reply("This is a test email.")

            assert result["original_email"] == "This is a test email."
            assert result["reply"] == "This is a test AI reply."
            assert result["model"] == "test-model"

# Testing error handling when AI provider raises an exception
def test_generate_reply_error_propagation():
    with patch("app.services.emailAnalyzer.QwenProvider") as MockProvider:
        mock_instance = MockProvider.return_value
        mock_instance.reply_to_email.side_effect = Exception("AI provider error")

        with patch("app.core.configLoader.Config.load", return_value={"aiModel": "test-model"}):

            analyzer = EmailAnalyzer()

            with pytest.raises(Exception) as exc_info:
                analyzer.generate_reply("This is a test email.")

            assert str(exc_info.value) == "AI provider error"
