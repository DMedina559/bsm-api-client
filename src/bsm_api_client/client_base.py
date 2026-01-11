# src/bsm_api_client/client_base.py
"""Base class for the Bedrock Server Manager API Client.

This module provides the `ClientBase` class, which handles common API client
functionality such as session management, authentication, and a core request
method for interacting with the Bedrock Server Manager API.
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
    Tuple,
)
from urllib.parse import urlparse

# Import exceptions from the same package level
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
from .models import Token
from .websocket_client import WebSocketClient

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.base")


class ClientBase:
    """Base class containing core API client logic.

    This class manages the HTTP session, authentication state, and provides
    low-level methods for making requests to the API. It is not intended to be
    used directly by end-users, but rather extended by the main API client class.

    Attributes:
        _host: The hostname of the Bedrock Server Manager.
        _port: The port of the Bedrock Server Manager.
        _username: The username for authentication.
        _password: The password for authentication.
        _session: The `aiohttp.ClientSession` used for making requests.
        _jwt_token: The JWT token used for authentication.
    """

    def __init__(
        self,
        base_url: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        jwt_token: Optional[str] = None,
        session: Optional[aiohttp.ClientSession] = None,
        base_path: str = "/api",
        request_timeout: int = 90,
        verify_ssl: bool = True,
    ):
        """Initializes the base API client.
        Args:
            base_url: The base URL of the Bedrock Server Manager (e.g., http://localhost:8080).
            username: The username for authentication.
            password: The password for authentication.
            jwt_token: An optional JWT token to use for authentication.
            session: An optional `aiohttp.ClientSession` to use for requests.
            base_path: The base path for the API.
            request_timeout: The timeout for requests in seconds.
            verify_ssl: Whether to verify the SSL certificate.
        """
        if not base_url:
            raise ValueError("base_url must be provided.")

        if not jwt_token and not (username and password):
            raise ValueError(
                "Either a JWT token or a username and password must be provided."
            )

        # Robustly parse the input base_url string
        parsed_uri = urlparse(base_url)
        if not parsed_uri.scheme or not parsed_uri.netloc:
            raise ValueError(
                f"Invalid base_url provided: '{base_url}'. Must include scheme (http/https) and hostname."
            )

        self._host = parsed_uri.hostname
        self._port = parsed_uri.port
        self._use_ssl = parsed_uri.scheme == "https"

        self._api_base_segment = (
            f"/{base_path.strip('/')}" if base_path.strip("/") else ""
        )

        # _server_root_url is the base part of the server's address (e.g., http://localhost:8000)
        self._server_root_url = f"{parsed_uri.scheme}://{parsed_uri.netloc}"
        # _base_url includes the _api_base_segment (e.g., /api) and is used for most standard API calls.
        self._base_url = f"{self._server_root_url}{self._api_base_segment}"

        self._username = username
        self._password = password
        self._request_timeout = request_timeout
        self._verify_ssl = verify_ssl

        if session is None:
            _LOGGER.debug("No session provided, creating an internal ClientSession.")
            connector = None
            if self._use_ssl and not self._verify_ssl:
                _LOGGER.warning(
                    "Creating internal session with SSL certificate verification DISABLED. "
                    "This is insecure for production."
                )
                connector = aiohttp.TCPConnector(ssl=False)
            self._session = aiohttp.ClientSession(connector=connector)
            self._close_session = True
        else:
            self._session = session
            self._close_session = False
            if self._use_ssl and not self._verify_ssl:
                _LOGGER.info(
                    "An external ClientSession is provided, and verify_ssl=False was requested by user. "
                    "The provided session's SSL verification behavior will take precedence."
                )

        self._jwt_token: Optional[str] = jwt_token
        self._default_headers: Mapping[str, str] = {
            "Accept": "application/json",
        }
        self._auth_lock = asyncio.Lock()

        _LOGGER.debug("ClientBase initialized for base URL: %s", self._base_url)

    async def close(self) -> None:
        """Closes the underlying aiohttp.ClientSession if it was created internally."""
        if self._session and self._close_session and not self._session.closed:
            await self._session.close()
            _LOGGER.debug(
                "Closed internally managed ClientSession for %s", self._base_url
            )

    async def __aenter__(self) -> "ClientBase":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    async def _extract_error_details(
        self, response: aiohttp.ClientResponse
    ) -> Tuple[str, Dict[str, Any]]:
        """Extracts error details from an API response.

        Tries to parse a JSON response body to find a detailed error message.
        Falls back to using the response text or reason if JSON parsing fails.

        Args:
            response: The `aiohttp.ClientResponse` object from the failed request.

        Returns:
            A tuple containing the error message string and the full error data dictionary.
        """
        response_text = ""
        error_data: Dict[str, Any] = {}

        try:
            response_text = await response.text()
            if response.content_type == "application/json":
                parsed_json = await response.json(content_type=None)
                if isinstance(parsed_json, dict):
                    error_data = parsed_json
                else:
                    error_data = {"raw_error": parsed_json}
            else:
                error_data = {"raw_error": response_text}

        except (aiohttp.ClientResponseError, ValueError, asyncio.TimeoutError) as e:
            _LOGGER.warning(
                f"Could not parse error response JSON or read text: {e}. Raw text (if available): {response_text[:200]}"
            )
            error_data = {
                "raw_error": response_text
                or response.reason
                or "Unknown error reading response."
            }

        # Prioritize "detail" for FastAPI standard errors (often a string),
        # then "message" (custom in this app), then "error" (generic).
        message = error_data.get("detail", "")
        if (
            not isinstance(message, str) or not message
        ):  # FastAPI's detail can sometimes be a list/dict for validation
            if (
                isinstance(message, (list, dict)) and message
            ):  # If detail is complex, try to serialize it
                try:
                    message = str(message)
                except:  # Fallback if str conversion fails
                    message = ""
            else:
                message = ""

        if not message:  # If detail was not a usable string
            message = error_data.get("message", "")
        if not message:
            message = error_data.get("error", "")

        # Fallback if none of the common keys yield a non-empty string message
        if not message:
            # If 'errors' field exists (like in some custom validation responses), try to summarize it
            if (
                "errors" in error_data
                and isinstance(error_data["errors"], dict)
                and error_data["errors"]
            ):
                try:
                    message = "; ".join(
                        [f"{k}: {v}" for k, v in error_data["errors"].items()]
                    )
                except Exception:  # In case items are not simple k:v strings
                    message = str(
                        error_data["errors"]
                    )  # fallback to string representation
            elif (
                "raw_error" in error_data
            ):  # If we stored raw text due to parsing failure
                message = error_data["raw_error"]
            else:  # Absolute fallback
                message = response.reason or "Unknown API error"

        return str(message), error_data

    async def _handle_api_error(
        self, response: aiohttp.ClientResponse, request_path_for_log: str
    ):
        """Processes an error response and raises the appropriate custom exception.

        This method maps HTTP status codes and specific error messages from the
        API response to the appropriate exception classes defined in the
        `exceptions` module.

        Args:
            response: The `aiohttp.ClientResponse` object from the failed request.
            request_path_for_log: The path of the request for logging purposes.

        Raises:
            InvalidInputError: For 400 or 422 status codes.
            AuthError: For 401 or 403 status codes.
            ServerNotFoundError: For 404 status codes on server-specific endpoints.
            NotFoundError: For other 404 status codes.
            OperationFailedError: For 501 status codes.
            ServerNotRunningError: If the error message indicates the server is not running.
            APIServerSideError: For 5xx status codes.
            APIError: For any other 4xx status codes.
        """
        message, error_data = await self._extract_error_details(response)
        status = response.status

        if status == 400:  # Bad Request
            raise InvalidInputError(
                message, status_code=status, response_data=error_data
            )
        if status == 401:  # Unauthorized
            # Check if it's a login attempt specifically, to give a more specific error.
            # Note: /auth/token is the new login path.
            if (
                request_path_for_log.endswith("/login")
                or request_path_for_log.endswith("/auth/token")
            ) and (
                "bad username or password" in message.lower()
                or "incorrect username or password" in message.lower()
            ):
                raise AuthError(
                    "Bad username or password",  # Keep generic message for this case
                    status_code=status,
                    response_data=error_data,
                )
            raise AuthError(message, status_code=status, response_data=error_data)
        if status == 403:  # Forbidden
            raise AuthError(
                message, status_code=status, response_data=error_data
            )  # AuthError is suitable for 403 too
        if status == 404:  # Not Found
            if (
                request_path_for_log.startswith("/server/")
                or "/server/" in request_path_for_log
            ):  # More general check
                raise ServerNotFoundError(  # Specific error for server-related 404s
                    message, status_code=status, response_data=error_data
                )
            raise NotFoundError(
                message, status_code=status, response_data=error_data
            )  # Generic 404
        if status == 422:  # Unprocessable Entity (Common for FastAPI validation errors)
            # HTTPValidationError from FastAPI will often have details in error_data["detail"]
            # (which _extract_error_details attempts to capture in 'message').
            # 'error_data' contains the full validation error structure from FastAPI.
            # Prefixing message for clarity that it's a validation issue.
            raise InvalidInputError(
                f"Validation Error: {message}",
                status_code=status,
                response_data=error_data,
            )
        if status == 501:  # Not Implemented
            raise OperationFailedError(
                message, status_code=status, response_data=error_data
            )

        # Check message content for ServerNotRunningError, as this can come with various status codes
        # (e.g., 409 Conflict, or even 200 OK with error in body from older API versions)
        # For new FastAPI, 409 is more standard for "server not running" if it's a prerequisite.
        msg_lower = str(message).lower()  # Ensure message is string for lower()
        if (
            "is not running" in msg_lower
            or ("screen session" in msg_lower and "not found" in msg_lower)
            or "pipe does not exist" in msg_lower
            or "server likely not running" in msg_lower
        ):
            if status >= 400:
                raise ServerNotRunningError(
                    message, status_code=status, response_data=error_data
                )

        if status >= 500:
            raise APIServerSideError(
                message, status_code=status, response_data=error_data
            )

        if status >= 400:
            raise APIError(message, status_code=status, response_data=error_data)

        _LOGGER.error(
            f"Unhandled API error condition: Status {status}, Message: {message}"
        )
        raise APIError(message, status_code=status, response_data=error_data)

    async def _request(
        self,
        method: str,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        authenticated: bool = True,
        is_retry: bool = False,
    ) -> Any:
        """Internal method to make API requests.

        This method constructs the full URL, adds authentication headers if
        required, and handles the request/response cycle, including error
        handling and automatic token refresh on 401 errors.

        Args:
            method: The HTTP method for the request (e.g., "GET", "POST").
            path: The API endpoint path.
            json_data: An optional dictionary to be sent as the JSON request body.
            params: An optional dictionary of query parameters.
            authenticated: Whether the request requires authentication.
            is_retry: Whether this is a retry attempt after a token refresh.

        Returns:
            The JSON response from the API as a dictionary or list.

        Raises:
            CannotConnectError: If a connection to the server cannot be established.
            APIError: For various API-related errors.
        """
        request_path_segment = path if path.startswith("/") else f"/{path}"
        url = f"{self._base_url}{request_path_segment}"

        headers: Dict[str, str] = dict(self._default_headers)
        if json_data is not None:
            headers["Content-Type"] = "application/json"

        if authenticated:
            async with self._auth_lock:
                if not self._jwt_token and not is_retry:
                    _LOGGER.debug(
                        "No token for auth request to %s, attempting login.", url
                    )
                    try:
                        await self.authenticate()
                    except AuthError:
                        raise
            if authenticated and not self._jwt_token:
                _LOGGER.error(
                    "Auth required for %s but no token after lock/login attempt.", url
                )
                raise AuthError(
                    "Authentication required but no token available after login attempt."
                )
            if authenticated and self._jwt_token:
                headers["Authorization"] = f"Bearer {self._jwt_token}"

        _LOGGER.debug(
            "Request: %s %s (Params: %s, Auth: %s)", method, url, params, authenticated
        )
        try:
            async with self._session.request(
                method,
                url,
                json=json_data,
                params=params,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=self._request_timeout),
            ) as response:
                _LOGGER.debug(
                    "Response Status for %s %s: %s", method, url, response.status
                )

                if not response.ok:
                    if response.status == 401 and authenticated and not is_retry:
                        _LOGGER.warning(
                            "Received 401 for %s, attempting token refresh and retry.",
                            url,
                        )
                        async with self._auth_lock:
                            self._jwt_token = None
                        return await self._request(
                            method,
                            request_path_segment,
                            json_data=json_data,
                            params=params,
                            authenticated=True,
                            is_retry=True,
                        )
                    await self._handle_api_error(response, request_path_segment)
                    raise APIError(  # Should be unreachable
                        "Error handler did not raise, this should not happen."
                    )

                _LOGGER.debug(
                    "API request successful for %s [%s]",
                    request_path_segment,
                    response.status,
                )
                if response.status == 204 or response.content_length == 0:
                    return {
                        "status": "success",
                        "message": "Operation successful (No Content)",
                    }

                try:
                    json_response: Union[Dict[str, Any], List[Any]] = (
                        await response.json(content_type=None)
                    )
                    if (
                        isinstance(json_response, dict)
                        and json_response.get("status") == "error"
                    ):
                        message = json_response.get(
                            "message", "Unknown error in successful HTTP response."
                        )
                        _LOGGER.error(
                            "API success status (%s) but error in JSON body for %s: %s. Data: %s",
                            response.status,
                            request_path_segment,
                            message,
                            json_response,
                        )
                        if "is not running" in message.lower():
                            raise ServerNotRunningError(
                                message,
                                status_code=response.status,
                                response_data=json_response,
                            )
                        raise APIError(
                            message,
                            status_code=response.status,
                            response_data=json_response,
                        )

                    if (
                        isinstance(json_response, dict)
                        and json_response.get("status") == "confirm_needed"
                    ):
                        _LOGGER.info(
                            "API returned 'confirm_needed' status for %s",
                            request_path_segment,
                        )
                        # Calling method handles this specific status.
                    return json_response
                except (
                    aiohttp.ContentTypeError,
                    ValueError,
                    asyncio.TimeoutError,
                ) as json_error:
                    resp_text = await response.text()
                    _LOGGER.warning(
                        "Successful API response (%s) for %s not valid JSON (%s). Raw: %s",
                        response.status,
                        request_path_segment,
                        json_error,
                        resp_text[:200],
                    )
                    return {
                        "status": "success_with_parsing_issue",
                        "message": "Operation successful (Non-JSON or malformed JSON response)",
                        "raw_response": resp_text,
                    }

        except aiohttp.ClientConnectionError as e:
            # Construct target address string for error message
            target_address = (
                f"{self._host}{f':{self._port}' if self._port is not None else ''}"
            )
            _LOGGER.error(
                "API connection error for %s: %s", url, e
            )  # url already has full path
            raise CannotConnectError(
                f"Connection Error: Cannot connect to host {target_address}.",  # Use specific target_address
                original_exception=e,
            ) from e
        except asyncio.TimeoutError as e:
            _LOGGER.error("API request timed out for %s: %s", url, e)
            raise CannotConnectError(
                f"Request timed out for {url}", original_exception=e
            ) from e
        except aiohttp.ClientError as e:
            _LOGGER.error("Generic aiohttp client error for %s: %s", url, e)
            raise CannotConnectError(
                f"AIOHTTP Client Error: {e}", original_exception=e
            ) from e
        except (
            APIError,
            AuthError,
            NotFoundError,
            ServerNotFoundError,
            ServerNotRunningError,
            CannotConnectError,
            InvalidInputError,
            OperationFailedError,
            APIServerSideError,
        ) as e:
            raise e
        except Exception as e:
            _LOGGER.exception("Unexpected error during API request to %s: %s", url, e)
            raise APIError(
                f"An unexpected error occurred during request to {url}: {e}"
            ) from e

    async def authenticate(self) -> Token:
        """Authenticates with the API and retrieves a JWT token.

        This method sends a POST request to the `/auth/token` endpoint with the
        username and password provided during client initialization. The retrieved
        JWT token is stored internally for subsequent authenticated requests.

        Returns:
            A `Token` object containing the access token and token type.

        Raises:
            AuthError: If authentication fails due to invalid credentials,
                connection issues, or other API errors.
        """
        _LOGGER.info("Attempting API authentication for user %s", self._username)
        self._jwt_token = None
        try:
            # FastAPI's OAuth2PasswordRequestForm expects x-www-form-urlencoded data.
            form_data = aiohttp.FormData()
            form_data.add_field("username", self._username)
            form_data.add_field("password", self._password)

            # Make the request without using self._request to avoid auth loop and content-type issues
            # Use _server_root_url for auth path as it's not under the general _api_base_segment (e.g. /api)
            url = f"{self._server_root_url}/auth/token"
            headers = {"Accept": "application/json"}  # Still expect JSON response

            _LOGGER.debug("Request: POST %s (Form Data Auth to root path)", url)
            async with self._session.post(
                url,
                data=form_data,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=self._request_timeout),
            ) as response:
                _LOGGER.debug("Response Status for POST %s: %s", url, response.status)
                if not response.ok:
                    # Use _handle_api_error for consistent error raising based on status
                    await self._handle_api_error(response, "/auth/token")
                    # Should be unreachable if _handle_api_error raises
                    raise AuthError(
                        f"Authentication failed with status {response.status}"
                    )

                try:
                    response_data = await response.json(content_type=None)
                except (
                    aiohttp.ContentTypeError,
                    ValueError,
                    asyncio.TimeoutError,
                ) as json_error:
                    resp_text = await response.text()
                    _LOGGER.error(
                        "Auth response was not valid JSON: %s. Raw: %s",
                        json_error,
                        resp_text[:200],
                    )
                    raise AuthError(
                        f"Authentication response was not valid JSON: {json_error}"
                    )

            token = Token.model_validate(response_data)
            self._jwt_token = token.access_token
            _LOGGER.info("Authentication successful, token received.")
            return token

        except AuthError:  # Re-raise specific AuthErrors
            _LOGGER.error("Authentication failed.")
            self._jwt_token = None
            raise
        except APIError as e:  # Catch errors from _handle_api_error
            _LOGGER.error("API error during authentication: %s", e)
            self._jwt_token = None
            # Wrap it in AuthError if it's not already one (e.g. 400 from _handle_api_error)
            if not isinstance(e, AuthError):
                raise AuthError(f"API error during login: {e.args[0]}") from e
            raise e
        except aiohttp.ClientConnectionError as e:
            target_address = (
                f"{self._host}{f':{self._port}' if self._port is not None else ''}"
            )
            _LOGGER.error(
                "Connection error during authentication to %s: %s", target_address, e
            )
            self._jwt_token = None
            raise AuthError(
                f"Connection error during login to {target_address}: {e}"
            ) from e
        except asyncio.TimeoutError as e:
            _LOGGER.error("Timeout during authentication: %s", e)
            self._jwt_token = None
            raise AuthError(f"Timeout during login: {e}") from e
        except Exception as e:
            _LOGGER.exception("Unexpected error during authentication: %s", e)
            self._jwt_token = None
            raise AuthError(f"An unexpected error occurred during login: {e}") from e

    async def async_logout(self) -> Dict[str, Any]:
        """Logs the current user out.

        This method calls the `GET /auth/logout` endpoint to invalidate the
        session on the server side and clears the internally stored JWT token.

        Returns:
            A dictionary containing the response from the API, typically a
            success message.

        Raises:
            APIError: If the logout request fails.
        """
        _LOGGER.info("Attempting API logout.")
        try:
            # Logout path is /auth/logout, relative to server root, not under the main API base segment.
            # Called directly using _session.get for consistency with authenticate().
            url = f"{self._server_root_url}/auth/logout"
            headers = dict(self._default_headers)
            if (
                self._jwt_token
            ):  # Should be present if authenticated=True logic was to be mimicked
                headers["Authorization"] = f"Bearer {self._jwt_token}"

            _LOGGER.debug("Request: GET %s (Logout to root path)", url)
            async with self._session.get(
                url,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=self._request_timeout),
            ) as response:
                _LOGGER.debug("Response Status for GET %s: %s", url, response.status)
                if not response.ok:
                    await self._handle_api_error(response, "/auth/logout")
                    # Should be unreachable
                    raise APIError(f"Logout failed with status {response.status}")

                try:
                    response_data = (
                        await response.json(content_type=None)
                        if response.content_length != 0
                        else {}
                    )
                except (
                    aiohttp.ContentTypeError,
                    ValueError,
                    asyncio.TimeoutError,
                ) as json_error:
                    resp_text = await response.text()
                    _LOGGER.warning(
                        "Logout response was not valid JSON: %s. Raw: %s",
                        json_error,
                        resp_text[:200],
                    )
                    # Still consider logout successful on server if HTTP 200 OK, even if response body is weird
                    response_data = {
                        "status": "success_with_parsing_issue",
                        "message": "Logout successful, but response parsing failed.",
                    }

            # Clear local token regardless of exact response content, if HTTP call was ok
            self._jwt_token = None
            _LOGGER.info("Logout request successful. Local token cleared.")
            return response_data  # Typically an empty dict or success message
        except APIError as e:
            _LOGGER.error("API error during logout: %s", e)
            # Decide if to clear local token even on error.
            # If auth error (401), token might be invalid anyway.
            if isinstance(e, AuthError):
                self._jwt_token = None
                _LOGGER.warning("AuthError during logout, cleared local token anyway.")
            raise
        except Exception as e:
            _LOGGER.exception("Unexpected error during logout: %s", e)
            raise APIError(f"An unexpected error occurred during logout: {e}") from e

    async def websocket_connect(self) -> WebSocketClient:
        """
        Connects to the WebSocket endpoint.

        Returns:
            A WebSocketClient instance.
        """
        # Ensure we have a token or try to authenticate
        async with self._auth_lock:
            if not self._jwt_token:
                await self.authenticate()

        ws_scheme = "wss" if self._use_ssl else "ws"
        # Typically the websocket endpoint is at /ws relative to the server root
        ws_url = (
            f"{ws_scheme}://{self._host}{f':{self._port}' if self._port else ''}/ws"
        )

        return WebSocketClient(self._session, ws_url, self._jwt_token)
