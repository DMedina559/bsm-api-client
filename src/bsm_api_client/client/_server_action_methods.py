# src/bsm_api_client/client/_server_action_methods.py
"""Mixin class for server action methods.

This module provides the `ServerActionMethodsMixin` class, which includes
methods for performing actions on a specific server instance, such as
starting, stopping, and sending commands.
"""
import logging
from typing import Any, Dict, Optional, List, TYPE_CHECKING
from urllib.parse import quote
from ..models import (
    CommandPayload,
    AllowlistAddPayload,
    AllowlistRemovePayload,
    PermissionsSetPayload,
    PropertiesPayload,
    ServiceUpdatePayload,
    ActionResponse,
)

if TYPE_CHECKING:
    from ..client_base import ClientBase

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

    async def async_start_server(self, server_name: str) -> ActionResponse:
        """Starts the specified Bedrock server instance.

        Args:
            server_name: The unique name of the server instance to start.

        Returns:
            An `ActionResponse` object confirming the action.
        """
        _LOGGER.info("Requesting start for server '%s'", server_name)
        response = await self._request(
            "POST",
            f"/server/{server_name}/start",
            authenticated=True,
        )
        return ActionResponse.model_validate(response)

    async def async_enable_server_service(self, server_name: str) -> ActionResponse:
        """Enables the system service for the specified server.

        Args:
            server_name: The name of the server.

        Returns:
            An `ActionResponse` object confirming the action.
        """
        _LOGGER.info("Enabling service for server '%s'", server_name)
        return await self.async_configure_server_os_service(
            server_name, ServiceUpdatePayload(autostart=True)
        )

    async def async_disable_server_service(self, server_name: str) -> ActionResponse:
        """Disables the system service for the specified server.

        Args:
            server_name: The name of the server.

        Returns:
            An `ActionResponse` object confirming the action.
        """
        _LOGGER.info("Disabling service for server '%s'", server_name)
        return await self.async_configure_server_os_service(
            server_name, ServiceUpdatePayload(autostart=False)
        )

    async def async_set_server_autoupdate(
        self, server_name: str, autoupdate: bool
    ) -> ActionResponse:
        """Sets the autoupdate flag for the specified server.

        Args:
            server_name: The name of the server.
            autoupdate: The desired autoupdate state.

        Returns:
            An `ActionResponse` object confirming the action.
        """
        _LOGGER.info(
            "Setting autoupdate for server '%s' to %s", server_name, autoupdate
        )
        return await self.async_configure_server_os_service(
            server_name, ServiceUpdatePayload(autoupdate=autoupdate)
        )

    async def async_create_server_service(
        self, server_name: str, autostart: bool
    ) -> ActionResponse:
        """Creates the system service for the specified server.

        Args:
            server_name: The name of the server.
            autostart: Whether the service should start on boot.

        Returns:
            An `ActionResponse` object confirming the action.
        """
        _LOGGER.info(
            "Creating service for server '%s' with autostart=%s",
            server_name,
            autostart,
        )
        return await self.async_configure_server_os_service(
            server_name, ServiceUpdatePayload(autostart=autostart)
        )

    async def async_stop_server(self, server_name: str) -> ActionResponse:
        """Stops the specified running Bedrock server instance.

        Args:
            server_name: The unique name of the server instance to stop.

        Returns:
            An `ActionResponse` object confirming the action.
        """
        _LOGGER.info("Requesting stop for server '%s'", server_name)
        response = await self._request(
            "POST",
            f"/server/{server_name}/stop",
            authenticated=True,
        )
        return ActionResponse.model_validate(response)

    async def async_restart_server(self, server_name: str) -> ActionResponse:
        """Restarts the specified Bedrock server instance.

        Args:
            server_name: The unique name of the server instance to restart.

        Returns:
            An `ActionResponse` object confirming the action.
        """
        _LOGGER.info("Requesting restart for server '%s'", server_name)
        response = await self._request(
            "POST",
            f"/server/{server_name}/restart",
            authenticated=True,
        )
        return ActionResponse.model_validate(response)

    async def async_send_server_command(
        self, server_name: str, command: CommandPayload
    ) -> ActionResponse:
        """Sends a command to the specified server's console.

        Args:
            server_name: The unique name of the target server instance.
            command: A `CommandPayload` object containing the command to send.

        Returns:
            An `ActionResponse` object confirming the action.
        """
        _LOGGER.info(
            "Sending command to server '%s': '%s'", server_name, command.command
        )

        response = await self._request(
            "POST",
            f"/server/{server_name}/send_command",
            json_data=command.model_dump(),
            authenticated=True,
        )
        return ActionResponse.model_validate(response)

    async def async_update_server(self, server_name: str) -> ActionResponse:
        """Checks for and applies updates to the specified server instance.

        Args:
            server_name: The unique name of the server instance to update.

        Returns:
            An `ActionResponse` object confirming the action.
        """
        _LOGGER.info("Requesting update for server '%s'", server_name)
        response = await self._request(
            "POST",
            f"/server/{server_name}/update",
            authenticated=True,
        )
        return ActionResponse.model_validate(response)

    async def async_add_server_allowlist(
        self, server_name: str, payload: AllowlistAddPayload
    ) -> ActionResponse:
        """Adds players to the server's allowlist.

        Args:
            server_name: The name of the server.
            payload: An `AllowlistAddPayload` object with the players to add.

        Returns:
            An `ActionResponse` object confirming the action.
        """
        _LOGGER.info(
            "Adding players %s to allowlist for server '%s' (ignores limit: %s)",
            payload.players,
            server_name,
            payload.ignoresPlayerLimit,
        )

        response = await self._request(
            "POST",
            f"/server/{server_name}/allowlist/add",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return ActionResponse.model_validate(response)

    async def async_remove_server_allowlist_players(
        self, server_name: str, payload: AllowlistRemovePayload
    ) -> ActionResponse:
        """Removes players from the server's allowlist.

        Args:
            server_name: The name of the server.
            payload: An `AllowlistRemovePayload` object with the players to remove.

        Returns:
            An `ActionResponse` object confirming the action.
        """
        _LOGGER.info(
            "Removing %d players from allowlist for server '%s': %s",
            len(payload.players),
            server_name,
            payload.players,
        )

        response = await self._request(
            "DELETE",
            f"/server/{server_name}/allowlist/remove",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return ActionResponse.model_validate(response)

    async def async_set_server_permissions(
        self, server_name: str, payload: PermissionsSetPayload
    ) -> ActionResponse:
        """Updates permission levels for players on the server.

        Args:
            server_name: The name of the server.
            payload: A `PermissionsSetPayload` object with the permissions to set.

        Returns:
            An `ActionResponse` object confirming the action.
        """
        _LOGGER.info(
            "Setting permissions for server '%s': %s",
            server_name,
            payload.permissions,
        )

        response = await self._request(
            "PUT",
            f"/server/{server_name}/permissions/set",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return ActionResponse.model_validate(response)

    async def async_update_server_properties(
        self, server_name: str, payload: PropertiesPayload
    ) -> ActionResponse:
        """Updates key-value pairs in the server's properties file.

        Args:
            server_name: The name of the server.
            payload: A `PropertiesPayload` object with the properties to update.

        Returns:
            An `ActionResponse` object confirming the action.
        """
        _LOGGER.info(
            "Updating properties for server '%s': %s", server_name, payload.properties
        )

        response = await self._request(
            "POST",
            f"/server/{server_name}/properties/set",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return ActionResponse.model_validate(response)

    async def async_configure_server_os_service(
        self, server_name: str, payload: ServiceUpdatePayload
    ) -> ActionResponse:
        """Configures OS-specific service settings for the server.

        Args:
            server_name: The name of the server.
            payload: A `ServiceUpdatePayload` object with the service settings.

        Returns:
            An `ActionResponse` object confirming the action.
        """
        _LOGGER.info(
            "Requesting OS service config for server '%s' with payload: %s",
            server_name,
            payload.model_dump(),
        )

        response = await self._request(
            "POST",
            f"/server/{server_name}/service/update",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return ActionResponse.model_validate(response)

    async def async_delete_server(self, server_name: str) -> ActionResponse:
        """Permanently deletes a server instance.

        Warning:
            This action is irreversible and will delete all data associated with the server.

        Args:
            server_name: The unique name of the server instance to delete.

        Returns:
            An `ActionResponse` object confirming the action.
        """
        _LOGGER.warning(
            "Requesting DELETION of server '%s'. THIS IS IRREVERSIBLE.", server_name
        )
        response = await self._request(
            "DELETE",
            f"/server/{server_name}/delete",
            authenticated=True,
        )
        return ActionResponse.model_validate(response)
