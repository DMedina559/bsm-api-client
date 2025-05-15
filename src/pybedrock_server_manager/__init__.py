# src/pybedrock_server_manager/__init__.py
"""Python client library for the Bedrock Server Manager API."""
import logging
from importlib import metadata

from .exceptions import (
    APIError,
    AuthError,
    NotFoundError,
    ServerNotFoundError,
    ServerNotRunningError,
    CannotConnectError,
    InvalidInputError,
    OperationFailedError,
    APIServerSideError,
)
from .api_client import BedrockServerManagerApi

__all__ = [
    "BedrockServerManagerApi",
    "APIError",
    "AuthError",
    "ServerNotFoundError",
    "ServerNotRunningError",
    "CannotConnectError",
    "InvalidInputError",
    "OperationFailedError",
    "APIServerSideError",
    "__version__",
]

try:
    __version__ = metadata.version(__name__)
except metadata.PackageNotFoundError:
    __version__ = "0.0.0"

# Add a NullHandler to the root logger of the library.
# This prevents log messages from being output by default if the
# consuming application/script doesn't configure logging.
logging.getLogger(__name__).addHandler(logging.NullHandler())
