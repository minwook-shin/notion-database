"""
Notion API exceptions.
"""


class NotionError(Exception):
    """Base exception for all notion-database errors."""


class NotionAPIError(NotionError):
    """Raised when the Notion API returns an error response.

    Attributes:
        status_code: HTTP status code returned by the API.
        code: Notion error code string (e.g. "validation_error").
        message: Human-readable error message from the API.
    """

    def __init__(self, status_code: int, code: str, message: str) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        super().__init__(f"[{status_code}] {code}: {message}")


class NotionValidationError(NotionAPIError):
    """HTTP 400 – The request body is malformed or missing required fields."""


class NotionUnauthorizedError(NotionAPIError):
    """HTTP 401 – The integration token is invalid or missing."""


class NotionForbiddenError(NotionAPIError):
    """HTTP 403 – The integration lacks permission for the requested resource."""


class NotionNotFoundError(NotionAPIError):
    """HTTP 404 – The requested resource does not exist."""


class NotionConflictError(NotionAPIError):
    """HTTP 409 – A conflict occurred (e.g. duplicate transaction ID)."""


class NotionRateLimitError(NotionAPIError):
    """HTTP 429 – The request has been rate limited."""


class NotionInternalError(NotionAPIError):
    """HTTP 5xx – An internal error occurred on Notion's servers."""
