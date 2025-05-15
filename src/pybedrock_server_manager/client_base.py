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
    Tuple,
)

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
        use_ssl: bool = False,
        verify_ssl: bool = True,
    ):
        """Initialize the base API client."""
        protocol = "https" if use_ssl else "http"
        clean_host = host.replace("http://", "").replace("https://", "")
        self._host = clean_host
        self._port = port
        self._api_base_segment = (
            f"/{base_path.strip('/')}" if base_path.strip("/") else ""
        )
        self._base_url = (
            f"{protocol}://{self._host}:{self._port}{self._api_base_segment}"
        )

        self._username = username
        self._password = password
        self._request_timeout = request_timeout
        self._use_ssl = use_ssl  # Store use_ssl for connector logic
        self._verify_ssl = verify_ssl  # Store verify_ssl

        if session is None:
            connector = None  # Default connector
            if self._use_ssl:  # Only apply SSL logic if use_ssl is True
                if not self._verify_ssl:
                    _LOGGER.warning(
                        "SSL certificate verification is DISABLED. "
                        "This is insecure and not recommended for production environments."
                    )
                    # For aiohttp, ssl=False in TCPConnector disables certificate verification for HTTPS
                    connector = aiohttp.TCPConnector(ssl=False)
                # If self._verify_ssl is True (default for HTTPS),
                # connector remains None, and ClientSession uses its default secure connector.

            self._session = aiohttp.ClientSession(connector=connector)
            self._close_session = True
        else:
            self._session = session
            self._close_session = False
            if self._use_ssl and not self._verify_ssl:
                _LOGGER.warning(
                    "An external ClientSession is provided, but verify_ssl=False was also requested. "
                    "The external session's SSL verification behavior will take precedence. "
                    "Ensure the provided session is configured to disable SSL verification if that's intended."
                )

        self._jwt_token: Optional[str] = None
        # Default headers; Content-Type can be overridden by specific requests if needed (e.g., file uploads)
        self._default_headers: Mapping[str, str] = {
            "Accept": "application/json",
            # "Content-Type": "application/json", # Set per request if it has a body
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

    async def _extract_error_details(
        self, response: aiohttp.ClientResponse
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Extracts a primary error message and the full error data from an error response.
        Tries to parse JSON, falls back to text.
        Returns (error_message_str, error_data_dict).
        """
        response_text = ""
        error_data: Dict[str, Any] = {}

        try:
            response_text = await response.text()
            if response.content_type == "application/json":
                # Try to parse, response.json() might fail if text is empty or malformed
                parsed_json = await response.json(
                    content_type=None
                )  # content_type=None for robustness
                if isinstance(parsed_json, dict):
                    error_data = parsed_json
                else:  # API returned JSON but not a dict (e.g. list of errors)
                    error_data = {"raw_error": parsed_json}
            else:  # Not JSON content type
                error_data = {"raw_error": response_text}

        except (aiohttp.ClientResponseError, ValueError, asyncio.TimeoutError) as e:
            _LOGGER.warning(
                f"Could not parse error response JSON or read text: {e}. Raw text (if available): {response_text[:200]}"
            )
            # Use response.reason if text reading failed completely
            error_data = {
                "raw_error": response_text
                or response.reason
                or "Unknown error reading response."
            }

        # Determine primary message string
        message = error_data.get("message", "")
        if not message and "error" in error_data:  # Some auth errors use "error"
            message = error_data.get("error", "")
        if not message and "detail" in error_data:  # Common in DRF, FastAPI
            message = error_data.get("detail", "")
        if not message:  # Fallback to raw error if it was a dict, or the general reason
            message = error_data.get(
                "raw_error", response.reason or "Unknown API error"
            )

        return str(message), error_data

    async def _handle_api_error(
        self, response: aiohttp.ClientResponse, request_path_for_log: str
    ):
        """
        Processes an error response and raises the appropriate custom exception.
        """
        message, error_data = await self._extract_error_details(response)
        status = response.status

        # Use the refined exceptions with message, status_code, and response_data
        if status == 400:
            raise InvalidInputError(
                message, status_code=status, response_data=error_data
            )
        if status == 401:
            # Special check for /login failure for more specific message
            if (
                request_path_for_log.endswith("/login")
                and "bad username or password" in message.lower()
            ):
                raise AuthError(
                    "Bad username or password",
                    status_code=status,
                    response_data=error_data,
                )
            raise AuthError(message, status_code=status, response_data=error_data)
        if status == 403:
            raise AuthError(
                message, status_code=status, response_data=error_data
            )  # Or a PermissionDeniedError
        if status == 404:
            if request_path_for_log.startswith("/server/"):  # Path relative to API base
                raise ServerNotFoundError(
                    message, status_code=status, response_data=error_data
                )
            raise NotFoundError(message, status_code=status, response_data=error_data)
        if status == 501:
            raise OperationFailedError(
                message, status_code=status, response_data=error_data
            )

        # Infer ServerNotRunningError (example based on your API's error messages)
        # This might need adjustment based on how consistently your API signals this.
        msg_lower = message.lower()
        if (
            "is not running" in msg_lower
            or ("screen session" in msg_lower and "not found" in msg_lower)
            or "pipe does not exist" in msg_lower
            or "server likely not running" in msg_lower
        ):
            # Check if this error should indeed be ServerNotRunningError,
            # even if status is e.g. 500. If so, raise it specifically.
            # This is a strong assumption; ensure your API is consistent.
            # Alternatively, let ServerNotRunningError be raised by the mixin methods
            # based on the *content* of a successful (e.g. 200 OK) but operationally failed response.
            if status >= 400:  # Only if it's an error status
                raise ServerNotRunningError(
                    message, status_code=status, response_data=error_data
                )

        if status >= 500:
            raise APIServerSideError(
                message, status_code=status, response_data=error_data
            )

        # Default for other 4xx errors not caught above
        if status >= 400:
            raise APIError(message, status_code=status, response_data=error_data)

        # Should not be reached if response.ok is false, but as a fallback
        _LOGGER.error(
            f"Unhandled API error condition: Status {status}, Message: {message}"
        )
        raise APIError(message, status_code=status, response_data=error_data)

    async def _request(
        self,
        method: str,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,  # Renamed from 'data' for clarity
        params: Optional[Dict[str, Any]] = None,
        authenticated: bool = True,
        is_retry: bool = False,
    ) -> Any:
        """Internal method to make API requests."""
        request_path_segment = path if path.startswith("/") else f"/{path}"
        url = f"{self._base_url}{request_path_segment}"

        headers: Dict[str, str] = dict(self._default_headers)
        if json_data is not None:  # Only set Content-Type if there's a JSON body
            headers["Content-Type"] = "application/json"

        if authenticated:
            async with self._auth_lock:
                if not self._jwt_token and not is_retry:
                    _LOGGER.debug(
                        "No token for auth request to %s, attempting login.", url
                    )
                    try:
                        await self.authenticate()
                    except AuthError:  # Authenticate already logs, just re-raise
                        raise
            if (
                authenticated and not self._jwt_token
            ):  # Check again after potential auth
                _LOGGER.error(
                    "Auth required for %s but no token after lock/login attempt.", url
                )
                raise AuthError(
                    "Authentication required but no token available after login attempt."
                )
            if (
                authenticated and self._jwt_token
            ):  # Token might have been set by authenticate()
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
                # raise_for_status=False, # We handle status checks manually
                timeout=aiohttp.ClientTimeout(total=self._request_timeout),
            ) as response:
                _LOGGER.debug(
                    "Response Status for %s %s: %s", method, url, response.status
                )

                if not response.ok:  # Covers 4xx and 5xx status codes
                    if response.status == 401 and authenticated and not is_retry:
                        _LOGGER.warning(
                            "Received 401 for %s, attempting token refresh and retry.",
                            url,
                        )
                        async with self._auth_lock:  # Re-acquire lock for token modification
                            self._jwt_token = None  # Force re-authentication
                            # The recursive call will re-evaluate authentication
                        return await self._request(
                            method,
                            request_path_segment,  # Use the already processed segment
                            json_data=json_data,
                            params=params,
                            authenticated=True,  # Still true, retry will handle auth
                            is_retry=True,
                        )
                    # For all other non-ok statuses, or if it's a retry of 401
                    await self._handle_api_error(response, request_path_segment)
                    # _handle_api_error always raises, so this line below is for linters/type checkers.
                    # In reality, execution won't reach here if _handle_api_error is called.
                    raise APIError(
                        "Error handler did not raise, this should not happen."
                    )

                # --- Handle Success (response.ok is True) ---
                _LOGGER.debug(
                    "API request successful for %s [%s]",
                    request_path_segment,
                    response.status,
                )
                if (
                    response.status == 204 or response.content_length == 0
                ):  # No Content or empty body
                    return {  # Or return None, or an empty dict {}
                        "status": "success",
                        "message": "Operation successful (No Content)",
                    }

                try:
                    # Can return dict or list or other simple JSON types
                    json_response: Union[Dict[str, Any], List[Any]] = (
                        await response.json(content_type=None)
                    )
                    # Check for API-level errors reported in a 2xx response's JSON body
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
                        # Decide which exception to raise based on content
                        if "is not running" in message.lower():  # Example
                            raise ServerNotRunningError(
                                message,
                                status_code=response.status,
                                response_data=json_response,
                            )
                        # You might want to map other specific 'message' contents to specific exceptions here
                        raise APIError(
                            message,
                            status_code=response.status,
                            response_data=json_response,
                        )

                    # Check for "confirm_needed" status specifically for server install
                    if (
                        isinstance(json_response, dict)
                        and json_response.get("status") == "confirm_needed"
                    ):
                        _LOGGER.info(
                            "API returned 'confirm_needed' status for %s",
                            request_path_segment,
                        )
                        # This specific status is handled by the calling method (e.g., install_server)
                        # which will not treat it as an error but as a specific state.
                        # The BedrockManagerClientError in the HTTP docs for this case seems like a general description
                        # rather than an actual exception raised by the client for this 200 OK response.
                        # So, we just return the data.

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
                    # This is a choice: return raw text or raise an error.
                    # If API contract guarantees JSON, this could be an APIError.
                    # For now, returning it as part of a success-like structure.
                    return {
                        "status": "success_with_parsing_issue",
                        "message": "Operation successful (Non-JSON or malformed JSON response)",
                        "raw_response": resp_text,
                    }

        except aiohttp.ClientConnectionError as e:
            _LOGGER.error("API connection error for %s: %s", url, e)
            raise CannotConnectError(
                f"Connection Error: Cannot connect to host {self._host}:{self._port}",
                original_exception=e,
            ) from e
        except asyncio.TimeoutError as e:
            _LOGGER.error("API request timed out for %s: %s", url, e)
            raise CannotConnectError(
                f"Request timed out for {url}", original_exception=e
            ) from e
        except aiohttp.ClientError as e:  # Catch other aiohttp client errors
            _LOGGER.error("Generic aiohttp client error for %s: %s", url, e)
            raise CannotConnectError(
                f"AIOHTTP Client Error: {e}", original_exception=e
            ) from e
        # Re-raise exceptions already handled/created by us
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

    async def authenticate(self) -> bool:
        """Authenticates with the API and stores the JWT token."""
        _LOGGER.info("Attempting API authentication for user %s", self._username)
        self._jwt_token = None  # Clear any existing token
        try:
            response_data = await self._request(
                "POST",
                "/login",  # Path relative to the API base URL
                json_data={"username": self._username, "password": self._password},
                authenticated=False,  # This request itself does not require prior auth
            )
            if not isinstance(response_data, dict):  # Should be a dict from API
                _LOGGER.error(
                    "Auth response was not a dictionary: %s", type(response_data)
                )
                raise AuthError("Login response was not in the expected format.")

            token = response_data.get("access_token")
            if not token or not isinstance(token, str):
                _LOGGER.error(
                    "Auth successful but 'access_token' missing/invalid in response: %s",
                    response_data,
                )
                raise AuthError(
                    "Login response missing or contained an invalid access_token."
                )

            _LOGGER.info("Authentication successful, token received.")
            self._jwt_token = token
            return True
        except AuthError:  # Re-raise AuthError specifically from login
            _LOGGER.error("Authentication failed during direct login attempt.")
            self._jwt_token = None
            raise
        except APIError as e:  # Catch other APIErrors from _request during login
            _LOGGER.error("API error during authentication: %s", e)
            self._jwt_token = None
            # Wrap in AuthError for consistency if it's an error during the login process
            raise AuthError(f"API error during login: {e.args[0]}") from e
        except CannotConnectError as e:
            _LOGGER.error("Connection error during authentication: %s", e)
            self._jwt_token = None
            raise AuthError(f"Connection error during login: {e.args[0]}") from e
