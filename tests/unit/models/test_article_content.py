"""
Unit tests for ArticleContent Pydantic model.

This module tests the validation rules and behavior of the ArticleContent model,
which represents crawled and processed article content in markdown format.
"""

import pytest
from datetime import datetime, timezone
from pydantic import ValidationError

from src.models.article_content import ArticleContent


class TestArticleContentValidation:
    """Test ArticleContent model validation rules."""

    def test_valid_instantiation_with_all_required_fields(self):
        """Test that ArticleContent can be created with all required fields."""
        content = ArticleContent(
            url="https://example.com/article",
            title="Introduction to Python",
            markdown="# Python\n\nPython is a programming language...",
            word_count=1500,
        )

        assert str(content.url) == "https://example.com/article"
        assert content.title == "Introduction to Python"
        assert content.markdown.startswith("# Python")
        assert content.word_count == 1500
        assert content.detected_language is None  # Optional
        assert content.metadata is None  # Optional
        assert isinstance(content.crawl_timestamp, datetime)

    def test_valid_instantiation_with_all_fields(self):
        """Test creating ArticleContent with all optional fields."""
        metadata = {"source": "firecrawl", "version": "v2"}
        content = ArticleContent(
            url="https://example.com/article",
            title="Introduction to Python",
            markdown="# Python\n\nPython is a programming language...",
            detected_language="en",
            word_count=1500,
            metadata=metadata,
        )

        assert content.detected_language == "en"
        assert content.metadata == metadata

    def test_url_validation_accepts_valid_urls(self):
        """Test that valid HTTP/HTTPS URLs are accepted."""
        content = ArticleContent(
            url="https://example.com/article", title="Test", markdown="Content", word_count=100
        )
        assert str(content.url) == "https://example.com/article"

    def test_url_validation_rejects_invalid_url(self):
        """Test that invalid URLs are rejected."""
        with pytest.raises(ValidationError):
            ArticleContent(url="not-a-valid-url", title="Test", markdown="Content", word_count=100)

    def test_title_field_required(self):
        """Test that title field is required."""
        with pytest.raises(ValidationError) as exc_info:
            ArticleContent(url="https://example.com/article", markdown="Content", word_count=100)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("title",) for error in errors)

    def test_markdown_field_required(self):
        """Test that markdown field is required."""
        with pytest.raises(ValidationError) as exc_info:
            ArticleContent(url="https://example.com/article", title="Test", word_count=100)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("markdown",) for error in errors)

    def test_word_count_field_required(self):
        """Test that word_count field is required."""
        with pytest.raises(ValidationError) as exc_info:
            ArticleContent(url="https://example.com/article", title="Test", markdown="Content")

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("word_count",) for error in errors)

    def test_word_count_accepts_zero(self):
        """Test that word_count can be zero for empty articles."""
        content = ArticleContent(
            url="https://example.com/article", title="Empty Article", markdown="", word_count=0
        )
        assert content.word_count == 0

    def test_word_count_accepts_large_values(self):
        """Test that word_count accepts large values."""
        content = ArticleContent(
            url="https://example.com/article",
            title="Long Article",
            markdown="Very long content...",
            word_count=50000,
        )
        assert content.word_count == 50000

    def test_detected_language_optional(self):
        """Test that detected_language is optional."""
        content = ArticleContent(
            url="https://example.com/article", title="Test", markdown="Content", word_count=100
        )
        assert content.detected_language is None

    def test_detected_language_accepts_iso_codes(self):
        """Test that detected_language accepts ISO 639-1 codes."""
        languages = ["en", "zh", "ja", "es", "fr", "de"]
        for lang in languages:
            content = ArticleContent(
                url="https://example.com/article",
                title="Test",
                markdown="Content",
                word_count=100,
                detected_language=lang,
            )
            assert content.detected_language == lang

    def test_metadata_optional(self):
        """Test that metadata is optional."""
        content = ArticleContent(
            url="https://example.com/article", title="Test", markdown="Content", word_count=100
        )
        assert content.metadata is None

    def test_metadata_accepts_dict(self):
        """Test that metadata accepts dictionary values."""
        metadata = {
            "source": "firecrawl",
            "version": "v2",
            "extraction_time": "2025-10-12T10:00:00Z",
        }
        content = ArticleContent(
            url="https://example.com/article",
            title="Test",
            markdown="Content",
            word_count=100,
            metadata=metadata,
        )
        assert content.metadata == metadata

    def test_crawl_timestamp_auto_generation(self):
        """Test that crawl_timestamp is automatically generated."""
        before = datetime.now(timezone.utc)
        content = ArticleContent(
            url="https://example.com/article", title="Test", markdown="Content", word_count=100
        )
        after = datetime.now(timezone.utc)

        assert isinstance(content.crawl_timestamp, datetime)
        assert before <= content.crawl_timestamp <= after


