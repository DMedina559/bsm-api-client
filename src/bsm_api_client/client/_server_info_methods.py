# src/bsm_api_client/client/_server_info_methods.py
"""Mixin class containing server information retrieval methods."""
import logging
from typing import Any, Dict, Optional, List, TYPE_CHECKING, Union
from urllib.parse import quote

if TYPE_CHECKING:
    from ..client_base import ClientBase
    from ..exceptions import APIError, ServerNotFoundError

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.server_info")


class ServerInfoMethodsMixin:
    """Mixin for server information endpoints."""

    _request: callable
    if TYPE_CHECKING:
        # This is a type hint for the _request method that will be present
        # on the ClientBase instance when this mixin is used.
        async def _request(
            self: "ClientBase",
            method: str,
            path: str,
            json_data: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None,
            authenticated: bool = True,
            is_retry: bool = False,
            expect_json: bool = True,
        ) -> Any: ...

        # We also need access to self._session for raw requests if not adapting _request
        _session: Any
        _base_url: str
        _default_headers: Dict[str, str]
        _jwt_token: Optional[str]
        _auth_lock: Any
        _request_timeout: int

        # Method from ClientBase we might need if not using self._request for icon
        async def authenticate(self) -> bool: ...
        async def _handle_api_error(
            self, response: Any, request_path_for_log: str
        ) -> None: ...

    async def async_get_servers_details(self) -> List[Dict[str, str]]:
        """
        Fetches a list of all detected Bedrock server instances with their details
        (name, status, version).

        Corresponds to `GET /api/servers`.
        Requires authentication.

        Returns:
            A list of dictionaries, where each dictionary represents a server
            and contains 'name', 'status', and 'version' keys.

        Raises:
            APIError: For API communication or processing errors.
        """
        _LOGGER.debug("Fetching server details list from /api/servers")
        try:
            response_data = await self._request("GET", "/servers", authenticated=True)

            if (
                not isinstance(response_data, dict)
                or response_data.get("status") != "success"
            ):
                _LOGGER.error(
                    "Received non-success or unexpected response structure from /api/servers: %s",
                    response_data,
                )
                raise APIError(  # type: ignore
                    f"Failed to get server list, API status: {response_data.get('status')}",
                    response_data=response_data,
                )

            servers_data_list = response_data.get("servers")
            if not isinstance(servers_data_list, list):
                _LOGGER.error(
                    "Invalid server list response: 'servers' key not a list or missing. Data: %s",
                    response_data,
                )
                raise APIError(  # type: ignore
                    "Invalid response format from /api/servers: 'servers' key not a list or missing.",
                    response_data=response_data,
                )

            processed_servers: List[Dict[str, str]] = []
            for item in servers_data_list:
                if (
                    isinstance(item, dict)
                    and isinstance(item.get("name"), str)
                    and isinstance(item.get("status"), str)
                    and isinstance(item.get("version"), str)
                ):
                    processed_servers.append(
                        {
                            "name": item["name"],
                            "status": item["status"],
                            "version": item["version"],
                        }
                    )
                else:
                    _LOGGER.warning(
                        "Skipping malformed server item in /servers response: %s", item
                    )

            if (
                response_data.get("message")
                and "error" in response_data.get("message", "").lower()
            ):
                _LOGGER.warning(
                    "API reported errors while fetching server list: %s",
                    response_data.get("message"),
                )

            return processed_servers
        except APIError as e:
            _LOGGER.error("API error fetching server list: %s", e)
            raise
        except Exception as e:
            _LOGGER.exception("Unexpected error processing server list response: %s", e)
            raise APIError(f"Unexpected error processing server list: {e}")  # type: ignore

    async def async_get_server_names(self) -> List[str]:
        """
        Fetches a simplified list of just server names.
        A convenience wrapper around `async_get_servers_details`.

        Returns:
            A sorted list of server names.
        """
        _LOGGER.debug("Fetching server names list")
        server_details_list = await self.async_get_servers_details()
        server_names = [
            server.get("name", "")
            for server in server_details_list
            if server.get("name")
        ]
        return sorted(filter(None, server_names))

    async def async_get_server_is_running(self, server_name: str) -> bool:
        """
        Checks if the Bedrock server process for the specified server instance is currently running.

        Corresponds to `GET /api/server/{server_name}/status`.
        Requires authentication.

        Args:
            server_name: The name of the server.

        Returns:
            True if the server is running, False otherwise.

        Raises:
            ServerNotFoundError: If the server does not exist.
            APIError: For other API communication or processing errors.
        """
        _LOGGER.debug("Fetching running status for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        try:
            response_data = await self._request(
                "GET",
                f"/server/{encoded_server_name}/status",
                authenticated=True,
            )
            if (
                isinstance(response_data, dict)
                and response_data.get("status") == "success"
                and isinstance(response_data.get("is_running"), bool)
            ):
                return response_data["is_running"]

            _LOGGER.error(
                "Received non-success or unexpected response structure from /api/server/.../status: %s",
                response_data,
            )
            raise APIError(  # type: ignore
                f"Failed to get server running status, API response: {response_data.get('status') if isinstance(response_data, dict) else 'N/A'}",
                response_data=(
                    response_data
                    if isinstance(response_data, dict)
                    else {"raw": response_data}
                ),
            )
        except APIError as e:
            _LOGGER.error(
                "API error fetching running status for server '%s': %s", server_name, e
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error processing running status for server '%s': %s",
                server_name,
                e,
            )
            raise APIError(f"Unexpected error processing running status for '{server_name}': {e}")  # type: ignore

    async def async_get_server_config_status(self, server_name: str) -> str:
        """
        Gets the status string stored in the server's configuration file.

        Corresponds to `GET /api/server/{server_name}/config_status`.
        Requires authentication.

        Args:
            server_name: The name of the server.

        Returns:
            The configuration status string.

        Raises:
            ServerNotFoundError: If the server does not exist.
            APIError: For other API communication or processing errors.
        """
        _LOGGER.debug("Fetching config status for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        try:
            response_data = await self._request(
                "GET",
                f"/server/{encoded_server_name}/config_status",
                authenticated=True,
            )
            if (
                isinstance(response_data, dict)
                and response_data.get("status") == "success"
                and isinstance(response_data.get("config_status"), str)
            ):
                return response_data["config_status"]

            _LOGGER.error(
                "Received non-success or unexpected response structure from /api/server/.../config_status: %s",
                response_data,
            )
            raise APIError(  # type: ignore
                f"Failed to get server config status, API response: {response_data.get('status') if isinstance(response_data, dict) else 'N/A'}",
                response_data=(
                    response_data
                    if isinstance(response_data, dict)
                    else {"raw": response_data}
                ),
            )
        except APIError as e:
            _LOGGER.error(
                "API error fetching config status for server '%s': %s", server_name, e
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error processing config status for server '%s': %s",
                server_name,
                e,
            )
            raise APIError(f"Unexpected error processing config status for '{server_name}': {e}")  # type: ignore

    async def async_get_server_version(self, server_name: str) -> str:
        """
        Gets the installed Bedrock server version from the server's config file.

        Corresponds to `GET /api/server/{server_name}/version`.
        Requires authentication.

        Args:
            server_name: The name of the server.

        Returns:
            The installed version string.

        Raises:
            ServerNotFoundError: If the server does not exist.
            APIError: If the version cannot be determined or other API errors.
        """
        _LOGGER.debug("Fetching version for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        try:
            data = await self._request(
                "GET",
                f"/server/{encoded_server_name}/version",
                authenticated=True,
            )
            if isinstance(data, dict) and data.get("status") == "success":
                version = data.get("installed_version")
                if isinstance(version, str):
                    return version
            _LOGGER.warning(
                "Unexpected response structure or missing version for server '%s': %s",
                server_name,
                data,
            )
            raise APIError(  # type: ignore
                f"Could not determine version for server '{server_name}'. Response: {data}",
                response_data=data if isinstance(data, dict) else {"raw": data},
            )
        except APIError as e:
            _LOGGER.warning(
                "API error fetching version for server '%s': %s", server_name, e
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error processing server version for '%s': %s",
                server_name,
                e,
            )
            raise APIError(f"Unexpected error processing version for '{server_name}': {e}")  # type: ignore

    async def async_get_server_validate(self, server_name: str) -> bool:
        """
        Validates if the server directory and executable exist for the specified server.

        Corresponds to `GET /api/server/{server_name}/validate`.
        Requires authentication.

        Args:
            server_name: The name of the server to validate.

        Returns:
            True if the server is found and considered valid by the API.

        Raises:
            ServerNotFoundError: If the API returns a 404 for this server.
            APIError: For other API communication or processing errors.
        """
        _LOGGER.debug("Validating existence of server: '%s'", server_name)
        encoded_server_name = quote(server_name)
        try:
            response = await self._request(
                "GET",
                f"/server/{encoded_server_name}/validate",
                authenticated=True,
            )
            return isinstance(response, dict) and response.get("status") == "success"
        except APIError as e:
            _LOGGER.error(
                "API error during validation for server '%s': %s", server_name, e
            )
            raise  # ServerNotFoundError will be raised by _request if it's a 404

    async def async_get_server_process_info(
        self, server_name: str
    ) -> Optional[Dict[str, Any]]:
        """
        Gets runtime status information (PID, CPU, Memory, Uptime) for a server.
        The 'process_info' key in the response will be null if the server is not running.

        Corresponds to `GET /api/server/{server_name}/process_info`.
        Requires authentication.

        Args:
            server_name: The name of the server.

        Returns:
            A dictionary with process info if running, or None if not running.
            Example: {"pid": 123, "cpu_percent": 10.5, "memory_mb": 512.5, "uptime": "1:00:00"}

        Raises:
            ServerNotFoundError: If the server does not exist.
            APIError: For other API communication or processing errors.
        """
        _LOGGER.debug("Fetching process info for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        try:
            response_data = await self._request(
                "GET",
                f"/server/{encoded_server_name}/process_info",
                authenticated=True,
            )
            if (
                isinstance(response_data, dict)
                and response_data.get("status") == "success"
            ):
                return response_data.get("process_info")  # Can be dict or null

            _LOGGER.error(
                "Received non-success or unexpected response structure from /api/server/.../process_info: %s",
                response_data,
            )
            raise APIError(  # type: ignore
                f"Failed to get server process info, API response: {response_data.get('status') if isinstance(response_data, dict) else 'N/A'}",
                response_data=(
                    response_data
                    if isinstance(response_data, dict)
                    else {"raw": response_data}
                ),
            )
        except APIError as e:
            _LOGGER.error(
                "API error fetching process info for server '%s': %s", server_name, e
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error processing process info for server '%s': %s",
                server_name,
                e,
            )
            raise APIError(f"Unexpected error processing process info for '{server_name}': {e}")  # type: ignore

    async def async_get_server_world_icon(self, server_name: str) -> bytes:
        """
        Gets the server's world icon as JPEG image data.

        Corresponds to `GET /api/server/{server_name}/world/icon`.
        Requires authentication.

        Args:
            server_name: The name of the server.

        Returns:
            The raw bytes of the JPEG image.

        Raises:
            ServerNotFoundError: If the server does not exist.
            APIError: If the icon cannot be retrieved or for other API errors.
        """
        _LOGGER.debug("Fetching world icon for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        # Path for logging in _handle_api_error if needed
        request_path_for_log = f"/server/{encoded_server_name}/world/icon"
        url = f"{self._base_url}{request_path_for_log}"  # type: ignore # self will be ClientBase

        headers: Dict[str, str] = dict(self._default_headers)  # type: ignore
        # Authentication
        async with self._auth_lock:  # type: ignore
            if not self._jwt_token:  # type: ignore
                await self.authenticate()  # type: ignore
        if not self._jwt_token:  # type: ignore
            # Ensure APIError is available in this scope if it's not automatically
            from ..exceptions import (
                APIError as ClientAPIError,
            )  # Use an alias to avoid conflict if any

            raise ClientAPIError(
                "Authentication required for world icon but no token available."
            )
        headers["Authorization"] = f"Bearer {self._jwt_token}"  # type: ignore

        try:
            # Using _session directly as _request is tailored for JSON
            async with self._session.get(  # type: ignore
                url,
                headers=headers,
                timeout=self._request_timeout,  # type: ignore
            ) as response:
                if not response.ok:
                    # Use the existing error handler from ClientBase
                    await self._handle_api_error(response, request_path_for_log)  # type: ignore
                    # Should not be reached if _handle_api_error works
                    from ..exceptions import APIError as ClientAPIError

                    raise ClientAPIError(
                        f"Error fetching world icon: {response.status}",
                        response_data={"raw": await response.text()},
                    )

                if response.content_type != "image/jpeg":
                    _LOGGER.warning(
                        "Expected image/jpeg for world icon but got %s for server %s",
                        response.content_type,
                        server_name,
                    )
                    # Depending on strictness, could raise or still return data

                return await response.read()
        except APIError as e:  # Re-raise APIError (including ServerNotFoundError)
            _LOGGER.error("API error fetching world icon for '%s': %s", server_name, e)
            raise
        except Exception as e:  # Catch other errors like aiohttp client errors
            _LOGGER.exception(
                "Unexpected error fetching world icon for '%s': %s", server_name, e
            )
            from ..exceptions import APIError as ClientAPIError

            raise ClientAPIError(
                f"Unexpected error fetching world icon for '{server_name}': {e}"
            )

    async def async_get_server_properties(self, server_name: str) -> Dict[str, str]:
        """
        Retrieves the parsed content of the server's server.properties file.

        Corresponds to `GET /api/server/{server_name}/properties/get`.
        Requires authentication.

        Args:
            server_name: The name of the server.

        Returns:
            A dictionary of server properties.

        Raises:
            ServerNotFoundError: If the server does not exist or properties file not found.
            APIError: For other API communication or processing errors.
        """
        _LOGGER.debug("Fetching server.properties for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        try:
            response_data = await self._request(
                "GET",
                f"/server/{encoded_server_name}/properties/get",
                authenticated=True,
            )
            if (
                isinstance(response_data, dict)
                and response_data.get("status") == "success"
                and isinstance(response_data.get("properties"), dict)
            ):
                # Ensure all values in properties are strings as per typical .properties files
                return {str(k): str(v) for k, v in response_data["properties"].items()}

            _LOGGER.error(
                "Received non-success or unexpected response structure from /api/server/.../properties/get: %s",
                response_data,
            )
            raise APIError(  # type: ignore
                f"Failed to get server properties, API response: {response_data.get('status') if isinstance(response_data, dict) else 'N/A'}",
                response_data=(
                    response_data
                    if isinstance(response_data, dict)
                    else {"raw": response_data}
                ),
            )
        except APIError as e:
            _LOGGER.error(
                "API error fetching server properties for '%s': %s", server_name, e
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error processing server properties for '%s': %s",
                server_name,
                e,
            )
            raise APIError(f"Unexpected error processing server properties for '{server_name}': {e}")  # type: ignore

    async def async_get_server_permissions(
        self, server_name: str
    ) -> List[Dict[str, Union[str, bool]]]:  # Corrected return type hint
        """
        Retrieves player permissions from the server's permissions.json file.

        Corresponds to `GET /api/server/{server_name}/permissions/get`.
        Requires authentication.

        Args:
            server_name: The name of the server.

        Returns:
            A list of player permission objects. E.g.,
            `[{"xuid": "...", "name": "...", "permission_level": "..."}]`

        Raises:
            ServerNotFoundError: If the server does not exist or permissions file not found.
            APIError: For other API communication or processing errors.
        """
        _LOGGER.debug("Fetching permissions.json data for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        try:
            response_data = await self._request(
                "GET",
                f"/server/{encoded_server_name}/permissions/get",
                authenticated=True,
            )
            if (
                isinstance(response_data, dict)
                and response_data.get("status") == "success"
                and isinstance(response_data.get("data"), dict)
                and isinstance(response_data["data"].get("permissions"), list)
            ):
                return response_data["data"]["permissions"]

            _LOGGER.error(
                "Received non-success or unexpected response structure from /api/server/.../permissions/get: %s",
                response_data,
            )
            raise APIError(  # type: ignore
                f"Failed to get server permissions, API response: {response_data.get('status') if isinstance(response_data, dict) else 'N/A'}",
                response_data=(
                    response_data
                    if isinstance(response_data, dict)
                    else {"raw": response_data}
                ),
            )
        except APIError as e:
            _LOGGER.error(
                "API error fetching server permissions for '%s': %s", server_name, e
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error processing server permissions for '%s': %s",
                server_name,
                e,
            )
            raise APIError(f"Unexpected error processing server permissions for '{server_name}': {e}")  # type: ignore

    async def async_get_server_allowlist(
        self, server_name: str
    ) -> List[Dict[str, Union[str, bool]]]:  # Corrected return type hint
        """
        Retrieves the list of players from the server's allowlist.json file.

        Corresponds to `GET /api/server/{server_name}/allowlist/get`.
        Requires authentication.

        Args:
            server_name: The name of the server.

        Returns:
            A list of player objects from the allowlist. E.g.,
            `[{"ignoresPlayerLimit": false, "name": "PlayerName"}]`

        Raises:
            ServerNotFoundError: If the server does not exist or allowlist file not found.
            APIError: For other API communication or processing errors.
        """
        _LOGGER.debug("Fetching allowlist.json for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        try:
            response_data = await self._request(
                "GET",
                f"/server/{encoded_server_name}/allowlist/get",
                authenticated=True,
            )
            if (
                isinstance(response_data, dict)
                and response_data.get("status") == "success"
                and isinstance(response_data.get("existing_players"), list)
            ):
                return response_data["existing_players"]

            _LOGGER.error(
                "Received non-success or unexpected response structure from /api/server/.../allowlist/get: %s",
                response_data,
            )
            raise APIError(  # type: ignore
                f"Failed to get server allowlist, API response: {response_data.get('status') if isinstance(response_data, dict) else 'N/A'}",
                response_data=(
                    response_data
                    if isinstance(response_data, dict)
                    else {"raw": response_data}
                ),
            )
        except APIError as e:
            _LOGGER.error(
                "API error fetching server allowlist for '%s': %s", server_name, e
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error processing server allowlist for '%s': %s",
                server_name,
                e,
            )
            raise APIError(f"Unexpected error processing server allowlist for '{server_name}': {e}")  # type: ignore
