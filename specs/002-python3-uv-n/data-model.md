# Data Model: Web Crawler CLI Tool

**Branch**: `002-python3-uv-n` | **Date**: 2025-10-10 | **Phase**: 1 (Design & Contracts)

## Overview

This document defines the core data models for the Web Crawler CLI Tool using Pydantic for validation and type safety. All models use Python 3.10+ type hints and follow PEP 8 naming conventions.

---

## 1. Configuration Models

### Settings

**Purpose**: Application configuration loaded from environment variables using python-dotenv.

**Location**: `src/config/settings.py`

**Fields**:

| Field | Type | Required | Default | Validation | Description |
|-------|------|----------|---------|------------|-------------|
| `firecrawl_api_url` | `str` | Yes | - | Must be valid URL | Self-hosted Firecrawl API base URL |
| `firecrawl_api_key` | `str` | No | `""` | - | API key (optional for self-hosted with auth disabled) |

**Validation Rules**:
- `firecrawl_api_url` must be a valid HTTP/HTTPS URL
- If `firecrawl_api_key` is empty string, assume self-hosted without authentication

**State Transitions**: N/A (immutable configuration)

**Example**:
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    firecrawl_api_url: str
    firecrawl_api_key: str = ""

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False
    }
```

---

## 2. Request Models

### OutputFormat

**Purpose**: Enum defining supported output formats for scraped content.

**Location**: `src/models/scrape.py`

**Values**:

| Value | Description | File Extension |
|-------|-------------|----------------|
| `MARKDOWN` | Markdown formatted content | `.md` |
| `HTML` | HTML formatted content | `.html` |

**Example**:
```python
from enum import Enum

class OutputFormat(str, Enum):
    MARKDOWN = "markdown"
    HTML = "html"
```

**Future Extensions** (P2 - User Story 2):
- `JSON` = "json"
- `TEXT` = "text"

---

### ScrapeRequest

**Purpose**: Input parameters for a web scraping operation.

**Location**: `src/models/scrape.py`

**Fields**:

| Field | Type | Required | Default | Validation | Description |
|-------|------|----------|---------|------------|-------------|
| `url` | `str` | Yes | - | Valid HTTP/HTTPS URL | Web page URL to scrape |
| `format` | `OutputFormat` | No | `OutputFormat.MARKDOWN` | Must be valid enum value | Desired output format |
| `output_path` | `Optional[str]` | No | `None` | Valid file path if provided | Output file path (None = stdout) |

**Validation Rules**:
- `url` must start with `http://` or `https://`
- `url` must be parseable by `urllib.parse.urlparse`
- If `output_path` is provided:
  - Must be a valid file path for the OS
  - Parent directory must exist or be creatable
  - Must not be a directory (must be a file path)
- File extension in `output_path` should match `format` (warning if mismatch)

**Relationships**:
- Uses `OutputFormat` enum for format validation
- Consumed by `FirecrawlService.scrape()`
- Created from CLI arguments in `src/cli/scrape.py`

**Example**:
```python
from pydantic import BaseModel, HttpUrl, field_validator
from typing import Optional

class ScrapeRequest(BaseModel):
    url: HttpUrl
    format: OutputFormat = OutputFormat.MARKDOWN
    output_path: Optional[str] = None

    @field_validator('output_path')
    @classmethod
    def validate_output_path(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            # Validation logic for file path
            pass
        return v
```

---

## 3. Response Models

### ScrapeMetadata

**Purpose**: Metadata about the scraped web page.

**Location**: `src/models/scrape.py`

**Fields**:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `title` | `Optional[str]` | No | `None` | Page title from HTML `<title>` tag |
| `description` | `Optional[str]` | No | `None` | Page description from meta tags |
| `keywords` | `Optional[str]` | No | `None` | Keywords from meta tags |
| `source_url` | `str` | Yes | - | Original URL that was scraped |
| `scraped_at` | `datetime` | Yes | - | Timestamp when scraping occurred |

**Example**:
```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ScrapeMetadata(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    keywords: Optional[str] = None
    source_url: str
    scraped_at: datetime
```

---

### ScrapeResponse

**Purpose**: Result of a web scraping operation including content and metadata.

**Location**: `src/models/scrape.py`

