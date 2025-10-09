# Implementation Tasks: Web Crawler CLI Tool

**Branch**: `002-python3-uv-n` | **Date**: 2025-10-10
**Feature**: Basic web scraping CLI with Typer and Firecrawl v2 API

## Task Summary

- **Total Tasks**: 47
- **User Story 1 (P1)**: 30 tasks (MVP - Basic Web Page Crawling)
- **User Story 2 (P2)**: 6 tasks (Multiple Format Support)
- **User Story 3 (P3)**: 5 tasks (Batch Crawling)
- **User Story 4 (P3)**: 2 tasks (Custom Filenames)
- **Setup/Foundational**: 4 tasks
- **Polish/Cross-cutting**: 0 tasks (covered in US1)

**MVP Scope**: User Story 1 (Tasks T001-T034) - Delivers core single-page scraping with markdown/HTML output

**Estimated Implementation Time**:
- Setup: 1 hour
- US1 (P1): 8-12 hours
- US2 (P2): 2-3 hours
- US3 (P3): 3-4 hours
- US4 (P3): 1 hour

---

## Implementation Strategy

### TDD Workflow (Constitutional Requirement)

**Every task follows the Red-Green-Refactor cycle**:

1. **RED**: Write test first, verify it fails
2. **GREEN**: Implement minimal code to pass the test
3. **REFACTOR**: Improve code while keeping tests green
4. **COMMIT**: Commit after complete cycle

### Incremental Delivery

- **Phase 1-2**: Setup and foundational infrastructure
- **Phase 3**: User Story 1 (P1) - Deliverable MVP
  - Checkpoint after tests pass
  - Independent test: `crawler scrape --url https://example.com --output test.md`
- **Phase 4**: User Story 2 (P2) - Format extensions
  - Checkpoint after JSON/TEXT formats work
- **Phase 5**: User Story 3 (P3) - Batch processing
  - Checkpoint after batch scraping 10 URLs
- **Phase 6**: User Story 4 (P3) - Custom filenames
  - Final checkpoint

### Parallel Execution Opportunities

Tasks marked with **[P]** can be executed in parallel with other [P] tasks in the same phase, as they work on different files with no dependencies.

---

## Phase 1: Project Setup

**Goal**: Initialize project structure, dependencies, and configuration

### T001: Initialize pyproject.toml and project metadata
**File**: `pyproject.toml`
**Type**: Setup
**Description**: Create pyproject.toml with project metadata, Python version requirement (3.10+), and prepare dependency sections.

**Acceptance Criteria**:
- pyproject.toml exists with correct project name, version, description
- Python version constrained to >=3.10
- Build system configured for UV
- Entry point defined: `crawler = src.cli.main:app`

**Implementation Steps**:
```toml
[project]
name = "web-crawler-cli"
version = "0.1.0"
description = "CLI tool for web scraping using Firecrawl"
requires-python = ">=3.10"
dependencies = []  # Will add in T002

[project.scripts]
crawler = "src.cli.main:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

---

### T002: Add production dependencies to pyproject.toml
**File**: `pyproject.toml`
**Type**: Setup
**Description**: Add all production dependencies: typer, firecrawl-py, python-dotenv, pydantic, pydantic-settings.

**Acceptance Criteria**:
- All production dependencies listed with version constraints
- Dependencies align with research.md findings

**Implementation Steps**:
```toml
dependencies = [
    "typer>=0.9.0",
    "firecrawl-py>=0.0.16",
    "python-dotenv>=1.0.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
]
```

---

### T003: Add development and test dependencies to pyproject.toml [P]
**File**: `pyproject.toml`
**Type**: Setup
**Description**: Add dev dependencies: pytest, pytest-cov, pytest-mock, ruff, mypy, bandit.

**Acceptance Criteria**:
- All dev dependencies listed in optional dependency group
- Tool configurations prepared for ruff, mypy, pytest

**Implementation Steps**:
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.11.0",
    "ruff>=0.1.0",
    "mypy>=1.5.0",
    "bandit>=1.7.5",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--cov=src --cov-report=html --cov-report=term-missing"

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]

[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
warn_unused_configs = true
```

---

### T004: Create .env.example and .gitignore [P]
**Files**: `.env.example`, `.gitignore`
**Type**: Setup
**Description**: Create example environment file and gitignore patterns.

**Acceptance Criteria**:
- .env.example contains FIRECRAWL_API_URL and FIRECRAWL_API_KEY templates
- .gitignore excludes .env, .venv/, __pycache__/, .pytest_cache/, htmlcov/, *.pyc

**Implementation Steps**:
```ini
# .env.example
FIRECRAWL_API_URL=http://localhost:3002
FIRECRAWL_API_KEY=
```

```
# .gitignore
.env
.venv/
__pycache__/
*.pyc
.pytest_cache/
htmlcov/
.coverage
uv.lock
*.egg-info/
dist/
build/
```

---

## Phase 2: Foundational Infrastructure

**Goal**: Create core directory structure and exception hierarchy needed by all user stories

### T005: Create source directory structure
**Files**: `src/models/__init__.py`, `src/services/__init__.py`, `src/cli/__init__.py`, `src/config/__init__.py`, `src/lib/__init__.py`
**Type**: Foundational
**Description**: Create all source directories with __init__.py files.

**Acceptance Criteria**:
- All directories exist: src/models, src/services, src/cli, src/config, src/lib
- Each contains empty __init__.py

**Implementation Steps**:
```bash
mkdir -p src/{models,services,cli,config,lib}
touch src/{models,services,cli,config,lib}/__init__.py
```

---

### T006: Create test directory structure [P]
**Files**: `tests/unit/__init__.py`, `tests/integration/__init__.py`, `tests/contract/__init__.py`
**Type**: Foundational
**Description**: Create test directories with __init__.py files.

**Acceptance Criteria**:
- All test directories exist: tests/unit, tests/integration, tests/contract
- Each contains empty __init__.py

**Implementation Steps**:
```bash
mkdir -p tests/{unit,integration,contract}
touch tests/{unit,integration,contract}/__init__.py
```

---

### T007 [TDD-RED]: Write tests for exception hierarchy
**File**: `tests/unit/test_exceptions.py`
**Type**: Test - Foundational
**Story**: Shared infrastructure
**Description**: Write unit tests for CrawlerError base class and all derived exceptions (ConfigurationError, ValidationError, FirecrawlApiError, RateLimitError, AuthenticationError, ServerError, OutputError).

