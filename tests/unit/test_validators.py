"""Unit tests for input validators."""
import pytest
from src.lib.validators import validate_url, validate_output_path
from src.lib.exceptions import ValidationError


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
    """Test validate_output_path accepts valid file paths."""
    assert validate_output_path("/path/to/file.md")
    assert validate_output_path("./relative/path/file.html")
    assert validate_output_path("C:\\Windows\\path\\file.txt")


def test_validate_output_path_directory():
    """Test validate_output_path rejects directory paths."""
    with pytest.raises(ValidationError):
        validate_output_path("/path/to/directory/")

    with pytest.raises(ValidationError):
        validate_output_path("C:\\path\\to\\directory\\")
