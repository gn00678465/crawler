"""Input validation utilities."""

import re
from urllib.parse import urlparse
from src.lib.exceptions import ValidationError
from src.models.scrape import OutputFormat


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
    """Validate output path and detect if it's a directory.

    Args:
        path: File or directory path to validate

    Returns:
        True if path is a directory, False if it's a file path
    """
    return path.endswith(("/", "\\"))


def generate_filename_from_url(url: str, format: OutputFormat) -> str:
    """Generate filename from URL path following FR-010 algorithm.

    Args:
        url: Source URL to extract filename from
        format: Output format to determine file extension

    Returns:
        Sanitized filename with appropriate extension

    Example:
        >>> generate_filename_from_url("https://example.com/path/page-name", OutputFormat.HTML)
        'page-name.html'
    """
    parsed = urlparse(url)

    # Extract last path segment
    path_parts = [p for p in parsed.path.split("/") if p]
    if path_parts:
        base_name = path_parts[-1]
    else:
        # Fallback to domain name
        base_name = parsed.netloc.replace(".", "-")

    # Sanitize: replace special characters with hyphens
    base_name = re.sub(r'[/\\?#:*"<>|]', "-", base_name)
    base_name = re.sub(r"-+", "-", base_name)  # Collapse multiple hyphens
    base_name = base_name.strip("-")

    # Limit length to 200 characters
    if len(base_name) > 200:
        base_name = base_name[:200]

    # Append extension
    if format == OutputFormat.MARKDOWN:
        extension = ".md"
    elif format == OutputFormat.HTML:
        extension = ".html"
    else:
        # Default to markdown
        extension = ".md"

    return base_name + extension