**Acceptance Criteria**:
- Test CrawlerError initialization with message, code, details
- Test each subclass with correct exit code
- Test exception inheritance chain
- **Tests must FAIL** (exceptions don't exist yet)

**Test Cases**:
```python
def test_crawler_error_initialization():
    """Test CrawlerError with custom message and code."""
    error = CrawlerError("Test error", code=42, details={"key": "value"})
    assert error.message == "Test error"
    assert error.code == 42
    assert error.details == {"key": "value"}

def test_configuration_error():
    """Test ConfigurationError has code 2."""
    error = ConfigurationError("Missing config")
    assert error.code == 2
    assert "Missing config" in str(error)

def test_rate_limit_error():
    """Test RateLimitError has code 3."""
    error = RateLimitError()
    assert error.code == 3
    assert "Rate limit" in error.message
```

---

### T008 [TDD-GREEN]: Implement exception hierarchy
**File**: `src/lib/exceptions.py`
**Type**: Implementation - Foundational
**Story**: Shared infrastructure
**Description**: Implement CrawlerError base exception and all derived exception classes as defined in data-model.md section 6.

**Acceptance Criteria**:
- CrawlerError base class with message, code (default 1), details
- ConfigurationError (code 2)
- ValidationError (code 1)
- FirecrawlApiError (code 1) with subclasses:
  - RateLimitError (code 3)
  - AuthenticationError (code 1)
  - ServerError (code 1)
- OutputError (code 1)
- All tests from T007 pass
- Type hints on all methods

**Implementation Outline**:
```python
class CrawlerError(Exception):
    """Base exception for all crawler errors."""
    def __init__(self, message: str, code: int = 1, details: dict | None = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)

class ConfigurationError(CrawlerError):
    """Configuration missing or invalid."""
    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message, code=2, details=details)

# ... implement other exceptions
```

---

## Phase 3: User Story 1 (P1) - Basic Web Page Crawling

**Story Goal**: As a developer, I want to crawl a single web page and save its content in a specific format to a specified location.

**Independent Test**:
```bash
crawler scrape --url https://example.com --markdown --output ./test.md
# Verify: test.md exists with markdown content
```

**Acceptance Scenarios**:
1. Valid URL + markdown + output path → file created with markdown content
2. Valid URL + HTML format → content saved as HTML
3. Invalid URL → error message displayed
4. Non-existent output directory → directories created automatically

---

### T009 [TDD-RED]: Write tests for OutputFormat enum [US1]
**File**: `tests/unit/test_models.py`
**Type**: Test
**Story**: US1
**Description**: Write tests for OutputFormat enum with MARKDOWN and HTML values.

**Acceptance Criteria**:
- Test OutputFormat.MARKDOWN value is "markdown"
- Test OutputFormat.HTML value is "html"
- Test enum membership
- **Tests must FAIL** (enum doesn't exist yet)

**Test Cases**:
```python
def test_output_format_enum_values():
    """Test OutputFormat enum has correct values."""
    assert OutputFormat.MARKDOWN.value == "markdown"
    assert OutputFormat.HTML.value == "html"

def test_output_format_membership():
    """Test OutputFormat enum membership."""
    assert "markdown" in [f.value for f in OutputFormat]
    assert "html" in [f.value for f in OutputFormat]
```

---

### T010 [TDD-GREEN]: Implement OutputFormat enum [US1]
**File**: `src/models/scrape.py`
**Type**: Implementation
**Story**: US1
**Description**: Create OutputFormat enum with MARKDOWN and HTML values as specified in data-model.md section 2.

**Acceptance Criteria**:
- Enum inherits from str and Enum
- MARKDOWN = "markdown"
- HTML = "html"
- All tests from T009 pass
- Docstring documenting the enum

**Implementation**:
```python
"""Data models for scrape operations."""
from enum import Enum

class OutputFormat(str, Enum):
    """Supported output formats for scraped content."""
    MARKDOWN = "markdown"
    HTML = "html"
```

---

### T011 [TDD-RED]: Write tests for ScrapeMetadata model [US1] [P]
**File**: `tests/unit/test_models.py`
**Type**: Test
**Story**: US1
**Description**: Write tests for ScrapeMetadata Pydantic model with all fields and validation.

**Acceptance Criteria**:
- Test valid metadata creation with all fields
- Test optional fields (title, description, keywords) default to None
- Test required fields (source_url, scraped_at)
- Test datetime parsing
- **Tests must FAIL**

**Test Cases**:
```python
from datetime import datetime

def test_scrape_metadata_valid():
    """Test creating valid ScrapeMetadata."""
    metadata = ScrapeMetadata(
        title="Test Page",
        description="Test description",
        keywords="test, page",
        source_url="https://example.com",
        scraped_at=datetime.now()
    )
    assert metadata.title == "Test Page"
    assert metadata.source_url == "https://example.com"

def test_scrape_metadata_optional_fields():
    """Test ScrapeMetadata with only required fields."""
    metadata = ScrapeMetadata(
        source_url="https://example.com",
        scraped_at=datetime.now()
    )
    assert metadata.title is None
    assert metadata.description is None
```

---

### T012 [TDD-GREEN]: Implement ScrapeMetadata model [US1] [P]
**File**: `src/models/scrape.py`
**Type**: Implementation
**Story**: US1
**Description**: Create ScrapeMetadata Pydantic model as specified in data-model.md section 3.

**Acceptance Criteria**:
- All fields defined with correct types
- Optional fields have None defaults
- Google-style docstring
- All tests from T011 pass

**Implementation Outline**:
```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ScrapeMetadata(BaseModel):
    """Metadata about a scraped web page."""
    title: Optional[str] = None
    description: Optional[str] = None
    keywords: Optional[str] = None
    source_url: str
    scraped_at: datetime
```

---

### T013 [TDD-RED]: Write tests for ScrapeRequest model [US1] [P]
**File**: `tests/unit/test_models.py`
**Type**: Test
**Story**: US1
**Description**: Write tests for ScrapeRequest model including URL validation, format defaults, and output_path validation.

**Acceptance Criteria**:
- Test valid HTTP/HTTPS URLs accepted
- Test invalid URLs rejected (no protocol, invalid format)
- Test format defaults to MARKDOWN
- Test output_path optional
- **Tests must FAIL**

**Test Cases**:
```python
def test_scrape_request_valid():
    """Test creating valid ScrapeRequest."""
    request = ScrapeRequest(
        url="https://example.com",
        format=OutputFormat.MARKDOWN,
        output_path="/path/to/file.md"
    )
    assert str(request.url) == "https://example.com/"
    assert request.format == OutputFormat.MARKDOWN

def test_scrape_request_invalid_url():
    """Test ScrapeRequest rejects invalid URL."""
    with pytest.raises(ValidationError):
        ScrapeRequest(url="not-a-url")

def test_scrape_request_defaults():
    """Test ScrapeRequest defaults."""
    request = ScrapeRequest(url="https://example.com")
    assert request.format == OutputFormat.MARKDOWN
    assert request.output_path is None
```

---

### T014 [TDD-GREEN]: Implement ScrapeRequest model [US1] [P]
**File**: `src/models/scrape.py`
**Type**: Implementation
**Story**: US1
**Description**: Create ScrapeRequest Pydantic model with HttpUrl validation as specified in data-model.md section 2.

**Acceptance Criteria**:
- url field uses HttpUrl type for validation
- format defaults to OutputFormat.MARKDOWN
- output_path is Optional[str]
- Google-style docstring
- All tests from T013 pass

**Implementation Outline**:
```python
from pydantic import BaseModel, HttpUrl
from typing import Optional

class ScrapeRequest(BaseModel):
    """Request parameters for scraping a web page."""
    url: HttpUrl
    format: OutputFormat = OutputFormat.MARKDOWN
    output_path: Optional[str] = None
```

---

### T015 [TDD-RED]: Write tests for ScrapeResponse model [US1] [P]
**File**: `tests/unit/test_models.py`
**Type**: Implementation
**Story**: US1
**Description**: Write tests for ScrapeResponse model including success/error validation.

**Acceptance Criteria**:
- Test successful response with content
- Test failed response with error_message
- Test validation: error_message required when success=False
- **Tests must FAIL**

**Test Cases**:
```python
def test_scrape_response_success():
    """Test successful ScrapeResponse."""
    metadata = ScrapeMetadata(source_url="https://example.com", scraped_at=datetime.now())
    response = ScrapeResponse(
        content="# Test Content",
        format=OutputFormat.MARKDOWN,
        metadata=metadata,
        success=True
    )
    assert response.success
    assert response.error_message is None

def test_scrape_response_failure():
    """Test failed ScrapeResponse requires error_message."""
    metadata = ScrapeMetadata(source_url="https://example.com", scraped_at=datetime.now())
    with pytest.raises(ValidationError):
        ScrapeResponse(
            content="",
            format=OutputFormat.MARKDOWN,
            metadata=metadata,
            success=False
            # Missing error_message - should fail validation
        )
```

---

### T016 [TDD-GREEN]: Implement ScrapeResponse model [US1] [P]
**File**: `src/models/scrape.py`
**Type**: Implementation
**Story**: US1
**Description**: Create ScrapeResponse Pydantic model with validation as specified in data-model.md section 3.

**Acceptance Criteria**:
- All fields defined with correct types
- field_validator for error_message
- Google-style docstring
- All tests from T015 pass

**Implementation Outline**:
```python
from pydantic import BaseModel, field_validator
from typing import Optional

class ScrapeResponse(BaseModel):
    """Response from a web scraping operation."""
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

### T017 [TDD-RED]: Write tests for Settings configuration [US1]
**File**: `tests/unit/test_config.py`
**Type**: Test
**Story**: US1
**Description**: Write tests for Settings Pydantic model loading from environment variables.

**Acceptance Criteria**:
- Test Settings loads from environment variables
- Test firecrawl_api_url is required
- Test firecrawl_api_key defaults to empty string
- Test URL validation for firecrawl_api_url
- **Tests must FAIL**

**Test Cases**:
```python
import os
from src.config.settings import Settings

def test_settings_from_env(monkeypatch):
    """Test Settings loads from environment."""
    monkeypatch.setenv("FIRECRAWL_API_URL", "http://localhost:3002")
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-key")

    settings = Settings()
    assert settings.firecrawl_api_url == "http://localhost:3002"
    assert settings.firecrawl_api_key == "test-key"

def test_settings_missing_required():
    """Test Settings raises error if FIRECRAWL_API_URL missing."""
    with pytest.raises(ValidationError):
        Settings()
```

---

### T018 [TDD-GREEN]: Implement Settings configuration [US1]
**File**: `src/config/settings.py`
**Type**: Implementation
**Story**: US1
**Description**: Create Settings class using Pydantic BaseSettings as specified in data-model.md section 1.

**Acceptance Criteria**:
- Inherits from BaseSettings
- firecrawl_api_url: str (required)
- firecrawl_api_key: str = "" (optional)
- model_config for .env file loading
- Google-style docstring
- All tests from T017 pass

**Implementation**:
```python
"""Configuration management using environment variables."""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Attributes:
        firecrawl_api_url: Base URL of self-hosted Firecrawl API instance
        firecrawl_api_key: Optional API key for authentication
    """
    firecrawl_api_url: str
    firecrawl_api_key: str = ""

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False
    }
```

---

### T019 [TDD-RED]: Write tests for URL validator [US1]
**File**: `tests/unit/test_validators.py`
**Type**: Test
**Story**: US1
**Description**: Write tests for URL validation function.

**Acceptance Criteria**:
- Test valid HTTP/HTTPS URLs pass
- Test URLs without protocol fail
- Test invalid URL formats fail
- Test localhost URLs pass
- **Tests must FAIL**

**Test Cases**:
```python
def test_validate_url_valid():
    """Test validate_url accepts valid URLs."""
    assert validate_url("https://example.com")
    assert validate_url("http://localhost:3000")
    assert validate_url("https://sub.domain.com/path?query=1")

def test_validate_url_invalid():
    """Test validate_url rejects invalid URLs."""
    with pytest.raises(ValidationError):
        validate_url("not-a-url")
    with pytest.raises(ValidationError):
        validate_url("example.com")  # Missing protocol
```

---

### T020 [TDD-GREEN]: Implement URL validator [US1]
**File**: `src/lib/validators.py`
**Type**: Implementation
**Story**: US1
**Description**: Implement validate_url function using urllib.parse.

**Acceptance Criteria**:
- Function accepts URL string
- Returns bool or raises ValidationError
- Validates protocol (http/https)
- Google-style docstring
- All tests from T019 pass

**Implementation Outline**:
```python
"""Input validation utilities."""
from urllib.parse import urlparse
from src.lib.exceptions import ValidationError

def validate_url(url: str) -> bool:
    """Validate URL has proper format and protocol.

    Args:
        url: URL string to validate

    Returns:
        True if valid

    Raises:
        ValidationError: If URL is invalid or missing http/https protocol
    """
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            raise ValidationError(f"URL must use http:// or https:// protocol: {url}")
        if not parsed.netloc:
            raise ValidationError(f"Invalid URL format: {url}")
        return True
    except Exception as e:
        raise ValidationError(f"Invalid URL: {url}") from e
```

---

### T021 [TDD-RED]: Write tests for path validator [US1] [P]
**File**: `tests/unit/test_validators.py`
**Type**: Test
**Story**: US1
**Description**: Write tests for output path validation function.

**Acceptance Criteria**:
- Test valid file paths pass
- Test directory paths fail (must be file)
- Test path with non-existent parent directories passes (will be created)
- **Tests must FAIL**

**Test Cases**:
```python
def test_validate_output_path_valid():
    """Test validate_output_path accepts valid file paths."""
    assert validate_output_path("/path/to/file.md")
    assert validate_output_path("./relative/path/file.html")

def test_validate_output_path_directory():
    """Test validate_output_path rejects directory paths."""
    with pytest.raises(ValidationError):
        validate_output_path("/path/to/directory/")
```

---

### T022 [TDD-GREEN]: Implement path validator [US1] [P]
**File**: `src/lib/validators.py`
**Type**: Implementation
**Story**: US1
**Description**: Implement validate_output_path function.

**Acceptance Criteria**:
- Function accepts path string
- Validates path is not a directory
- Returns bool or raises ValidationError
- Google-style docstring
- All tests from T021 pass

**Implementation Outline**:
```python
from pathlib import Path

def validate_output_path(path: str) -> bool:
    """Validate output path is a file path, not a directory.

    Args:
        path: File path to validate

    Returns:
        True if valid

    Raises:
        ValidationError: If path is a directory or invalid
    """
    if path.endswith(("/", "\\")):
        raise ValidationError(f"Output path must be a file, not a directory: {path}")
    return True
```

---

### T023 [TDD-RED]: Write tests for FirecrawlService [US1]
**File**: `tests/unit/test_firecrawl.py`
**Type**: Test
**Story**: US1
**Description**: Write tests for FirecrawlService.scrape() method with mocked Firecrawl client.

**Acceptance Criteria**:
- Test successful scrape with markdown format
- Test successful scrape with HTML format
- Test API error handling (rate limit, server error)
- Test connection error handling
- Mock firecrawl-py client
- **Tests must FAIL**

**Test Cases**:
```python
from unittest.mock import Mock, patch
from src.services.firecrawl import FirecrawlService

def test_firecrawl_service_scrape_markdown(mocker):
    """Test FirecrawlService.scrape returns markdown content."""
    # Mock Firecrawl client
    mock_client = mocker.Mock()
    mock_client.scrape.return_value = {
        "markdown": "# Test Content",
        "html": "<h1>Test Content</h1>",
        "metadata": {
            "title": "Test Page",
            "sourceURL": "https://example.com"
        }
    }

    with patch('src.services.firecrawl.Firecrawl', return_value=mock_client):
        service = FirecrawlService(settings)
        response = service.scrape(request)

        assert response.success
        assert response.content == "# Test Content"
        assert response.format == OutputFormat.MARKDOWN

def test_firecrawl_service_rate_limit(mocker):
    """Test FirecrawlService handles rate limit errors."""
    mock_client = mocker.Mock()
    mock_client.scrape.side_effect = Exception("429: Rate limit exceeded")

    with patch('src.services.firecrawl.Firecrawl', return_value=mock_client):
        service = FirecrawlService(settings)
        with pytest.raises(RateLimitError):
            service.scrape(request)
```

---

### T024 [TDD-GREEN]: Implement FirecrawlService [US1]
**File**: `src/services/firecrawl.py`
**Type**: Implementation
**Story**: US1
**Description**: Create FirecrawlService class that wraps firecrawl-py client as specified in data-model.md section 4.

**Acceptance Criteria**:
- Initialize Firecrawl client with settings
- scrape() method accepts ScrapeRequest, returns ScrapeResponse
- Transforms Firecrawl API response to ScrapeResponse
- Handles errors and raises appropriate exceptions
- Google-style docstrings
- All tests from T023 pass

**Implementation Outline**:
```python
"""Firecrawl API integration service."""
from datetime import datetime
from firecrawl import Firecrawl
from src.models.scrape import ScrapeRequest, ScrapeResponse, ScrapeMetadata, OutputFormat
from src.config.settings import Settings
from src.lib.exceptions import RateLimitError, FirecrawlApiError

class FirecrawlService:
    """Service for interacting with Firecrawl API."""

    def __init__(self, settings: Settings):
        """Initialize Firecrawl client.

        Args:
            settings: Application settings with API URL and key
        """
        self.client = Firecrawl(
            api_key=settings.firecrawl_api_key,
            api_url=settings.firecrawl_api_url
        )

    def scrape(self, request: ScrapeRequest) -> ScrapeResponse:
        """Scrape a web page and return content.

        Args:
            request: Scrape request with URL and format

        Returns:
            ScrapeResponse with content and metadata

        Raises:
            RateLimitError: If API rate limit exceeded
            FirecrawlApiError: If API returns error
        """
        try:
            result = self.client.scrape(
                str(request.url),
                formats=['markdown', 'html']
            )

            # Select content based on requested format
            content = result.get('markdown', '') if request.format == OutputFormat.MARKDOWN else result.get('html', '')

            # Build metadata
            metadata = ScrapeMetadata(
                title=result.get('metadata', {}).get('title'),
                description=result.get('metadata', {}).get('description'),
                keywords=result.get('metadata', {}).get('keywords'),
                source_url=result.get('metadata', {}).get('sourceURL', str(request.url)),
                scraped_at=datetime.now()
            )

            return ScrapeResponse(
                content=content,
                format=request.format,
                metadata=metadata,
                success=True
            )
        except Exception as e:
            if "429" in str(e) or "rate limit" in str(e).lower():
                raise RateLimitError("Firecrawl API rate limit exceeded") from e
            raise FirecrawlApiError(f"Failed to scrape URL: {e}") from e
```

---

### T025 [TDD-RED]: Write tests for OutputService [US1]
**File**: `tests/unit/test_output.py`
**Type**: Test
**Story**: US1
**Description**: Write tests for OutputService write_to_file() and print_to_console() methods.

**Acceptance Criteria**:
- Test write_to_file creates file with content
- Test write_to_file creates parent directories
- Test print_to_console outputs to stdout
- Mock file system operations
- **Tests must FAIL**

**Test Cases**:
```python
from src.services.output import OutputService
from pathlib import Path

def test_output_service_write_to_file(tmp_path):
    """Test OutputService.write_to_file creates file."""
    service = OutputService()
    file_path = tmp_path / "test.md"
    response = ScrapeResponse(...)  # Create test response

    service.write_to_file(response, str(file_path))

    assert file_path.exists()
    assert file_path.read_text() == response.content

def test_output_service_creates_directories(tmp_path):
    """Test OutputService creates parent directories."""
    service = OutputService()
    file_path = tmp_path / "nested" / "path" / "test.md"
    response = ScrapeResponse(...)

    service.write_to_file(response, str(file_path))

    assert file_path.exists()
    assert file_path.parent.exists()
```

---

### T026 [TDD-GREEN]: Implement OutputService [US1]
**File**: `src/services/output.py`
**Type**: Implementation
**Story**: US1
**Description**: Create OutputService class for writing output to files or console.

**Acceptance Criteria**:
- write_to_file() creates parent directories if needed
- write_to_file() writes content to file
- print_to_console() outputs to stdout
- Google-style docstrings
- All tests from T025 pass

**Implementation Outline**:
```python
"""Output handling service for saving or displaying scraped content."""
from pathlib import Path
import sys
from src.models.scrape import ScrapeResponse
from src.lib.exceptions import OutputError

class OutputService:
    """Service for writing scraped content to files or console."""

    def write_to_file(self, response: ScrapeResponse, file_path: str) -> None:
        """Write scraped content to file.

        Args:
            response: Scrape response with content
            file_path: Path where content will be saved

        Raises:
            OutputError: If file cannot be written
        """
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(response.content, encoding='utf-8')
        except Exception as e:
            raise OutputError(f"Failed to write output file: {e}") from e

    def print_to_console(self, response: ScrapeResponse) -> None:
        """Print scraped content to stdout.

        Args:
            response: Scrape response with content
        """
        print(response.content)
```

---

### T027 [TDD-RED]: Write integration test for Firecrawl API contract [US1]
**File**: `tests/contract/test_firecrawl_api.py`
**Type**: Contract Test
**Story**: US1
**Description**: Write contract test that validates Firecrawl API /scrape endpoint matches our OpenAPI specification.

**Acceptance Criteria**:
- Test connects to real or mock Firecrawl instance
- Test validates response structure matches contract
- Test validates markdown and html fields present
- Test validates metadata structure
- Marked with pytest.mark.contract decorator
- **Tests must FAIL** (or be skipped if no Firecrawl available)

**Test Cases**:
```python
import pytest
from firecrawl import Firecrawl

@pytest.mark.contract
def test_firecrawl_scrape_endpoint_contract():
    """Test Firecrawl API /scrape endpoint matches contract."""
    # Skip if FIRECRAWL_API_URL not set (CI environment)
    settings = Settings()
    client = Firecrawl(
        api_key=settings.firecrawl_api_key,
        api_url=settings.firecrawl_api_url
    )

    result = client.scrape("https://example.com", formats=["markdown", "html"])

    # Validate response structure per OpenAPI contract
    assert "markdown" in result
    assert "html" in result
    assert "metadata" in result
    assert isinstance(result["metadata"], dict)
    assert "sourceURL" in result["metadata"]

@pytest.mark.contract
def test_firecrawl_error_responses():
    """Test Firecrawl API error response structure."""
    # Test with invalid URL should return error
    # Validate error structure matches contract
    pass
```

---

### T028 [TDD-GREEN]: Verify Firecrawl API contract [US1]
**Type**: Verification
**Story**: US1
**Description**: Run contract tests against Firecrawl instance. If failures occur, investigate and fix FirecrawlService implementation.

**Acceptance Criteria**:
- Contract tests pass when Firecrawl is available
- Contract tests are properly skipped in CI if no Firecrawl
- pytest.ini configured with contract marker

**Implementation Steps**:
1. Run `pytest tests/contract/ -v`
2. Verify all contract assumptions are correct
3. Update FirecrawlService if contract violations found
4. Add to pytest.ini:
```ini
[tool.pytest.ini_options]
markers = [
    "contract: Contract tests for external APIs (skipped if service unavailable)",
]
```

---

### T029 [TDD-RED]: Write CLI scrape command tests [US1]
**File**: `tests/integration/test_scrape_command.py`
**Type**: Integration Test
**Story**: US1
**Description**: Write end-to-end tests for CLI scrape command using Typer CliRunner.

**Acceptance Criteria**:
- Test `crawler scrape --url <URL> --output file.md` creates file
- Test `crawler scrape --url <URL>` outputs to stdout
- Test `crawler scrape --url <URL> --html` uses HTML format
- Test invalid URL shows error
- Test missing config shows error
- Mock Firecrawl API calls
- **Tests must FAIL** (CLI command doesn't exist)

**Test Cases**:
```python
from typer.testing import CliRunner
from src.cli.main import app

runner = CliRunner()

def test_scrape_command_to_file(tmp_path, mocker):
    """Test scrape command saves to file."""
    output_file = tmp_path / "test.md"

    # Mock FirecrawlService
    mock_scrape = mocker.patch('src.services.firecrawl.FirecrawlService.scrape')
    mock_scrape.return_value = ScrapeResponse(...)

    result = runner.invoke(app, [
        "scrape",
        "--url", "https://example.com",
        "--output", str(output_file)
    ])

    assert result.exit_code == 0
    assert output_file.exists()

def test_scrape_command_to_stdout(mocker):
    """Test scrape command outputs to console."""
    mock_scrape = mocker.patch('src.services.firecrawl.FirecrawlService.scrape')
    mock_scrape.return_value = ScrapeResponse(content="# Test", ...)

    result = runner.invoke(app, [
        "scrape",
        "--url", "https://example.com"
    ])

    assert result.exit_code == 0
    assert "# Test" in result.stdout

def test_scrape_command_invalid_url():
    """Test scrape command with invalid URL."""
    result = runner.invoke(app, [
        "scrape",
        "--url", "not-a-url"
    ])

    assert result.exit_code == 1
    assert "Invalid URL" in result.stderr
```

---

### T030 [TDD-GREEN]: Implement CLI scrape command [US1]
**File**: `src/cli/scrape.py`
**Type**: Implementation
**Story**: US1
**Description**: Implement Typer CLI command for scrape operation following contracts/cli-interface.md specification.

**Acceptance Criteria**:
- Command: `scrape`
- Options: --url (required), --markdown (default), --html, --output (optional)
- Loads Settings, initializes services
- Calls FirecrawlService.scrape()
- Calls OutputService.write_to_file() or print_to_console()
- Handles exceptions and exits with appropriate codes
- All tests from T029 pass

**Implementation Outline**:
```python
"""Typer CLI command for scraping web pages."""
import typer
from typing import Optional
from src.config.settings import Settings
from src.models.scrape import ScrapeRequest, OutputFormat
from src.services.firecrawl import FirecrawlService
from src.services.output import OutputService
from src.lib.validators import validate_url, validate_output_path
from src.lib.exceptions import CrawlerError, ConfigurationError, ValidationError

app = typer.Typer()

@app.command()
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

        # Validate output path if provided
        if output:
            validate_output_path(output)

        # Load settings
        try:
            settings = Settings()
        except Exception as e:
            typer.secho(f"Error: Missing required configuration: {e}", fg=typer.colors.RED, err=True)
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
```

---

### T031 [TDD-GREEN]: Create CLI main entry point [US1]
**File**: `src/cli/main.py`
**Type**: Implementation
**Story**: US1
**Description**: Create main Typer app entry point that includes scrape command.

**Acceptance Criteria**:
- Creates Typer() app instance
- Includes scrape command from src.cli.scrape
- Configured as entry point in pyproject.toml

**Implementation**:
```python
"""Main CLI application entry point."""
import typer
from src.cli.scrape import scrape

app = typer.Typer(
    name="crawler",
    help="Web Crawler CLI Tool - Scrape web pages using Firecrawl"
)

# Register commands
app.command()(scrape)

if __name__ == "__main__":
    app()
```

---

### T032 [TDD-RED]: Write integration test for file I/O [US1]
**File**: `tests/integration/test_file_output.py`
**Type**: Integration Test
**Story**: US1
**Description**: Write integration tests for OutputService file operations with real file system.

**Acceptance Criteria**:
- Test writing to file with parent directory creation
- Test file content matches ScrapeResponse content
- Test file encoding (UTF-8)
- Test permission errors handled
- **Tests must FAIL**

**Test Cases**:
```python
def test_output_service_creates_nested_directories(tmp_path):
    """Test OutputService creates nested parent directories."""
    service = OutputService()
    file_path = tmp_path / "level1" / "level2" / "level3" / "test.md"
    response = ScrapeResponse(
        content="# Test Content\n\nThis is a test.",
        format=OutputFormat.MARKDOWN,
        metadata=ScrapeMetadata(source_url="https://example.com", scraped_at=datetime.now()),
        success=True
    )

    service.write_to_file(response, str(file_path))

    assert file_path.exists()
    assert file_path.parent.exists()
    content = file_path.read_text(encoding='utf-8')
    assert content == "# Test Content\n\nThis is a test."
```

---

### T033 [TDD-GREEN]: Verify file I/O integration [US1]
**Type**: Verification
**Story**: US1
**Description**: Run integration tests for file I/O and verify they pass.

**Acceptance Criteria**:
- All tests in test_file_output.py pass
- File encoding verified as UTF-8
- Parent directory creation works

**Implementation Steps**:
1. Run `pytest tests/integration/test_file_output.py -v`
2. Verify all tests pass
3. Fix any issues in OutputService if tests fail

---

### T034 [US1-CHECKPOINT]: Manual acceptance test for User Story 1
**Type**: Manual Test
**Story**: US1
**Description**: Perform manual end-to-end test of User Story 1 acceptance scenarios.

**Acceptance Criteria**:
- Install package: `uv pip install -e .`
- Create .env file with FIRECRAWL_API_URL
- Run: `crawler scrape --url https://example.com --output test.md`
- Verify: test.md created with markdown content
- Run: `crawler scrape --url https://example.com --html --output test.html`
- Verify: test.html created with HTML content
- Run: `crawler scrape --url invalid-url`
- Verify: Error message displayed, exit code 1
- Run: `crawler scrape --url https://example.com --output ./nested/path/test.md`
- Verify: nested/path/ directories created, test.md exists

**Test Script**:
```bash
# Setup
uv venv
source .venv/bin/activate  # or .venv\Scripts\Activate.ps1 on Windows
uv pip install -e .
cp .env.example .env
# Edit .env to set FIRECRAWL_API_URL

# Test Scenario 1: Markdown to file
crawler scrape --url https://example.com --output test.md
test -f test.md && echo "✓ test.md created"

# Test Scenario 2: HTML to file
crawler scrape --url https://example.com --html --output test.html
test -f test.html && echo "✓ test.html created"

# Test Scenario 3: Invalid URL
crawler scrape --url not-a-url || echo "✓ Error displayed correctly"

# Test Scenario 4: Nested directories
crawler scrape --url https://example.com --output ./data/nested/test.md
test -f ./data/nested/test.md && echo "✓ Nested directories created"

echo "✅ User Story 1 (P1) - Basic Web Page Crawling COMPLETE"
```

---

## Phase 4: User Story 2 (P2) - Multiple Format Support

**Story Goal**: As a content manager, I want to save crawled web content in different formats (markdown, HTML, JSON, plain text).

**Note**: Markdown and HTML already implemented in US1. This phase adds JSON and TEXT formats.

**Independent Test**:
```bash
crawler scrape --url https://example.com --json --output test.json
# Verify: test.json contains {"title": "...", "content": "...", "metadata": {...}}

crawler scrape --url https://example.com --text --output test.txt
# Verify: test.txt contains plain text without HTML/markdown formatting
```

---

### T035 [TDD-RED]: Write tests for JSON and TEXT formats [US2]
**File**: `tests/unit/test_models.py`
**Type**: Test
**Story**: US2
**Description**: Add tests for OutputFormat.JSON and OutputFormat.TEXT enum values.

**Acceptance Criteria**:
- Test OutputFormat.JSON value is "json"
- Test OutputFormat.TEXT value is "text"
- **Tests must FAIL**

**Test Cases**:
```python
def test_output_format_json_text():
    """Test OutputFormat includes JSON and TEXT."""
    assert OutputFormat.JSON.value == "json"
    assert OutputFormat.TEXT.value == "text"
```

---

### T036 [TDD-GREEN]: Add JSON and TEXT to OutputFormat enum [US2]
**File**: `src/models/scrape.py`
**Type**: Implementation
**Story**: US2
**Description**: Extend OutputFormat enum with JSON and TEXT values.

**Acceptance Criteria**:
- JSON = "json"
- TEXT = "text"
- All tests from T035 pass
- Docstring updated

**Implementation**:
```python
class OutputFormat(str, Enum):
    """Supported output formats for scraped content."""
    MARKDOWN = "markdown"
    HTML = "html"
    JSON = "json"      # P2: JSON format with structured data
    TEXT = "text"      # P2: Plain text format
```

---

### T037 [TDD-RED]: Write tests for JSON/TEXT scraping [US2]
**File**: `tests/unit/test_firecrawl.py`
**Type**: Test
**Story**: US2
**Description**: Add tests for FirecrawlService handling JSON and TEXT format requests.

**Acceptance Criteria**:
- Test JSON format returns structured JSON string
- Test TEXT format returns plain text (stripped HTML)
- Mock Firecrawl API responses
- **Tests must FAIL**

**Test Cases**:
```python
def test_firecrawl_service_scrape_json(mocker):
    """Test FirecrawlService.scrape with JSON format."""
    mock_client = mocker.Mock()
    mock_client.scrape.return_value = {
        "markdown": "# Test",
        "html": "<h1>Test</h1>",
        "metadata": {"title": "Test", "sourceURL": "https://example.com"}
    }

    request = ScrapeRequest(url="https://example.com", format=OutputFormat.JSON)
    service = FirecrawlService(settings)
    response = service.scrape(request)

    assert response.format == OutputFormat.JSON
    import json
    data = json.loads(response.content)
    assert "title" in data
    assert "content" in data
    assert "metadata" in data
```

---

### T038 [TDD-GREEN]: Implement JSON/TEXT format handling [US2]
**File**: `src/services/firecrawl.py`
**Type**: Implementation
**Story**: US2
**Description**: Extend FirecrawlService.scrape() to handle JSON and TEXT formats.

**Acceptance Criteria**:
- JSON format: returns JSON string with {"title", "content", "metadata"}
- TEXT format: strips HTML tags from content, returns plain text
- All tests from T037 pass

**Implementation**:
```python
import json
import re

def scrape(self, request: ScrapeRequest) -> ScrapeResponse:
    """Scrape a web page and return content in requested format."""
    try:
        result = self.client.scrape(str(request.url), formats=['markdown', 'html'])

        # Select content based on format
        if request.format == OutputFormat.MARKDOWN:
            content = result.get('markdown', '')
        elif request.format == OutputFormat.HTML:
            content = result.get('html', '')
        elif request.format == OutputFormat.JSON:
            # Return structured JSON
            content = json.dumps({
                "title": result.get('metadata', {}).get('title'),
                "content": result.get('markdown', ''),
                "metadata": result.get('metadata', {})
            }, indent=2)
        elif request.format == OutputFormat.TEXT:
            # Strip HTML tags to get plain text
            html_content = result.get('html', '')
            content = re.sub(r'<[^>]+>', '', html_content)
            content = re.sub(r'\s+', ' ', content).strip()
        else:
            content = result.get('markdown', '')

        # ... rest of implementation
```

---

### T039 [TDD-RED]: Write CLI tests for --json and --text flags [US2]
**File**: `tests/integration/test_scrape_command.py`
**Type**: Integration Test
**Story**: US2
**Description**: Add tests for CLI --json and --text options.

**Acceptance Criteria**:
- Test `crawler scrape --url <URL> --json` uses JSON format
- Test `crawler scrape --url <URL> --text` uses TEXT format
- Test JSON output is valid JSON
- **Tests must FAIL**

**Test Cases**:
```python
def test_scrape_command_json_format(tmp_path, mocker):
    """Test scrape command with --json flag."""
    output_file = tmp_path / "test.json"
    mock_scrape = mocker.patch('src.services.firecrawl.FirecrawlService.scrape')
    mock_scrape.return_value = ScrapeResponse(
        content='{"title": "Test", "content": "..."}',
        format=OutputFormat.JSON,
        ...
    )

    result = runner.invoke(app, [
        "scrape",
        "--url", "https://example.com",
        "--json",
        "--output", str(output_file)
    ])

    assert result.exit_code == 0
    assert output_file.exists()
    # Verify JSON is valid
    import json
    data = json.loads(output_file.read_text())
    assert "title" in data
```

---

### T040 [TDD-GREEN]: Add --json and --text CLI options [US2]
**File**: `src/cli/scrape.py`
**Type**: Implementation
**Story**: US2
**Description**: Add --json and --text flags to scrape command.

**Acceptance Criteria**:
- New options: --json (bool), --text (bool)
- Format selection priority: --json > --text > --html > --markdown
- All tests from T039 pass
- Help text updated

**Implementation**:
```python
@app.command()
def scrape(
    url: str = typer.Option(..., help="URL to scrape"),
    markdown: bool = typer.Option(True, help="Output as markdown (default)"),
    html: bool = typer.Option(False, help="Output as HTML"),
    json_format: bool = typer.Option(False, "--json", help="Output as JSON"),
    text: bool = typer.Option(False, help="Output as plain text"),
    output: Optional[str] = typer.Option(None, help="Output file path")
):
    """Scrape a single web page using Firecrawl."""
    # Determine format (priority: json > text > html > markdown)
    if json_format:
        format_choice = OutputFormat.JSON
    elif text:
        format_choice = OutputFormat.TEXT
    elif html:
        format_choice = OutputFormat.HTML
    else:
        format_choice = OutputFormat.MARKDOWN

    # ... rest of implementation
```

---

### T041 [US2-CHECKPOINT]: Manual acceptance test for User Story 2
**Type**: Manual Test
**Story**: US2
**Description**: Verify JSON and TEXT formats work end-to-end.

**Test Script**:
```bash
# Test JSON format
crawler scrape --url https://example.com --json --output test.json
cat test.json | jq . && echo "✓ Valid JSON output"

# Test TEXT format
crawler scrape --url https://example.com --text --output test.txt
test -f test.txt && echo "✓ Plain text output created"

echo "✅ User Story 2 (P2) - Multiple Format Support COMPLETE"
```

---

## Phase 5: User Story 3 (P3) - Batch Crawling from URL List

**Story Goal**: As a researcher, I want to crawl multiple URLs from a list file.

**Independent Test**:
```bash
echo -e "https://example.com\nhttps://example.org" > urls.txt
crawler scrape --url-file urls.txt --output-dir ./data/
# Verify: ./data/ contains 2 files with scraped content
```

---

### T042 [TDD-RED]: Write tests for batch scraping [US3]
**File**: `tests/integration/test_scrape_command.py`
**Type**: Integration Test
**Story**: US3
**Description**: Add tests for CLI --url-file and --output-dir options.

**Acceptance Criteria**:
- Test batch scraping creates multiple files
- Test handles errors for individual URLs
- Test generates summary report
- **Tests must FAIL**

---

### T043 [TDD-GREEN]: Implement --url-file and --output-dir options [US3]
**File**: `src/cli/scrape.py`
**Type**: Implementation
**Story**: US3
**Description**: Add batch scraping functionality with --url-file option.

**Acceptance Criteria**:
- Reads URLs from file (one per line)
- Scrapes each URL
- Saves to output-dir with auto-generated filenames
- Continues on error, logs failures
- Displays summary report

---

### T044 [TDD-GREEN]: Add async batch scraping support [US3]
**File**: `src/services/firecrawl.py`
**Type**: Implementation
**Story**: US3
**Description**: Refactor to use AsyncFirecrawl for concurrent batch scraping (per SC-007: 50+ concurrent).

**Acceptance Criteria**:
- Supports async/await patterns
- Uses asyncio.gather() for concurrent scraping
- Max concurrency configurable (default 50)

---

### T045 [US3-CHECKPOINT]: Manual acceptance test for User Story 3
**Type**: Manual Test
**Story**: US3
**Description**: Verify batch scraping works with multiple URLs.

**Test Script**:
```bash
# Create URL list
cat > urls.txt <<EOF
https://example.com
https://example.org
https://example.net
EOF

# Batch scrape
crawler scrape --url-file urls.txt --output-dir ./batch_data/

# Verify
ls -l ./batch_data/ | grep -c ".md" | grep "3" && echo "✓ 3 files created"

echo "✅ User Story 3 (P3) - Batch Crawling COMPLETE"
```

---

## Phase 6: User Story 4 (P3) - Custom Output Filename

**Story Goal**: As a data analyst, I want to specify custom filenames for crawled content.

**Independent Test**:
```bash
crawler scrape --url https://example.com --filename my-custom-name --output ./data/
# Verify: ./data/my-custom-name.md exists
```

---

### T046 [TDD-RED+GREEN]: Add --filename option [US4]
**File**: `src/cli/scrape.py`
**Type**: Test + Implementation
**Story**: US4
**Description**: Add --filename option to scrape command.

**Acceptance Criteria**:
- New option: --filename (str, optional)
- Uses custom filename when provided
- Auto-generates filename if not provided (from page title or URL)
- Tests pass

---

### T047 [US4-CHECKPOINT]: Manual acceptance test for User Story 4
**Type**: Manual Test
**Story**: US4
**Description**: Verify custom filenames work.

**Test Script**:
```bash
crawler scrape --url https://example.com --filename my-page --output my-page.md
test -f my-page.md && echo "✓ Custom filename used"

echo "✅ User Story 4 (P3) - Custom Filename COMPLETE"
```

---

## Dependency Graph

```
Phase 1 (Setup)
├── T001: pyproject.toml metadata
├── T002: production dependencies
├── T003: dev dependencies [P]
└── T004: .env.example, .gitignore [P]
    │
    ▼
Phase 2 (Foundational)
├── T005: source directories
├── T006: test directories [P]
├── T007-T008: exception hierarchy (TDD)
    │
    ▼
Phase 3 (US1 - MVP)
├── T009-T010: OutputFormat enum (TDD)
├── T011-T012: ScrapeMetadata model (TDD) [P]
├── T013-T014: ScrapeRequest model (TDD) [P]
├── T015-T016: ScrapeResponse model (TDD) [P]
├── T017-T018: Settings config (TDD)
├── T019-T020: URL validator (TDD)
├── T021-T022: path validator (TDD) [P]
├── T023-T024: FirecrawlService (TDD)
├── T025-T026: OutputService (TDD) [P]
├── T027-T028: Firecrawl contract test
├── T029-T030: CLI scrape command (TDD)
├── T031: CLI main entry point
├── T032-T033: file I/O integration test
└── T034: US1 manual checkpoint ✓
    │
    ▼
Phase 4 (US2 - Format Extensions)
├── T035-T036: JSON/TEXT enum (TDD)
├── T037-T038: JSON/TEXT service logic (TDD)
├── T039-T040: CLI --json/--text options (TDD)
└── T041: US2 manual checkpoint ✓
    │
    ▼
Phase 5 (US3 - Batch Processing)
├── T042-T043: --url-file option (TDD)
├── T044: async batch scraping
└── T045: US3 manual checkpoint ✓
    │
    ▼
Phase 6 (US4 - Custom Filenames)
├── T046: --filename option (TDD)
└── T047: US4 manual checkpoint ✓
```

---

## Parallel Execution Examples

### Phase 3 (US1) Parallelization

**After T010 completes, run in parallel**:
- T011-T012: ScrapeMetadata model
- T013-T014: ScrapeRequest model
- T015-T016: ScrapeResponse model

**After T018 completes, run in parallel**:
- T021-T022: path validator
- T025-T026: OutputService

### Phase 4 (US2) Parallelization

**Minimal parallelization** (sequential dependencies on US1 completion)

### Phase 5 (US3) Parallelization

**After T043 completes**:
- T044 can be developed and tested independently

---

## Quality Gates

### After Each User Story Phase

Run full quality checks:

```bash
# Run all tests
pytest -v --cov=src --cov-report=term-missing

# Type checking
mypy src/ --strict

# Linting
ruff check src/

# Security scan
bandit -r src/

# Coverage check (must be ≥80%)
pytest --cov=src --cov-fail-under=80
```

### Before Final Release

- All user stories tested manually
- All tests pass (unit + integration + contract)
- Code coverage ≥ 80%
- No mypy errors in strict mode
- No ruff lint warnings
- No critical bandit findings
- Documentation complete (README.md updated)

---

## Implementation Notes

### TDD Discipline

**Every implementation task MUST**:
1. Have a corresponding test task that runs FIRST
2. Verify the test FAILS before implementation
3. Implement ONLY enough code to make the test pass
4. Refactor while keeping tests green
5. Commit after complete red-green-refactor cycle

### Constitutional Compliance

- ✅ Python 3.10+ (all tasks)
- ✅ UV package manager (T001-T004)
- ✅ TDD workflow (all TDD tasks paired)
- ✅ Integration tests (T027-T028, T029-T034, T032-T033)
- ✅ Code quality tools (T003, quality gates)
- ✅ 80% coverage target (quality gates)
- ✅ Type hints (all implementation tasks)
- ✅ Google-style docstrings (all implementation tasks)

---

**Tasks Generated**: 2025-10-10
**Ready for Implementation**: ✅
**Estimated Total Time**: 15-20 hours
**MVP Delivery**: After T034 (User Story 1)
