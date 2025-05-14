# src/pybedrock_server_manager/__init__.py
"""Python client library for the Bedrock Server Manager API."""

from .exceptions import (
    APIError,
    AuthError,
    ServerNotFoundError,
    ServerNotRunningError,
    CannotConnectError,
)
from .api_client import BedrockServerManagerApi

# Define what is available directly on import 'pybedrock_server_manager'
__all__ = [
    "BedrockServerManagerApi",
    "APIError",
    "AuthError",
    "ServerNotFoundError",
    "ServerNotRunningError",
    "CannotConnectError",
]

# You might want to add a package version here later, often synced from pyproject.toml
# Example using importlib.metadata (requires Python 3.8+):
# from importlib import metadata
# try:
#     __version__ = metadata.version(__name__)
# except metadata.PackageNotFoundError:
#     # package is not installed
#     __version__ = "0.0.0" # Or some other placeholder
