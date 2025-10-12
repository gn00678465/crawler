# Data Model: AI-Powered Article Summarization

**Feature**: `003-markdown-summary-ai`
**Date**: 2025-10-12
**Related**: [spec.md](./spec.md) | [plan.md](./plan.md)

## Overview

This document defines the data models (Pydantic classes) for the AI summarization feature. All models follow Python 3.10+ type hints and Pydantic v2 conventions.

## Model Hierarchy

```
SummarizeRequest (input)
    ↓
ArticleContent (intermediate)
    ↓
AISummary (output)
    ↓
OutputFile (result)

AIModelConfiguration (config)
```

## Models

### 1. SummarizeRequest

**Purpose**: Represents user input for the summarize command

**Module**: `src/models/summarize_request.py`

**Fields**:

```python
from typing import Optional, Literal
from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime

class SummarizeRequest(BaseModel):
    """
    Represents a request to summarize a web article.

    Attributes:
        url: The web page URL to crawl and summarize
        model: AI model identifier in LiteLLM format (e.g., 'gemini/gemini-pro')
        summary_length: Desired summary verbosity level
        output_path: Optional file or directory path for saving summary
        save_original: Whether to save original markdown alongside summary
        timestamp: Request creation timestamp
    """
    url: HttpUrl = Field(..., description="URL of article to summarize")
    model: Optional[str] = Field(
        default=None,
        description="AI model in format 'provider/model-name' (e.g., 'gemini/gemini-pro')"
    )
    summary_length: Literal["brief", "standard", "detailed"] = Field(
        default="standard",
        description="Summary verbosity level"
    )
    output_path: Optional[str] = Field(
        default=None,
        description="Output file or directory path"
    )
    save_original: bool = Field(
        default=False,
        description="Save original markdown alongside summary"
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://example.com/article",
                "model": "gemini/gemini-pro",
                "summary_length": "standard",
                "output_path": "./summaries/",
                "save_original": False
            }
        }
```

**Validation Rules**:
- `url`: Must be valid HTTP/HTTPS URL (Pydantic HttpUrl handles this)
- `model`: If provided, must match LiteLLM format (validated in service layer)
- `summary_length`: Must be one of ["brief", "standard", "detailed"]
- `output_path`: Optional, validated in file service layer

**Relationships**:
- Created from CLI command arguments
- Used by crawler service to fetch article
- Passed to AI service for summarization

---

### 2. AIModelConfiguration

**Purpose**: Parsed AI model configuration with provider routing information

**Module**: `src/models/ai_model_config.py`

**Fields**:

```python
from typing import Optional
from pydantic import BaseModel, Field, validator

class AIModelConfiguration(BaseModel):
    """
    Represents a parsed AI model configuration.

    Attributes:
        full_name: Complete model identifier (e.g., 'gemini/gemini-pro')
        provider: Provider name (e.g., 'gemini', 'openai', 'ollama')
        model_name: Model name without provider prefix (e.g., 'gemini-pro')
        api_key_env_var: Expected environment variable name for API key
        is_local: Whether this is a local model (Ollama, vLLM)
    """
    full_name: str = Field(..., description="Full LiteLLM model identifier")
    provider: str = Field(..., description="Model provider (e.g., 'gemini', 'openai')")
    model_name: str = Field(..., description="Model name without provider prefix")
    api_key_env_var: Optional[str] = Field(
        None,
        description="Environment variable name for API key (e.g., 'GOOGLE_API_KEY')"
    )
    is_local: bool = Field(
        default=False,
        description="Whether this is a local model (no API key required)"
    )

    @validator("full_name")
    def validate_format(cls, v):
        """Ensure model name follows 'provider/model' format"""
        if "/" not in v:
            raise ValueError(
                f"Model name must be in format 'provider/model-name', got: {v}"
            )
        parts = v.split("/")
        if len(parts) != 2 or not parts[0] or not parts[1]:
            raise ValueError(
                f"Invalid model format. Expected 'provider/model-name', got: {v}"
            )
        return v

    @classmethod
    def from_model_string(cls, model_string: str) -> "AIModelConfiguration":
        """
        Factory method to parse model string into configuration.

        Args:
            model_string: LiteLLM model identifier (e.g., 'gemini/gemini-pro')

        Returns:
            AIModelConfiguration instance

        Example:
            >>> config = AIModelConfiguration.from_model_string("gemini/gemini-pro")
            >>> config.provider
            'gemini'
            >>> config.api_key_env_var
            'GOOGLE_API_KEY'
        """
        provider, model_name = model_string.split("/", 1)

        # Map provider to API key environment variable
        api_key_map = {
            "gemini": "GOOGLE_API_KEY",
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "ollama": None,  # Local, no API key
            "vllm": None,    # Local, no API key
        }

        is_local = provider in ["ollama", "vllm"]
        api_key_env_var = api_key_map.get(provider)

        return cls(
            full_name=model_string,
            provider=provider,
            model_name=model_name,
            api_key_env_var=api_key_env_var,
            is_local=is_local
        )

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "gemini/gemini-pro",
                "provider": "gemini",
                "model_name": "gemini-pro",
                "api_key_env_var": "GOOGLE_API_KEY",
                "is_local": False
            }
        }
```

