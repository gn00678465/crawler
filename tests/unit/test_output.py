"""Unit tests for output service."""
from datetime import datetime
from pathlib import Path
import pytest
from src.services.output import OutputService
from src.models.scrape import ScrapeResponse, ScrapeMetadata, OutputFormat
from src.lib.exceptions import OutputError


@pytest.fixture
def sample_response():
    """Create sample ScrapeResponse for testing."""
    metadata = ScrapeMetadata(
        source_url="https://example.com",
        scraped_at=datetime.now(),
        title="Test Page"
    )
    return ScrapeResponse(
        content="# Test Content\n\nThis is a test.",
        format=OutputFormat.MARKDOWN,
        metadata=metadata,
        success=True
    )


def test_output_service_write_to_file(tmp_path, sample_response):
    """Test OutputService.write_to_file creates file."""
    service = OutputService()
    file_path = tmp_path / "test.md"

    service.write_to_file(sample_response, str(file_path))

    assert file_path.exists()
    assert file_path.read_text(encoding='utf-8') == sample_response.content


def test_output_service_creates_directories(tmp_path, sample_response):
    """Test OutputService creates parent directories."""
    service = OutputService()
    file_path = tmp_path / "nested" / "path" / "test.md"

    service.write_to_file(sample_response, str(file_path))

    assert file_path.exists()
    assert file_path.parent.exists()


def test_output_service_print_to_console(capsys, sample_response):
    """Test OutputService.print_to_console outputs to stdout."""
    service = OutputService()

    service.print_to_console(sample_response)

    captured = capsys.readouterr()
    assert sample_response.content in captured.out
