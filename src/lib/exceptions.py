"""Custom exception hierarchy for the web crawler."""


class CrawlerError(Exception):
    """Base exception for all crawler errors.

    Attributes:
        message: Human-readable error message
        code: Exit code for CLI (default: 1)
        details: Optional dictionary with additional error context
    """

    def __init__(self, message: str, code: int = 1, details: dict | None = None):
        """Initialize CrawlerError.

        Args:
            message: Error message
            code: Exit code (default: 1 for general errors)
            details: Additional error context
        """
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)


class ConfigurationError(CrawlerError):
    """Configuration missing or invalid.

    Examples:
        - Missing FIRECRAWL_API_URL environment variable
        - Invalid configuration format
        - Required settings not provided
    """

    def __init__(self, message: str, details: dict | None = None):
        """Initialize ConfigurationError with exit code 2.

        Args:
            message: Configuration error description
            details: Additional context (e.g., missing variable name)
        """
        super().__init__(message, code=2, details=details)


class ValidationError(CrawlerError):
    """Input validation error.

    Examples:
        - Invalid URL format
        - Invalid output path
        - Malformed request parameters
    """

    def __init__(self, message: str, details: dict | None = None):
        """Initialize ValidationError with exit code 1.

        Args:
            message: Validation error description
            details: Additional context (e.g., invalid value)
        """
        super().__init__(message, code=1, details=details)


class FirecrawlApiError(CrawlerError):
    """Base class for Firecrawl API errors.

    Examples:
        - Network connectivity issues
        - API endpoint unreachable
        - Unexpected API response format
    """

    def __init__(self, message: str, details: dict | None = None):
        """Initialize FirecrawlApiError with exit code 1.

        Args:
            message: API error description
            details: Additional context (e.g., HTTP status code)
        """
        super().__init__(message, code=1, details=details)


class RateLimitError(FirecrawlApiError):
    """Rate limit exceeded error (HTTP 429).

    Raised when the Firecrawl API rate limit is exceeded.
    User should retry after a delay.
    """

    def __init__(self, message: str = "Rate limit exceeded", details: dict | None = None):
        """Initialize RateLimitError with exit code 3.

        Args:
            message: Rate limit error message
            details: Additional context (e.g., retry-after header)
        """
        # Override code to 3 for rate limits
        CrawlerError.__init__(self, message, code=3, details=details)


class AuthenticationError(FirecrawlApiError):
    """Authentication failed error (HTTP 401).

    Examples:
        - Invalid API key
        - Missing API key when required
        - Expired credentials
    """

    def __init__(self, message: str, details: dict | None = None):
        """Initialize AuthenticationError with exit code 1.

        Args:
            message: Authentication error description
            details: Additional context
        """
        super().__init__(message, details=details)


class ServerError(FirecrawlApiError):
    """Server error from Firecrawl API (HTTP 5xx).

    Examples:
        - Internal server error (500)
        - Service unavailable (503)
        - Gateway timeout (504)
    """

    def __init__(self, message: str, details: dict | None = None):
        """Initialize ServerError with exit code 1.

        Args:
            message: Server error description
            details: Additional context (e.g., HTTP status code)
        """
        super().__init__(message, details=details)


class OutputError(CrawlerError):
    """File output error.

    Examples:
        - Cannot create output directory
        - Permission denied writing file
        - Disk full
    """

    def __init__(self, message: str, details: dict | None = None):
        """Initialize OutputError with exit code 1.

        Args:
            message: Output error description
            details: Additional context (e.g., file path)
        """
        super().__init__(message, code=1, details=details)