class TestArticleContentIsMinimalProperty:
    """Test ArticleContent.is_minimal computed property."""

    def test_is_minimal_true_for_zero_words(self):
        """Test that is_minimal returns True for 0 words."""
        content = ArticleContent(
            url="https://example.com/article", title="Empty", markdown="", word_count=0
        )
        assert content.is_minimal is True

    def test_is_minimal_true_for_under_100_words(self):
        """Test that is_minimal returns True for articles under 100 words."""
        content = ArticleContent(
            url="https://example.com/article",
            title="Short Article",
            markdown="Brief content with only a few words.",
            word_count=50,
        )
        assert content.is_minimal is True

    def test_is_minimal_true_for_99_words(self):
        """Test that is_minimal returns True for exactly 99 words."""
        content = ArticleContent(
            url="https://example.com/article",
            title="Short Article",
            markdown="Content...",
            word_count=99,
        )
        assert content.is_minimal is True

    def test_is_minimal_false_for_100_words(self):
        """Test that is_minimal returns False for exactly 100 words."""
        content = ArticleContent(
            url="https://example.com/article",
            title="Standard Article",
            markdown="Content...",
            word_count=100,
        )
        assert content.is_minimal is False

    def test_is_minimal_false_for_over_100_words(self):
        """Test that is_minimal returns False for articles over 100 words."""
        content = ArticleContent(
            url="https://example.com/article",
            title="Full Article",
            markdown="Full content with many paragraphs...",
            word_count=1500,
        )
        assert content.is_minimal is False

    def test_is_minimal_false_for_long_articles(self):
        """Test that is_minimal returns False for long articles."""
        content = ArticleContent(
            url="https://example.com/article",
            title="Long Article",
            markdown="Very long content...",
            word_count=50000,
        )
        assert content.is_minimal is False


class TestArticleContentSerialization:
    """Test ArticleContent JSON serialization and deserialization."""

    def test_model_can_be_serialized_to_json(self):
        """Test that ArticleContent can be serialized to JSON."""
        content = ArticleContent(
            url="https://example.com/article",
            title="Introduction to Python",
            markdown="# Python\n\nPython is a programming language...",
            word_count=1500,
            detected_language="en",
        )

        json_data = content.model_dump_json()
        assert isinstance(json_data, str)
        assert "example.com" in json_data
        assert "Introduction to Python" in json_data

    def test_model_can_be_deserialized_from_dict(self):
        """Test that ArticleContent can be created from dict."""
        data = {
            "url": "https://example.com/article",
            "title": "Introduction to Python",
            "markdown": "# Python\n\nPython is a programming language...",
            "detected_language": "en",
            "word_count": 1500,
            "crawl_timestamp": "2025-10-12T10:00:00Z",
        }

        content = ArticleContent(**data)
        assert content.title == "Introduction to Python"
        assert content.word_count == 1500

    def test_model_round_trip_serialization(self):
        """Test that ArticleContent can be serialized and deserialized."""
        original = ArticleContent(
            url="https://example.com/article",
            title="Test Article",
            markdown="Test content",
            word_count=500,
            detected_language="en",
        )

        # Serialize to dict and back
        data = original.model_dump()
        reconstructed = ArticleContent(**data)

        assert str(reconstructed.url) == str(original.url)
        assert reconstructed.title == original.title
        assert reconstructed.markdown == original.markdown
        assert reconstructed.word_count == original.word_count
        assert reconstructed.detected_language == original.detected_language


class TestArticleContentEdgeCases:
    """Test edge cases and special scenarios."""

    def test_markdown_with_special_characters(self):
        """Test that markdown with special characters is accepted."""
        markdown = "# Test\n\n**Bold** and *italic* and `code`\n\n```python\nprint('hello')\n```"
        content = ArticleContent(
            url="https://example.com/article", title="Test", markdown=markdown, word_count=100
        )
        assert content.markdown == markdown

    def test_markdown_with_unicode_characters(self):
        """Test that markdown with Unicode characters is accepted."""
        markdown = "# 中文標題\n\n這是中文內容。日本語もあります。"
        content = ArticleContent(
            url="https://example.com/article", title="多語言文章", markdown=markdown, word_count=50
        )
        assert "中文" in content.markdown

    def test_title_with_unicode_characters(self):
        """Test that titles with Unicode characters are accepted."""
        content = ArticleContent(
            url="https://example.com/article",
            title="Python入門：初心者ガイド",
            markdown="Content",
            word_count=100,
        )
        assert content.title == "Python入門：初心者ガイド"

    def test_very_long_title(self):
        """Test that very long titles are accepted."""
        long_title = "A " + "very " * 100 + "long title"
        content = ArticleContent(
            url="https://example.com/article", title=long_title, markdown="Content", word_count=100
        )
        assert content.title == long_title

    def test_very_long_markdown_content(self):
        """Test that very long markdown content is accepted."""
        long_markdown = "# Article\n\n" + ("Paragraph. " * 10000)
        content = ArticleContent(
            url="https://example.com/article",
            title="Long Article",
            markdown=long_markdown,
            word_count=50000,
        )
        assert len(content.markdown) > 100000

    def test_metadata_with_nested_dict(self):
        """Test that metadata accepts nested dictionaries."""
        metadata = {
            "firecrawl": {"version": "v2", "status": "success"},
            "extraction": {"method": "html", "timestamp": "2025-10-12T10:00:00Z"},
        }
        content = ArticleContent(
            url="https://example.com/article",
            title="Test",
            markdown="Content",
            word_count=100,
            metadata=metadata,
        )
        assert content.metadata["firecrawl"]["version"] == "v2"

    def test_empty_metadata_dict(self):
        """Test that empty metadata dict is accepted."""
        content = ArticleContent(
            url="https://example.com/article",
            title="Test",
            markdown="Content",
            word_count=100,
            metadata={},
        )
        assert content.metadata == {}
