import pytest
import json
import os
from unittest.mock import patch, MagicMock
from src.models import InputPayload
from src.detector import Detector
from src.fetcher import Fetcher

# Load test data
with open('tests/test_data.json', 'r') as f:
    TEST_DATA = json.load(f)

def test_payload_parsing():
    """Test standard payload parsing from the test data."""
    payload = InputPayload(**TEST_DATA)
    assert payload.entity_id == "0x1234567890abcdef1234567890abcdef12345678"
    assert len(payload.transactions) > 0

def test_detector_basic():
    """Test that detector runs without error on test data."""
    payload = InputPayload(**TEST_DATA)
    detector = Detector()
    findings = detector.analyze(payload)
    # We expect findings or empty list, but no exception
    assert isinstance(findings, list)

def test_fetcher_requires_api_key():
    """Test that Fetcher raises ValueError if no API key is present."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="POLYGONSCAN_API_KEY"):
            Fetcher()

def test_fetcher_initialization():
    """Test that Fetcher initializes with an API key."""
    with patch.dict(os.environ, {"POLYGONSCAN_API_KEY": "fake_key"}, clear=True):
        fetcher = Fetcher()
        assert fetcher.api_key == "fake_key"

def test_fetcher_explicit_key():
    """Test that Fetcher prefers explicit API key."""
    fetcher = Fetcher(api_key="explicit_key")
    assert fetcher.api_key == "explicit_key"
