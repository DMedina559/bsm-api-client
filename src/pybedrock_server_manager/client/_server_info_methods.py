# src/pybedrock_server_manager/client/_server_info_methods.py
"""Mixin class containing server information retrieval methods."""
import logging
from typing import Any, Dict, Optional, List, TYPE_CHECKING
from urllib.parse import quote

if TYPE_CHECKING:
    from ..client_base import ClientBase
    from ..exceptions import APIError, ServerNotFoundError

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.server_info")


class ServerInfoMethodsMixin:
    """Mixin for server information endpoints."""

    _request: callable
    if TYPE_CHECKING:

        async def _request(
            self: "ClientBase",
            method: str,
            path: str,
            json_data: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None,
            authenticated: bool = True,
            is_retry: bool = False,
        ) -> Any: ...

    async def async_get_servers_details(self) -> List[Dict[str, Any]]:
        """
        Fetches a list of all detected Bedrock server instances with their details
        (name, status, version).

        Corresponds to `GET /api/servers`.
        Requires authentication.

        Returns:
            A list of dictionaries, where each dictionary represents a server
            and contains 'name', 'status', and 'version' keys.
            Returns an empty list if no servers are found or if an error occurs
            that is handled by returning an empty list (e.g., malformed response).
        """
        _LOGGER.debug("Fetching server details list from /api/servers")
        try:
            response_data = await self._request("GET", "/servers", authenticated=True)

            # API response includes "status": "success" and "servers": [...]
            # or "status": "success", "servers": [...], "message": "Completed with errors..."
            if (
                not isinstance(response_data, dict)
                or response_data.get("status") != "success"
            ):
                _LOGGER.error(
                    "Received non-success or unexpected response structure from /api/servers: %s",
                    response_data,
                )
                # For now, let's be strict if "status" isn't "success".
                raise APIError(
                    f"Failed to get server list, API status: {response_data.get('status')}",
                    response_data=response_data,
                )

            servers_data_list = response_data.get("servers")
            if not isinstance(servers_data_list, list):
                _LOGGER.error(
                    "Invalid server list response: 'servers' key not a list or missing. Data: %s",
                    response_data,
                )
                # Depending on strictness, could return [] or raise APIError.
                # Raising error if the structure is fundamentally wrong.
                raise APIError(
                    "Invalid response format from /api/servers: 'servers' key not a list or missing.",
                    response_data=response_data,
                )

            processed_servers: List[Dict[str, Any]] = []
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

            return processed_servers  # Already a list of dicts
        except APIError as e:
            _LOGGER.error("API error fetching server list: %s", e)
            raise  # Re-raise the original APIError
        except Exception as e:  # Catch unexpected errors during parsing
            _LOGGER.exception("Unexpected error processing server list response: %s", e)
            raise APIError(f"Unexpected error processing server list: {e}")

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
        return sorted(
            filter(None, server_names)
        )  # Filter out any empty names just in case

    async def async_get_server_validate(self, server_name: str) -> bool:
        """
        Validates if the server directory and executable exist for the specified server.
        Returns True if valid, raises ServerNotFoundError if not found, or APIError for other issues.

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

    async def async_get_server_status_info(self, server_name: str) -> Dict[str, Any]:
        """
        Gets runtime status information (PID, CPU, Memory, Uptime) for a server.
        The 'process_info' key in the response will be null if the server is not running.

        Corresponds to `GET /api/server/{server_name}/status_info`.
        Requires authentication.

        Args:
            server_name: The name of the server.
        """
        _LOGGER.debug("Fetching status info for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        return await self._request(
            "GET",
            f"/server/{encoded_server_name}/status_info",
            authenticated=True,
        )

    async def async_get_server_running_status(self, server_name: str) -> Dict[str, Any]:
        """
        Checks if the Bedrock server process is currently running.
        Response contains `{"is_running": true/false}`.

        Corresponds to `GET /api/server/{server_name}/running_status`.
        Requires authentication.

        Args:
            server_name: The name of the server.
        """
        _LOGGER.debug("Fetching running status for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        return await self._request(
            "GET",
            f"/server/{encoded_server_name}/running_status",
            authenticated=True,
        )

    async def async_get_server_config_status(self, server_name: str) -> Dict[str, Any]:
        """
        Gets the status string stored in the server's configuration file.
        Response contains `{"config_status": "status_string"}`.

        Corresponds to `GET /api/server/{server_name}/config_status`.
        Requires authentication.

        Args:
            server_name: The name of the server.
        """
        _LOGGER.debug("Fetching config status for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        return await self._request(
            "GET",
            f"/server/{encoded_server_name}/config_status",
            authenticated=True,
        )

    async def async_get_server_version(self, server_name: str) -> Optional[str]:
        """
        Gets the installed Bedrock server version from the server's config file.
        Returns the version string or None if not found/error.

        Corresponds to `GET /api/server/{server_name}/version`.
        Requires authentication.

        Args:
            server_name: The name of the server.
        """
        _LOGGER.debug("Fetching version for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        try:
            data = await self._request(
                "GET",
                f"/server/{encoded_server_name}/version",
                authenticated=True,
            )
            # API returns {"status": "success", "installed_version": "1.x.y.z"}
            if isinstance(data, dict) and data.get("status") == "success":
                version = data.get("installed_version")
                return str(version) if version is not None else None
            _LOGGER.warning(
                "Unexpected response structure for server version: %s", data
            )
            return None
        except APIError as e:  # Includes ServerNotFoundError if server path is invalid
            _LOGGER.warning(
                "Could not fetch version for server '%s': %s", server_name, e
            )
            return None

    async def async_get_server_world_name(self, server_name: str) -> Optional[str]:
        """
        Gets the configured world name (level-name) from server.properties.
        Returns the world name string or None if not found/error.

        Corresponds to `GET /api/server/{server_name}/world_name`.
        Requires authentication.

        Args:
            server_name: The name of the server.
        """
        _LOGGER.debug("Fetching world name for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        try:
            data = await self._request(
                "GET",
                f"/server/{encoded_server_name}/world_name",
                authenticated=True,
            )
            # API returns {"status": "success", "world_name": "..."}
            if isinstance(data, dict) and data.get("status") == "success":
                world = data.get("world_name")
                return str(world) if world is not None else None
            _LOGGER.warning(
                "Unexpected response structure for server world name: %s", data
            )
            return None
        except APIError as e:
            _LOGGER.warning(
                "Could not fetch world name for server '%s': %s", server_name, e
            )
            return None

    async def async_get_server_properties(self, server_name: str) -> Dict[str, Any]:
        """
        Retrieves the parsed content of the server's server.properties file.
        The actual properties are under the "properties" key in the response.

        Corresponds to `GET /api/server/{server_name}/read_properties`.
        Requires authentication.

        Args:
            server_name: The name of the server.
        """
        _LOGGER.debug("Fetching server.properties for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        return await self._request(
            "GET",
            f"/server/{encoded_server_name}/read_properties",
            authenticated=True,
        )

    async def async_get_server_permissions_data(
        self, server_name: str
    ) -> Dict[str, Any]:
        """
        Retrieves player permissions from the server's permissions.json file.
        The actual permissions list is under the "data.permissions" key in the response.

        Corresponds to `GET /api/server/{server_name}/permissions_data`.
        Requires authentication.

        Args:
            server_name: The name of the server.
        """
        _LOGGER.debug("Fetching permissions.json data for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        return await self._request(
            "GET",
            f"/server/{encoded_server_name}/permissions_data",
            authenticated=True,
        )

    async def async_get_server_allowlist(self, server_name: str) -> Dict[str, Any]:
        """
        Retrieves the list of players from the server's allowlist.json file.
        The player list is under the "existing_players" key in the response.

        Corresponds to `GET /api/server/{server_name}/allowlist`.
        Requires authentication.

        Args:
            server_name: The name of the server.
        """
        _LOGGER.debug("Fetching allowlist.json for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        return await self._request(
            "GET",
            f"/server/{encoded_server_name}/allowlist",
            authenticated=True,
        )
