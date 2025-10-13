"""Firecrawl API integration service."""

from datetime import datetime
from firecrawl import Firecrawl
from src.models.scrape import ScrapeRequest, ScrapeResponse, ScrapeMetadata, OutputFormat
from src.models.article_content import ArticleContent
from src.config.settings import Settings
from src.lib.exceptions import RateLimitError, FirecrawlApiError


class FirecrawlService:
    """Service for interacting with Firecrawl API.

    This service wraps the official Firecrawl Python SDK and provides
    methods for scraping web pages.
    """

    def __init__(self, settings: Settings):
        """Initialize Firecrawl client.

        Args:
            settings: Application settings with API URL and key
        """
        # Use a placeholder API key if none provided (for self-hosted instances)
        api_key = (
            settings.firecrawl_api_key
            if settings.firecrawl_api_key
            else "dummy-key-for-self-hosted"
        )
        self.client = Firecrawl(api_key=api_key, api_url=settings.firecrawl_api_url)

    def scrape(self, request: ScrapeRequest) -> ScrapeResponse:
        """Scrape a web page and return content.

        Args:
            request: Scrape request with URL and format

        Returns:
            ScrapeResponse with content and metadata

        Raises:
            RateLimitError: If API rate limit exceeded
            FirecrawlApiError: If API returns error
        """
        try:
            result = self.client.scrape(str(request.url), formats=["markdown", "html"])

            # Handle both dict and object response formats
            if hasattr(result, "__dict__"):
                # Object format (newer API versions)
                result_dict = result.__dict__
                content = (
                    getattr(result, "markdown", "")
                    if request.format == OutputFormat.MARKDOWN
                    else getattr(result, "html", "")
                )
                metadata_obj = getattr(result, "metadata", None)
                metadata_dict = metadata_obj.__dict__ if hasattr(metadata_obj, "__dict__") else {}
            else:
                # Dict format (older API versions)
                result_dict = result
                content = (
                    result.get("markdown", "")
                    if request.format == OutputFormat.MARKDOWN
                    else result.get("html", "")
                )
                metadata_dict = result.get("metadata", {})

            # Build metadata
            metadata = ScrapeMetadata(
                title=metadata_dict.get("title")
                if isinstance(metadata_dict, dict)
                else getattr(metadata_dict, "title", None),
                description=metadata_dict.get("description")
                if isinstance(metadata_dict, dict)
                else getattr(metadata_dict, "description", None),
                keywords=metadata_dict.get("keywords")
                if isinstance(metadata_dict, dict)
                else getattr(metadata_dict, "keywords", None),
                source_url=metadata_dict.get("sourceURL", str(request.url))
                if isinstance(metadata_dict, dict)
                else getattr(metadata_dict, "sourceURL", str(request.url)),
                scraped_at=datetime.now(),
            )

            return ScrapeResponse(
                content=content, format=request.format, metadata=metadata, success=True
            )
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "rate limit" in error_str.lower():
                raise RateLimitError("Firecrawl API rate limit exceeded") from e
            raise FirecrawlApiError(f"Failed to scrape URL: {e}") from e

    def scrape_to_article_content(self, url: str) -> ArticleContent:
        """
        Scrape URL and return ArticleContent model.

        This method is a convenience wrapper that scrapes a URL
        and returns it in the ArticleContent format used by the
        AI summarization feature.

        Args:
            url: URL to scrape

        Returns:
            ArticleContent with markdown and metadata

        Raises:
            RateLimitError: If API rate limit exceeded
            FirecrawlApiError: If API returns error

        Examples:
            >>> service = FirecrawlService(settings)
            >>> article = service.scrape_to_article_content("https://example.com")
            >>> print(article.title)
        """
        # Create a ScrapeRequest for markdown format
        request = ScrapeRequest(url=url, format=OutputFormat.MARKDOWN)

        # Use existing scrape method
        result = self.scrape(request)

        # Calculate word count
        word_count = len(result.content.split())

        # Build ArticleContent from ScrapeResponse
        return ArticleContent(
            url=url,
            title=result.metadata.title or url.split("/")[-1],
            markdown=result.content,
            word_count=word_count,
            detected_language=None,  # Will be detected by AI
            crawl_timestamp=result.metadata.scraped_at,
            metadata={
                "source_url": result.metadata.source_url,
                "description": result.metadata.description,
                "keywords": result.metadata.keywords,
            },
        )
