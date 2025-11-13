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

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.base")


class ClientBase:
    """Base class containing core API client logic."""

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
        if not base_url:
            raise ValueError("base_url must be provided.")

        if not jwt_token and not (username and password):
            raise ValueError(
                "Either a JWT token or a username and password must be provided."
            )

        parsed_uri = urlparse(base_url)
        if not parsed_uri.scheme or not parsed_uri.netloc:
            raise ValueError(
                f"Invalid base_url provided: '{base_url}'. Must include scheme (http/https) and hostname."
            )

        self._host = parsed_uri.hostname
        self._port = parsed_uri.port
        self._use_ssl = parsed_uri.scheme == "https"
        self._api_base_segment = f"/{base_path.strip('/')}" if base_path.strip("/") else ""
        self._server_root_url = f"{parsed_uri.scheme}://{parsed_uri.netloc}"
        self._base_url = f"{self._server_root_url}{self._api_base_segment}"

        self._username = username
        self._password = password
        self._request_timeout = request_timeout
        self._verify_ssl = verify_ssl

        if session is None:
            _LOGGER.debug("No session provided, creating an internal ClientSession.")
            connector = None
            if self._use_ssl and not self._verify_ssl:
                _LOGGER.warning("Creating internal session with SSL certificate verification DISABLED.")
                connector = aiohttp.TCPConnector(ssl=False)
            self._session = aiohttp.ClientSession(connector=connector)
            self._close_session = True
        else:
            self._session = session
            self._close_session = False
            if self._use_ssl and not self._verify_ssl:
                _LOGGER.info("External ClientSession provided, SSL verification behavior will take precedence.")

        self._jwt_token: Optional[str] = jwt_token
        self._default_headers: Mapping[str, str] = {"Accept": "application/json"}
        self._auth_lock = asyncio.Lock()

        _LOGGER.debug("ClientBase initialized for base URL: %s", self._base_url)

    async def close(self) -> None:
        """Closes the underlying aiohttp.ClientSession if it was created internally."""
        if self._session and self._close_session and not self._session.closed:
            await self._session.close()
            _LOGGER.debug("Closed internally managed ClientSession for %s", self._base_url)

    async def __aenter__(self) -> "ClientBase":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    def _build_url(self, path: str, use_api_base: bool) -> str:
        """Constructs the full URL for a given API path."""
        base = self._base_url if use_api_base else self._server_root_url
        request_path_segment = path if path.startswith("/") else f"/{path}"
        return f"{base}{request_path_segment}"

    async def _get_headers(self, authenticated: bool, has_json_data: bool, is_retry: bool = False) -> Dict[str, str]:
        """Constructs the request headers."""
        headers: Dict[str, str] = dict(self._default_headers)
        if has_json_data:
            headers["Content-Type"] = "application/json"

        if authenticated:
            async with self._auth_lock:
                if not self._jwt_token and not is_retry:
                    _LOGGER.debug("No token for authenticated request, attempting login.")
                    try:
                        await self.authenticate()
                    except AuthError:
                        raise
            if not self._jwt_token:
                _LOGGER.error("Authentication required but no token is available.")
                raise AuthError("Authentication required but no token is available.")
            headers["Authorization"] = f"Bearer {self._jwt_token}"

        return headers

    async def _request(
        self,
        method: str,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        authenticated: bool = True,
        use_api_base: bool = True,
        is_retry: bool = False,
    ) -> Any:
        """Internal method to make API requests."""
        url = self._build_url(path, use_api_base)
        headers = await self._get_headers(authenticated, json_data is not None, is_retry)

        _LOGGER.debug("Request: %s %s (Params: %s, Auth: %s)", method, url, params, authenticated)
        try:
            async with self._session.request(
                method,
                url,
                json=json_data,
                data=data,
                params=params,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=self._request_timeout),
            ) as response:
                _LOGGER.debug("Response Status for %s %s: %s", method, url, response.status)

                if not response.ok:
                    if response.status == 401 and authenticated and not is_retry:
                        _LOGGER.warning("Received 401 Unauthorized, attempting token refresh and retry.")
                        async with self._auth_lock:
                            self._jwt_token = None
                        return await self._request(
                            method,
                            path,
                            json_data=json_data,
                            data=data,
                            params=params,
                            authenticated=True,
                            use_api_base=use_api_base,
                            is_retry=True,
                        )
                    await self._handle_api_error(response, path)
                    # This line should be unreachable if _handle_api_error raises correctly.
                    raise APIError("Error handler did not raise, this should not happen.")

                return await self._handle_response_body(response, path)

        except (aiohttp.ClientConnectionError, asyncio.TimeoutError) as e:
            self._handle_connection_error(e, url)
        except aiohttp.ClientError as e:
            _LOGGER.error("Generic aiohttp client error for %s: %s", url, e)
            raise CannotConnectError(f"AIOHTTP Client Error: {e}", original_exception=e) from e
        except APIError:
            raise
        except Exception as e:
            _LOGGER.exception("Unexpected error during API request to %s: %s", url, e)
            raise APIError(f"An unexpected error occurred during request to {url}: {e}") from e

    async def _handle_response_body(self, response: aiohttp.ClientResponse, request_path_segment: str) -> Any:
        """Processes the body of a successful API response."""
        _LOGGER.debug("API request successful for %s [%s]", request_path_segment, response.status)
        if response.status == 204 or response.content_length == 0:
            return {"status": "success", "message": "Operation successful (No Content)"}

        try:
            json_response: Union[Dict[str, Any], list] = await response.json(content_type=None)
            if isinstance(json_response, dict) and json_response.get("status") == "error":
                message = json_response.get("message", "Unknown error in successful HTTP response.")
                _LOGGER.error("API success status but error in JSON body for %s: %s", request_path_segment, message)
                if "is not running" in message.lower():
                    raise ServerNotRunningError(message, status_code=response.status, response_data=json_response)
                raise APIError(message, status_code=response.status, response_data=json_response)

            return json_response
        except (aiohttp.ContentTypeError, ValueError, asyncio.TimeoutError) as json_error:
            resp_text = await response.text()
            _LOGGER.warning("Successful API response (%s) for %s not valid JSON (%s).", response.status, request_path_segment, json_error)
            return {
                "status": "success_with_parsing_issue",
                "message": "Operation successful (Non-JSON or malformed JSON response)",
                "raw_response": resp_text,
            }

    def _handle_connection_error(self, e: Exception, url: str) -> None:
        """Handles connection errors and raises a consistent exception."""
        target_address = f"{self._host}{f':{self._port}' if self._port else ''}"
        if isinstance(e, asyncio.TimeoutError):
            _LOGGER.error("API request timed out for %s: %s", url, e)
            raise CannotConnectError(f"Request timed out for {url}", original_exception=e) from e

        _LOGGER.error("API connection error for %s: %s", url, e)
        raise CannotConnectError(
            f"Connection Error: Cannot connect to host {target_address}.", original_exception=e
        ) from e

    async def _extract_error_details(
        self, response: aiohttp.ClientResponse
    ) -> Tuple[str, Dict[str, Any]]:
        """Extracts error details from an API response."""
        response_text = ""
        error_data: Dict[str, Any] = {}

        try:
            response_text = await response.text()
            if response.content_type == "application/json":
                parsed_json = await response.json(content_type=None)
                error_data = parsed_json if isinstance(parsed_json, dict) else {"raw_error": parsed_json}
            else:
                error_data = {"raw_error": response_text}
        except (aiohttp.ClientResponseError, ValueError, asyncio.TimeoutError) as e:
            _LOGGER.warning("Could not parse error response JSON: %s.", e)
            error_data = {"raw_error": response_text or response.reason or "Unknown error reading response."}

        message = error_data.get("detail", error_data.get("message", error_data.get("error", "")))
        if not message or not isinstance(message, str):
            message = str(message) if message else ""

        if not message:
            if "errors" in error_data and isinstance(error_data["errors"], dict):
                message = "; ".join([f"{k}: {v}" for k, v in error_data["errors"].items()])
            else:
                message = error_data.get("raw_error", response.reason or "Unknown API error")

        return str(message), error_data

    async def _handle_api_error(
        self, response: aiohttp.ClientResponse, request_path_for_log: str
    ):
        """Processes an error response and raises the appropriate custom exception."""
        message, error_data = await self._extract_error_details(response)
        status = response.status

        error_map = {
            400: InvalidInputError,
            401: AuthError,
            403: AuthError,
            404: NotFoundError,
            422: InvalidInputError,
            501: OperationFailedError,
        }

        if status in error_map:
            if status == 404 and ("/server/" in request_path_for_log):
                raise ServerNotFoundError(message, status_code=status, response_data=error_data)
            raise error_map[status](message, status_code=status, response_data=error_data)

        if "is not running" in message.lower():
            raise ServerNotRunningError(message, status_code=status, response_data=error_data)

        if status >= 500:
            raise APIServerSideError(message, status_code=status, response_data=error_data)

        raise APIError(message, status_code=status, response_data=error_data)

    async def authenticate(self) -> Token:
        """Authenticates with the API and retrieves a JWT token."""
        _LOGGER.info("Attempting API authentication for user %s", self._username)
        self._jwt_token = None
        try:
            form_data = aiohttp.FormData()
            form_data.add_field("username", self._username)
            form_data.add_field("password", self._password)

            response_data = await self._request(
                "POST", "/auth/token", data=form_data, authenticated=False, use_api_base=False
            )
            token = Token.model_validate(response_data)
            self._jwt_token = token.access_token
            _LOGGER.info("Authentication successful, token received.")
            return token
        except APIError as e:
            _LOGGER.error("API error during authentication: %s", e)
            self._jwt_token = None
            if not isinstance(e, AuthError):
                raise AuthError(f"API error during login: {e.args[0]}") from e
            raise

    async def async_logout(self) -> Dict[str, Any]:
        """Logs the current user out."""
        _LOGGER.info("Attempting API logout.")
        try:
            response_data = await self._request("GET", "/auth/logout", authenticated=True, use_api_base=False)
            self._jwt_token = None
            _LOGGER.info("Logout request successful. Local token cleared.")
            return response_data
        except APIError as e:
            _LOGGER.error("API error during logout: %s", e)
            if isinstance(e, AuthError):
                self._jwt_token = None
                _LOGGER.warning("AuthError during logout, cleared local token anyway.")
            raise
