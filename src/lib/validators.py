"""Input validation utilities."""
from urllib.parse import urlparse
from src.lib.exceptions import ValidationError


def validate_url(url: str) -> bool:
    """Validate URL has proper format and protocol.

    Args:
        url: URL string to validate

    Returns:
        True if valid

    Raises:
        ValidationError: If URL is invalid or missing http/https protocol
    """
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            raise ValidationError(f"URL must use http:// or https:// protocol: {url}")
        if not parsed.netloc:
            raise ValidationError(f"Invalid URL format: {url}")
        return True
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid URL: {url}") from e


def validate_output_path(path: str) -> bool:
    """Validate output path is a file path, not a directory.

    Args:
        path: File path to validate

    Returns:
        True if valid

    Raises:
        ValidationError: If path is a directory or invalid
    """
    if path.endswith(("/", "\\")):
        raise ValidationError(f"Output path must be a file, not a directory: {path}")
    return True
