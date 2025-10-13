"""Unit tests for input validators."""

import pytest
from src.lib.validators import validate_url, validate_output_path, generate_filename_from_url
from src.lib.exceptions import ValidationError
from src.models.scrape import OutputFormat


# URL validator tests
def test_validate_url_valid():
    """Test validate_url accepts valid URLs."""
    assert validate_url("https://example.com")
    assert validate_url("http://localhost:3000")
    assert validate_url("https://sub.domain.com/path?query=1")


def test_validate_url_invalid():
    """Test validate_url rejects invalid URLs."""
    with pytest.raises(ValidationError):
        validate_url("not-a-url")


def test_validate_url_missing_protocol():
    """Test validate_url rejects URLs without protocol."""
    with pytest.raises(ValidationError):
        validate_url("example.com")  # Missing protocol


# Path validator tests
def test_validate_output_path_valid():
    """Test validate_output_path returns False for file paths."""
    assert validate_output_path("/path/to/file.md") == False
    assert validate_output_path("./relative/path/file.html") == False
    assert validate_output_path("C:\\Windows\\path\\file.txt") == False


def test_validate_output_path_directory():
    """Test validate_output_path returns True for directory paths."""
    assert validate_output_path("/path/to/directory/") == True
    assert validate_output_path("./relative/path/") == True
    assert validate_output_path("C:\\path\\to\\directory\\") == True


# Filename generation tests
def test_generate_filename_from_url_with_path():
    """Test filename generation from URL with path."""
    filename = generate_filename_from_url(
        "https://docs.lovable.dev/prompting/prompting-one", OutputFormat.HTML
    )
    assert filename == "prompting-one.html"


def test_generate_filename_from_url_root():
    """Test filename generation from URL ending with /."""
    filename = generate_filename_from_url("https://example.com/", OutputFormat.MARKDOWN)
    assert filename == "example-com.md"


def test_generate_filename_sanitization():
    """Test special character sanitization in filename."""
    filename = generate_filename_from_url(
        "https://example.com/path/file?query=1#anchor", OutputFormat.MARKDOWN
    )
    assert filename == "file.md"
    assert "?" not in filename
    assert "#" not in filename


def test_generate_filename_length_limit():
    """Test filename is limited to 200 characters."""
    long_path = "a" * 300
    filename = generate_filename_from_url(f"https://example.com/{long_path}", OutputFormat.MARKDOWN)
    # Should be 200 chars + ".md" extension
    assert len(filename) <= 203
