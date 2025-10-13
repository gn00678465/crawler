"""Unit tests for exception hierarchy."""

import pytest
from src.lib.exceptions import (
    CrawlerError,
    ConfigurationError,
    ValidationError,
    FirecrawlApiError,
    RateLimitError,
    AuthenticationError,
    ServerError,
    OutputError,
)


def test_crawler_error_initialization():
    """Test CrawlerError with custom message and code."""
    error = CrawlerError("Test error", code=42, details={"key": "value"})
    assert error.message == "Test error"
    assert error.code == 42
    assert error.details == {"key": "value"}
    assert str(error) == "Test error"


def test_crawler_error_defaults():
    """Test CrawlerError default values."""
    error = CrawlerError("Test")
    assert error.message == "Test"
    assert error.code == 1
    assert error.details == {}


def test_configuration_error():
    """Test ConfigurationError has code 2."""
    error = ConfigurationError("Missing config")
    assert error.code == 2
    assert "Missing config" in str(error)
    assert error.message == "Missing config"


def test_configuration_error_with_details():
    """Test ConfigurationError with details."""
    error = ConfigurationError("Missing API URL", details={"var": "FIRECRAWL_API_URL"})
    assert error.code == 2
    assert error.details == {"var": "FIRECRAWL_API_URL"}


def test_validation_error():
    """Test ValidationError has code 1."""
    error = ValidationError("Invalid URL")
    assert error.code == 1
    assert "Invalid URL" in error.message


def test_rate_limit_error():
    """Test RateLimitError has code 3."""
    error = RateLimitError()
    assert error.code == 3
    assert "Rate limit" in error.message or "rate limit" in error.message


def test_rate_limit_error_custom_message():
    """Test RateLimitError with custom message."""
    error = RateLimitError("Custom rate limit message")
    assert error.code == 3
    assert error.message == "Custom rate limit message"


def test_authentication_error():
    """Test AuthenticationError has code 1."""
    error = AuthenticationError("Invalid API key")
    assert error.code == 1
    assert "Invalid API key" in error.message


def test_server_error():
    """Test ServerError has code 1."""
    error = ServerError("500 Internal Server Error")
    assert error.code == 1
    assert "500" in error.message


def test_output_error():
    """Test OutputError has code 1."""
    error = OutputError("Cannot write file")
    assert error.code == 1
    assert "Cannot write file" in error.message


def test_firecrawl_api_error():
    """Test FirecrawlApiError base class."""
    error = FirecrawlApiError("API call failed")
    assert error.code == 1
    assert error.message == "API call failed"


def test_exception_inheritance():
    """Test exception inheritance chain."""
    # All custom exceptions inherit from CrawlerError
    assert issubclass(ConfigurationError, CrawlerError)
    assert issubclass(ValidationError, CrawlerError)
    assert issubclass(FirecrawlApiError, CrawlerError)
    assert issubclass(OutputError, CrawlerError)

    # FirecrawlApiError subclasses
    assert issubclass(RateLimitError, FirecrawlApiError)
    assert issubclass(AuthenticationError, FirecrawlApiError)
    assert issubclass(ServerError, FirecrawlApiError)

    # All inherit from Exception
    assert issubclass(CrawlerError, Exception)


def test_exception_can_be_raised():
    """Test that exceptions can be raised and caught."""
    with pytest.raises(CrawlerError):
        raise CrawlerError("Test")

    with pytest.raises(ConfigurationError):
        raise ConfigurationError("Test config error")

    with pytest.raises(RateLimitError):
        raise RateLimitError()

    # Can catch specific exception via parent
    with pytest.raises(FirecrawlApiError):
        raise RateLimitError()

    # Can catch any crawler exception via base class
    with pytest.raises(CrawlerError):
        raise ValidationError("Invalid")