**Fields**:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `content` | `str` | Yes | - | Scraped content in requested format |
| `format` | `OutputFormat` | Yes | - | Format of the content |
| `metadata` | `ScrapeMetadata` | Yes | - | Page metadata |
| `success` | `bool` | Yes | `True` | Whether scraping succeeded |
| `error_message` | `Optional[str]` | No | `None` | Error description if `success=False` |

**Validation Rules**:
- If `success=True`, `content` must not be empty
- If `success=False`, `error_message` must be provided

**Relationships**:
- Contains `ScrapeMetadata`
- Contains `OutputFormat`
- Returned by `FirecrawlService.scrape()`
- Consumed by `OutputService.write()`

**State Transitions**:
- Created with `success=True` when Firecrawl API returns 200
- Created with `success=False` when Firecrawl API returns error or exception occurs

**Example**:
```python
from pydantic import BaseModel, field_validator
from typing import Optional

class ScrapeResponse(BaseModel):
    content: str
    format: OutputFormat
    metadata: ScrapeMetadata
    success: bool = True
    error_message: Optional[str] = None

    @field_validator('error_message')
    @classmethod
    def validate_error_message(cls, v: Optional[str], info) -> Optional[str]:
        if not info.data.get('success') and v is None:
            raise ValueError('error_message required when success=False')
        return v
```

---

## 4. Service Internal Models

### FirecrawlApiResponse

**Purpose**: Raw response from Firecrawl API (internal to `FirecrawlService`).

**Location**: `src/services/firecrawl.py` (private model)

**Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `markdown` | `Optional[str]` | No | Markdown-formatted content |
| `html` | `Optional[str]` | No | HTML content |
| `metadata` | `dict` | No | Metadata dictionary from API |
| `links` | `list[str]` | No | Extracted links from page |

**Note**: This model maps directly to Firecrawl v2 API response structure. Not exposed outside `FirecrawlService`.

**Example**:
```python
from pydantic import BaseModel
from typing import Optional

class FirecrawlApiResponse(BaseModel):
    markdown: Optional[str] = None
    html: Optional[str] = None
    metadata: dict = {}
    links: list[str] = []
```

---

## 5. CLI Argument Models

### ScrapeArguments

**Purpose**: Parsed CLI arguments before conversion to `ScrapeRequest`.

**Location**: `src/cli/scrape.py` (internal to CLI layer)

**Note**: Typer handles argument parsing directly via function parameters with type hints. This is a conceptual model showing the CLI interface contract.

**CLI Parameters**:

| Parameter | Type | Required | Default | Flag | Description |
|-----------|------|----------|---------|------|-------------|
| `url` | `str` | Yes | - | `--url` | URL to scrape |
| `markdown` | `bool` | No | `True` | `--markdown` / `--no-markdown` | Output as markdown (default) |
| `html` | `bool` | No | `False` | `--html` | Output as HTML |
| `output` | `Optional[str]` | No | `None` | `--output` | Output file path |

**Validation Logic**:
- If both `--markdown` and `--html` specified, `--html` takes precedence
- `url` validated before creating `ScrapeRequest`

**Transformation**:
```python
# CLI args → ScrapeRequest
scrape_request = ScrapeRequest(
    url=url,
    format=OutputFormat.HTML if html else OutputFormat.MARKDOWN,
    output_path=output
)
```

---

## 6. Error Models

### CrawlerError

**Purpose**: Base exception for all crawler-specific errors.

**Location**: `src/lib/exceptions.py`

**Hierarchy**:
```
CrawlerError (base)
├── ConfigurationError       # Missing/invalid configuration
├── ValidationError          # Invalid input (URL, path)
├── FirecrawlApiError        # Firecrawl API errors
│   ├── RateLimitError       # 429 rate limit exceeded
│   ├── AuthenticationError  # 401 authentication failed
│   └── ServerError          # 500 server error
└── OutputError              # File writing errors
```

**Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `message` | `str` | Human-readable error message |
| `code` | `int` | Exit code for CLI |
| `details` | `Optional[dict]` | Additional error context |

**Example**:
```python
class CrawlerError(Exception):
    def __init__(self, message: str, code: int = 1, details: dict | None = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)

class RateLimitError(CrawlerError):
    def __init__(self, message: str = "Rate limit exceeded", details: dict | None = None):
        super().__init__(message, code=3, details=details)
```

---

## 7. Entity Relationship Diagram

