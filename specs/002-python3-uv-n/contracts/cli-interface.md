# CLI Interface Contract

**Branch**: `002-python3-uv-n` | **Date**: 2025-10-10 | **Phase**: 1 (Design & Contracts)

## Overview

This document defines the command-line interface contract for the Web Crawler CLI Tool. It specifies the exact commands, arguments, options, output formats, and exit codes that users and automated systems can depend on.

---

## Commands

### `scrape`

**Purpose**: Scrape a single web page and output content in specified format.

**Syntax**:
```bash
crawler scrape --url <URL> [OPTIONS]
```

**Primary Use Case**: User Story 1 - Basic Web Page Crawling (P1)

---

## Arguments & Options

### Required Arguments

#### `--url <URL>`

- **Type**: String (HTTP/HTTPS URL)
- **Required**: Yes
- **Description**: The web page URL to scrape
- **Validation**:
  - Must start with `http://` or `https://`
  - Must be a valid, parseable URL
- **Examples**:
  ```bash
  --url https://example.com
  --url http://localhost:8000/page
  ```
- **Error Behavior**:
  - Invalid URL → Exit code 1 with error message
  - Missing URL → Typer automatically shows usage help

---

### Format Options (Mutually Exclusive)

#### `--markdown` (default)

- **Type**: Boolean flag
- **Required**: No
- **Default**: `True`
- **Description**: Output content as markdown format
- **File Extension**: `.md`
- **Specification Reference**: FR-002 (support multiple output formats)
- **Example**:
  ```bash
  crawler scrape --url https://example.com --markdown
  ```

#### `--html`

- **Type**: Boolean flag
- **Required**: No
- **Default**: `False`
- **Description**: Output content as HTML format
- **File Extension**: `.html`
- **Specification Reference**: FR-002 (support multiple output formats)
- **Example**:
  ```bash
  crawler scrape --url https://example.com --html
  ```

**Precedence Rule**: If both `--markdown` and `--html` are specified, `--html` takes precedence.

---

### Output Options

#### `--output <PATH>`

- **Type**: String (file path)
- **Required**: No
- **Default**: `None` (output to stdout)
- **Description**: File path where scraped content will be saved
- **Validation**:
  - Must be a valid file path for the operating system
  - Parent directory must exist or be creatable
  - Must not be an existing directory (must be a file path)
- **Behavior**:
  - If `None`: Print content to console (stdout)
  - If provided: Write content to file
    - Create parent directories if they don't exist (FR-004)
    - Overwrite file if it already exists (with warning)
- **Specification Reference**: FR-003, FR-004
- **Examples**:
  ```bash
  # Output to file
  crawler scrape --url https://example.com --output ./data/page.md

  # Output to stdout (console)
  crawler scrape --url https://example.com
  ```

---

## Output Formats

### Stdout (Console Output)

When `--output` is not specified, content is printed to stdout:

```
[Content of the scraped page in specified format]
```

**Use Case**: Piping to other commands or viewing directly in terminal.

**Example**:
```bash
crawler scrape --url https://example.com | less
crawler scrape --url https://example.com --html > myfile.html
```

---

### File Output

When `--output <PATH>` is specified, content is written to the file:

**Success Behavior**:
1. Create parent directories if needed
2. Write content to file
3. Print confirmation message to stderr:
   ```
   ✓ Content saved to: /absolute/path/to/file.md
   ```

**File Naming**:
- User-specified filename is used exactly as provided
- No automatic extension correction (user responsible for correct extension)
- Warning if extension doesn't match format (`.md` for markdown, `.html` for HTML)

---

## Exit Codes

The CLI follows standard Unix exit code conventions:

| Code | Name | Description | When Used |
|------|------|-------------|-----------|
| 0 | Success | Operation completed successfully | Scraping succeeded and content outputted |
| 1 | General Error | Generic error (validation, network, etc.) | Invalid URL, network failure, scraping failed |
| 2 | Configuration Error | Missing or invalid configuration | Missing `FIRECRAWL_API_URL`, invalid API URL format |
| 3 | Rate Limit Error | Firecrawl API rate limit exceeded | HTTP 429 from Firecrawl API |

**Specification Reference**: FR-008 (display appropriate error messages)

---

## Error Messages

All error messages are printed to **stderr** (not stdout) to allow piping output.

### Format

```
Error: <Human-readable description>
<Optional: Additional context or suggestion>
```

### Examples

#### Invalid URL (Exit Code 1)
```
Error: Invalid URL format: 'not-a-url'
Please provide a valid HTTP or HTTPS URL using --url option.
```

#### Missing Configuration (Exit Code 2)
```
Error: Missing required configuration: FIRECRAWL_API_URL
Please set the FIRECRAWL_API_URL environment variable in your .env file.
```

