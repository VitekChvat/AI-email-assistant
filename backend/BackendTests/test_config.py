# Imports
from app.core.configLoader import Config
import pytest

# Testing the Config class for loading configuration files
def test_load_valid_config(tmp_path):
    file = tmp_path / "config.json"
    file.write_text('{"TestKey": "TestValue"}')

    result = Config.load(file)

    assert result["TestKey"] == "TestValue"

# Testing error handling for missing file and invalid JSON
def test_load_missing_file():
    with pytest.raises(FileNotFoundError):
        Config.load("non_existent_config.json")

# Testing error handling for invalid JSON format
def test_load_invalid_json(tmp_path):
    file = tmp_path / "config.json"
    file.write_text("{Invalid JSON}")

    with pytest.raises(ValueError):
        Config.load(file)