**Validation Rules**:
- `full_name`: Must contain "/" separator
- `provider` and `model_name`: Derived from splitting `full_name`
- `api_key_env_var`: Automatically mapped from provider name
- `is_local`: Determines if API key validation is required

**Relationships**:
- Created from `SummarizeRequest.model` or environment default
- Used by AI service to validate configuration at startup
- Determines which API key to check

---

### 3. ArticleContent

**Purpose**: Represents crawled and processed article content

**Module**: `src/models/article_content.py`

**Fields**:

```python
from typing import Optional
from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime

class ArticleContent(BaseModel):
    """
    Represents crawled article content in markdown format.

    Attributes:
        url: Original article URL
        title: Article title (extracted from HTML or URL)
        markdown: Article content in markdown format
        detected_language: Auto-detected language code (e.g., 'en', 'zh', 'ja')
        word_count: Number of words in markdown content
        crawl_timestamp: When the article was crawled
        metadata: Additional metadata from crawler (optional)
    """
    url: HttpUrl = Field(..., description="Original article URL")
    title: str = Field(..., description="Article title")
    markdown: str = Field(..., description="Article content in markdown format")
    detected_language: Optional[str] = Field(
        None,
        description="ISO 639-1 language code (e.g., 'en', 'zh')"
    )
    word_count: int = Field(..., description="Word count of markdown content")
    crawl_timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[dict] = Field(
        default=None,
        description="Additional metadata from Firecrawl"
    )

    @property
    def is_minimal(self) -> bool:
        """Check if content is too short to meaningfully summarize"""
        return self.word_count < 100

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://example.com/article",
                "title": "Introduction to Python",
                "markdown": "# Python\n\nPython is a programming language...",
                "detected_language": "en",
                "word_count": 1500,
                "crawl_timestamp": "2025-10-12T10:30:00Z"
            }
        }
```

**Validation Rules**:
- `url`: Must be valid HTTP/HTTPS URL
- `markdown`: Non-empty string
- `word_count`: Calculated from markdown content
- `detected_language`: Optional ISO 639-1 code (2-letter)

**Relationships**:
- Created by Firecrawl service from crawl response
- Input to AI service for summarization
- Optionally saved to file if `save_original` is True

---

### 4. AISummary

**Purpose**: Represents AI-generated summary with metadata

**Module**: `src/models/ai_summary.py`

**Fields**:

```python
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class AISummary(BaseModel):
    """
    Represents an AI-generated article summary.

    Attributes:
        summary_text: The generated summary content
        output_language: Language of the summary (should match source article)
        length_mode: Which summary length mode was used
        model_used: Full model identifier that generated this summary
        token_usage: Token count metadata from AI service
        generation_timestamp: When the summary was generated
        source_url: Original article URL
        source_title: Original article title
    """
    summary_text: str = Field(..., description="Generated summary content")
    output_language: Optional[str] = Field(
        None,
        description="ISO 639-1 language code of summary"
    )
    length_mode: str = Field(..., description="Summary length mode used")
    model_used: str = Field(..., description="AI model identifier")
    token_usage: Optional[dict] = Field(
        None,
        description="Token usage stats (prompt_tokens, completion_tokens, total_tokens)"
    )
    generation_timestamp: datetime = Field(default_factory=datetime.utcnow)
    source_url: str = Field(..., description="Original article URL")
    source_title: str = Field(..., description="Original article title")

    class Config:
        json_schema_extra = {
            "example": {
                "summary_text": "This article introduces Python as a high-level programming language...",
                "output_language": "en",
                "length_mode": "standard",
                "model_used": "gemini/gemini-pro",
                "token_usage": {
                    "prompt_tokens": 1500,
                    "completion_tokens": 150,
                    "total_tokens": 1650
                },
                "generation_timestamp": "2025-10-12T10:32:15Z",
                "source_url": "https://example.com/article",
                "source_title": "Introduction to Python"
            }
        }
```