#### Rate Limit Exceeded (Exit Code 3)
```
Error: Rate limit exceeded
The Firecrawl API rate limit has been reached. Please try again later.
```

#### Network Error (Exit Code 1)
```
Error: Failed to connect to Firecrawl API at http://localhost:3002
Please ensure the Firecrawl service is running and accessible.
```

#### File Write Error (Exit Code 1)
```
Error: Permission denied when writing to: /path/to/file.md
Please check file permissions and try again.
```

---

## Success Messages

Success messages are printed to **stderr** to keep stdout clean for piping.

### Console Output Success
```
✓ Scraped: https://example.com
```

### File Output Success
```
✓ Content saved to: /absolute/path/to/file.md
✓ Scraped: https://example.com
```

---

## Examples

### Example 1: Basic Scrape to Console (Markdown)

**Command**:
```bash
crawler scrape --url https://example.com
```

**Expected Output** (stdout):
```markdown
# Example Domain

This domain is for use in illustrative examples in documents...
```

**Expected Output** (stderr):
```
✓ Scraped: https://example.com
```

**Exit Code**: 0

---

### Example 2: Scrape to File (HTML)

**Command**:
```bash
crawler scrape --url https://example.com --html --output ./data/example.html
```

**Expected Output** (stderr):
```
✓ Content saved to: D:\Projects\crawler\data\example.html
✓ Scraped: https://example.com
```

**Exit Code**: 0

**File Content** (`data/example.html`):
```html
<!DOCTYPE html>
<html>
<head><title>Example Domain</title></head>
<body>
  <h1>Example Domain</h1>
  <p>This domain is for use in illustrative examples in documents...</p>
</body>
</html>
```

---

### Example 3: Error - Invalid URL

**Command**:
```bash
crawler scrape --url not-a-url
```

**Expected Output** (stderr):
```
Error: Invalid URL format: 'not-a-url'
Please provide a valid HTTP or HTTPS URL using --url option.
```

**Exit Code**: 1

---

### Example 4: Error - Missing Configuration

**Command** (with empty .env):
```bash
crawler scrape --url https://example.com
```

**Expected Output** (stderr):
```
Error: Missing required configuration: FIRECRAWL_API_URL
Please set the FIRECRAWL_API_URL environment variable in your .env file.
See .env.example for configuration template.
```

**Exit Code**: 2

---

### Example 5: Piping to Other Commands

**Command**:
```bash
crawler scrape --url https://example.com | grep "Example"
```

**Expected Output** (stdout):
```
# Example Domain
This domain is for use in illustrative examples in documents...
```

**Expected Output** (stderr):
```
✓ Scraped: https://example.com
```

**Exit Code**: 0

---

## Help Output

### `--help` Flag

**Command**:
```bash
crawler scrape --help
```

**Expected Output**:
```
Usage: crawler scrape [OPTIONS]

  Scrape a single web page using Firecrawl.

  Scrapes the specified URL and outputs the content in the chosen format
  (markdown or HTML). Content can be printed to console or saved to a file.

Options:
  --url TEXT              URL to scrape (required)  [required]
  --markdown              Output as markdown (default)  [default: True]
  --html                  Output as HTML
  --output TEXT           Output file path (default: stdout)
  --help                  Show this message and exit.

Examples:
  # Scrape to console (markdown)
  crawler scrape --url https://example.com

  # Scrape to file (HTML)
  crawler scrape --url https://example.com --html --output page.html
```

---

## Future Extensions (P2-P3)

### Additional Options (P2 - User Story 2)

```bash
--json                  # Output as JSON
--text                  # Output as plain text
```

### Batch Scraping (P3 - User Story 3)

```bash
--url-file <PATH>       # File containing list of URLs (one per line)
--output-dir <PATH>     # Directory to save multiple files
```

### Custom Filename (P3 - User Story 4)

```bash
--filename <NAME>       # Custom filename (without extension)
```

---

## Contract Testing

### Test Cases

Contract tests MUST verify:

1. **Command Existence**: `crawler scrape` command is available
2. **Required Arguments**: Missing `--url` shows help and exits non-zero
3. **Valid URL**: Accepts `http://` and `https://` URLs
4. **Invalid URL**: Rejects invalid URLs with exit code 1
5. **Format Flags**: `--markdown` and `--html` change output format
6. **File Output**: `--output` creates file with correct content
7. **Stdout Output**: Without `--output`, content goes to stdout
8. **Exit Codes**: Correct exit code for each error scenario
9. **Help Text**: `--help` displays usage information

### Test Location

`tests/integration/test_scrape_command.py`

---

**CLI Contract Completed**: 2025-10-10
**Status**: Interface fully specified ✅
**Compliance**: FR-001 through FR-015 covered
