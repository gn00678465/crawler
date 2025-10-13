"""Output handling service for saving or displaying scraped content."""

from pathlib import Path
import sys
from src.models.scrape import ScrapeResponse
from src.models.output_file import OutputFile
from src.lib.exceptions import OutputError


class OutputService:
    """Service for writing scraped content to files or console."""

    def write_to_file(self, response: ScrapeResponse, file_path: str) -> None:
        """Write scraped content to file.

        Creates parent directories if they don't exist.

        Args:
            response: Scrape response with content
            file_path: Path where content will be saved

        Raises:
            OutputError: If file cannot be written
        """
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(response.content, encoding="utf-8")
        except Exception as e:
            raise OutputError(f"Failed to write output file: {e}") from e

    def print_to_console(self, response: ScrapeResponse) -> None:
        """Print scraped content to stdout.

        Args:
            response: Scrape response with content
        """
        print(response.content)

    def save(self, content: str, output_path: Path) -> OutputFile:
        """
        Save content to file and return OutputFile result.

        This method supports both file paths and directory paths.
        If a directory is provided, it must already exist.

        Args:
            content: Text content to save
            output_path: Path object for output file

        Returns:
            OutputFile with file path and metadata

        Raises:
            OutputError: If file cannot be written

        Examples:
            >>> service = OutputService()
            >>> result = service.save("Summary text", Path("summary.md"))
            >>> print(result.file_path)
        """
        try:
            # Ensure parent directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Write content
            output_path.write_text(content, encoding="utf-8")

            # Get file size
            file_size = output_path.stat().st_size

            # Return OutputFile
            return OutputFile(
                file_path=str(output_path),
                format="markdown",  # Assume markdown for summaries
                file_size=file_size,
            )
        except Exception as e:
            raise OutputError(f"Failed to write output file: {e}") from e
