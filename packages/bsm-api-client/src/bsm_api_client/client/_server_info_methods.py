# src/bsm_api_client/client/_server_info_methods.py
"""Mixin class for server information retrieval methods.

This module provides the `ServerInfoMethodsMixin` class, which includes
methods for retrieving information about server instances from the Bedrock
Server Manager API.
"""

import asyncio
import logging
from typing import Any, Callable, List, Optional, cast
from urllib.parse import quote

import aiohttp

from ..exceptions import APIError, AuthError, CannotConnectError, ServerNotFoundError
from ..models import (
    AllowlistGetResponse,
    PermissionsGetResponse,
    PropertiesGetResponse,
    ServerProcessInfoResponse,
    ServerRunningStatusResponse,
    ServerSchemaResponse,
    ServerSettingItemPayload,
    ServerSettingsResponse,
    ServersListResponse,
)

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.server_info")


class ServerInfoMethodsMixin:
    """Mixin for server information endpoints."""

    _request: Callable[..., Any]
    _base_url: str
    _jwt_token: Optional[str]
    _session: aiohttp.ClientSession
    _request_timeout: aiohttp.ClientTimeout
    _auth_lock: asyncio.Lock
    authenticate: Callable[..., Any]
    _handle_api_error: Callable[..., Any]

    async def async_get_servers(self) -> ServersListResponse:
        """Retrieves a list of all detected server instances with their status and version.

        :returns: A `ServersListResponse` object containing a list of servers.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_get_servers()
        """
        _LOGGER.debug("Fetching server list from /api/servers")
        response_data = await self._request("GET", "/servers", authenticated=True)
        return cast(
            ServersListResponse, ServersListResponse.model_validate(response_data)
        )

    async def async_get_server_names(self) -> List[str]:
        """Fetches a list of server names.

        This is a convenience wrapper around `async_get_servers`.

        :returns: A sorted list of server names.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_get_server_names()
        """
        _LOGGER.debug("Fetching server names list")
        server_details = await self.async_get_servers()
        if server_details.servers:
            return sorted([server.name for server in server_details.servers])
        return []

    async def async_get_server_validate(self, server_name: str) -> bool:
        """Validates the existence of a server's directory and executable.

        :param server_name: The name of the server to validate.

        :returns: `True` if the server is valid, `False` otherwise.

        :raises ServerNotFoundError: If the server is not found.
        :raises APIError: For other API-related errors.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_get_server_validate('MyServer')
        """
        _LOGGER.debug("Validating existence of server: '%s'", server_name)
        # Server names might have characters needing encoding, though install rules try to limit this.
        encoded_server_name = quote(server_name)
        try:
            # This request will raise ServerNotFoundError via ClientBase if API returns 404
            # or other APIError for different issues.
            response = await self._request(
                "GET",
                f"/server/{encoded_server_name}/validate",
                authenticated=True,
            )
            # If no exception, and we get here, it means 200 OK.
            # The API docs say 200 OK means "status": "success"
            return isinstance(response, dict) and response.get("status") == "success"
        except ServerNotFoundError:
            _LOGGER.debug(
                "Validation API call indicated server '%s' not found.", server_name
            )
            raise
        except APIError as e:  # Catch other API errors
            _LOGGER.error(
                "API error during validation for server '%s': %s", server_name, e
            )
            raise

    async def async_get_server_summary(self, server_name: str) -> ServerSchemaResponse:
        """Retrieves the basic summary information for a specific server instance.

        :param server_name: The name of the server.
        :returns: A `ServerSchemaResponse` object containing the server summary.

        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_get_server_summary('MyServer')
        """
        _LOGGER.debug("Fetching summary for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        response = await self._request(
            "GET", f"/server/{encoded_server_name}/summary", authenticated=True
        )
        return cast(ServerSchemaResponse, ServerSchemaResponse.model_validate(response))

    async def async_get_server_process_info(
        self, server_name: str
    ) -> ServerProcessInfoResponse:
        """Gets runtime process information for a server.

        :param server_name: The name of the server.

        :returns: A `ServerProcessInfoResponse` object containing process information.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_get_server_process_info('MyServer')
        """
        _LOGGER.debug("Fetching status info for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        response = await self._request(
            "GET",
            f"/server/{encoded_server_name}/process_info",
            authenticated=True,
        )
        return cast(
            ServerProcessInfoResponse,
            ServerProcessInfoResponse.model_validate(response),
        )

    async def async_get_world_icon_image(self, server_name: str) -> bytes:  # noqa: C901
        """Retrieves the world icon image for a server.

        :param server_name: The name of the server.

        :returns: The raw bytes of the world icon image.

        :raises ValueError: If `server_name` is empty.
        :raises CannotConnectError: If a connection to the server cannot be established.
        :raises APIError: For other API-related errors.
        """
        if not server_name:
            raise ValueError("Server name cannot be empty.")
        _LOGGER.info("Fetching world icon for server '%s'.", server_name)

        encoded_server_name = quote(server_name)
        # Path is /api/server/{server_name}/world/icon.
        # self._base_url already contains /api, so path for _request should be server/...
        # However, for direct session call for binary data:
        url = f"{self._base_url}/server/{encoded_server_name}/world/icon"

        headers = {"Accept": "image/jpeg, */*"}
        if self._jwt_token:
            headers["Authorization"] = f"Bearer {self._jwt_token}"

        _LOGGER.debug("Request: GET %s for world icon", url)
        try:
            async with self._session.get(
                url,
                headers=headers,
                timeout=self._request_timeout,
            ) as response:
                _LOGGER.debug("Response Status for GET %s: %s", url, response.status)
                if not response.ok:
                    # Attempt re-authentication for 401, then retry or raise.
                    # This logic is complex to duplicate from _request.
                    # For simplicity in this direct call, we'll handle common errors directly.
                    if (
                        response.status == 401 and self._jwt_token
                    ):  # Check if token was used
                        _LOGGER.warning(
                            "Received 401 for world icon, attempting token refresh and retry once."
                        )
                        async with self._auth_lock:  # Ensure only one refresh attempt
                            self._jwt_token = None  # Clear potentially invalid token
                            await self.authenticate()  # Attempt to get a new token

                        if self._jwt_token:  # If new token obtained, retry the request
                            headers["Authorization"] = f"Bearer {self._jwt_token}"
                            async with self._session.get(
                                url,
                                headers=headers,
                                timeout=aiohttp.ClientTimeout(
                                    total=self._request_timeout
                                ),
                            ) as retry_response:
                                if not retry_response.ok:
                                    await self._handle_api_error(
                                        retry_response,
                                        f"/server/{encoded_server_name}/world/icon",
                                    )
                                    raise APIError(
                                        f"World icon request failed with status {retry_response.status} after retry."
                                    )
                                return await retry_response.read()
                        else:  # Failed to get new token
                            raise AuthError(
                                "Failed to re-authenticate for world icon request."
                            )

                    await self._handle_api_error(
                        response, f"/server/{encoded_server_name}/world/icon"
                    )
                    raise APIError(
                        f"World icon request failed with status {response.status}"
                    )  # Should be caught by _handle_api_error
                return cast(bytes, await response.read())  # Returns bytes
        except aiohttp.ClientError as e:
            _LOGGER.error(
                "AIOHTTP client error fetching world icon for '%s': %s", server_name, e
            )
            raise CannotConnectError(
                f"AIOHTTP Client Error fetching world icon: {e}", original_exception=e
            ) from e
        except APIError:  # Re-raise APIError from _handle_api_error or auth failure
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching world icon for '%s': %s", server_name, e
            )
            raise APIError(
                f"An unexpected error occurred fetching world icon: {e}"
            ) from e

    async def async_get_server_running_status(
        self, server_name: str
    ) -> ServerRunningStatusResponse:
        """Checks if the Bedrock server process is currently running.

        :param server_name: The name of the server.

        :returns: A `ServerRunningStatusResponse` object containing the running status.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_get_world_icon_image('MyServer')
        """
        _LOGGER.debug("Fetching running status for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        # Path changed from /running_status to /status for the new API.
        response = await self._request(
            "GET",
            f"/server/{encoded_server_name}/status",
            authenticated=True,
        )
        return cast(
            ServerRunningStatusResponse,
            ServerRunningStatusResponse.model_validate(response),
        )

    async def async_get_server_properties(
        self, server_name: str
    ) -> PropertiesGetResponse:
        """Retrieves the server's properties.

        :param server_name: The name of the server.

        :returns: A `PropertiesGetResponse` object containing the server properties.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_get_server_properties('MyServer')
        """
        _LOGGER.debug("Fetching server.properties for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        response = await self._request(
            "GET",
            f"/server/{encoded_server_name}/properties/get",
            authenticated=True,
        )
        return cast(
            PropertiesGetResponse, PropertiesGetResponse.model_validate(response)
        )

    async def async_get_server_permissions_data(
        self, server_name: str
    ) -> PermissionsGetResponse:
        """Retrieves player permissions from the server.

        :param server_name: The name of the server.

        :returns: A `PermissionsGetResponse` object containing the permissions data.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_get_server_permissions_data('MyServer')
        """
        _LOGGER.debug("Fetching permissions.json data for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        response = await self._request(
            "GET",
            f"/server/{encoded_server_name}/permissions/get",
            authenticated=True,
        )
        return cast(
            PermissionsGetResponse, PermissionsGetResponse.model_validate(response)
        )

    async def async_get_server_allowlist(
        self, server_name: str
    ) -> AllowlistGetResponse:
        """Retrieves the server's allowlist.

        :param server_name: The name of the server.

        :returns: A `AllowlistGetResponse` object containing the allowlist.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_get_server_allowlist('MyServer')
        """
        _LOGGER.debug("Fetching allowlist.json for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        response = await self._request(
            "GET",
            f"/server/{encoded_server_name}/allowlist/get",
            authenticated=True,
        )
        return cast(AllowlistGetResponse, AllowlistGetResponse.model_validate(response))

    async def async_get_server_settings(
        self, server_name: str
    ) -> ServerSettingsResponse:
        """Retrieves all settings for a specific server.

        :param server_name: The name of the server.
        :returns: A ServerSettingsResponse.
        """
        _LOGGER.debug("Fetching settings for server '%s'", server_name)
        response = await self._request(
            "GET",
            f"/server/{server_name}/settings/get",
            authenticated=True,
        )
        return cast(
            ServerSettingsResponse, ServerSettingsResponse.model_validate(response)
        )

    async def async_set_server_setting(
        self, server_name: str, payload: ServerSettingItemPayload
    ) -> ServerSettingsResponse:
        """Sets a specific setting for a server.

        :param server_name: The name of the server.
        :param payload: The ServerSettingItemPayload payload.
        :returns: A ServerSettingsResponse.
        """
        _LOGGER.debug(
            "Setting setting for server '%s': %s", server_name, payload.model_dump()
        )
        response = await self._request(
            "POST",
            f"/server/{server_name}/settings/set",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return cast(
            ServerSettingsResponse, ServerSettingsResponse.model_validate(response)
        )
