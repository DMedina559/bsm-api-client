from ..models import (
    GetAllowlistResponse,
    GetPermissionsResponse,
    GetPropertiesResponse,
    ServerSummary,
)

"Mixin class for server information retrieval methods.\n\nThis module provides the `ServerInfoMethodsMixin` class, which includes\nmethods for retrieving information about server instances from the Bedrock\nServer Manager API.\n"
import logging
from typing import List, cast

from ..exceptions import APIError, ServerNotFoundError
from ..generated_adapter import GeneratedOperationMethods
from ..models import (
    ServerProcessInfoResponse,
    ServerRunningStatusResponse,
    ServerSettingItemPayload,
    ServerSettingsResponse,
    ServersListResponse,
)
from ..validation import parse_response

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.server_info")


class ServerInfoMethodsMixin(GeneratedOperationMethods):
    """Mixin for server information endpoints."""

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
