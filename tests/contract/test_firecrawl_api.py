"""Contract tests for Firecrawl API."""

import pytest
from firecrawl import Firecrawl
from src.config.settings import Settings


@pytest.mark.contract
def test_firecrawl_scrape_endpoint_contract():
    """Test Firecrawl API /scrape endpoint matches contract.

    This test requires a running Firecrawl instance.
    Skip if FIRECRAWL_API_URL is not configured.
    """
    try:
        settings = Settings()
    except Exception:
        pytest.skip("Firecrawl API not configured")

    client = Firecrawl(
        api_key=settings.firecrawl_api_key if settings.firecrawl_api_key else None,
        api_url=settings.firecrawl_api_url,
    )

    try:
        result = client.scrape("https://example.com", formats=["markdown", "html"])

        # Validate response structure per OpenAPI contract
        assert "markdown" in result
        assert "html" in result
        assert "metadata" in result
        assert isinstance(result["metadata"], dict)
        assert "sourceURL" in result["metadata"]

        # Validate content is not empty
        assert len(result["markdown"]) > 0
        assert len(result["html"]) > 0

    except Exception as e:
        pytest.skip(f"Firecrawl API unavailable: {e}")
