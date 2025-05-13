# src/pybedrock_server_manager/exceptions.py
"""Custom Exceptions for the pybedrock_server_manager library."""


class APIError(Exception):
    """Generic API Error."""

    pass


class AuthError(APIError):
    """Authentication Error (e.g., 401 Unauthorized, Bad Credentials)."""

    pass


class ServerNotFoundError(APIError):
    """Server name not found (e.g., 404 on server-specific endpoint or validation)."""

    pass


class ServerNotRunningError(APIError):
    """Operation requires server to be running, but it is not."""

    pass


class CannotConnectError(APIError):
    """Error connecting to the API host."""

    pass
