"""Unit tests for Firecrawl service."""

from datetime import datetime
from unittest.mock import Mock, patch
import pytest
from src.services.firecrawl import FirecrawlService
from src.models.scrape import ScrapeRequest, ScrapeResponse, OutputFormat
from src.config.settings import Settings
from src.lib.exceptions import RateLimitError, FirecrawlApiError


@pytest.fixture
def mock_settings():
    """Create mock Settings for testing."""
    return Settings(firecrawl_api_url="http://localhost:3002", firecrawl_api_key="test-key")


def test_firecrawl_service_scrape_markdown(mocker, mock_settings):
    """Test FirecrawlService.scrape returns markdown content."""
    # Mock Firecrawl client
    mock_client = mocker.Mock()
    mock_client.scrape.return_value = {
        "markdown": "# Test Content",
        "html": "<h1>Test Content</h1>",
        "metadata": {"title": "Test Page", "sourceURL": "https://example.com"},
    }

    with patch("src.services.firecrawl.Firecrawl", return_value=mock_client):
        service = FirecrawlService(mock_settings)
        request = ScrapeRequest(url="https://example.com", format=OutputFormat.MARKDOWN)
        response = service.scrape(request)

        assert response.success
        assert response.content == "# Test Content"
        assert response.format == OutputFormat.MARKDOWN
        assert response.metadata.title == "Test Page"


def test_firecrawl_service_scrape_html(mocker, mock_settings):
    """Test FirecrawlService.scrape returns HTML content."""
    mock_client = mocker.Mock()
    mock_client.scrape.return_value = {
        "markdown": "# Test",
        "html": "<h1>Test</h1>",
        "metadata": {"sourceURL": "https://example.com"},
    }

    with patch("src.services.firecrawl.Firecrawl", return_value=mock_client):
        service = FirecrawlService(mock_settings)
        request = ScrapeRequest(url="https://example.com", format=OutputFormat.HTML)
        response = service.scrape(request)

        assert response.content == "<h1>Test</h1>"
        assert response.format == OutputFormat.HTML


def test_firecrawl_service_rate_limit(mocker, mock_settings):
    """Test FirecrawlService handles rate limit errors."""
    mock_client = mocker.Mock()
    mock_client.scrape.side_effect = Exception("429: Rate limit exceeded")

    with patch("src.services.firecrawl.Firecrawl", return_value=mock_client):
        service = FirecrawlService(mock_settings)
        request = ScrapeRequest(url="https://example.com")

        with pytest.raises(RateLimitError):
            service.scrape(request)


def test_firecrawl_service_general_error(mocker, mock_settings):
    """Test FirecrawlService handles general API errors."""
    mock_client = mocker.Mock()
    mock_client.scrape.side_effect = Exception("Network error")

    with patch("src.services.firecrawl.Firecrawl", return_value=mock_client):
        service = FirecrawlService(mock_settings)
        request = ScrapeRequest(url="https://example.com")

        with pytest.raises(FirecrawlApiError):
            service.scrape(request)
