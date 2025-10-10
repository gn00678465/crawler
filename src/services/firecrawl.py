"""Firecrawl API integration service."""
from datetime import datetime
from firecrawl import Firecrawl
from src.models.scrape import ScrapeRequest, ScrapeResponse, ScrapeMetadata, OutputFormat
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
        api_key = settings.firecrawl_api_key if settings.firecrawl_api_key else "dummy-key-for-self-hosted"
        self.client = Firecrawl(
            api_key=api_key,
            api_url=settings.firecrawl_api_url
        )

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
            result = self.client.scrape(
                str(request.url),
                formats=['markdown', 'html']
            )

            # Handle both dict and object response formats
            if hasattr(result, '__dict__'):
                # Object format (newer API versions)
                result_dict = result.__dict__
                content = (
                    getattr(result, 'markdown', '')
                    if request.format == OutputFormat.MARKDOWN
                    else getattr(result, 'html', '')
                )
                metadata_obj = getattr(result, 'metadata', None)
                metadata_dict = metadata_obj.__dict__ if hasattr(metadata_obj, '__dict__') else {}
            else:
                # Dict format (older API versions)
                result_dict = result
                content = (
                    result.get('markdown', '')
                    if request.format == OutputFormat.MARKDOWN
                    else result.get('html', '')
                )
                metadata_dict = result.get('metadata', {})

            # Build metadata
            metadata = ScrapeMetadata(
                title=metadata_dict.get('title') if isinstance(metadata_dict, dict) else getattr(metadata_dict, 'title', None),
                description=metadata_dict.get('description') if isinstance(metadata_dict, dict) else getattr(metadata_dict, 'description', None),
                keywords=metadata_dict.get('keywords') if isinstance(metadata_dict, dict) else getattr(metadata_dict, 'keywords', None),
                source_url=metadata_dict.get('sourceURL', str(request.url)) if isinstance(metadata_dict, dict) else getattr(metadata_dict, 'sourceURL', str(request.url)),
                scraped_at=datetime.now()
            )

            return ScrapeResponse(
                content=content,
                format=request.format,
                metadata=metadata,
                success=True
            )
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "rate limit" in error_str.lower():
                raise RateLimitError("Firecrawl API rate limit exceeded") from e
            raise FirecrawlApiError(f"Failed to scrape URL: {e}") from e
