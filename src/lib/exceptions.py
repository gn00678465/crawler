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


# AI Service Exceptions


class AIServiceError(CrawlerError):
    """Base exception for AI service errors.

    Examples:
        - Network errors connecting to AI API
        - Unexpected AI response format
        - AI service unavailable
    """

    def __init__(self, message: str, code: int = 3, details: dict | None = None):
        """Initialize AIServiceError.

        Args:
            message: AI service error description
            code: Exit code (default: 3 for AI service errors)
            details: Additional context
        """
        super().__init__(message, code=code, details=details)


class ModelNotFoundError(AIServiceError):
    """AI model not found or not supported.

    Raised when:
        - Model name is invalid
        - Model doesn't exist in the provider
        - Model is not supported by LiteLLM

    Exit code: 2 (configuration error)
    """

    def __init__(self, message: str, details: dict | None = None):
        """Initialize ModelNotFoundError.

        Args:
            message: Model not found error description
            details: Additional context (e.g., model name, provider)
        """
        super().__init__(message, code=2, details=details)


class RateLimitExceededError(AIServiceError):
    """AI service rate limit exceeded.

    Raised when:
        - Too many requests to AI API
        - Token rate limit exceeded
        - Quota exhausted

    Exit code: 3 (AI service error)
    """

    def __init__(
        self, message: str = "AI service rate limit exceeded", details: dict | None = None
    ):
        """Initialize RateLimitExceededError.

        Args:
            message: Rate limit error message
            details: Additional context (e.g., retry-after, reset time)
        """
        super().__init__(message, code=3, details=details)


class TokenLimitExceededError(AIServiceError):
    """Article exceeds AI model token limit.

    Raised when:
        - Article is too long for model context window
        - Combined prompt + article exceeds token limit

    Exit code: 3 (AI service error)

    Suggested actions:
        - Use a brief summary mode
        - Split article into sections
        - Use a model with larger context window
    """

    def __init__(
        self, message: str = "Article exceeds model token limit", details: dict | None = None
    ):
        """Initialize TokenLimitExceededError.

        Args:
            message: Token limit error message
            details: Additional context (e.g., token count, limit)
        """
        super().__init__(message, code=3, details=details)