```
┌─────────────────┐
│    Settings     │ (Configuration)
│                 │
│ - api_url       │
│ - api_key       │
└─────────────────┘
        │
        │ injected into
        ▼
┌─────────────────┐         ┌──────────────────┐
│ ScrapeRequest   │────────>│  OutputFormat    │
│                 │  uses   │  (Enum)          │
│ - url           │         │                  │
│ - format        │         │ - MARKDOWN       │
│ - output_path   │         │ - HTML           │
└─────────────────┘         └──────────────────┘
        │
        │ consumed by
        ▼
┌─────────────────┐         ┌──────────────────┐
│ FirecrawlService│────────>│ FirecrawlApi     │
│                 │  calls  │ Response         │
│ - scrape()      │         │                  │
└─────────────────┘         │ - markdown       │
        │                   │ - html           │
        │ returns           │ - metadata       │
        ▼                   └──────────────────┘
┌─────────────────┐
│ ScrapeResponse  │         ┌──────────────────┐
│                 │────────>│ ScrapeMetadata   │
│ - content       │contains │                  │
│ - format        │         │ - title          │
│ - metadata      │         │ - description    │
│ - success       │         │ - source_url     │
│ - error_message │         │ - scraped_at     │
└─────────────────┘         └──────────────────┘
        │
        │ consumed by
        ▼
┌─────────────────┐
│  OutputService  │
│                 │
│ - write()       │
│ - print()       │
└─────────────────┘
```

---

## 8. Model Usage Flow

### Successful Scrape Flow

1. **CLI Layer** (`src/cli/scrape.py`):
   - Parse arguments: `url`, `markdown`/`html`, `output`
   - Create `ScrapeRequest(url=url, format=OutputFormat.MARKDOWN, output_path=output)`

2. **Service Layer** (`src/services/firecrawl.py`):
   - Load `Settings` from environment
   - Initialize Firecrawl client with `settings.firecrawl_api_url` and `settings.firecrawl_api_key`
   - Call `client.scrape(url, formats=['markdown', 'html'])`
   - Receive `FirecrawlApiResponse` from API
   - Transform to `ScrapeResponse`:
     - Extract content based on requested format
     - Create `ScrapeMetadata` from API metadata
     - Set `success=True`

3. **Output Layer** (`src/services/output.py`):
   - Receive `ScrapeResponse`
   - If `output_path` is `None`: print content to stdout
   - If `output_path` provided: write content to file with proper extension

### Error Flow

1. **CLI Layer**:
   - Invalid URL → raise `ValidationError`

2. **Service Layer**:
   - Missing API key → raise `ConfigurationError`
   - 429 response → raise `RateLimitError`
   - Network error → raise `FirecrawlApiError`
   - Create `ScrapeResponse(success=False, error_message="...")`

3. **CLI Layer** (error handler):
   - Catch exception
   - Print error message to stderr
   - Exit with appropriate code

---

## 9. Validation Summary

| Model | Key Validations |
|-------|----------------|
| `Settings` | Valid URL format for `firecrawl_api_url` |
| `ScrapeRequest` | Valid HTTP/HTTPS URL, valid file path if provided, format enum validation |
| `ScrapeResponse` | `error_message` required when `success=False`, non-empty content when `success=True` |
| `ScrapeMetadata` | `scraped_at` must be valid datetime, `source_url` required |
| `OutputFormat` | Must be valid enum member |

---

## 10. Future Extensions (P2-P3)

### Batch Request Model (P3)

```python
class BatchScrapeRequest(BaseModel):
    urls: list[HttpUrl]  # Multiple URLs
    format: OutputFormat = OutputFormat.MARKDOWN
    output_dir: str  # Directory instead of single file
    max_concurrent: int = 50  # Per SC-007
```

### Custom Filename Model (P3)

```python
class ScrapeRequest(BaseModel):
    # ... existing fields ...
    custom_filename: Optional[str] = None  # Per User Story 4
```

### Additional Formats (P2)

```python
class OutputFormat(str, Enum):
    MARKDOWN = "markdown"
    HTML = "html"
    JSON = "json"       # P2 extension
    TEXT = "text"       # P2 extension
```

---

**Model Design Completed**: 2025-10-10
**Status**: All entities from spec identified and modeled ✅
**Next**: Generate API contracts in `contracts/`
