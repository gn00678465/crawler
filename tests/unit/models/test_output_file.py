"""
Unit tests for OutputFile Pydantic model.

This module tests the validation rules and behavior of the OutputFile model,
which represents a successfully written output file.
"""

import pytest
from pathlib import Path
from pydantic import ValidationError

from src.models.output_file import OutputFile


class TestOutputFileValidation:
    """Test OutputFile model validation rules."""

    def test_valid_instantiation_with_all_fields(self):
        """Test creating OutputFile with all fields."""
        output = OutputFile(
            file_path="/path/to/summaries/article-summary.md", file_size=2048, format="md"
        )

        assert output.file_path == "/path/to/summaries/article-summary.md"
        assert output.file_size == 2048
        assert output.format == "md"

    def test_file_path_required(self):
        """Test that file_path is required."""
        with pytest.raises(ValidationError) as exc_info:
            OutputFile(file_size=2048, format="md")

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("file_path",) for error in errors)

    def test_file_size_required(self):
        """Test that file_size is required."""
        with pytest.raises(ValidationError) as exc_info:
            OutputFile(file_path="/path/to/file.md", format="md")

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("file_size",) for error in errors)

    def test_format_required(self):
        """Test that format is required."""
        with pytest.raises(ValidationError) as exc_info:
            OutputFile(file_path="/path/to/file.md", file_size=2048)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("format",) for error in errors)

    def test_file_size_accepts_zero(self):
        """Test that file_size can be zero for empty files."""
        output = OutputFile(file_path="/path/to/empty.md", file_size=0, format="md")
        assert output.file_size == 0

    def test_file_size_accepts_large_values(self):
        """Test that file_size accepts large values."""
        output = OutputFile(
            file_path="/path/to/large-file.md",
            file_size=10000000,  # 10 MB
            format="md",
        )
        assert output.file_size == 10000000


class TestOutputFilePathObjProperty:
    """Test OutputFile.path_obj computed property."""

    def test_path_obj_returns_pathlib_path(self):
        """Test that path_obj returns a pathlib.Path object."""
        output = OutputFile(file_path="/path/to/file.md", file_size=2048, format="md")

        assert isinstance(output.path_obj, Path)
        # Path may normalize separators on Windows
        assert "file.md" in str(output.path_obj)

    def test_path_obj_preserves_windows_paths(self):
        """Test that path_obj handles Windows-style paths."""
        output = OutputFile(
            file_path="C:\\Users\\Documents\\summary.md", file_size=2048, format="md"
        )

        assert isinstance(output.path_obj, Path)
        assert "summary.md" in str(output.path_obj)

    def test_path_obj_preserves_unix_paths(self):
        """Test that path_obj handles Unix-style paths."""
        output = OutputFile(
            file_path="/home/user/documents/summary.md", file_size=2048, format="md"
        )

        assert isinstance(output.path_obj, Path)
        # Path may normalize separators based on OS
        assert "summary.md" in str(output.path_obj)
        assert "documents" in str(output.path_obj)


class TestOutputFileFormatTypes:
    """Test different file format types."""

    def test_markdown_format(self):
        """Test that markdown format is accepted."""
        output = OutputFile(file_path="/path/to/file.md", file_size=2048, format="md")
        assert output.format == "md"

    def test_html_format(self):
        """Test that html format is accepted."""
        output = OutputFile(file_path="/path/to/file.html", file_size=2048, format="html")
        assert output.format == "html"

    def test_text_format(self):
        """Test that text format is accepted."""
        output = OutputFile(file_path="/path/to/file.txt", file_size=2048, format="txt")
        assert output.format == "txt"

    def test_json_format(self):
        """Test that json format is accepted."""
        output = OutputFile(file_path="/path/to/file.json", file_size=2048, format="json")
        assert output.format == "json"


class TestOutputFileSerialization:
    """Test OutputFile JSON serialization and deserialization."""

    def test_model_can_be_serialized_to_json(self):
        """Test that OutputFile can be serialized to JSON."""
        output = OutputFile(
            file_path="/path/to/summaries/article-summary.md", file_size=2048, format="md"
        )

        json_data = output.model_dump_json()
        assert isinstance(json_data, str)
        assert "article-summary.md" in json_data

    def test_model_can_be_deserialized_from_dict(self):
        """Test that OutputFile can be created from dict."""
        data = {
            "file_path": "/path/to/summaries/article-summary.md",
            "file_size": 2048,
            "format": "md",
        }

        output = OutputFile(**data)
        assert output.file_path == "/path/to/summaries/article-summary.md"
        assert output.file_size == 2048

    def test_model_round_trip_serialization(self):
        """Test that OutputFile can be serialized and deserialized."""
        original = OutputFile(file_path="/path/to/file.md", file_size=4096, format="md")

        data = original.model_dump()
        reconstructed = OutputFile(**data)

        assert reconstructed.file_path == original.file_path
        assert reconstructed.file_size == original.file_size
        assert reconstructed.format == original.format


class TestOutputFileEdgeCases:
    """Test edge cases and special scenarios."""

    def test_very_long_file_path(self):
        """Test that very long file paths are accepted."""
        long_path = "/path/" + "/".join([f"dir{i}" for i in range(50)]) + "/file.md"
        output = OutputFile(file_path=long_path, file_size=2048, format="md")
        assert "dir49" in output.file_path

    def test_file_path_with_unicode_characters(self):
        """Test that file paths with Unicode characters are accepted."""
        output = OutputFile(file_path="/path/to/文章-summary.md", file_size=2048, format="md")
        assert "文章" in output.file_path

    def test_file_path_with_spaces(self):
        """Test that file paths with spaces are accepted."""
        output = OutputFile(file_path="/path/to/article summary.md", file_size=2048, format="md")
        assert "article summary" in output.file_path

    def test_format_without_dot(self):
        """Test that format is stored without dot prefix."""
        output = OutputFile(
            file_path="/path/to/file.md",
            file_size=2048,
            format="md",  # Not ".md"
        )
        assert output.format == "md"
        assert not output.format.startswith(".")

    def test_relative_file_path(self):
        """Test that relative file paths are accepted."""
        output = OutputFile(file_path="./summaries/article-summary.md", file_size=2048, format="md")
        assert output.file_path == "./summaries/article-summary.md"

    def test_absolute_windows_file_path(self):
        """Test that absolute Windows file paths are accepted."""
        output = OutputFile(
            file_path="D:\\Projects\\crawler\\summaries\\article-summary.md",
            file_size=2048,
            format="md",
        )
        assert "D:" in output.file_path or "D:\\\\" in output.file_path
