"""Main CLI application entry point."""

import typer
from src.cli.scrape import scrape
from src.cli.summarize import summarize

app = typer.Typer(
    name="crawler", help="Web Crawler CLI Tool - Scrape web pages and summarize articles with AI"
)

# Register commands
app.command("scrape")(scrape)
app.command("summarize")(summarize)


if __name__ == "__main__":
    app()
