# src/pybedrock_server_manager/client_base.py
"""Base class for the Bedrock Server Manager API Client.

Handles initialization, session management, authentication, and the core request logic.
"""

import aiohttp
import asyncio
import logging
from typing import (
    Any,
    Dict,
    Optional,
    Mapping,
    Union,
    List,
)  # Added List for json_response hint

# Import exceptions from the same package level
from .exceptions import (
    APIError,
    AuthError,
    ServerNotFoundError,
    ServerNotRunningError,
    CannotConnectError,
)

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
        base_path: str = "/api",  # This is the segment like "/api"
        request_timeout: int = 10,
    ):
        """Initialize the base API client."""
        host = host.replace("http://", "").replace("https://", "")
        self._host = host
        self._port = port
        # Ensure base_path starts with a slash and doesn't end with one for consistency
        self._api_base_segment = (
            f"/{base_path.strip('/')}" if base_path.strip("/") else ""
        )
        self._base_url = f"http://{host}:{port}{self._api_base_segment}"  # e.g., http://host:port/api

        self._username = username
        self._password = password
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

        _LOGGER.debug("ClientBase initialized for base URL: %s", self._base_url)

    async def close(self) -> None:
        """Close the underlying session if it was created internally."""
        if self._session and self._close_session and not self._session.closed:
            await self._session.close()
            _LOGGER.debug(
                "Closed internally managed ClientSession for %s", self._base_url
            )

    async def __aenter__(self) -> "ClientBase":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    async def _request(
        self,
        method: str,
        path: str,  # This path is now relative to self._base_url (e.g., "/login", "/servers")
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,  # Added for query parameters
        authenticated: bool = True,
        is_retry: bool = False,
    ) -> Any:  # Changed to Any as response can be dict or list
        """Internal method to make API requests."""
        # Ensure path starts with a /
        request_path = path if path.startswith("/") else f"/{path}"
        url = f"{self._base_url}{request_path}"  # e.g. http://host:port/api + /login

        headers: Dict[str, str] = dict(self._headers)

        if authenticated:
            async with self._auth_lock:
                if not self._jwt_token and not is_retry:
                    _LOGGER.debug(
                        "No token found for auth request to %s, attempting login.", url
                    )
                    try:
                        await self.authenticate()
                    except AuthError:
                        _LOGGER.error(
                            "Initial authentication failed for request to %s", url
                        )
                        raise
            if authenticated and not self._jwt_token:
                _LOGGER.error(
                    "Auth required for %s but no token after lock/login.", url
                )
                raise AuthError(
                    "Auth required but no token available after login attempt."
                )
            if authenticated and self._jwt_token:
                headers["Authorization"] = f"Bearer {self._jwt_token}"

        _LOGGER.debug("Request: %s %s (Params: %s)", method, url, params)
        try:
            async with self._session.request(
                method,
                url,
                json=data,
                params=params,
                headers=headers,
                raise_for_status=False,
                timeout=aiohttp.ClientTimeout(total=self._request_timeout),
            ) as response:
                _LOGGER.debug(
                    "Response Status for %s %s: %s", method, url, response.status
                )

                if response.status == 401 and authenticated and not is_retry:
                    _LOGGER.warning(
                        "Received 401 for %s, attempting token refresh and retry.", url
                    )
                    async with self._auth_lock:
                        self._jwt_token = None
                        return await self._request(
                            method,
                            request_path,
                            data=data,
                            params=params,
                            authenticated=True,
                            is_retry=True,
                        )

                # Check for specific error conditions
                resp_text_for_error: Optional[str] = (
                    None  # To avoid multiple await response.text()
                )

                if response.status == 401:
                    if resp_text_for_error is None:
                        resp_text_for_error = await response.text()
                    error_message = await self._extract_error_message(
                        response, resp_text_for_error
                    )
                    # request_path is now like "/login"
                    if (
                        request_path == "/login"
                        and "bad username or password" in error_message.lower()
                    ):
                        raise AuthError("Bad username or password")
                    else:
                        raise AuthError(f"Authentication Failed (401): {error_message}")

                # For ServerNotFoundError, check if the path relative to the API root starts with /server/
                # e.g. if _api_base_segment is "/api", request_path is "/server/my_server/validate"
                if response.status == 404 and request_path.startswith("/server/"):
                    if resp_text_for_error is None:
                        resp_text_for_error = await response.text()
                    error_message = await self._extract_error_message(
                        response, resp_text_for_error
                    )
                    raise ServerNotFoundError(
                        f"Server Not Found (404) for path {request_path}: {error_message}"
                    )

                if response.status == 501:  # Not Implemented
                    if resp_text_for_error is None:
                        resp_text_for_error = await response.text()
                    error_message = await self._extract_error_message(
                        response, resp_text_for_error
                    )
                    raise APIError(
                        f"Feature Not Implemented (501) for {request_path}: {error_message}"
                    )

                if response.status >= 400:  # Other client/server errors
                    if resp_text_for_error is None:
                        resp_text_for_error = await response.text()
                    error_message = await self._extract_error_message(
                        response, resp_text_for_error
                    )
                    msg_lower = error_message.lower()
                    if (
                        response.status == 500
                        and authenticated
                        and (
                            "is not running" in msg_lower
                            or (
                                "screen session" in msg_lower
                                and "not found" in msg_lower
                            )
                            or "pipe does not exist" in msg_lower
                            or "server likely not running" in msg_lower
                        )
                    ):
                        raise ServerNotRunningError(
                            f"Operation failed for {request_path}: {error_message}"
                        )
                    raise APIError(
                        f"API Error {response.status} for {request_path}: {error_message}"
                    )

                # --- Handle Success ---
                _LOGGER.debug(
                    "API request successful for %s [%s]", request_path, response.status
                )
                if response.status == 204:  # No Content
                    return {
                        "status": "success",
                        "message": "Operation successful (No Content)",
                    }

                try:
                    # Can return dict or list or other simple JSON types
                    json_response: Union[Dict[str, Any], List[Any]] = (
                        await response.json(content_type=None)
                    )
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
                            request_path,
                            error_message,
                        )
                        if "is not running" in error_message.lower():
                            raise ServerNotRunningError(error_message)
                        else:
                            raise APIError(error_message)
                    return json_response
                except (
                    aiohttp.ContentTypeError,
                    ValueError,
                    asyncio.TimeoutError,
                ) as json_error:
                    resp_text = await response.text()
                    _LOGGER.warning(
                        "Successful API response (%s) for %s not valid JSON (%s): %s",
                        response.status,
                        request_path,
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
            _LOGGER.error(
                "API request timed out for %s", url
            )  # Method was in previous log
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
            raise e  # Re-raise our specific exceptions
        except Exception as e:
            _LOGGER.exception("Unexpected error during API request to %s: %s", url, e)
            raise APIError(
                f"An unexpected error occurred during request to {url}: {e}"
            ) from e

    async def _extract_error_message(
        self, response: aiohttp.ClientResponse, fallback_text: str
    ) -> str:
        # Check content type before attempting to read JSON
        if response.content_type != "application/json":
            # If it's HTML and a 405, the fallback_text (which is the HTML) is probably what we want.
            # Otherwise, a more generic message might be better if it's not JSON.
            if response.status == 405 and "text/html" in response.content_type:
                return (
                    fallback_text  # Return the HTML for 405, it has the error message
                )
            return f"Non-JSON error response (Content-Type: {response.content_type}). Raw: {fallback_text[:200]}"

        try:
            error_data = await response.json(
                content_type=None
            )  # Try to parse even if content-type is wrong
            if isinstance(error_data, dict):
                if "detail" in error_data:
                    return str(error_data["detail"])
                if "message" in error_data:
                    return str(error_data["message"])
                if "error" in error_data:
                    return str(error_data["error"])
                return str(error_data)  # Fallback to whole dict string
            return str(
                error_data
            )  # If not a dict but still JSON (e.g., a list of errors)
        except (aiohttp.ContentTypeError, ValueError, asyncio.TimeoutError):
            return fallback_text  # Fallback to raw text if JSON parsing fails

    async def authenticate(self) -> bool:
        _LOGGER.info("Attempting API authentication for user %s", self._username)
        self._jwt_token = None
        try:
            # Path is now relative to base_url (e.g., "/api")
            # So, this becomes POST to <base_url>/login
            response_data = await self._request(
                "POST",
                "/login",
                data={"username": self._username, "password": self._password},
                authenticated=False,
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
        except (APIError, CannotConnectError) as e:  # Catch other errors from _request
            _LOGGER.error("API error during authentication: %s", e)
            self._jwt_token = None
            # Wrap in AuthError for consistency if it's during login
            raise AuthError(f"API error during login: {e}") from e
