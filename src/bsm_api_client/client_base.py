# src/bsm_api_client/client_base.py
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

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.base")


class ClientBase:
    """Base class containing core API client logic."""

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        port: Optional[int] = None,
        session: Optional[aiohttp.ClientSession] = None,
        base_path: str = "/api",
        request_timeout: int = 10,
        use_ssl: bool = False,
        verify_ssl: bool = True,
    ):
        """Initialize the base API client."""
        protocol = "https" if use_ssl else "http"

        # Robustly parse the input host string
        # It might contain a scheme, port, or path, which we want to handle/ignore appropriately.
        if "://" not in host:
            # urlparse needs a scheme to correctly parse netloc, prepend // if missing
            parsed_uri = urlparse(f"//{host}")
        else:
            parsed_uri = urlparse(host)

        actual_hostname = parsed_uri.hostname
        port_from_host_uri = parsed_uri.port

        if not actual_hostname:
            raise ValueError(
                f"Invalid host string provided: '{host}'. Could not determine hostname."
            )

        self._host: str = actual_hostname

        # Determine effective port: explicit port param > port in host string > None
        if port is not None:
            self._port: Optional[int] = port
        elif port_from_host_uri is not None:
            self._port = port_from_host_uri
        else:
            self._port = None

        self._api_base_segment = (
            f"/{base_path.strip('/')}" if base_path.strip("/") else ""
        )

        # Construct port string for URL: ":<port>" or ""
        port_str = f":{self._port}" if self._port is not None else ""
        self._base_url = f"{protocol}://{self._host}{port_str}{self._api_base_segment}"

        self._username = username
        self._password = password
        self._request_timeout = request_timeout
        self._use_ssl = use_ssl
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
                    "The provided session's SSL verification behavior (ideally configured via verify_ssl to async_get_clientsession) "
                    "will take precedence."
                )

        self._jwt_token: Optional[str] = None
        self._default_headers: Mapping[str, str] = {
            "Accept": "application/json",
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

        message = error_data.get("message", "")
        if not message and "error" in error_data:
            message = error_data.get("error", "")
        if not message and "detail" in error_data:
            message = error_data.get("detail", "")
        if not message:
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

        if status == 400:
            raise InvalidInputError(
                message, status_code=status, response_data=error_data
            )
        if status == 401:
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
            raise AuthError(message, status_code=status, response_data=error_data)
        if status == 404:
            if request_path_for_log.startswith("/server/"):
                raise ServerNotFoundError(
                    message, status_code=status, response_data=error_data
                )
            raise NotFoundError(message, status_code=status, response_data=error_data)
        if status == 501:
            raise OperationFailedError(
                message, status_code=status, response_data=error_data
            )

        msg_lower = message.lower()
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
        """Internal method to make API requests."""
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

    async def authenticate(self) -> bool:
        """Authenticates with the API and stores the JWT token."""
        _LOGGER.info("Attempting API authentication for user %s", self._username)
        self._jwt_token = None
        try:
            response_data = await self._request(
                "POST",
                "/login",
                json_data={"username": self._username, "password": self._password},
                authenticated=False,
            )
            if not isinstance(response_data, dict):
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
        except AuthError:
            _LOGGER.error("Authentication failed during direct login attempt.")
            self._jwt_token = None
            raise
        except APIError as e:
            _LOGGER.error("API error during authentication: %s", e)
            self._jwt_token = None
            raise AuthError(f"API error during login: {e.args[0]}") from e
        except CannotConnectError as e:
            _LOGGER.error("Connection error during authentication: %s", e)
            self._jwt_token = None
            # e.args[0] will contain the message from CannotConnectError,
            # which is now correctly formatted with or without port.
            raise AuthError(f"Connection error during login: {e.args[0]}") from e
