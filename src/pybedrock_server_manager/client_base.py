# src/pybedrock_server_manager/client_base.py
"""Base class for the Bedrock Server Manager API Client.

Handles initialization, session management, authentication, and the core request logic.
"""

import aiohttp
import asyncio
import logging
from typing import Any, Dict, Optional, Mapping, Union

# Import exceptions from the same package level
from .exceptions import (
    APIError,
    AuthError,
    ServerNotFoundError,
    ServerNotRunningError,
    CannotConnectError,
)

# Logger specifically for the base client logic
_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.base")


class ClientBase:
    """Base class containing core API client logic."""

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        session: Optional[aiohttp.ClientSession] = None,
        base_path: str = "/api",
        request_timeout: int = 10,
    ):
        """Initialize the base API client."""
        host = host.replace("http://", "").replace("https://", "")
        self._host = host
        self._port = port
        self._base_url = f"http://{host}:{port}{base_path}"
        self._username = username
        self._password = password
        self._base_path = base_path
        self._request_timeout = request_timeout

        if session is None:
            self._session = aiohttp.ClientSession()
            self._close_session = True
        else:
            self._session = session
            self._close_session = False

        self._jwt_token: Optional[str] = None
        self._headers: Mapping[str, str] = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self._auth_lock = asyncio.Lock()

        _LOGGER.debug("ClientBase initialized for %s", self._base_url)

    async def close(self) -> None:
        """Close the underlying session if it was created internally."""
        if self._session and self._close_session and not self._session.closed:
            await self._session.close()
            _LOGGER.debug(
                "Closed internally managed ClientSession for %s", self._base_url
            )

    async def __aenter__(self) -> "ClientBase":
        """Async context manager entry."""
        return self  # Or return self cast to the final type if type hinting needs it

    async def __aexit__(self, exc_type, exc, tb) -> None:
        """Async context manager exit."""
        await self.close()

    async def _request(
        self,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        authenticated: bool = True,
        is_retry: bool = False,
    ) -> Dict[str, Any]:
        """Internal method to make API requests."""
        url = f"{self._base_url}{path}"
        headers: Dict[str, str] = dict(self._headers)

        if authenticated:
            async with self._auth_lock:
                if not self._jwt_token and not is_retry:
                    _LOGGER.debug(
                        "No token found for auth request %s, attempting login.", path
                    )
                    try:
                        await self.authenticate()  # Call the authenticate method (defined below)
                    except AuthError:
                        _LOGGER.error(
                            "Initial authentication failed for request %s", path
                        )
                        raise

            if authenticated and not self._jwt_token:
                _LOGGER.error(
                    "Auth required for %s but no token after lock/login.", path
                )
                raise AuthError(
                    "Auth required but no token available after login attempt."
                )

            if authenticated and self._jwt_token:
                headers["Authorization"] = f"Bearer {self._jwt_token}"
                # _LOGGER.debug("Added Bearer token to headers for %s", path) # Less noisy

        # _LOGGER.debug("Request: %s %s (Headers: %s, Data: %s)", method, url, headers, data) # Can be very verbose
        _LOGGER.debug("Request: %s %s", method, url)
        try:
            async with self._session.request(
                method,
                url,
                json=data,
                headers=headers,
                raise_for_status=False,
                timeout=aiohttp.ClientTimeout(total=self._request_timeout),
            ) as response:
                _LOGGER.debug(
                    "Response Status for %s %s: %s", method, path, response.status
                )

                if response.status == 401 and authenticated and not is_retry:
                    _LOGGER.warning(
                        "Received 401 for %s, attempting token refresh and retry.", path
                    )
                    async with self._auth_lock:
                        self._jwt_token = None
                        # Use the public request method of the final class for retry
                        return await self._request(
                            method, path, data=data, authenticated=True, is_retry=True
                        )

                if response.status == 401:
                    resp_text = await response.text()
                    error_message = await self._extract_error_message(
                        response, resp_text
                    )  # Use helper
                    # Check login path using stored base path
                    if (
                        path == f"{self._base_path}/login"
                        and "bad username or password" in error_message.lower()
                    ):
                        raise AuthError("Bad username or password")
                    else:
                        raise AuthError(f"Authentication Failed (401): {error_message}")

                if response.status == 404 and path.startswith(
                    f"{self._base_path}/server/"
                ):
                    resp_text = await response.text()
                    error_message = await self._extract_error_message(
                        response, resp_text
                    )
                    raise ServerNotFoundError(
                        f"Server Not Found (404): {error_message}"
                    )

                if response.status == 501:
                    resp_text = await response.text()
                    error_message = await self._extract_error_message(
                        response, resp_text
                    )
                    raise APIError(f"Feature Not Implemented (501): {error_message}")

                if response.status >= 400:
                    resp_text = await response.text()
                    error_message = await self._extract_error_message(
                        response, resp_text
                    )
                    msg_lower = error_message.lower()
                    if (
                        response.status == 500
                        and authenticated
                        and (
                            "is not running" in msg_lower
                            or "screen session" in msg_lower
                            and "not found" in msg_lower
                            or "pipe does not exist" in msg_lower
                            or "server likely not running" in msg_lower
                        )
                    ):
                        raise ServerNotRunningError(
                            f"Operation failed: {error_message}"
                        )
                    raise APIError(f"API Error {response.status}: {error_message}")

                # --- Handle Success ---
                _LOGGER.debug(
                    "API request successful for %s [%s]", path, response.status
                )
                if response.status == 204:
                    return {
                        "status": "success",
                        "message": "Operation successful (No Content)",
                    }

                try:
                    json_response = await response.json(content_type=None)
                    if (
                        isinstance(json_response, dict)
                        and json_response.get("status") == "error"
                    ):
                        error_message = json_response.get(
                            "message", "Unknown error in success response."
                        )
                        _LOGGER.error(
                            "API success status (%s) but error body for %s: %s",
                            response.status,
                            path,
                            error_message,
                        )
                        if "is not running" in error_message.lower():
                            raise ServerNotRunningError(error_message)
                        else:
                            raise APIError(error_message)
                    # Return raw JSON potentially non-dict if API returns list etc.
                    # The calling methods should handle the expected structure.
                    # Ensure we always return *something* dict-like if possible.
                    return (
                        json_response
                        if isinstance(json_response, (dict, list))
                        else {"data": json_response}
                    )

                except (
                    aiohttp.ContentTypeError,
                    ValueError,
                    asyncio.TimeoutError,
                ) as json_error:
                    resp_text = await response.text()
                    _LOGGER.warning(
                        "Successful API response (%s) for %s not valid JSON (%s): %s",
                        response.status,
                        path,
                        json_error,
                        resp_text[:100],
                    )
                    return {
                        "status": "success",
                        "message": "Operation successful (Non-JSON response)",
                        "raw_response": resp_text,
                    }

        except aiohttp.ClientConnectionError as e:
            _LOGGER.error("API connection error for %s: %s", url, e)
            raise CannotConnectError(
                f"Connection Error: Cannot connect to host {self._host}:{self._port}"
            ) from e
        except asyncio.TimeoutError as e:
            _LOGGER.error("API request timed out for %s %s", method, url)
            raise CannotConnectError(f"Request timed out for {url}") from e
        except aiohttp.ClientError as e:
            _LOGGER.error("Generic API client error for %s: %s", url, e)
            raise CannotConnectError(f"Client Error: {e}") from e
        except (
            AuthError,
            ServerNotFoundError,
            ServerNotRunningError,
            APIError,
            CannotConnectError,
        ) as e:
            raise e
        except Exception as e:
            _LOGGER.exception("Unexpected error during API request to %s: %s", url, e)
            raise APIError(f"An unexpected error occurred during request: {e}") from e

    async def _extract_error_message(
        self, response: aiohttp.ClientResponse, fallback_text: str
    ) -> str:
        """Helper to try parsing JSON error messages, falling back to text."""
        # Check content type before attempting to read JSON
        if response.content_type != "application/json":
            return fallback_text

        try:
            # Setting content_type=None might still be needed if server sends wrong header
            error_data = await response.json(content_type=None)
            if isinstance(error_data, dict):
                # Prioritize specific error fields if they exist
                if "detail" in error_data:  # Common in FastAPI errors
                    return str(error_data["detail"])
                if "message" in error_data:
                    return str(error_data["message"])
                if "error" in error_data:
                    return str(error_data["error"])
                # Fallback to string representation of the whole dict if no known key
                return str(error_data)
            # If JSON is not a dict, return its string representation
            return str(error_data)
        except (aiohttp.ContentTypeError, ValueError, asyncio.TimeoutError):
            # If JSON parsing fails even after checking content type, use fallback
            return fallback_text

    async def authenticate(self) -> bool:
        """Authenticate with the API and store the JWT. Raises AuthError on failure."""
        # This method uses _request, so the lock logic inside _request handles concurrency.
        _LOGGER.info("Attempting API authentication for user %s", self._username)
        self._jwt_token = None  # Clear token before attempt
        try:
            # Call _request directly - it handles non-authenticated requests too
            response_data = await self._request(
                "POST",
                f"{self._base_path}/login",
                data={"username": self._username, "password": self._password},
                authenticated=False,  # Explicitly false for login endpoint
            )
            token = response_data.get("access_token")
            if not token or not isinstance(token, str):
                _LOGGER.error(
                    "Auth successful but 'access_token' missing/invalid: %s",
                    response_data,
                )
                raise AuthError("Login response missing or invalid access_token.")
            _LOGGER.info("Authentication successful, token received.")
            self._jwt_token = token
            return True
        except AuthError as e:
            _LOGGER.error("Authentication failed during login attempt: %s", e)
            self._jwt_token = None
            raise
        except (APIError, CannotConnectError) as e:
            _LOGGER.error("API error during authentication: %s", e)
            self._jwt_token = None
            raise AuthError(f"API error during login: {e}") from e
