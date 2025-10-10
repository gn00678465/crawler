"""Data models for scrape operations."""
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, HttpUrl, model_validator


class OutputFormat(str, Enum):
    """Supported output formats for scraped content.

    Attributes:
        MARKDOWN: Markdown formatted content
        HTML: HTML formatted content
    """
    MARKDOWN = "markdown"
    HTML = "html"


class ScrapeMetadata(BaseModel):
    """Metadata about a scraped web page.

    Attributes:
        title: Page title from HTML <title> tag
        description: Page description from meta tags
        keywords: Keywords from meta tags
        source_url: Original URL that was scraped
        scraped_at: Timestamp when scraping occurred
    """
    title: Optional[str] = None
    description: Optional[str] = None
    keywords: Optional[str] = None
    source_url: str
    scraped_at: datetime


class ScrapeRequest(BaseModel):
    """Request parameters for scraping a web page.

    Attributes:
        url: Web page URL to scrape (must be valid HTTP/HTTPS URL)
        format: Desired output format (default: MARKDOWN)
        output_path: Output file path, None means stdout
    """
    url: HttpUrl
    format: OutputFormat = OutputFormat.MARKDOWN
    output_path: Optional[str] = None


class ScrapeResponse(BaseModel):
    """Response from a web scraping operation.

    Attributes:
        content: Scraped content in requested format
        format: Format of the content
        metadata: Page metadata
        success: Whether scraping succeeded
        error_message: Error description if success=False
    """
    content: str
    format: OutputFormat
    metadata: ScrapeMetadata
    success: bool = True
    error_message: Optional[str] = None

    @model_validator(mode='after')
    def validate_error_message(self) -> 'ScrapeResponse':
        """Validate that error_message is provided when success=False.

        Returns:
            The validated model

        Raises:
            ValueError: If success=False and error_message is None
        """
        if not self.success and self.error_message is None:
            raise ValueError('error_message required when success=False')
        return self
