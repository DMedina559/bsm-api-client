# src/pybedrock_server_manager/client/_server_info_methods.py
"""Mixin class containing server information retrieval methods."""
import logging
from typing import Any, Dict, Optional, List
from ..exceptions import APIError, ServerNotFoundError  # Relative import for exceptions

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.server_info")


class ServerInfoMethodsMixin:
    """Mixin for server information endpoints."""

    async def async_get_servers(self) -> List[str]:
        """Fetches the list of server names from the API. Calls GET /api/servers."""
        _LOGGER.debug("Fetching server list from API endpoint /servers")
        try:
            response_data = await self._request(
                "GET", f"{self._base_path}/servers", authenticated=True
            )
            servers_raw = response_data.get("servers")
            if not isinstance(servers_raw, list):
                _LOGGER.error(
                    "Invalid server list response: Expected list, got %s. Data: %s",
                    type(servers_raw).__name__,
                    response_data,
                )
                raise APIError(
                    f"Invalid format for server list response: Expected list, got {type(servers_raw).__name__}"
                )

            server_list: List[str] = []
            for item in servers_raw:
                name_to_add = None
                if isinstance(item, dict):
                    name_to_add = item.get("name")
                elif isinstance(item, str):
                    name_to_add = item

                if isinstance(name_to_add, str) and name_to_add:
                    server_list.append(name_to_add)
                else:
                    _LOGGER.warning("Skipping invalid item in server list: %s", item)

            if (
                not server_list and servers_raw
            ):  # If original raw list was not empty but processed list is
                _LOGGER.warning(
                    "API returned server data but no valid server names could be extracted."
                )
            elif not server_list:  # If raw list was also empty
                _LOGGER.info("API returned an empty server list.")
            return sorted(server_list)
        except APIError as e:
            _LOGGER.error("API error fetching server list: %s", e)
            raise

    async def async_get_server_validate(self, server_name: str) -> bool:
        """Checks if a server configuration exists. Calls GET /api/server/{server_name}/validate."""
        _LOGGER.debug("Validating existence of server: %s", server_name)
        try:
            await self._request(
                "GET",
                f"{self._base_path}/server/{server_name}/validate",
                authenticated=True,
            )
            return True
        except ServerNotFoundError:
            _LOGGER.warning(
                "Validation failed: Server %s not found via API.", server_name
            )
            raise
        except APIError as e:
            _LOGGER.error("Error validating server %s: %s", server_name, e)
            raise

    async def async_get_server_status_info(self, server_name: str) -> Dict[str, Any]:
        """Gets runtime status info for a server. Calls GET /api/server/{server_name}/status_info."""
        _LOGGER.debug("Fetching status info for server '%s'", server_name)
        return await self._request(
            "GET",
            f"{self._base_path}/server/{server_name}/status_info",
            authenticated=True,
        )

    async def async_get_server_running_status(self, server_name: str) -> Dict[str, Any]:
        """Gets running status for a server. Calls GET /api/server/{server_name}/running_status."""
        _LOGGER.debug("Fetching running status for server '%s'", server_name)
        return await self._request(
            "GET",
            f"{self._base_path}/server/{server_name}/running_status",
            authenticated=True,
        )

    async def async_get_server_config_status(self, server_name: str) -> Dict[str, Any]:
        """Gets config status for a server. Calls GET /api/server/{server_name}/config_status."""
        _LOGGER.debug("Fetching config status for server '%s'", server_name)
        return await self._request(
            "GET",
            f"{self._base_path}/server/{server_name}/config_status",
            authenticated=True,
        )

    async def async_get_server_version(self, server_name: str) -> Optional[str]:
        """Gets the installed version for a server. Calls GET /api/server/{server_name}/version."""
        _LOGGER.debug("Fetching version for server '%s'", server_name)
        try:
            data = await self._request(
                "GET",
                f"{self._base_path}/server/{server_name}/version",
                authenticated=True,
            )
            version = data.get("installed_version")
            return str(version) if version is not None else None
        except APIError as e:
            _LOGGER.warning(
                "Could not fetch version for server '%s': %s", server_name, e
            )
            return None

    async def async_get_server_world_name(self, server_name: str) -> Optional[str]:
        """Gets the configured world name for a server. Calls GET /api/server/{server_name}/world_name."""
        _LOGGER.debug("Fetching world name for server '%s'", server_name)
        try:
            data = await self._request(
                "GET",
                f"{self._base_path}/server/{server_name}/world_name",
                authenticated=True,
            )
            world = data.get("world_name")
            return str(world) if world is not None else None
        except APIError as e:
            _LOGGER.warning(
                "Could not fetch world name for server '%s': %s", server_name, e
            )
            return None

    async def async_get_server_properties(self, server_name: str) -> Dict[str, Any]:
        """Gets server.properties content. Calls GET /api/server/{server_name}/read_properties."""
        _LOGGER.debug("Fetching server properties for server '%s'", server_name)
        return await self._request(
            "GET",
            f"{self._base_path}/server/{server_name}/read_properties",
            authenticated=True,
        )

    async def async_get_server_permissions_data(
        self, server_name: str
    ) -> Dict[str, Any]:
        """Gets permissions.json content for a server. Calls GET /api/server/{server_name}/permissions_data."""
        _LOGGER.debug("Fetching server permissions data for server '%s'", server_name)
        return await self._request(
            "GET",
            f"{self._base_path}/server/{server_name}/permissions_data",
            authenticated=True,
        )

    async def async_get_server_allowlist(self, server_name: str) -> Dict[str, Any]:
        """Gets the current allowlist for a server. Calls GET /api/server/{server_name}/allowlist."""
        _LOGGER.debug("Fetching allowlist for server '%s'", server_name)
        return await self._request(
            "GET",
            f"{self._base_path}/server/{server_name}/allowlist",
            authenticated=True,
        )
