# src/bsm_api_client/client/_server_action_methods.py
"""Mixin class for server action methods.

This module provides the `ServerActionMethodsMixin` class, which includes
methods for performing actions on a specific server instance, such as
starting, stopping, and sending commands.
"""

import logging
from typing import Any, Callable, cast

from ..models import (
    ActionResponse,
    AllowlistAddPayload,
    AllowlistRemovePayload,
    BanAddRequest,
    BanRemoveRequest,
    BaseApiResponse,
    CommandPayload,
    PermissionsSetPayload,
    PermissionsUpdateResponse,
    PropertiesPayload,
)

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

    _request: Callable[..., Any]
    is_linux_server: Callable[..., bool]
    is_windows_server: Callable[..., bool]

    async def async_start_server(self, server_name: str) -> ActionResponse:
        """Starts the specified Bedrock server instance.

        :param server_name: The unique name of the server instance to start.

        :returns: An `ActionResponse` object confirming the action.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_start_server('MyServer')
        """
        _LOGGER.info("Requesting start for server '%s'", server_name)
        response = await self._request(
            "POST",
            f"/server/{server_name}/start",
            authenticated=True,
        )
        return cast(ActionResponse, ActionResponse.model_validate(response))

    async def async_stop_server(self, server_name: str) -> ActionResponse:
        """Stops the specified running Bedrock server instance.

        :param server_name: The unique name of the server instance to stop.

        :returns: An `ActionResponse` object confirming the action.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_stop_server('MyServer')
        """
        _LOGGER.info("Requesting stop for server '%s'", server_name)
        response = await self._request(
            "POST",
            f"/server/{server_name}/stop",
            authenticated=True,
        )
        return cast(ActionResponse, ActionResponse.model_validate(response))

    async def async_restart_server(self, server_name: str) -> ActionResponse:
        """Restarts the specified Bedrock server instance.

        :param server_name: The unique name of the server instance to restart.

        :returns: An `ActionResponse` object confirming the action.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_restart_server('MyServer')
        """
        _LOGGER.info("Requesting restart for server '%s'", server_name)
        response = await self._request(
            "POST",
            f"/server/{server_name}/restart",
            authenticated=True,
        )
        return cast(ActionResponse, ActionResponse.model_validate(response))

    async def async_send_server_command(
        self, server_name: str, command: CommandPayload
    ) -> ActionResponse:
        """Sends a command to the specified server's console.

        :param server_name: The unique name of the target server instance.
        :param command: A `CommandPayload` object containing the command to send.

        :returns: An `ActionResponse` object confirming the action.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_send_server_command('MyServer')
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
        return cast(ActionResponse, ActionResponse.model_validate(response))

    async def async_update_server(self, server_name: str) -> ActionResponse:
        """Checks for and applies updates to the specified server instance.

        :param server_name: The unique name of the server instance to update.

        :returns: An `ActionResponse` object confirming the action.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_update_server('MyServer')
        """
        _LOGGER.info("Requesting update for server '%s'", server_name)
        response = await self._request(
            "POST",
            f"/server/{server_name}/update",
            authenticated=True,
        )
        return cast(ActionResponse, ActionResponse.model_validate(response))

    async def async_add_server_allowlist(
        self, server_name: str, payload: AllowlistAddPayload
    ) -> BaseApiResponse:
        """Adds players to the server's allowlist.

        :param server_name: The name of the server.
        :param payload: An `AllowlistAddPayload` object with the players to add.

        :returns: A `BaseApiResponse` object confirming the action.


        .. rubric:: Example:
        .. code-block:: python

            payload = ...
            response = await client.async_add_server_allowlist(payload)
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
        return cast(BaseApiResponse, BaseApiResponse.model_validate(response))

    async def async_remove_server_allowlist_players(
        self, server_name: str, payload: AllowlistRemovePayload
    ) -> BaseApiResponse:
        """Removes players from the server's allowlist.

        :param server_name: The name of the server.
        :param payload: An `AllowlistRemovePayload` object with the players to remove.

        :returns: A `BaseApiResponse` object confirming the action.


        .. rubric:: Example:
        .. code-block:: python

            payload = ...
            response = await client.async_remove_server_allowlist_players(payload)
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
        return cast(BaseApiResponse, BaseApiResponse.model_validate(response))

    async def async_set_server_permissions(
        self, server_name: str, payload: PermissionsSetPayload
    ) -> PermissionsUpdateResponse:
        """Updates permission levels for players on the server.

        :param server_name: The name of the server.
        :param payload: A `PermissionsSetPayload` object with the permissions to set.

        :returns: A `PermissionsUpdateResponse` object confirming the action.


        .. rubric:: Example:
        .. code-block:: python

            payload = ...
            response = await client.async_set_server_permissions(payload)
        """
        _LOGGER.info(
            "Setting permissions for server '%s': %s",
            server_name,
            payload.permissions,
        )

        response = await self._request(
            "POST",
            f"/server/{server_name}/permissions/set",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return cast(
            PermissionsUpdateResponse,
            PermissionsUpdateResponse.model_validate(response),
        )

    async def async_update_server_properties(
        self, server_name: str, payload: PropertiesPayload
    ) -> BaseApiResponse:
        """Updates key-value pairs in the server's properties file.

        :param server_name: The name of the server.
        :param payload: A `PropertiesPayload` object with the properties to update.

        :returns: A `BaseApiResponse` object confirming the action.


        .. rubric:: Example:
        .. code-block:: python

            payload = ...
            response = await client.async_update_server_properties(payload)
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
        return cast(BaseApiResponse, BaseApiResponse.model_validate(response))

    async def async_delete_server(self, server_name: str) -> ActionResponse:
        """Permanently deletes a server instance.

        Warning:
            This action is irreversible and will delete all data associated with the server.

        :param server_name: The unique name of the server instance to delete.

        :returns: An `ActionResponse` object confirming the action.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_delete_server('MyServer')
        """
        _LOGGER.warning(
            "Requesting DELETION of server '%s'. THIS IS IRREVERSIBLE.", server_name
        )
        response = await self._request(
            "DELETE",
            f"/server/{server_name}/delete",
            authenticated=True,
        )
        return cast(ActionResponse, ActionResponse.model_validate(response))

    async def async_get_server_bans(self, server_name: str) -> dict[str, Any]:
        """Get all bans for a specific server.

        :param server_name: The name of the server.
        :returns: A dictionary containing the bans.
        """
        _LOGGER.debug("Fetching bans for server '%s'", server_name)
        response = await self._request(
            "GET",
            f"/server/{server_name}/bans/get",
            authenticated=True,
        )
        return dict(response)

    async def async_add_server_ban(
        self, server_name: str, payload: "BanAddRequest"
    ) -> dict[str, Any]:
        """Add a player to the server ban list.

        :param server_name: The name of the server.
        :param payload: The BanAddRequest payload.
        :returns: A dictionary response.
        """
        _LOGGER.debug(
            "Adding ban for server '%s': %s", server_name, payload.model_dump()
        )
        response = await self._request(
            "POST",
            f"/server/{server_name}/bans/add",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return dict(response)

    async def async_remove_server_ban(
        self, server_name: str, payload: "BanRemoveRequest"
    ) -> dict[str, Any]:
        """Remove a player from the server ban list.

        :param server_name: The name of the server.
        :param payload: The BanRemoveRequest payload.
        :returns: A dictionary response.
        """
        _LOGGER.debug(
            "Removing ban for server '%s': %s", server_name, payload.model_dump()
        )
        response = await self._request(
            "DELETE",
            f"/server/{server_name}/bans/remove",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return dict(response)
