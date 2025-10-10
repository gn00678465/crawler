# Feature Specification: Web Crawler CLI Tool

**Feature Branch**: `002-python3-uv-n`
**Created**: 2025-10-09
**Status**: Draft
**Input**: User description: "使用 python3 做為開發語言，且一律使用 uv 作為套件管理\n結構化資料夾，如: service 相關的放在 services 內, cli 相關的放在 cli 內...\n使用 cli 指令方式爬取網頁並且可以將內容以特定格式存放在特定路徑內, 如 clawler --url --markdown --output xxx/"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Basic Web Page Crawling (Priority: P1)

As a developer, I want to crawl a single web page and save its content in a specific format to a specified location, so that I can archive or process web content programmatically.

**Why this priority**: This is the core functionality of the crawler. Without this, no other features can be built. It delivers immediate value by enabling basic web scraping capabilities.

**Independent Test**: Can be fully tested by running `crawler --url <URL> --markdown --output ./test/` and verifying that the file is created with correct markdown content at the specified path.

**Acceptance Scenarios**:

1. **Given** a valid URL, **When** user runs `crawler --url https://example.com/path/page-name --markdown --output ./data/`, **Then** the web page content is saved as a markdown file in the ./data/ directory with filename auto-generated from URL path (e.g., ./data/page-name.md)
2. **Given** a valid URL, **When** user runs `crawler --url https://example.com --markdown --output ./data/myfile.md`, **Then** the content is saved to the exact file path ./data/myfile.md
3. **Given** a valid URL, **When** user specifies a different output format (e.g., HTML, JSON), **Then** the content is saved in the requested format with appropriate extension
4. **Given** an invalid URL, **When** user runs the crawler, **Then** an error message is displayed indicating the URL is invalid
5. **Given** a non-existent output directory, **When** user runs the crawler, **Then** the directory (and any parent directories) are automatically created

---

### User Story 2 - Multiple Format Support (Priority: P2)

As a content manager, I want to save crawled web content in different formats (markdown, HTML, JSON, plain text), so that I can use the data in various downstream systems and workflows.

**Why this priority**: Different use cases require different output formats. Markdown for documentation, JSON for APIs, HTML for archiving, etc. This enhances the tool's versatility.

**Independent Test**: Can be tested by crawling the same URL with different format flags and verifying each output file has correct formatting and content preservation.

**Acceptance Scenarios**:

1. **Given** a URL, **When** user specifies `--markdown`, **Then** content is converted and saved as markdown with proper formatting
2. **Given** a URL, **When** user specifies `--html`, **Then** the raw HTML is saved to the output path
3. **Given** a URL, **When** user specifies `--json`, **Then** structured content (title, body, metadata) is saved as JSON
4. **Given** a URL, **When** user specifies `--text`, **Then** plain text content is extracted and saved

---

### User Story 3 - Batch Crawling from URL List (Priority: P3)

As a researcher, I want to crawl multiple URLs from a list file, so that I can efficiently collect data from many sources without manual repetition.

**Why this priority**: This is a productivity enhancement that builds on the basic crawling capability. While valuable, users can still accomplish this manually with the P1 feature using scripts.

**Independent Test**: Can be tested by providing a file with multiple URLs and verifying that all pages are crawled and saved to the output directory with appropriate filenames.

**Acceptance Scenarios**:

1. **Given** a text file containing multiple URLs (one per line), **When** user runs `crawler --url-file urls.txt --markdown --output ./data/`, **Then** each URL is crawled and saved as a separate file
2. **Given** a batch crawl operation, **When** one URL fails, **Then** the crawler continues with remaining URLs and logs the error
3. **Given** a batch crawl, **When** completed, **Then** a summary report shows success/failure count

---

### User Story 4 - Custom Output Filename (Priority: P3)

As a data analyst, I want to specify custom filenames for crawled content, so that I can organize files according to my naming conventions.

**Why this priority**: Improves organization and automation workflows, but the default auto-generated filename (based on URL or timestamp) is sufficient for basic use.

**Independent Test**: Can be tested by specifying a custom filename and verifying the output file uses that exact name.

**Acceptance Scenarios**:

1. **Given** a URL and `--filename custom_name`, **When** crawler runs, **Then** the output file is named `custom_name.md` (or appropriate extension)
2. **Given** no filename specified, **When** crawler runs, **Then** a default filename is generated from the page title or URL slug

---

### Edge Cases

- What happens when the target URL requires authentication or cookies?
- What happens when the web page uses JavaScript to render content (dynamic content)? (Note: Firecrawl handles this)
- How does the system handle very large pages (e.g., > 100MB)?
- What happens when the user lacks write permissions to the output directory?
- How does the system handle non-UTF-8 encoded pages?
- What happens when crawling a URL that returns 404, 403, or 500 errors?
- How does the system handle duplicate URLs in batch mode?
- What happens when network connection is lost during crawling?
- What happens when Firecrawl API rate limits are exceeded?
- How does the system handle missing or invalid Firecrawl API credentials?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept a URL via command-line argument `--url <URL>`
- **FR-002**: System MUST support multiple output formats: markdown, HTML, JSON, and plain text
- **FR-003**: System MUST accept both file paths and directory paths via `--output <path>` argument. When a directory path is provided (ending with `/` or `\`), the system MUST automatically generate a filename and save the file in that directory. When a file path is provided, the system MUST save directly to that path.
- **FR-004**: System MUST save crawled content to the specified output path
- **FR-005**: System MUST validate URL format before attempting to crawl
- **FR-006**: System MUST handle HTTP/HTTPS protocols for web page access
- **FR-007**: System MUST extract and convert web page content according to the specified format
- **FR-008**: System MUST display appropriate error messages for failed crawl attempts (network errors, invalid URLs, access denied)
- **FR-009**: System MUST support batch crawling from a file containing multiple URLs
- **FR-010**: System MUST generate appropriate filenames when not explicitly specified or when output path is a directory. Filename generation algorithm: (1) Extract last path segment from URL (e.g., "prompting-one" from "https://example.com/path/prompting-one"), (2) If URL ends with "/" or has no path, use page title converted to slug format, (3) If page title unavailable, use domain name plus timestamp. Generated filenames MUST be sanitized by replacing special characters (`/`, `\`, `?`, `#`, `:`, `*`, `"`, `<`, `>`, `|`) with hyphens, limiting length to 200 characters, and appending the appropriate format extension (.md, .html, .json, .txt)
- **FR-011**: System MUST allow users to specify custom output filenames via `--filename` argument
- **FR-012**: System MUST preserve essential content elements during format conversion (headings, paragraphs, links, images)
- **FR-013**: System MUST follow HTTP redirects automatically (up to 5 hops by default)
- **FR-014**: System MUST use timeout settings as configured by the underlying crawling library (Firecrawl)
- **FR-015**: System MUST respect robots.txt and provide option to override for authorized use cases

### Assumptions

- The crawler will use Firecrawl library for web scraping capabilities, including timeout management and content extraction
- Firecrawl handles both static and dynamic (JavaScript-rendered) content
- Output directories are automatically created (including parent directories) if they don't exist
- Default encoding is UTF-8; other encodings will be detected and converted
- HTTP redirects (301/302) are followed automatically (up to 5 hops)
- User has write permissions to the specified output directory
- Network connectivity is available during operation
- The tool is designed for legitimate data collection and research purposes, not for malicious scraping
- Firecrawl API credentials or configuration are properly set up in the environment

### Key Entities

- **Crawl Request**: Represents a single web crawling operation with attributes including source URL, target format, output path, optional filename, and timestamp
- **Crawled Content**: The extracted web page content with metadata including original URL, crawl timestamp, status code, title, body content, and format type
- **Output File**: The saved result with attributes including file path, format type, size, and creation timestamp

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully crawl a web page and save it to disk in under 10 seconds for pages < 1MB
- **SC-002**: The crawler handles at least 95% of standard web pages (static HTML) without errors
- **SC-003**: Format conversion preserves at least 98% of visible text content accurately
- **SC-004**: Users can successfully complete a basic crawl operation (URL to output file) with a single command in under 30 seconds
- **SC-005**: Error messages clearly indicate the failure reason (invalid URL, network error, access denied, etc.) in 100% of error cases
- **SC-006**: Batch crawling processes at least 100 URLs without manual intervention
- **SC-007**: The tool supports concurrent crawling of at least 50 URLs for batch operations
