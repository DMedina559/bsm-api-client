import logging
from typing import List, cast

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
    GetRawPropertiesResponse,
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
    """Server lifecycle, configuration, access control, and installation workflows."""

    async def async_get_servers(self) -> ServersListResponse:
        """Retrieves a list of all detected server instances with their status and version.

        :returns: `ServersListResponse`.

        .. code-block:: python

            response = await client.servers.async_get_servers()
        """
        _LOGGER.debug("Fetching server list from /api/servers")
        response_data = await self.async_call_generated(
            "list_servers", authenticated=True, typed=True
        )
        return cast(
            ServersListResponse, parse_response(ServersListResponse, response_data)
        )

    async def async_get_server_names(self) -> List[str]:
        """Fetches a list of server names.

        :returns: `List[str]`.

        .. code-block:: python

            response = await client.servers.async_get_server_names()
        """
        _LOGGER.debug("Fetching server names list")
        server_details = await self.async_get_servers()
        if server_details.servers:
            return sorted([server.name for server in server_details.servers])
        return []

    async def async_get_server_validate(self, server_name: str) -> bool:
        """Validate the server using the backend validation rules.

        :param server_name: The name of the server to validate.

        :returns: `bool`.

        .. code-block:: python

            response = await client.servers.async_get_server_validate("MyServer")
        """
        _LOGGER.debug("Validating existence of server: '%s'", server_name)
        try:
            response = await self.async_call_generated(
                "validate_server",
                parameters={"server_name": server_name},
                authenticated=True,
                typed=True,
            )
            return bool(response.get("status") == "success")
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

        :returns: `ServerSummary`.

        .. code-block:: python

            response = await client.servers.async_get_server_summary("MyServer")
        """
        _LOGGER.debug("Fetching summary for server '%s'", server_name)
        response = await self.async_call_generated(
            "get_server_summary",
            parameters={"server_name": server_name},
            authenticated=True,
            typed=True,
        )
        return cast(ServerSummary, parse_response(ServerSummary, response))

    async def async_get_server_process_info(
        self, server_name: str
    ) -> ServerProcessInfoResponse:
        """Gets runtime process information for a server.

        :param server_name: The name of the server.

        :returns: `ServerProcessInfoResponse`.

        .. code-block:: python

            response = await client.servers.async_get_server_process_info("MyServer")
        """
        _LOGGER.debug("Fetching status info for server '%s'", server_name)
        response = await self.async_call_generated(
            "get_server_process_info",
            parameters={"server_name": server_name},
            authenticated=True,
            typed=True,
        )
        return cast(
            ServerProcessInfoResponse,
            parse_response(ServerProcessInfoResponse, response),
        )

    async def async_get_world_icon_image(self, server_name: str) -> bytes:
        """Retrieves the world icon image for a server.

        :param server_name: The name of the server.

        :returns: `bytes`.
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

        :returns: `ServerRunningStatusResponse`.

        .. code-block:: python

            response = await client.servers.async_get_server_running_status("MyServer")
        """
        _LOGGER.debug("Fetching running status for server '%s'", server_name)
        response = await self.async_call_generated(
            "get_server_status",
            parameters={"server_name": server_name},
            authenticated=True,
            typed=True,
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

        :returns: `GetPropertiesResponse`.

        .. code-block:: python

            response = await client.servers.async_get_server_properties("MyServer")
        """
        _LOGGER.debug("Fetching server.properties for server '%s'", server_name)
        response = await self.async_call_generated(
            "get_properties",
            parameters={"server_name": server_name},
            authenticated=True,
            typed=True,
        )
        return cast(
            GetPropertiesResponse,
            parse_response(GetPropertiesResponse, response),
        )

    async def async_get_raw_server_properties(
        self, server_name: str
    ) -> GetRawPropertiesResponse:
        """Return the complete read-only properties document, including Mojang comments."""
        response = await self.async_call_generated(
            "get_raw_properties",
            parameters={"server_name": server_name},
            authenticated=True,
            typed=True,
        )
        return cast(
            GetRawPropertiesResponse, parse_response(GetRawPropertiesResponse, response)
        )

    async def async_get_server_permissions_data(
        self, server_name: str
    ) -> GetPermissionsResponse:
        """Retrieves player permissions from the server.

        :param server_name: The name of the server.

        :returns: `GetPermissionsResponse`.

        .. code-block:: python

            response = await client.servers.async_get_server_permissions_data("MyServer")
        """
        _LOGGER.debug("Fetching permissions.json data for server '%s'", server_name)
        response = await self.async_call_generated(
            "get_permissions",
            parameters={"server_name": server_name},
            authenticated=True,
            typed=True,
        )
        return cast(
            GetPermissionsResponse, parse_response(GetPermissionsResponse, response)
        )

    async def async_get_server_allowlist(
        self, server_name: str
    ) -> GetAllowlistResponse:
        """Retrieves the server's allowlist.

        :param server_name: The name of the server.

        :returns: `GetAllowlistResponse`.

        .. code-block:: python

            response = await client.servers.async_get_server_allowlist("MyServer")
        """
        _LOGGER.debug("Fetching allowlist.json for server '%s'", server_name)
        response = await self.async_call_generated(
            "get_allowlist",
            parameters={"server_name": server_name},
            authenticated=True,
            typed=True,
        )
        return cast(
            GetAllowlistResponse, parse_response(GetAllowlistResponse, response)
        )

    async def async_get_server_settings(
        self, server_name: str
    ) -> ServerSettingsResponse:
        """Retrieves all settings for a specific server.

        :param server_name: The name of the server.

        :returns: `ServerSettingsResponse`.
        """
        _LOGGER.debug("Fetching settings for server '%s'", server_name)
        response = await self.async_call_generated(
            "get_server_settings",
            parameters={"server_name": server_name},
            authenticated=True,
            typed=True,
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

        :returns: `ServerSettingsResponse`.
        """
        _LOGGER.debug("Updating setting '%s' for server '%s'", payload.key, server_name)
        response = await self.async_call_generated(
            "set_server_setting",
            parameters={"server_name": server_name},
            body=payload.model_dump(),
            authenticated=True,
            typed=True,
        )
        return cast(
            ServerSettingsResponse, parse_response(ServerSettingsResponse, response)
        )

    async def async_start_server(self, server_name: str) -> StartServerResponse:
        """Starts the specified Bedrock server instance.

        :param server_name: The unique name of the server instance to start.

        :returns: `StartServerResponse`.

        .. code-block:: python

            response = await client.servers.async_start_server("MyServer")
        """
        _LOGGER.info("Requesting start for server '%s'", server_name)
        response = await self.async_call_generated(
            "start_server",
            parameters={"server_name": server_name},
            authenticated=True,
            typed=True,
        )
        return cast(StartServerResponse, parse_response(StartServerResponse, response))

    async def async_stop_server(self, server_name: str) -> StopServerResponse:
        """Stops the specified running Bedrock server instance.

        :param server_name: The unique name of the server instance to stop.

        :returns: `StopServerResponse`.

        .. code-block:: python

            response = await client.servers.async_stop_server("MyServer")
        """
        _LOGGER.info("Requesting stop for server '%s'", server_name)
        response = await self.async_call_generated(
            "stop_server",
            parameters={"server_name": server_name},
            authenticated=True,
            typed=True,
        )
        return cast(StopServerResponse, parse_response(StopServerResponse, response))

    async def async_restart_server(self, server_name: str) -> RestartServerResponse:
        """Restarts the specified Bedrock server instance.

        :param server_name: The unique name of the server instance to restart.

        :returns: `RestartServerResponse`.

        .. code-block:: python

            response = await client.servers.async_restart_server("MyServer")
        """
        _LOGGER.info("Requesting restart for server '%s'", server_name)
        response = await self.async_call_generated(
            "restart_server",
            parameters={"server_name": server_name},
            authenticated=True,
            typed=True,
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

        :returns: `ActionResponse`.

        .. code-block:: python

            response = await client.servers.async_send_server_command("MyServer", command)
        """
        _LOGGER.debug("Sending a console command to server '%s'", server_name)
        response = await self.async_call_generated(
            "send_command",
            parameters={"server_name": server_name},
            body=command.model_dump(),
            authenticated=True,
            typed=True,
        )
        return cast(ActionResponse, parse_response(ActionResponse, response))

    async def async_update_server(self, server_name: str) -> TaskAcceptedResponse:
        """Checks for and applies updates to the specified server instance.

        :param server_name: The unique name of the server instance to update.

        :returns: `TaskAcceptedResponse`.

        .. code-block:: python

            response = await client.servers.async_update_server("MyServer")
        """
        _LOGGER.info("Requesting update for server '%s'", server_name)
        response = await self.async_call_generated(
            "update_server",
            parameters={"server_name": server_name},
            authenticated=True,
            typed=True,
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

        :returns: `BaseApiResponse`.

        .. code-block:: python

            response = await client.servers.async_add_server_allowlist("MyServer", payload)
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
            typed=True,
        )
        return cast(BaseApiResponse, parse_response(BaseApiResponse, response))

    async def async_remove_server_allowlist_players(
        self, server_name: str, payload: AllowlistRemovePayload
    ) -> BaseApiResponse:
        """Removes players from the server's allowlist.

        :param server_name: The name of the server.

        :param payload: An `AllowlistRemovePayload` object with the players to remove.

        :returns: `BaseApiResponse`.

        .. code-block:: python

            response = await client.servers.async_remove_server_allowlist_players("MyServer", payload)
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
            typed=True,
        )
        return cast(BaseApiResponse, parse_response(BaseApiResponse, response))

    async def async_set_server_permissions(
        self, server_name: str, payload: PermissionsSetPayload
    ) -> PermissionsUpdateResponse:
        """Updates permission levels for players on the server.

        :param server_name: The name of the server.

        :param payload: A `PermissionsSetPayload` object with the permissions to set.

        :returns: `PermissionsUpdateResponse`.

        .. code-block:: python

            response = await client.servers.async_set_server_permissions("MyServer", payload)
        """
        _LOGGER.info(
            "Setting permissions for server '%s': %s", server_name, payload.permissions
        )
        response = await self.async_call_generated(
            "set_permissions",
            parameters={"server_name": server_name},
            body=payload.model_dump(),
            authenticated=True,
            typed=True,
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

        :returns: `BaseApiResponse`.

        .. code-block:: python

            response = await client.servers.async_update_server_properties("MyServer", payload)
        """
        _LOGGER.info(
            "Updating properties for server '%s': %s", server_name, payload.properties
        )
        response = await self.async_call_generated(
            "set_properties",
            parameters={"server_name": server_name},
            body=payload.model_dump(),
            authenticated=True,
            typed=True,
        )
        return cast(BaseApiResponse, parse_response(BaseApiResponse, response))

    async def async_delete_server(self, server_name: str) -> TaskAcceptedResponse:
        """Permanently deletes a server instance.

        Deletes the server data permanently. The returned task tracks completion.

        :param server_name: The unique name of the server instance to delete.

        :returns: `TaskAcceptedResponse`.

        .. code-block:: python

            response = await client.servers.async_delete_server("MyServer")
        """
        _LOGGER.warning(
            "Requesting DELETION of server '%s'. THIS IS IRREVERSIBLE.", server_name
        )
        response = await self.async_call_generated(
            "delete_server",
            parameters={"server_name": server_name},
            authenticated=True,
            typed=True,
        )
        return cast(
            TaskAcceptedResponse, parse_response(TaskAcceptedResponse, response)
        )

    async def async_get_server_bans(self, server_name: str) -> GetServerBansResponse:
        """Get all bans for a specific server.

        :param server_name: The name of the server.

        :returns: `GetServerBansResponse`.
        """
        _LOGGER.debug("Fetching bans for server '%s'", server_name)
        response = await self.async_call_generated(
            "get_server_bans",
            parameters={"server_name": server_name},
            authenticated=True,
            typed=True,
        )
        return cast(
            GetServerBansResponse,
            parse_response(GetServerBansResponse, response),
        )

    async def async_add_server_ban(
        self, server_name: str, payload: "BanAddRequest"
    ) -> AddServerBanResponse:
        """Add a player to the server ban list.

        :param server_name: The name of the server.

        :param payload: The BanAddRequest payload.

        :returns: `AddServerBanResponse`.
        """
        _LOGGER.debug(
            "Adding ban for server '%s': %s", server_name, payload.model_dump()
        )
        response = await self.async_call_generated(
            "add_server_ban",
            parameters={"server_name": server_name},
            body=payload.model_dump(),
            authenticated=True,
            typed=True,
        )
        return cast(
            AddServerBanResponse,
            parse_response(AddServerBanResponse, response),
        )

    async def async_remove_server_ban(
        self, server_name: str, payload: "BanRemoveRequest"
    ) -> RemoveServerBanResponse:
        """Remove a player from the server ban list.

        :param server_name: The name of the server.

        :param payload: The BanRemoveRequest payload.

        :returns: `RemoveServerBanResponse`.
        """
        _LOGGER.debug(
            "Removing ban for server '%s': %s", server_name, payload.model_dump()
        )
        response = await self.async_call_generated(
            "remove_server_ban",
            parameters={"server_name": server_name},
            body=payload.model_dump(),
            authenticated=True,
            typed=True,
        )
        return cast(
            RemoveServerBanResponse,
            parse_response(RemoveServerBanResponse, response),
        )

    async def async_install_new_server(
        self, payload: InstallServerPayload
    ) -> InstallServerResponse:
        """Requests the installation of a new Bedrock server instance.

        :param payload: The InstallServerPayload request model.

        :returns: `InstallServerResponse`.
        """
        _LOGGER.info(
            "Requesting installation for server '%s', version: '%s', overwrite: %s",
            payload.server_name,
            payload.server_version,
            payload.overwrite,
        )
        response = await self.async_call_generated(
            "install_server", body=payload.model_dump(), authenticated=True, typed=True
        )
        return cast(
            InstallServerResponse, parse_response(InstallServerResponse, response)
        )
