"""Unit tests for data models."""
from datetime import datetime
import pytest
from pydantic import ValidationError
from src.models.scrape import (
    OutputFormat,
    ScrapeMetadata,
    ScrapeRequest,
    ScrapeResponse,
)


# T009: OutputFormat enum tests
def test_output_format_enum_values():
    """Test OutputFormat enum has correct values."""
    assert OutputFormat.MARKDOWN.value == "markdown"
    assert OutputFormat.HTML.value == "html"


def test_output_format_membership():
    """Test OutputFormat enum membership."""
    assert "markdown" in [f.value for f in OutputFormat]
    assert "html" in [f.value for f in OutputFormat]


# T011: ScrapeMetadata model tests
def test_scrape_metadata_valid():
    """Test creating valid ScrapeMetadata."""
    metadata = ScrapeMetadata(
        title="Test Page",
        description="Test description",
        keywords="test, page",
        source_url="https://example.com",
        scraped_at=datetime.now()
    )
    assert metadata.title == "Test Page"
    assert metadata.source_url == "https://example.com"
    assert metadata.description == "Test description"
    assert metadata.keywords == "test, page"


def test_scrape_metadata_optional_fields():
    """Test ScrapeMetadata with only required fields."""
    metadata = ScrapeMetadata(
        source_url="https://example.com",
        scraped_at=datetime.now()
    )
    assert metadata.title is None
    assert metadata.description is None
    assert metadata.keywords is None
    assert metadata.source_url == "https://example.com"


# T013: ScrapeRequest model tests
def test_scrape_request_valid():
    """Test creating valid ScrapeRequest."""
    request = ScrapeRequest(
        url="https://example.com",
        format=OutputFormat.MARKDOWN,
        output_path="/path/to/file.md"
    )
    assert str(request.url) == "https://example.com/"
    assert request.format == OutputFormat.MARKDOWN
    assert request.output_path == "/path/to/file.md"


def test_scrape_request_invalid_url():
    """Test ScrapeRequest rejects invalid URL."""
    with pytest.raises(ValidationError):
        ScrapeRequest(url="not-a-url")


def test_scrape_request_defaults():
    """Test ScrapeRequest defaults."""
    request = ScrapeRequest(url="https://example.com")
    assert request.format == OutputFormat.MARKDOWN
    assert request.output_path is None


# T015: ScrapeResponse model tests
def test_scrape_response_success():
    """Test successful ScrapeResponse."""
    metadata = ScrapeMetadata(source_url="https://example.com", scraped_at=datetime.now())
    response = ScrapeResponse(
        content="# Test Content",
        format=OutputFormat.MARKDOWN,
        metadata=metadata,
        success=True
    )
    assert response.success
    assert response.error_message is None
    assert response.content == "# Test Content"


def test_scrape_response_failure():
    """Test failed ScrapeResponse requires error_message."""
    metadata = ScrapeMetadata(source_url="https://example.com", scraped_at=datetime.now())
    with pytest.raises(ValidationError):
        ScrapeResponse(
            content="",
            format=OutputFormat.MARKDOWN,
            metadata=metadata,
            success=False
            # Missing error_message - should fail validation
        )


def test_scrape_response_failure_with_message():
    """Test failed ScrapeResponse with error_message."""
    metadata = ScrapeMetadata(source_url="https://example.com", scraped_at=datetime.now())
    response = ScrapeResponse(
        content="",
        format=OutputFormat.MARKDOWN,
        metadata=metadata,
        success=False,
        error_message="Network error"
    )
    assert not response.success
    assert response.error_message == "Network error"
