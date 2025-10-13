"""
Unit tests for SummarizeRequest Pydantic model.

This module tests the validation rules and behavior of the SummarizeRequest model,
which represents user input for the summarize command.
"""

import pytest
from datetime import datetime, timezone
from pydantic import ValidationError

from src.models.summarize_request import SummarizeRequest


class TestSummarizeRequestValidation:
    """Test SummarizeRequest model validation rules."""

    def test_valid_instantiation_with_all_fields(self):
        """Test that SummarizeRequest can be created with all valid fields."""
        request = SummarizeRequest(
            url="https://example.com/article",
            model="gemini/gemini-pro",
            summary_length="standard",
            output_path="./summaries/output.md",
            save_original=True,
        )

        assert str(request.url) == "https://example.com/article"
        assert request.model == "gemini/gemini-pro"
        assert request.summary_length == "standard"
        assert request.output_path == "./summaries/output.md"
        assert request.save_original is True
        assert isinstance(request.timestamp, datetime)

    def test_valid_instantiation_with_minimal_fields(self):
        """Test that SummarizeRequest can be created with only required fields."""
        request = SummarizeRequest(url="https://example.com/article")

        assert str(request.url) == "https://example.com/article"
        assert request.model is None
        assert request.summary_length == "standard"  # default
        assert request.output_path is None
        assert request.save_original is False  # default
        assert isinstance(request.timestamp, datetime)

    def test_url_validation_accepts_valid_http_url(self):
        """Test that HTTP URLs are accepted."""
        request = SummarizeRequest(url="http://example.com/article")
        assert str(request.url) == "http://example.com/article"

    def test_url_validation_accepts_valid_https_url(self):
        """Test that HTTPS URLs are accepted."""
        request = SummarizeRequest(url="https://example.com/article")
        assert str(request.url) == "https://example.com/article"

    def test_url_validation_rejects_invalid_url(self):
        """Test that invalid URLs are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            SummarizeRequest(url="not-a-valid-url")

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("url",) for error in errors)

    def test_url_validation_rejects_empty_string(self):
        """Test that empty string URL is rejected."""
        with pytest.raises(ValidationError):
            SummarizeRequest(url="")

    def test_url_validation_rejects_file_protocol(self):
        """Test that file:// URLs are rejected (only HTTP/HTTPS allowed)."""
        with pytest.raises(ValidationError):
            SummarizeRequest(url="file:///path/to/file")

    def test_summary_length_validation_accepts_brief(self):
        """Test that 'brief' summary length is accepted."""
        request = SummarizeRequest(url="https://example.com/article", summary_length="brief")
        assert request.summary_length == "brief"

    def test_summary_length_validation_accepts_standard(self):
        """Test that 'standard' summary length is accepted."""
        request = SummarizeRequest(url="https://example.com/article", summary_length="standard")
        assert request.summary_length == "standard"

    def test_summary_length_validation_accepts_detailed(self):
        """Test that 'detailed' summary length is accepted."""
        request = SummarizeRequest(url="https://example.com/article", summary_length="detailed")
        assert request.summary_length == "detailed"

    def test_summary_length_validation_rejects_invalid_value(self):
        """Test that invalid summary length values are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            SummarizeRequest(
                url="https://example.com/article",
                summary_length="invalid",  # type: ignore
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("summary_length",) for error in errors)

    def test_summary_length_defaults_to_standard(self):
        """Test that summary_length defaults to 'standard' when not specified."""
        request = SummarizeRequest(url="https://example.com/article")
        assert request.summary_length == "standard"

    def test_optional_model_field(self):
        """Test that model field is optional."""
        request = SummarizeRequest(url="https://example.com/article")
        assert request.model is None

    def test_optional_model_field_accepts_value(self):
        """Test that model field accepts a valid value."""
        request = SummarizeRequest(
            url="https://example.com/article", model="gemini/gemini-1.5-flash"
        )
        assert request.model == "gemini/gemini-1.5-flash"

    def test_optional_output_path_field(self):
        """Test that output_path field is optional."""
        request = SummarizeRequest(url="https://example.com/article")
        assert request.output_path is None

    def test_optional_output_path_accepts_file_path(self):
        """Test that output_path accepts file path."""
        request = SummarizeRequest(
            url="https://example.com/article", output_path="./summaries/output.md"
        )
        assert request.output_path == "./summaries/output.md"

    def test_optional_output_path_accepts_directory_path(self):
        """Test that output_path accepts directory path."""
        request = SummarizeRequest(url="https://example.com/article", output_path="./summaries/")
        assert request.output_path == "./summaries/"

    def test_save_original_defaults_to_false(self):
        """Test that save_original defaults to False when not specified."""
        request = SummarizeRequest(url="https://example.com/article")
        assert request.save_original is False

    def test_save_original_accepts_true(self):
        """Test that save_original accepts True value."""
        request = SummarizeRequest(url="https://example.com/article", save_original=True)
        assert request.save_original is True

    def test_timestamp_auto_generation(self):
        """Test that timestamp is automatically generated."""
        before = datetime.now(timezone.utc)
        request = SummarizeRequest(url="https://example.com/article")
        after = datetime.now(timezone.utc)

        assert isinstance(request.timestamp, datetime)
        assert before <= request.timestamp <= after

    def test_timestamp_is_utc(self):
        """Test that auto-generated timestamp is in UTC."""
        request = SummarizeRequest(url="https://example.com/article")
        # Verify timestamp is close to now(UTC) (within 1 second)
        now = datetime.now(timezone.utc)
        time_diff = abs((request.timestamp - now).total_seconds())
        assert time_diff < 1.0


class TestSummarizeRequestSerialization:
    """Test SummarizeRequest JSON serialization and deserialization."""

    def test_model_can_be_serialized_to_json(self):
        """Test that SummarizeRequest can be serialized to JSON."""
        request = SummarizeRequest(
            url="https://example.com/article", model="gemini/gemini-pro", summary_length="brief"
        )

        json_data = request.model_dump_json()
        assert isinstance(json_data, str)
        assert "example.com" in json_data
        assert "gemini/gemini-pro" in json_data

    def test_model_can_be_deserialized_from_dict(self):
        """Test that SummarizeRequest can be created from dict."""
        data = {
            "url": "https://example.com/article",
            "model": "gemini/gemini-pro",
            "summary_length": "detailed",
            "output_path": "./output.md",
            "save_original": True,
            "timestamp": "2025-10-12T10:00:00",
        }

        request = SummarizeRequest(**data)
        assert str(request.url) == "https://example.com/article"
        assert request.model == "gemini/gemini-pro"
        assert request.summary_length == "detailed"

    def test_model_round_trip_serialization(self):
        """Test that SummarizeRequest can be serialized and deserialized."""
        original = SummarizeRequest(
            url="https://example.com/article", model="gemini/gemini-pro", summary_length="standard"
        )

        # Serialize to dict and back
        data = original.model_dump()
        reconstructed = SummarizeRequest(**data)

        assert str(reconstructed.url) == str(original.url)
        assert reconstructed.model == original.model
        assert reconstructed.summary_length == original.summary_length


class TestSummarizeRequestEdgeCases:
    """Test edge cases and error conditions."""

    def test_url_with_query_parameters(self):
        """Test that URLs with query parameters are accepted."""
        request = SummarizeRequest(url="https://example.com/article?page=1&lang=en")
        assert "page=1" in str(request.url)

    def test_url_with_fragment(self):
        """Test that URLs with fragments are accepted."""
        request = SummarizeRequest(url="https://example.com/article#section")
        assert "section" in str(request.url)

    def test_url_with_non_english_characters(self):
        """Test that URLs with international characters are accepted."""
        request = SummarizeRequest(url="https://example.com/文章")
        # URLs are percent-encoded, so check for the encoded form
        assert "%E6%96%87%E7%AB%A0" in str(request.url) or "文章" in str(request.url)

    def test_very_long_url(self):
        """Test that very long URLs are accepted."""
        long_path = "/".join([f"segment{i}" for i in range(100)])
        url = f"https://example.com/{long_path}"
        request = SummarizeRequest(url=url)
        assert "segment99" in str(request.url)

    def test_model_with_version_number(self):
        """Test that model names with version numbers are accepted."""
        request = SummarizeRequest(
            url="https://example.com/article", model="gemini/gemini-1.5-pro-001"
        )
        assert request.model == "gemini/gemini-1.5-pro-001"

    def test_output_path_with_windows_style_path(self):
        """Test that Windows-style paths are accepted."""
        request = SummarizeRequest(
            url="https://example.com/article", output_path="C:\\Users\\Documents\\summary.md"
        )
        assert request.output_path == "C:\\Users\\Documents\\summary.md"

    def test_output_path_with_unix_style_path(self):
        """Test that Unix-style paths are accepted."""
        request = SummarizeRequest(
            url="https://example.com/article", output_path="/home/user/documents/summary.md"
        )
        assert request.output_path == "/home/user/documents/summary.md"
