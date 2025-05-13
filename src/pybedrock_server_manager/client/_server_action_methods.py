# src/pybedrock_server_manager/client/_server_action_methods.py
"""Mixin class containing server action methods."""
import logging
from typing import Any, Dict, Optional, List

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.server_actions")


class ServerActionMethodsMixin:
    """Mixin for server action endpoints."""

    async def async_start_server(self, server_name: str) -> Dict[str, Any]:
        """Starts the server. Calls POST /api/server/{server_name}/start."""
        _LOGGER.info("Requesting start for server '%s'", server_name)
        return await self._request(
            "POST", f"{self._base_path}/server/{server_name}/start", authenticated=True
        )

    async def async_stop_server(self, server_name: str) -> Dict[str, Any]:
        """Stops the server. Calls POST /api/server/{server_name}/stop."""
        _LOGGER.info("Requesting stop for server '%s'", server_name)
        return await self._request(
            "POST", f"{self._base_path}/server/{server_name}/stop", authenticated=True
        )

    async def async_restart_server(self, server_name: str) -> Dict[str, Any]:
        """Restarts the server. Calls POST /api/server/{server_name}/restart."""
        _LOGGER.info("Requesting restart for server '%s'", server_name)
        return await self._request(
            "POST",
            f"{self._base_path}/server/{server_name}/restart",
            authenticated=True,
        )

    async def async_send_server_command(
        self, server_name: str, command: str
    ) -> Dict[str, Any]:
        """Sends a command to the server. Calls POST /api/server/{server_name}/send_command."""
        _LOGGER.info("Sending command to server '%s': %s", server_name, command)
        payload = {"command": command}
        return await self._request(
            "POST",
            f"{self._base_path}/server/{server_name}/send_command",
            data=payload,
            authenticated=True,
        )

    async def async_update_server(self, server_name: str) -> Dict[str, Any]:
        """Triggers the server update process. Calls POST /api/server/{server_name}/update."""
        _LOGGER.info("Requesting update for server '%s'", server_name)
        return await self._request(
            "POST", f"{self._base_path}/server/{server_name}/update", authenticated=True
        )

    async def async_add_server_allowlist(
        self, server_name: str, players: List[str], ignores_player_limit: bool = False
    ) -> Dict[str, Any]:
        """Adds players to the allowlist. Calls POST /api/server/{server_name}/allowlist/add."""
        _LOGGER.info(
            "Adding players %s to allowlist for server '%s'", players, server_name
        )
        payload = {"players": players, "ignoresPlayerLimit": ignores_player_limit}
        return await self._request(
            "POST",
            f"{self._base_path}/server/{server_name}/allowlist/add",
            data=payload,
            authenticated=True,
        )

    async def async_remove_server_allowlist_player(
        self, server_name: str, player_name: str
    ) -> Dict[str, Any]:
        """Removes a player from the allowlist. Calls DELETE /api/server/{server_name}/allowlist/player/{player_name}."""
        _LOGGER.info(
            "Removing player '%s' from allowlist for server '%s'",
            player_name,
            server_name,
        )
        return await self._request(
            "DELETE",
            f"{self._base_path}/server/{server_name}/allowlist/player/{player_name}",
            data=None,
            authenticated=True,
        )

    async def async_set_server_permissions(
        self, server_name: str, permissions_dict: Dict[str, str]
    ) -> Dict[str, Any]:
        """Sets permissions for multiple players. Calls PUT /api/server/{server_name}/permissions."""
        _LOGGER.info(
            "Setting permissions for server '%s': %s", server_name, permissions_dict
        )
        payload = {"permissions": permissions_dict}
        return await self._request(
            "PUT",
            f"{self._base_path}/server/{server_name}/permissions",
            data=payload,
            authenticated=True,
        )

    async def async_update_server_properties(
        self, server_name: str, properties_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Updates server.properties. Calls POST /api/server/{server_name}/properties."""
        _LOGGER.info(
            "Updating properties for server '%s': %s", server_name, properties_dict
        )
        payload = properties_dict  # API expects the dictionary directly
        return await self._request(
            "POST",
            f"{self._base_path}/server/{server_name}/properties",
            data=payload,
            authenticated=True,
        )

    async def async_configure_server_os_service(
        self, server_name: str, payload: Dict[str, bool]
    ) -> Dict[str, Any]:
        """Configures OS-specific service settings. Calls POST /api/server/{server_name}/service."""
        _LOGGER.info(
            "Requesting OS service config for server '%s' with payload: %s",
            server_name,
            payload,
        )
        return await self._request(
            "POST",
            f"{self._base_path}/server/{server_name}/service",
            data=payload,
            authenticated=True,
        )

    async def async_delete_server(self, server_name: str) -> Dict[str, Any]:
        """Deletes the server. Calls DELETE /api/server/{server_name}/delete. USE WITH CAUTION!"""
        _LOGGER.warning(
            "Requesting deletion of server '%s'. This is irreversible.", server_name
        )
        return await self._request(
            "DELETE",
            f"{self._base_path}/server/{server_name}/delete",
            data=None,
            authenticated=True,
        )
