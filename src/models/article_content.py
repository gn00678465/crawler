"""
Pydantic model for article content.

This module defines the ArticleContent model which represents crawled and
processed article content in markdown format.
"""

from typing import Optional
from pydantic import BaseModel, HttpUrl, Field, ConfigDict
from datetime import datetime, timezone


class ArticleContent(BaseModel):
    """
    Represents crawled article content in markdown format.

    This model encapsulates the result of web crawling, including the original URL,
    extracted title, markdown-formatted content, language detection, and metadata
    from the crawler service.

    Attributes:
        url: Original article URL. Must be a valid HTTP or HTTPS URL.
        title: Article title extracted from HTML or derived from URL.
        markdown: Article content converted to markdown format. May include
            headings, lists, code blocks, and other markdown elements.
        detected_language: Auto-detected ISO 639-1 language code (e.g., 'en' for English,
            'zh' for Chinese, 'ja' for Japanese). Optional, may be None if language
            detection was not performed.
        word_count: Number of words in the markdown content. Used to determine
            if the article is substantial enough for summarization.
        crawl_timestamp: UTC timestamp when the article was crawled. Auto-generated.
        metadata: Additional metadata from the Firecrawl crawler service. Optional
            dictionary that may contain extraction method, version, status, etc.

    Properties:
        is_minimal: Returns True if word_count < 100, indicating the article may be
            too short to meaningfully summarize.

    Examples:
        >>> # Create ArticleContent with minimal fields
        >>> content = ArticleContent(
        ...     url="https://example.com/article",
        ...     title="Introduction to Python",
        ...     markdown="# Python\\n\\nPython is a programming language...",
        ...     word_count=1500
        ... )
        >>>
        >>> # Check if article is substantial
        >>> content.is_minimal
        False
        >>>
        >>> # Create with language detection
        >>> content = ArticleContent(
        ...     url="https://example.com/chinese-article",
        ...     title="Python 入門",
        ...     markdown="# Python\\n\\nPython 是一種程式語言...",
        ...     detected_language="zh",
        ...     word_count=2000
        ... )
    """

    url: HttpUrl = Field(..., description="Original article URL")

    title: str = Field(..., description="Article title extracted from HTML or URL")

    markdown: str = Field(..., description="Article content in markdown format")

    detected_language: Optional[str] = Field(
        default=None, description="ISO 639-1 language code (e.g., 'en', 'zh', 'ja')"
    )

    word_count: int = Field(..., description="Word count of markdown content")

    crawl_timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="When the article was crawled (UTC)",
    )

    metadata: Optional[dict] = Field(
        default=None, description="Additional metadata from Firecrawl crawler"
    )

    @property
    def is_minimal(self) -> bool:
        """
        Check if content is too short to meaningfully summarize.

        Returns:
            True if word_count < 100, False otherwise

        Examples:
            >>> content = ArticleContent(
            ...     url="https://example.com/short",
            ...     title="Brief Note",
            ...     markdown="Just a few words.",
            ...     word_count=50
            ... )
            >>> content.is_minimal
            True
            >>>
            >>> content = ArticleContent(
            ...     url="https://example.com/article",
            ...     title="Full Article",
            ...     markdown="Comprehensive content...",
            ...     word_count=1500
            ... )
            >>> content.is_minimal
            False
        """
        return self.word_count < 100

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "url": "https://example.com/article",
                "title": "Introduction to Python",
                "markdown": "# Python\\n\\nPython is a programming language...",
                "detected_language": "en",
                "word_count": 1500,
                "crawl_timestamp": "2025-10-12T10:30:00Z",
            }
        }
    )
