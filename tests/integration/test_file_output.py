"""Integration tests for file output operations."""

from datetime import datetime
from pathlib import Path
import pytest
from src.services.output import OutputService
from src.models.scrape import ScrapeResponse, ScrapeMetadata, OutputFormat


def test_output_service_creates_nested_directories(tmp_path):
    """Test OutputService creates nested parent directories."""
    service = OutputService()
    file_path = tmp_path / "level1" / "level2" / "level3" / "test.md"

    metadata = ScrapeMetadata(source_url="https://example.com", scraped_at=datetime.now())
    response = ScrapeResponse(
        content="# Test Content\n\nThis is a test.",
        format=OutputFormat.MARKDOWN,
        metadata=metadata,
        success=True,
    )

    service.write_to_file(response, str(file_path))

    assert file_path.exists()
    assert file_path.parent.exists()
    content = file_path.read_text(encoding="utf-8")
    assert content == "# Test Content\n\nThis is a test."


def test_output_service_utf8_encoding(tmp_path):
    """Test OutputService handles UTF-8 content correctly."""
    service = OutputService()
    file_path = tmp_path / "utf8_test.md"

    metadata = ScrapeMetadata(source_url="https://example.com", scraped_at=datetime.now())
    response = ScrapeResponse(
        content="# Test 中文 العربية 日本語",
        format=OutputFormat.MARKDOWN,
        metadata=metadata,
        success=True,
    )

    service.write_to_file(response, str(file_path))

    assert file_path.exists()
    content = file_path.read_text(encoding="utf-8")
    assert "中文" in content
    assert "العربية" in content
    assert "日本語" in content
