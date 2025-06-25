# src/bsm_api_client/client/_player_management_methods.py
"""Mixin class containing server-specific player management methods."""
import logging
from typing import Any, Dict, Optional, List, TYPE_CHECKING, Union
from urllib.parse import quote

if TYPE_CHECKING:
    from ..client_base import ClientBase
    from ..exceptions import APIError, InvalidInputError

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.player_mgmt")

ALLOWED_PERMISSION_LEVELS = [
    "visitor",
    "member",
    "operator",
]  # As per API doc for permissions/set


class PlayerManagementMethodsMixin:
    """Mixin for server-specific player management endpoints (allowlist, permissions)."""

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

    async def async_get_server_allowlist(
        self, server_name: str
    ) -> List[Dict[str, Union[str, bool]]]:
        """
        Retrieves the current list of players from the server's allowlist.json file.

        Corresponds to `GET /api/server/{server_name}/allowlist/get`.
        Requires authentication.

        Args:
            server_name: The name of the server.

        Returns:
            A list of player objects from the allowlist. E.g.,
            `[{"ignoresPlayerLimit": false, "name": "PlayerName"}]`

        Raises:
            ServerNotFoundError: If the server does not exist.
            APIError: For other API communication or processing errors.
        """
        _LOGGER.debug("Fetching allowlist for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        try:
            response_data = await self._request(
                "GET",
                f"/server/{encoded_server_name}/allowlist/get",
                authenticated=True,
            )
            if (
                isinstance(response_data, dict)
                and response_data.get("status") == "success"
                and isinstance(response_data.get("existing_players"), list)
            ):
                return response_data["existing_players"]

            _LOGGER.error(
                "Received non-success or unexpected structure for server allowlist: %s",
                response_data,
            )
            from ..exceptions import APIError as ClientAPIError

            raise ClientAPIError(
                f"Failed to get server allowlist, API response: {response_data.get('status') if isinstance(response_data, dict) else 'N/A'}",
                response_data=(
                    response_data
                    if isinstance(response_data, dict)
                    else {"raw": response_data}
                ),
            )
        except APIError as e:  # type: ignore
            _LOGGER.error(
                "API error fetching server allowlist for '%s': %s", server_name, e
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error processing server allowlist for '%s': %s",
                server_name,
                e,
            )
            from ..exceptions import APIError as ClientAPIError

            raise ClientAPIError(
                f"Unexpected error processing server allowlist for '{server_name}': {e}"
            )

    async def async_add_to_server_allowlist(
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

        Returns:
            API response dictionary.
        """
        if not isinstance(players, list):
            from ..exceptions import InvalidInputError

            raise InvalidInputError("Players must be a list of strings.")
        # API allows empty list, but individual names should be valid if list is not empty
        if players and not all(isinstance(p, str) and p.strip() for p in players):
            from ..exceptions import InvalidInputError

            raise InvalidInputError(
                "All player names in a non-empty list must be non-empty strings."
            )

        _LOGGER.info(
            "Adding players %s to allowlist for server '%s' (ignores limit: %s)",
            players,
            server_name,
            ignores_player_limit,
        )
        payload = {"players": players, "ignoresPlayerLimit": ignores_player_limit}
        encoded_server_name = quote(server_name)
        return await self._request(
            "POST",
            f"/server/{encoded_server_name}/allowlist/add",
            json_data=payload,
            authenticated=True,
        )

    async def async_remove_from_server_allowlist(
        self, server_name: str, players: List[str]
    ) -> Dict[str, Any]:
        """
        Removes one or more players from the server's allowlist.json.
        Response includes details of removed and not_found players.

        Corresponds to `DELETE /api/server/{server_name}/allowlist/remove`.
        Requires authentication.

        Args:
            server_name: The name of the server.
            players: A list of player names to remove.

        Returns:
            API response dictionary. E.g.,
            `{"status": "success", "message": "...", "details": {"removed": [], "not_found": []}}`
        """
        if not isinstance(players, list) or not players:  # Must be a non-empty list
            from ..exceptions import InvalidInputError

            raise InvalidInputError(
                "Players list cannot be empty and must be a list of strings."
            )
        if not all(isinstance(p, str) and p.strip() for p in players):
            from ..exceptions import InvalidInputError

            raise InvalidInputError(
                "All player names in the list must be non-empty strings."
            )

        _LOGGER.info(
            "Removing players %s from allowlist for server '%s'", players, server_name
        )
        payload = {"players": players}
        encoded_server_name = quote(server_name)
        return await self._request(
            "DELETE",
            f"/server/{encoded_server_name}/allowlist/remove",
            json_data=payload,  # API Doc says DELETE with body
            authenticated=True,
        )

    async def async_get_server_player_permissions(
        self, server_name: str
    ) -> List[Dict[str, Union[str, bool]]]:
        """
        Retrieves player permissions from the server's permissions.json file.

        Corresponds to `GET /api/server/{server_name}/permissions/get`.
        Requires authentication.

        Args:
            server_name: The name of the server.

        Returns:
            A list of player permission objects. E.g.,
            `[{"xuid": "...", "name": "...", "permission_level": "..."}]`

        Raises:
            ServerNotFoundError: If the server does not exist.
            APIError: For other API communication or processing errors.
        """
        _LOGGER.debug("Fetching player permissions for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        try:
            response_data = await self._request(
                "GET",
                f"/server/{encoded_server_name}/permissions/get",
                authenticated=True,
            )
            if (
                isinstance(response_data, dict)
                and response_data.get("status") == "success"
                and isinstance(response_data.get("data"), dict)
                and isinstance(response_data["data"].get("permissions"), list)
            ):
                return response_data["data"]["permissions"]

            _LOGGER.error(
                "Received non-success or unexpected structure for server permissions: %s",
                response_data,
            )
            from ..exceptions import APIError as ClientAPIError

            raise ClientAPIError(
                f"Failed to get server permissions, API response: {response_data.get('status') if isinstance(response_data, dict) else 'N/A'}",
                response_data=(
                    response_data
                    if isinstance(response_data, dict)
                    else {"raw": response_data}
                ),
            )
        except APIError as e:  # type: ignore
            _LOGGER.error(
                "API error fetching server permissions for '%s': %s", server_name, e
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error processing server permissions for '%s': %s",
                server_name,
                e,
            )
            from ..exceptions import APIError as ClientAPIError

            raise ClientAPIError(
                f"Unexpected error processing server permissions for '{server_name}': {e}"
            )

    async def async_set_server_player_permissions(
        self, server_name: str, permissions_map: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Updates permission levels for players in the server's permissions.json.

        Corresponds to `PUT /api/server/{server_name}/permissions/set`.
        Requires authentication.

        Args:
            server_name: The name of the server.
            permissions_map: A dictionary mapping player XUIDs (strings) to
                              permission levels ("visitor", "member", "operator").

        Returns:
            API response dictionary.
        """
        if not isinstance(permissions_map, dict):
            from ..exceptions import InvalidInputError

            raise InvalidInputError("permissions_map must be a dictionary.")

        processed_permissions: Dict[str, str] = {}
        for xuid, level in permissions_map.items():
            if not isinstance(xuid, str) or not xuid.strip():
                from ..exceptions import InvalidInputError

                raise InvalidInputError("Player XUIDs must be non-empty strings.")
            if (
                not isinstance(level, str)
                or level.lower() not in ALLOWED_PERMISSION_LEVELS
            ):
                from ..exceptions import InvalidInputError

                raise InvalidInputError(
                    f"Invalid permission level '{level}' for XUID '{xuid}'. "
                    f"Allowed levels are: {', '.join(ALLOWED_PERMISSION_LEVELS)}"
                )
            processed_permissions[xuid] = level.lower()

        _LOGGER.info(
            "Setting player permissions for server '%s': %s",
            server_name,
            processed_permissions,
        )
        payload = {"permissions": processed_permissions}
        encoded_server_name = quote(server_name)
        return await self._request(
            "PUT",
            f"/server/{encoded_server_name}/permissions/set",
            json_data=payload,
            authenticated=True,
        )
