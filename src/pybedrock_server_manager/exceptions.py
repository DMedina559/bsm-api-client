# src/pybedrock_server_manager/exceptions.py
"""Custom Exceptions for the pybedrock_server_manager library."""

from typing import Optional, Dict, Any


class APIError(Exception):
    """
    Generic base exception for errors originating from or related to the Bedrock Server Manager API.
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data if response_data is not None else {}
        # Extract common fields from API response if available for convenience
        self.api_message: str = self.response_data.get("message", "")
        self.api_errors: Dict[str, Any] = self.response_data.get("errors", {})

    def __str__(self):
        base_str = super().__str__()
        if self.status_code:
            base_str = f"[Status {self.status_code}] {base_str}"

        # Append API message if it's different from the main exception message and not empty
        if self.api_message and self.api_message.lower() not in base_str.lower():
            base_str += f" (API Message: {self.api_message})"

        if self.api_errors:
            base_str += f" (API Errors: {self.api_errors})"
        return base_str


class CannotConnectError(
    APIError
):  # Changed from Exception to APIError for consistency, but could be Exception
    """
    Raised when the client cannot connect to the Bedrock Server Manager API host.
    This typically wraps a lower-level connection error from the HTTP client (e.g., requests.exceptions.ConnectionError).
    """

    def __init__(self, message: str, original_exception: Optional[Exception] = None):
        # Pass status_code=None and response_data=None as this isn't an API response error
        super().__init__(message, status_code=None, response_data=None)
        self.original_exception = original_exception

    def __str__(self):
        # Call the parent's __str__ to get its formatting (without status_code part)
        base_str = Exception.__str__(self)  # Get the original message part directly
        if self.original_exception:
            base_str += f" (Original error: {type(self.original_exception).__name__}: {str(self.original_exception)})"
        return base_str


class AuthError(APIError):
    """Authentication Error (e.g., 401 Unauthorized, 403 Forbidden, Bad Credentials)."""

    pass


# Consider a more general NotFoundError if 404s can be for things other than servers
class NotFoundError(APIError):
    """Resource Not Found Error (e.g., 404 Not Found)."""

    pass


class ServerNotFoundError(NotFoundError):  # Make ServerNotFoundError more specific
    """Server name not found (e.g., 404 on server-specific endpoint or validation)."""

    pass


class ServerNotRunningError(APIError):
    """Operation requires server to be running, but it is not."""

    # This might not always have a direct HTTP status, but could be inferred
    # or be a specific API error message.
    pass


class InvalidInputError(APIError):
    """Client-side input validation error (e.g., 400 Bad Request)."""

    pass


class OperationFailedError(APIError):
    """A general error when an API operation fails for reasons not covered by other exceptions (e.g. 501 Not Implemented, or other specific failures)."""

    pass


class APIServerSideError(APIError):
    """Indicates a server-side error on the API (e.g., 500 Internal Server Error)."""

    pass
