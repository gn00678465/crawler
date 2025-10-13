"""Integration tests for CLI scrape command."""

from datetime import datetime
from unittest.mock import patch
import pytest
from typer.testing import CliRunner
from src.cli.main import app
from src.models.scrape import ScrapeResponse, ScrapeMetadata, OutputFormat


runner = CliRunner()


@pytest.fixture
def mock_successful_scrape(mocker):
    """Mock successful scrape operation."""
    metadata = ScrapeMetadata(
        source_url="https://example.com", scraped_at=datetime.now(), title="Example Domain"
    )
    response = ScrapeResponse(
        content="# Example Domain\n\nThis is a test.",
        format=OutputFormat.MARKDOWN,
        metadata=metadata,
        success=True,
    )

    mock_service = mocker.Mock()
    mock_service.scrape.return_value = response

    mocker.patch("src.cli.scrape.FirecrawlService", return_value=mock_service)
    mocker.patch.dict(
        "os.environ", {"FIRECRAWL_API_URL": "http://localhost:3002", "FIRECRAWL_API_KEY": ""}
    )

    return response


def test_scrape_command_to_file(tmp_path, mock_successful_scrape):
    """Test scrape command saves to file."""
    output_file = tmp_path / "test.md"

    result = runner.invoke(
        app, ["scrape", "--url", "https://example.com", "--output", str(output_file)]
    )

    assert result.exit_code == 0
    assert output_file.exists()
    assert "Example Domain" in output_file.read_text()


def test_scrape_command_to_stdout(mock_successful_scrape):
    """Test scrape command outputs to console."""
    result = runner.invoke(app, ["scrape", "--url", "https://example.com"])

    assert result.exit_code == 0
    assert "# Example Domain" in result.stdout


def test_scrape_command_invalid_url():
    """Test scrape command with invalid URL."""
    result = runner.invoke(app, ["scrape", "--url", "not-a-url"])

    assert result.exit_code == 1
    assert "Error" in result.stderr or "Error" in result.stdout


def test_scrape_command_html_format(tmp_path, mocker):
    """Test scrape command with HTML format."""
    output_file = tmp_path / "test.html"

    metadata = ScrapeMetadata(source_url="https://example.com", scraped_at=datetime.now())
    response = ScrapeResponse(
        content="<h1>Test</h1>", format=OutputFormat.HTML, metadata=metadata, success=True
    )

    mock_service = mocker.Mock()
    mock_service.scrape.return_value = response
    mocker.patch("src.cli.scrape.FirecrawlService", return_value=mock_service)
    mocker.patch.dict("os.environ", {"FIRECRAWL_API_URL": "http://localhost:3002"})

    result = runner.invoke(
        app, ["scrape", "--url", "https://example.com", "--html", "--output", str(output_file)]
    )

    assert result.exit_code == 0
    assert output_file.exists()
    assert "<h1>Test</h1>" in output_file.read_text()
