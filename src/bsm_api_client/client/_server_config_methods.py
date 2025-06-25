# src/bsm_api_client/client/_server_config_methods.py
"""Mixin class containing server-specific configuration methods."""
import logging
from typing import Any, Dict, Optional, List, TYPE_CHECKING, Union
from urllib.parse import quote

if TYPE_CHECKING:
    from ..client_base import ClientBase
    from ..exceptions import APIError, InvalidInputError

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.server_config")

# As per API documentation for POST /api/server/{server_name}/properties/set
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


class ServerConfigMethodsMixin:
    """Mixin for server-specific configuration endpoints."""

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

    async def async_set_server_properties(
        self, server_name: str, properties_to_set: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Updates specified key-value pairs in the server's server.properties file.
        Only properties present in a predefined allowlist can be modified by the API.

        Corresponds to `POST /api/server/{server_name}/properties/set`.
        Requires authentication.

        Args:
            server_name: The name of the server.
            properties_to_set: A dictionary of properties to update.
                               Values are typically strings, but numbers are accepted by API for relevant fields.

        Returns:
            API response dictionary.

        Raises:
            InvalidInputError: If properties_to_set is not a dictionary.
            APIError: For other API communication or processing errors.
        """
        if not isinstance(properties_to_set, dict):
            from ..exceptions import InvalidInputError

            raise InvalidInputError("properties_to_set must be a dictionary.")

        # Log a warning for any keys not in the API's documented allowlist
        for key_provided in properties_to_set.keys():
            if key_provided not in ALLOWED_SERVER_PROPERTIES_TO_UPDATE:
                _LOGGER.warning(
                    "Property '%s' is not in the API's documented list of allowed "
                    "modifiable properties and might be ignored by the API or cause an error.",
                    key_provided,
                )

        _LOGGER.info(
            "Updating server properties for '%s': %s", server_name, properties_to_set
        )
        encoded_server_name = quote(server_name)
        # The API expects the properties_to_set dictionary directly as the JSON body.
        return await self._request(
            "POST",
            f"/server/{encoded_server_name}/properties/set",
            json_data=properties_to_set,
            authenticated=True,
        )

    async def async_update_server_service_config(
        self, server_name: str, service_config_payload: Dict[str, bool]
    ) -> Dict[str, Any]:
        """
        Configures OS-specific service settings for the server instance.
        Payload depends on the host OS (Linux: autoupdate, autostart; Windows: autoupdate).

        Corresponds to `POST /api/server/{server_name}/service/update`.
        Requires authentication.

        Args:
            server_name: The name of the server.
            service_config_payload: A dictionary with OS-specific boolean flags.
                                    E.g., {"autoupdate": True, "autostart": True} for Linux.

        Returns:
            API response dictionary.

        Raises:
            InvalidInputError: If service_config_payload is not a dictionary or contains non-boolean values.
            APIError: For other API communication or processing errors.
        """
        if not isinstance(service_config_payload, dict):
            from ..exceptions import InvalidInputError

            raise InvalidInputError("service_config_payload must be a dictionary.")

        for key, value in service_config_payload.items():
            if not isinstance(value, bool):
                from ..exceptions import InvalidInputError

                raise InvalidInputError(
                    f"Value for service config key '{key}' must be a boolean. Got: {value}"
                )

        _LOGGER.info(
            "Updating OS service config for server '%s': %s",
            server_name,
            service_config_payload,
        )
        encoded_server_name = quote(server_name)
        return await self._request(
            "POST",
            f"/server/{encoded_server_name}/service/update",
            json_data=service_config_payload,
            authenticated=True,
        )
