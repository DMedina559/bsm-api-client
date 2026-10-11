import logging
from typing import Any, List, cast

from ..exceptions import APIError, ServerNotFoundError
from ..models import (
    ActionResponse,
    AddServerBanResponse,
    AllowlistAddPayload,
    AllowlistRemovePayload,
    BanAddRequest,
    BanRemoveRequest,
    BaseApiResponse,
    CommandPayload,
    GetAllowlistResponse,
    GetPermissionsResponse,
    GetPropertiesResponse,
    GetServerBansResponse,
    InstallServerPayload,
    InstallServerResponse,
    PermissionsSetPayload,
    PermissionsUpdateResponse,
    PropertiesPayload,
    RemoveServerBanResponse,
    RestartServerResponse,
    ServerProcessInfoResponse,
    ServerRunningStatusResponse,
    ServerSettingItemPayload,
    ServerSettingsResponse,
    ServersListResponse,
    ServerSummary,
    StartServerResponse,
    StopServerResponse,
    TaskAcceptedResponse,
)
from ..validation import parse_response
from .base import Service

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.server_info")


class ServersService(Service):
    """Service for server information endpoints."""

    async def async_get_servers(self) -> ServersListResponse:
        """Retrieves a list of all detected server instances with their status and version.

        :returns: A `ServersListResponse` object containing a list of servers.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_get_servers()
        """
        _LOGGER.debug("Fetching server list from /api/servers")
        response_data = await self.async_call_generated(
            "list_servers", authenticated=True
        )
        return cast(
            ServersListResponse, parse_response(ServersListResponse, response_data)
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
        try:
            response = await self.async_call_generated(
                "validate_server",
                parameters={"server_name": server_name},
                authenticated=True,
            )
            return isinstance(response, dict) and response.get("status") == "success"
        except ServerNotFoundError:
            _LOGGER.debug(
                "Validation API call indicated server '%s' not found.", server_name
            )
            raise
        except APIError as e:
            _LOGGER.error(
                "API error during validation for server '%s': %s", server_name, e
            )
            raise

    async def async_get_server_summary(self, server_name: str) -> ServerSummary:
        """Retrieves the basic summary information for a specific server instance.

        :param server_name: The name of the server.
        :returns: A `ServerSchemaResponse` object containing the server summary.

        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_get_server_summary('MyServer')
        """
        _LOGGER.debug("Fetching summary for server '%s'", server_name)
        response = await self.async_call_generated(
            "get_server_summary",
            parameters={"server_name": server_name},
            authenticated=True,
        )
        return cast(ServerSummary, parse_response(ServerSummary, response))

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
        response = await self.async_call_generated(
            "get_server_process_info",
            parameters={"server_name": server_name},
            authenticated=True,
        )
        return cast(
            ServerProcessInfoResponse,
            parse_response(ServerProcessInfoResponse, response),
        )

    async def async_get_world_icon_image(self, server_name: str) -> bytes:
        """Retrieves the world icon image for a server.

        :param server_name: The name of the server.

        :returns: The raw bytes of the world icon image.

        :raises ValueError: If `server_name` is empty.
        :raises CannotConnectError: If a connection to the server cannot be established.
        :raises APIError: For other API-related errors.
        """
        if not server_name:
            raise ValueError("Server name cannot be empty.")
        response = await self.async_call_generated(
            "get_world_icon",
            parameters={"server_name": server_name},
            authenticated=True,
            detailed=True,
        )
        return cast(bytes, response.content)

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
        response = await self.async_call_generated(
            "get_server_status",
            parameters={"server_name": server_name},
            authenticated=True,
        )
        return cast(
            ServerRunningStatusResponse,
            parse_response(ServerRunningStatusResponse, response),
        )

    async def async_get_server_properties(
        self, server_name: str
    ) -> GetPropertiesResponse:
        """Retrieves the server's properties.

        :param server_name: The name of the server.

        :returns: A `PropertiesGetResponse` object containing the server properties.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_get_server_properties('MyServer')
        """
        _LOGGER.debug("Fetching server.properties for server '%s'", server_name)
        response = await self.async_call_generated(
            "get_properties",
            parameters={"server_name": server_name},
            authenticated=True,
        )
        return cast(
            GetPropertiesResponse, parse_response(GetPropertiesResponse, response)
        )

    async def async_get_server_permissions_data(
        self, server_name: str
    ) -> GetPermissionsResponse:
        """Retrieves player permissions from the server.

        :param server_name: The name of the server.

        :returns: A `PermissionsGetResponse` object containing the permissions data.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_get_server_permissions_data('MyServer')
        """
        _LOGGER.debug("Fetching permissions.json data for server '%s'", server_name)
        response = await self.async_call_generated(
            "get_permissions",
            parameters={"server_name": server_name},
            authenticated=True,
        )
        return cast(
            GetPermissionsResponse, parse_response(GetPermissionsResponse, response)
        )

    async def async_get_server_allowlist(
        self, server_name: str
    ) -> GetAllowlistResponse:
        """Retrieves the server's allowlist.

        :param server_name: The name of the server.

        :returns: A `AllowlistGetResponse` object containing the allowlist.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_get_server_allowlist('MyServer')
        """
        _LOGGER.debug("Fetching allowlist.json for server '%s'", server_name)
        response = await self.async_call_generated(
            "get_allowlist", parameters={"server_name": server_name}, authenticated=True
        )
        return cast(
            GetAllowlistResponse, parse_response(GetAllowlistResponse, response)
        )

    async def async_get_server_settings(
        self, server_name: str
    ) -> ServerSettingsResponse:
        """Retrieves all settings for a specific server.

        :param server_name: The name of the server.
        :returns: A ServerSettingsResponse.
        """
        _LOGGER.debug("Fetching settings for server '%s'", server_name)
        response = await self.async_call_generated(
            "get_server_settings",
            parameters={"server_name": server_name},
            authenticated=True,
        )
        return cast(
            ServerSettingsResponse, parse_response(ServerSettingsResponse, response)
        )

    async def async_set_server_setting(
        self, server_name: str, payload: ServerSettingItemPayload
    ) -> ServerSettingsResponse:
        """Sets a specific setting for a server.

        :param server_name: The name of the server.
        :param payload: The ServerSettingItemPayload payload.
        :returns: A ServerSettingsResponse.
        """
        _LOGGER.debug("Updating setting '%s' for server '%s'", payload.key, server_name)
        response = await self.async_call_generated(
            "set_server_setting",
            parameters={"server_name": server_name},
            body=payload.model_dump(),
            authenticated=True,
        )
        return cast(
            ServerSettingsResponse, parse_response(ServerSettingsResponse, response)
        )

    async def async_start_server(self, server_name: str) -> StartServerResponse:
        """Starts the specified Bedrock server instance.

        :param server_name: The unique name of the server instance to start.

        :returns: An `StartServerResponse` object confirming the action.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_start_server('MyServer')
        """
        _LOGGER.info("Requesting start for server '%s'", server_name)
        response = await self.async_call_generated(
            "start_server", parameters={"server_name": server_name}, authenticated=True
        )
        return cast(StartServerResponse, parse_response(StartServerResponse, response))

    async def async_stop_server(self, server_name: str) -> StopServerResponse:
        """Stops the specified running Bedrock server instance.

        :param server_name: The unique name of the server instance to stop.

        :returns: An `StopServerResponse` object confirming the action.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_stop_server('MyServer')
        """
        _LOGGER.info("Requesting stop for server '%s'", server_name)
        response = await self.async_call_generated(
            "stop_server", parameters={"server_name": server_name}, authenticated=True
        )
        return cast(StopServerResponse, parse_response(StopServerResponse, response))

    async def async_restart_server(self, server_name: str) -> RestartServerResponse:
        """Restarts the specified Bedrock server instance.

        :param server_name: The unique name of the server instance to restart.

        :returns: An `RestartServerResponse` object confirming the action.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_restart_server('MyServer')
        """
        _LOGGER.info("Requesting restart for server '%s'", server_name)
        response = await self.async_call_generated(
            "restart_server",
            parameters={"server_name": server_name},
            authenticated=True,
        )
        return cast(
            RestartServerResponse, parse_response(RestartServerResponse, response)
        )

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
        _LOGGER.debug("Sending a console command to server '%s'", server_name)
        response = await self.async_call_generated(
            "send_command",
            parameters={"server_name": server_name},
            body=command.model_dump(),
            authenticated=True,
        )
        return cast(ActionResponse, parse_response(ActionResponse, response))

    async def async_update_server(self, server_name: str) -> TaskAcceptedResponse:
        """Checks for and applies updates to the specified server instance.

        :param server_name: The unique name of the server instance to update.

        :returns: An `ActionResponse` object confirming the action.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_update_server('MyServer')
        """
        _LOGGER.info("Requesting update for server '%s'", server_name)
        response = await self.async_call_generated(
            "update_server", parameters={"server_name": server_name}, authenticated=True
        )
        return cast(
            TaskAcceptedResponse, parse_response(TaskAcceptedResponse, response)
        )

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
        response = await self.async_call_generated(
            "add_allowlist_players",
            parameters={"server_name": server_name},
            body=payload.model_dump(),
            authenticated=True,
        )
        return cast(BaseApiResponse, parse_response(BaseApiResponse, response))

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
        response = await self.async_call_generated(
            "remove_allowlist_players",
            parameters={"server_name": server_name},
            body=payload.model_dump(),
            authenticated=True,
        )
        return cast(BaseApiResponse, parse_response(BaseApiResponse, response))

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
            "Setting permissions for server '%s': %s", server_name, payload.permissions
        )
        response = await self.async_call_generated(
            "set_permissions",
            parameters={"server_name": server_name},
            body=payload.model_dump(),
            authenticated=True,
        )
        return cast(
            PermissionsUpdateResponse,
            parse_response(PermissionsUpdateResponse, response),
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
        response = await self.async_call_generated(
            "set_properties",
            parameters={"server_name": server_name},
            body=payload.model_dump(),
            authenticated=True,
        )
        return cast(BaseApiResponse, parse_response(BaseApiResponse, response))

    async def async_delete_server(self, server_name: str) -> TaskAcceptedResponse:
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
        response = await self.async_call_generated(
            "delete_server", parameters={"server_name": server_name}, authenticated=True
        )
        return cast(
            TaskAcceptedResponse, parse_response(TaskAcceptedResponse, response)
        )

    async def async_get_server_bans(self, server_name: str) -> dict[str, Any]:
        """Get all bans for a specific server.

        :param server_name: The name of the server.
        :returns: A dictionary containing the bans.
        """
        _LOGGER.debug("Fetching bans for server '%s'", server_name)
        response = await self.async_call_generated(
            "get_server_bans",
            parameters={"server_name": server_name},
            authenticated=True,
        )
        return cast(
            dict[str, Any],
            parse_response(GetServerBansResponse, response).model_dump(mode="json"),
        )

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
        response = await self.async_call_generated(
            "add_server_ban",
            parameters={"server_name": server_name},
            body=payload.model_dump(),
            authenticated=True,
        )
        return cast(
            dict[str, Any],
            parse_response(AddServerBanResponse, response).model_dump(mode="json"),
        )

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
        response = await self.async_call_generated(
            "remove_server_ban",
            parameters={"server_name": server_name},
            body=payload.model_dump(),
            authenticated=True,
        )
        return cast(
            dict[str, Any],
            parse_response(RemoveServerBanResponse, response).model_dump(mode="json"),
        )

    async def async_install_new_server(
        self, payload: InstallServerPayload
    ) -> InstallServerResponse:
        """Requests the installation of a new Bedrock server instance.

        Args:
            payload: An `InstallServerPayload` object containing the server details.

        Returns:
            An `InstallServerResponse` object with the result of the installation request.
        """
        _LOGGER.info(
            "Requesting installation for server '%s', version: '%s', overwrite: %s",
            payload.server_name,
            payload.server_version,
            payload.overwrite,
        )
        response = await self.async_call_generated(
            "install_server", body=payload.model_dump(), authenticated=True
        )
        return cast(
            InstallServerResponse, parse_response(InstallServerResponse, response)
        )
