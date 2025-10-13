"""
Pydantic model for output file results.

This module defines the OutputFile model which represents a successfully
written output file.
"""

from pydantic import BaseModel, Field, ConfigDict
from pathlib import Path


class OutputFile(BaseModel):
    """
    Represents a successfully written output file.

    This model encapsulates information about a file that has been successfully
    written to the filesystem, including its path, size, and format.

    Attributes:
        file_path: Absolute or relative path to the written file. Can be Windows-style
            (C:\\path\\to\\file.md) or Unix-style (/path/to/file.md).
        file_size: Size of the file in bytes. Can be 0 for empty files.
        format: File format/extension without the dot (e.g., 'md', 'html', 'txt').

    Properties:
        path_obj: Returns a pathlib.Path object for convenient file operations.

    Examples:
        >>> # Create OutputFile for a markdown summary
        >>> output = OutputFile(
        ...     file_path="/path/to/summaries/article-summary.md",
        ...     file_size=2048,
        ...     format="md"
        ... )
        >>>
        >>> # Access as pathlib.Path
        >>> output.path_obj
        PosixPath('/path/to/summaries/article-summary.md')
        >>>
        >>> # Get file name
        >>> output.path_obj.name
        'article-summary.md'
    """

    file_path: str = Field(..., description="Absolute or relative path to output file")

    file_size: int = Field(..., description="File size in bytes")

    format: str = Field(..., description="File format/extension without dot (e.g., 'md', 'html')")

    @property
    def path_obj(self) -> Path:
        """
        Return pathlib.Path object for file operations.

        Returns:
            Path object representing the file path

        Examples:
            >>> output = OutputFile(
            ...     file_path="/path/to/file.md",
            ...     file_size=2048,
            ...     format="md"
            ... )
            >>> output.path_obj.parent
            PosixPath('/path/to')
            >>> output.path_obj.stem
            'file'
        """
        return Path(self.file_path)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "file_path": "/path/to/summaries/article-summary.md",
                "file_size": 2048,
                "format": "md",
            }
        }
    )
