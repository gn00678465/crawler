"""Unit tests for configuration management."""

import pytest
from pydantic import ValidationError
from src.config.settings import Settings


def test_settings_from_env(monkeypatch):
    """Test Settings loads from environment."""
    monkeypatch.setenv("FIRECRAWL_API_URL", "http://localhost:3002")
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-key")

    settings = Settings()
    assert settings.firecrawl_api_url == "http://localhost:3002"
    assert settings.firecrawl_api_key == "test-key"


def test_settings_default_api_key(monkeypatch):
    """Test Settings defaults firecrawl_api_key to empty string."""
    monkeypatch.setenv("FIRECRAWL_API_URL", "http://localhost:3002")
    # Don't set FIRECRAWL_API_KEY

    settings = Settings()
    assert settings.firecrawl_api_url == "http://localhost:3002"
    assert settings.firecrawl_api_key == ""


def test_settings_missing_required(monkeypatch):
    """Test Settings raises error if FIRECRAWL_API_URL missing."""
    # Clear all env vars
    monkeypatch.delenv("FIRECRAWL_API_URL", raising=False)
    monkeypatch.delenv("FIRECRAWL_API_KEY", raising=False)

    with pytest.raises(ValidationError):
        Settings()
