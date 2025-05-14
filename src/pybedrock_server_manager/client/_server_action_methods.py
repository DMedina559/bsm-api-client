# src/pybedrock_server_manager/client/_server_action_methods.py
"""Mixin class containing server action methods."""
import logging
from typing import Any, Dict, Optional, List, TYPE_CHECKING
from urllib.parse import quote  # For URL encoding path parameters

if TYPE_CHECKING:
    from ..client_base import ClientBase  # For type hinting _request

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.server_actions")

ALLOWED_PERMISSION_LEVELS = ["visitor", "member", "operator"]
ALLOWED_SERVER_PROPERTIES_TO_UPDATE = [
    "server-name",
    "level-name",
    "gamemode",
    "difficulty",
    "allow-cheats",
    "max-players",
    "server-port",
    "server-portv6",
    "enable-lan-visibility",
    "allow-list",
    "default-player-permission-level",
    "view-distance",
    "tick-distance",
    "level-seed",
    "online-mode",
    "texturepack-required",
]


class ServerActionMethodsMixin:
    """Mixin for server action endpoints."""

    _request: callable
    if TYPE_CHECKING:

        def is_linux_server(self: "ClientBase") -> bool: ...
        def is_windows_server(self: "ClientBase") -> bool: ...

        async def _request(
            self: "ClientBase",
            method: str,
            path: str,
            json_data: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None,
            authenticated: bool = True,
            is_retry: bool = False,
        ) -> Any: ...

    async def async_start_server(self, server_name: str) -> Dict[str, Any]:
        """
        Starts the specified Bedrock server instance.

        Corresponds to `POST /api/server/{server_name}/start`.
        Requires authentication.

        Args:
            server_name: The unique name of the server instance to start.
        """
        _LOGGER.info("Requesting start for server '%s'", server_name)
        return await self._request(
            "POST",
            f"/server/{server_name}/start",
            authenticated=True,
        )

    async def async_stop_server(self, server_name: str) -> Dict[str, Any]:
        """
        Stops the specified running Bedrock server instance.

        Corresponds to `POST /api/server/{server_name}/stop`.
        Requires authentication.

        Args:
            server_name: The unique name of the server instance to stop.
        """
        _LOGGER.info("Requesting stop for server '%s'", server_name)
        return await self._request(
            "POST",
            f"/server/{server_name}/stop",
            authenticated=True,
        )

    async def async_restart_server(self, server_name: str) -> Dict[str, Any]:
        """
        Restarts the specified Bedrock server instance.

        Corresponds to `POST /api/server/{server_name}/restart`.
        Requires authentication.

        Args:
            server_name: The unique name of the server instance to restart.
        """
        _LOGGER.info("Requesting restart for server '%s'", server_name)
        return await self._request(
            "POST",
            f"/server/{server_name}/restart",
            authenticated=True,
        )

    async def async_send_server_command(
        self, server_name: str, command: str
    ) -> Dict[str, Any]:
        """
        Sends a command string to the specified server's console.

        Corresponds to `POST /api/server/{server_name}/send_command`.
        Requires authentication.

        Args:
            server_name: The unique name of the target server instance.
            command: The command string to send.
        """
        if not command or command.isspace():
            raise ValueError("Command cannot be empty or just whitespace.")
        _LOGGER.info("Sending command to server '%s': '%s'", server_name, command)
        payload = {"command": command}

        return await self._request(
            "POST",
            f"/server/{server_name}/send_command",
            json_data=payload,
            authenticated=True,
        )

    async def async_update_server(self, server_name: str) -> Dict[str, Any]:
        """
        Checks for and applies updates to the specified server instance.

        Corresponds to `POST /api/server/{server_name}/update`.
        Requires authentication.

        Args:
            server_name: The unique name of the server instance to update.
        """
        _LOGGER.info("Requesting update for server '%s'", server_name)
        return await self._request(
            "POST",
            f"/server/{server_name}/update",
            authenticated=True,
        )

    async def async_add_server_allowlist(
        self, server_name: str, players: List[str], ignores_player_limit: bool = False
    ) -> Dict[str, Any]:
        """
        Adds players to the server's allowlist.json file.

        Corresponds to `POST /api/server/{server_name}/allowlist/add`.
        Requires authentication.

        Args:
            server_name: The name of the server.
            players: A list of player names (Gamertags) to add.
            ignores_player_limit: Sets the 'ignoresPlayerLimit' flag for added players.
        """
        if not isinstance(players, list):
            raise TypeError("Players must be a list of strings.")
        if (
            not all(isinstance(p, str) and p.strip() for p in players) and players
        ):  # Allow empty list, but not list with empty/invalid names
            raise ValueError("All player names in the list must be non-empty strings.")

        _LOGGER.info(
            "Adding players %s to allowlist for server '%s' (ignores limit: %s)",
            players,
            server_name,
            ignores_player_limit,
        )
        payload = {"players": players, "ignoresPlayerLimit": ignores_player_limit}

        return await self._request(
            "POST",
            f"/server/{server_name}/allowlist/add",
            json_data=payload,
            authenticated=True,
        )

    async def async_remove_server_allowlist_player(
        self, server_name: str, player_name: str
    ) -> Dict[str, Any]:
        """
        Removes a specific player from the server's allowlist.json.
        The player_name in the path will be URL-encoded.

        Corresponds to `DELETE /api/server/{server_name}/allowlist/player/{player_name}`.
        Requires authentication.

        Args:
            server_name: The name of the server.
            player_name: The name of the player to remove (case-insensitive on API side).
        """
        if not player_name or player_name.isspace():
            raise ValueError("Player name cannot be empty or just whitespace.")

        _LOGGER.info(
            "Removing player '%s' from allowlist for server '%s'",
            player_name,
            server_name,
        )
        encoded_player_name = quote(player_name)

        return await self._request(
            "DELETE",
            f"/server/{server_name}/allowlist/player/{encoded_player_name}",
            authenticated=True,
        )

    async def async_set_server_permissions(
        self, server_name: str, permissions_dict: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Updates permission levels for players in the server's permissions.json.

        Corresponds to `PUT /api/server/{server_name}/permissions`.
        Requires authentication.

        Args:
            server_name: The name of the server.
            permissions_dict: A dictionary mapping player XUIDs (strings) to
                              permission levels ("visitor", "member", "operator").
        """
        if not isinstance(permissions_dict, dict):
            raise TypeError("permissions_dict must be a dictionary.")

        processed_permissions: Dict[str, str] = {}
        for xuid, level in permissions_dict.items():
            if (
                not isinstance(level, str)
                or level.lower() not in ALLOWED_PERMISSION_LEVELS
            ):
                _LOGGER.error(
                    "Invalid permission level '%s' for XUID '%s'. Allowed: %s",
                    level,
                    xuid,
                    ALLOWED_PERMISSION_LEVELS,
                )
                raise ValueError(
                    f"Invalid permission level '{level}' for XUID '{xuid}'. "
                    f"Allowed levels are: {', '.join(ALLOWED_PERMISSION_LEVELS)}"
                )
            processed_permissions[xuid] = level.lower()  # API stores lowercase

        _LOGGER.info(
            "Setting permissions for server '%s': %s",
            server_name,
            processed_permissions,
        )
        payload = {"permissions": processed_permissions}

        return await self._request(
            "PUT",
            f"/server/{server_name}/permissions",
            json_data=payload,
            authenticated=True,
        )

    async def async_update_server_properties(
        self, server_name: str, properties_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Updates specified key-value pairs in the server's server.properties file.
        Only allowed properties will be modified by the API.

        Corresponds to `POST /api/server/{server_name}/properties`.
        Requires authentication.

        Args:
            server_name: The name of the server.
            properties_dict: A dictionary of properties to update.
        """
        if not isinstance(properties_dict, dict):
            raise TypeError("properties_dict must be a dictionary.")

        for key_provided in properties_dict.keys():
            if key_provided not in ALLOWED_SERVER_PROPERTIES_TO_UPDATE:
                _LOGGER.warning(
                    "Property '%s' is not in the list of API-allowed modifiable properties and might be ignored by the API.",
                    key_provided,
                )

        _LOGGER.info(
            "Updating properties for server '%s': %s", server_name, properties_dict
        )
        # The API expects the properties directly as the JSON body, not nested under a key.
        payload = properties_dict

        return await self._request(
            "POST",
            f"/server/{server_name}/properties",
            json_data=payload,
            authenticated=True,
        )

    async def async_configure_server_os_service(
        self, server_name: str, service_config: Dict[str, bool]
    ) -> Dict[str, Any]:
        """
        Configures OS-specific service settings (e.g., systemd, autoupdate flag).
        The exact keys required in `service_config` depend on the server's OS.
        Linux: {"autoupdate": bool, "autostart": bool}
        Windows: {"autoupdate": bool}

        Corresponds to `POST /api/server/{server_name}/service`.
        Requires authentication.

        Args:
            server_name: The name of the server.
            service_config: A dictionary with OS-specific boolean flags.
        """
        if not isinstance(service_config, dict):
            raise TypeError("service_config must be a dictionary.")
        for key, value in service_config.items():
            if not isinstance(value, bool):
                raise ValueError(
                    f"Value for service config key '{key}' must be a boolean."
                )

        _LOGGER.info(
            "Requesting OS service config for server '%s' with payload: %s",
            server_name,
            service_config,
        )

        return await self._request(
            "POST",
            f"/server/{server_name}/service",
            json_data=service_config,
            authenticated=True,
        )

    async def async_delete_server(self, server_name: str) -> Dict[str, Any]:
        """
        Permanently deletes all data associated with the specified server instance.
        **USE WITH EXTREME CAUTION: This action is irreversible.**

        Corresponds to `DELETE /api/server/{server_name}/delete`.
        Requires authentication.

        Args:
            server_name: The unique name of the server instance to delete.
        """
        _LOGGER.warning(
            "Requesting DELETION of server '%s'. THIS IS IRREVERSIBLE.", server_name
        )
        return await self._request(
            "DELETE",
            f"/server/{server_name}/delete",
            authenticated=True,
        )