**Validation Rules**:
- `summary_text`: Non-empty string
- `length_mode`: Should be one of ["brief", "standard", "detailed"]
- `model_used`: LiteLLM model identifier
- `token_usage`: Optional dictionary with known keys

**Relationships**:
- Created by AI service from LiteLLM response
- Contains reference to source `ArticleContent`
- Passed to file output service for saving

---

### 5. OutputFile

**Purpose**: Represents result of file write operation

**Module**: `src/models/output_file.py` (may already exist, extend if needed)

**Fields**:

```python
from pydantic import BaseModel, Field
from pathlib import Path

class OutputFile(BaseModel):
    """
    Represents a successfully written output file.

    Attributes:
        file_path: Absolute path to written file
        file_size: Size in bytes
        format: File format/extension (e.g., 'md', 'html')
    """
    file_path: str = Field(..., description="Absolute path to output file")
    file_size: int = Field(..., description="File size in bytes")
    format: str = Field(..., description="File format/extension")

    @property
    def path_obj(self) -> Path:
        """Return pathlib.Path object for file operations"""
        return Path(self.file_path)

    class Config:
        json_schema_extra = {
            "example": {
                "file_path": "/path/to/summaries/article-summary.md",
                "file_size": 2048,
                "format": "md"
            }
        }
```

**Validation Rules**:
- `file_path`: Must be valid file system path
- `file_size`: Non-negative integer
- `format`: File extension without dot

**Relationships**:
- Returned by file output service after write operation
- Can represent summary file or original markdown file
- Displayed to user as confirmation

---

## Model Usage Flow

```
1. CLI Command → SummarizeRequest
   ↓
2. Validate & Parse → AIModelConfiguration (from model string or DEFAULT_AI_MODEL)
   ↓
3. Crawl URL → ArticleContent (via Firecrawl)
   ↓
4. Summarize → AISummary (via LiteLLM)
   ↓
5. Save/Display → OutputFile (if output_path provided)
```

## Validation Strategy

### Unit Tests (`tests/unit/models/`)

Each model should have tests for:
- Valid instantiation with all fields
- Validation errors for invalid fields
- Edge cases (empty strings, negative numbers, etc.)
- Factory methods and computed properties
- Pydantic JSON serialization/deserialization

**Example Test Structure**:
```python
def test_summarize_request_valid():
    """Test valid SummarizeRequest creation"""
    request = SummarizeRequest(
        url="https://example.com/article",
        model="gemini/gemini-pro",
        summary_length="standard"
    )
    assert request.url == "https://example.com/article"
    assert request.summary_length == "standard"

def test_summarize_request_invalid_url():
    """Test validation rejects invalid URL"""
    with pytest.raises(ValidationError):
        SummarizeRequest(url="not-a-url")

def test_ai_model_config_from_string():
    """Test AIModelConfiguration factory method"""
    config = AIModelConfiguration.from_model_string("gemini/gemini-pro")
    assert config.provider == "gemini"
    assert config.api_key_env_var == "GOOGLE_API_KEY"
    assert config.is_local == False
```

---

## Notes

- All timestamps use UTC (`datetime.utcnow()`)
- Pydantic models are immutable by default (use `Config.frozen = True` if enforcing)
- Type hints ensure mypy strict mode compliance
- Factory methods (`from_model_string`) encapsulate parsing logic
- Computed properties (`is_minimal`, `path_obj`) keep logic close to data

---

**Next Steps**: Generate contracts/ for API specifications

