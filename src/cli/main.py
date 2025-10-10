"""Main CLI application entry point."""
import typer
from src.cli.scrape import scrape

app = typer.Typer(
    name="crawler",
    help="Web Crawler CLI Tool - Scrape web pages using Firecrawl"
)

# Register commands
app.command("scrape")(scrape)


if __name__ == "__main__":
    app()
