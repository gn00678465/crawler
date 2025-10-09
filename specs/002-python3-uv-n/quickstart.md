# Quickstart Guide: Web Crawler CLI Tool

**Branch**: `002-python3-uv-n` | **Date**: 2025-10-10 | **Phase**: 1 (Design & Contracts)

## Overview

This guide provides step-by-step instructions for setting up and using the Web Crawler CLI Tool. Follow these instructions to go from zero to scraping your first web page in under 5 minutes.

---

## Prerequisites

Before you begin, ensure you have:

1. **Python 3.10 or higher** installed
   ```bash
   python --version  # Should show Python 3.10+
   ```

2. **UV package manager** installed
   ```bash
   # Install UV (if not already installed)
   # Windows (PowerShell)
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Verify installation
   uv --version
   ```

3. **Self-hosted Firecrawl instance** running
   - See [Firecrawl self-hosting guide](https://docs.firecrawl.dev/contributing/self-host)
   - Default: `http://localhost:3002`

---

## Step 1: Clone and Navigate to Project

```bash
# Clone the repository
git clone <repository-url>
cd crawler

# Switch to feature branch
git checkout 002-python3-uv-n
```

---

## Step 2: Set Up Environment

### Create Virtual Environment

```bash
# Create virtual environment using UV
uv venv

# Activate virtual environment
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (CMD)
.venv\Scripts\activate.bat

# macOS/Linux
source .venv/bin/activate
```

### Install Dependencies

```bash
# Install all dependencies from pyproject.toml
uv pip install -e .

# Verify installation
python -c "import typer; import firecrawl; print('Dependencies installed successfully!')"
```

---

## Step 3: Configure Environment Variables

### Create `.env` File

```bash
# Copy example configuration
cp .env.example .env
```

### Edit `.env` File

Open `.env` in your text editor and set the following variables:

```ini
# Firecrawl API Configuration
FIRECRAWL_API_URL=http://localhost:3002
FIRECRAWL_API_KEY=

# Note: FIRECRAWL_API_KEY can be empty for self-hosted instances
# with USE_DB_AUTHENTICATION=false (default for self-hosted)
```

**Configuration Reference**:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `FIRECRAWL_API_URL` | Yes | - | Base URL of self-hosted Firecrawl instance |
| `FIRECRAWL_API_KEY` | No | `""` | API key (optional for self-hosted) |

---

## Step 4: Verify Firecrawl Connection

Test that your Firecrawl instance is accessible:

```bash
# Windows (PowerShell)
Invoke-WebRequest -Uri http://localhost:3002/health

# macOS/Linux
curl http://localhost:3002/health
```

**Expected Response**: HTTP 200 OK

If you receive an error, ensure:
- Firecrawl Docker container is running
- Port 3002 is not blocked by firewall
- `FIRECRAWL_API_URL` in `.env` matches your Firecrawl instance URL

---

## Step 5: Run Your First Scrape

### Example 1: Scrape to Console (Markdown)

```bash
crawler scrape --url https://example.com
```

**Expected Output**:
```markdown
# Example Domain

This domain is for use in illustrative examples in documents. You may use this
domain in literature without prior coordination or asking for permission.

[More information...](https://www.iana.org/domains/example)
```

**Success Indicator** (stderr):
```
✓ Scraped: https://example.com
```

---

### Example 2: Scrape to File (Markdown)

```bash
crawler scrape --url https://example.com --output ./data/example.md
```

**Expected Output** (stderr):
```
✓ Content saved to: D:\Projects\crawler\data\example.md
✓ Scraped: https://example.com
```

**Verify File Created**:
```bash
# Windows
type data\example.md

# macOS/Linux
cat data/example.md
```

---

### Example 3: Scrape as HTML

```bash
crawler scrape --url https://example.com --html --output ./data/example.html
```

**Expected Output** (stderr):
```
✓ Content saved to: D:\Projects\crawler\data\example.html
✓ Scraped: https://example.com
```

---

## Step 6: Explore Additional Options

### View Help Documentation

```bash
crawler scrape --help
```

### Scrape and Pipe to Other Commands

```bash
# Search for specific content
crawler scrape --url https://example.com | grep "Example"

# Save output using shell redirection
crawler scrape --url https://example.com > page.md
```

---

## Common Use Cases

### Use Case 1: Scrape a Blog Post

```bash
crawler scrape --url https://blog.example.com/post-title --markdown --output ./articles/post-title.md
```

### Use Case 2: Archive a Web Page as HTML

```bash
crawler scrape --url https://important-page.com --html --output ./archive/page-$(date +%Y%m%d).html
```

### Use Case 3: Extract Content for Analysis

```bash
crawler scrape --url https://data-source.com | python analyze.py
```

---

## Troubleshooting

### Problem: "Error: Missing required configuration: FIRECRAWL_API_URL"

**Solution**: Ensure `.env` file exists in project root and contains `FIRECRAWL_API_URL`.

```bash
# Check if .env exists
ls .env

# Verify contents
# Windows
type .env

# macOS/Linux
cat .env
```

---

### Problem: "Error: Failed to connect to Firecrawl API"

**Solution**: Verify Firecrawl instance is running and accessible.

```bash
# Check if Firecrawl container is running
docker ps | grep firecrawl

# Test connection
curl http://localhost:3002/health

# Restart Firecrawl if needed
docker-compose restart firecrawl
```

---

### Problem: "Error: Invalid URL format"

**Solution**: Ensure URL starts with `http://` or `https://`.

**Incorrect**:
```bash
crawler scrape --url example.com  # Missing protocol
```

**Correct**:
```bash
crawler scrape --url https://example.com
```

---

### Problem: "Error: Rate limit exceeded"

**Solution**: Wait and retry. For self-hosted instances, you can adjust rate limits in Firecrawl configuration.

**Temporary Workaround**: Wait 60 seconds and retry.

**Long-term Solution**: Adjust `REDIS_RATE_LIMIT_URL` settings in Firecrawl configuration.

---

### Problem: Permission denied when writing output file

**Solution**: Ensure you have write permissions for the output directory.

```bash
# Create output directory if it doesn't exist
mkdir -p ./data

# Check permissions (Unix)
ls -ld ./data
```

---

## Next Steps

### Run Tests (for Developers)

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_validators.py
```

### Code Quality Checks

```bash
# Format code
ruff format src/

# Lint code
ruff check src/

# Type checking
mypy src/
```

### Contributing

Before submitting changes:

1. **Write tests first** (TDD per constitution)
2. **Run quality checks** (linting, type checking, tests)
3. **Ensure 80%+ code coverage**
4. **Update documentation** if adding new features

---

## Quick Reference

### Basic Commands

```bash
# Scrape to console (markdown)
crawler scrape --url <URL>

# Scrape to file (markdown)
crawler scrape --url <URL> --output <FILE.md>

# Scrape as HTML
crawler scrape --url <URL> --html --output <FILE.html>

# Show help
crawler scrape --help
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error (invalid URL, network failure) |
| 2 | Configuration error (missing API URL) |
| 3 | Rate limit exceeded |

### Environment Variables

```ini
FIRECRAWL_API_URL=http://localhost:3002  # Required
FIRECRAWL_API_KEY=                       # Optional
```

---

## Additional Resources

- **Feature Specification**: [spec.md](./spec.md)
- **Data Models**: [data-model.md](./data-model.md)
- **API Contracts**: [contracts/](./contracts/)
- **Implementation Plan**: [plan.md](./plan.md)
- **Research Findings**: [research.md](./research.md)

- **Firecrawl Documentation**: https://docs.firecrawl.dev/
- **Typer Documentation**: https://typer.tiangolo.com/
- **UV Documentation**: https://docs.astral.sh/uv/

---

## Support

For issues or questions:

1. Check [Troubleshooting](#troubleshooting) section above
2. Review specification documents in `specs/002-python3-uv-n/`
3. Check Firecrawl logs: `docker logs firecrawl`
4. Verify environment configuration in `.env`

---

**Quickstart Guide Version**: 1.0.0
**Last Updated**: 2025-10-10
**Status**: Ready for implementation ✅
