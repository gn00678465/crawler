"""Typer CLI command for scraping web pages."""
import typer
from typing import Optional
from src.config.settings import Settings
from src.models.scrape import ScrapeRequest, OutputFormat
from src.services.firecrawl import FirecrawlService
from src.services.output import OutputService
from src.lib.validators import validate_url, validate_output_path, generate_filename_from_url
from src.lib.exceptions import CrawlerError, ValidationError


def scrape(
    url: str = typer.Option(..., help="URL to scrape"),
    markdown: bool = typer.Option(True, help="Output as markdown (default)"),
    html: bool = typer.Option(False, help="Output as HTML"),
    output: Optional[str] = typer.Option(None, help="Output file path (default: stdout)")
):
    """Scrape a single web page using Firecrawl.

    Scrapes the specified URL and outputs the content in the chosen format
    (markdown or HTML). Content can be printed to console or saved to a file.

    Examples:

        # Scrape to console (markdown)

        crawler scrape --url https://example.com

        # Scrape to file (HTML)

        crawler scrape --url https://example.com --html --output page.html
    """
    try:
        # Validate URL
        validate_url(url)

        # Determine if output is a directory and generate filename if needed
        is_directory = False
        if output:
            is_directory = validate_output_path(output)

        # Load settings
        try:
            settings = Settings()
        except Exception as e:
            typer.secho(
                f"Error: Missing required configuration: {e}",
                fg=typer.colors.RED,
                err=True
            )
            raise typer.Exit(2)

        # Determine format
        format_choice = OutputFormat.HTML if html else OutputFormat.MARKDOWN

        # Create request
        request = ScrapeRequest(
            url=url,
            format=format_choice,
            output_path=output
        )

        # Scrape page
        firecrawl_service = FirecrawlService(settings)
        response = firecrawl_service.scrape(request)

        # Output results
        output_service = OutputService()
        if output:
            # If output is a directory, generate filename from URL
            if is_directory:
                from pathlib import Path
                filename = generate_filename_from_url(url, format_choice)
                final_path = str(Path(output) / filename)
                output_service.write_to_file(response, final_path)
                typer.secho(f"✓ Content saved to: {final_path}", fg=typer.colors.GREEN, err=True)
            else:
                output_service.write_to_file(response, output)
                typer.secho(f"✓ Content saved to: {output}", fg=typer.colors.GREEN, err=True)
        else:
            output_service.print_to_console(response)

        typer.secho(f"✓ Scraped: {url}", fg=typer.colors.GREEN, err=True)

    except ValidationError as e:
        typer.secho(f"Error: {e.message}", fg=typer.colors.RED, err=True)
        raise typer.Exit(e.code)
    except CrawlerError as e:
        typer.secho(f"Error: {e.message}", fg=typer.colors.RED, err=True)
        raise typer.Exit(e.code)
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)
