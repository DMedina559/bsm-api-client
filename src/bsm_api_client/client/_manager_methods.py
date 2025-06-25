# src/bsm_api_client/client/_manager_methods.py
"""Mixin class containing manager-level API methods."""
import logging
from typing import Any, Dict, Optional, List, TYPE_CHECKING
from urllib.parse import quote  # Added quote

if TYPE_CHECKING:
    from ..client_base import ClientBase

    # Ensure APIError and InvalidInputError are available for type hints if used
    from ..exceptions import APIError, InvalidInputError


_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.manager")


class ManagerMethodsMixin:
    """Mixin for manager-level endpoints."""

    _request: callable
    if TYPE_CHECKING:
        # Copied from _server_info_methods for consistency for panorama method
        _session: Any
        _base_url: str
        # _default_headers: Dict[str, str] # Not strictly needed if _request handles it
        # _jwt_token: Optional[str] # Not needed if auth is false
        # _auth_lock: Any # Not needed
        _request_timeout: int

        async def _handle_api_error(
            self, response: Any, request_path_for_log: str
        ) -> None: ...

        async def _request(
            self: "ClientBase",
            method: str,
            path: str,
            json_data: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None,
            authenticated: bool = True,
            is_retry: bool = False,
        ) -> Any: ...

    async def async_get_info(self) -> Dict[str, Any]:
        """
        Gets system and application information from the manager.
        The actual data is under the "data" key in the response.
        E.g. {"os_type": "Linux", "app_version": "3.2.1"}

        Corresponds to `GET /api/info`.
        Requires no authentication.

        Returns:
            The dictionary under the "data" key of the API response.

        Raises:
            APIError: If the response format is unexpected or for API errors.
        """
        _LOGGER.debug("Fetching manager system and application information from /info")
        try:
            response_data = await self._request(
                method="GET", path="/info", authenticated=False
            )
            if (
                isinstance(response_data, dict)
                and response_data.get("status") == "success"
            ):
                app_data = response_data.get("data")
                if isinstance(app_data, dict):
                    return app_data

            _LOGGER.error(
                "Received non-success or unexpected structure for info: %s",
                response_data,
            )
            from ..exceptions import APIError as ClientAPIError

            raise ClientAPIError(
                f"Failed to get app info, API response: {response_data.get('status') if isinstance(response_data, dict) else 'N/A'}",
                response_data=(
                    response_data
                    if isinstance(response_data, dict)
                    else {"raw": response_data}
                ),
            )
        except APIError as e:  # type: ignore
            _LOGGER.error("API error fetching app info: %s", e)
            raise
        except Exception as e:
            _LOGGER.exception("Unexpected error processing app info response: %s", e)
            from ..exceptions import APIError as ClientAPIError

            raise ClientAPIError(f"Unexpected error processing app info: {e}")

    async def async_scan_players(self) -> Dict[str, Any]:
        """
        Triggers scanning of player logs across all servers.
        Response includes `{"players_found": true/false, "message": "..."}`.

        Corresponds to `POST /api/players/scan`.
        Requires authentication.
        Returns: API response dictionary.
        """
        _LOGGER.info("Triggering player log scan")
        return await self._request(
            method="POST", path="/players/scan", authenticated=True
        )

    async def async_get_players(self) -> List[Dict[str, Any]]:
        """
        Gets the global list of known players (name and XUID).

        Corresponds to `GET /api/players/get`.
        Requires authentication.

        Returns:
            A list of player dictionaries. Each dictionary contains player info like 'name', 'xuid'.
            Returns an empty list if the player file is not found or is empty.

        Raises:
            APIError: For other API communication or processing errors.
        """
        _LOGGER.debug("Fetching global player list from /players/get")
        try:
            response_data = await self._request(
                method="GET", path="/players/get", authenticated=True
            )
            if (
                isinstance(response_data, dict)
                and response_data.get("status") == "success"
                and isinstance(response_data.get("players"), list)
            ):
                return response_data["players"]

            if (
                isinstance(response_data, dict)
                and response_data.get("status") == "success"
            ):
                if response_data.get("players") == []:
                    if response_data.get("message"):
                        _LOGGER.info(
                            "Global player list is empty or not found: %s",
                            response_data["message"],
                        )
                    return []

            _LOGGER.error(
                "Received non-success or unexpected structure for global player list: %s",
                response_data,
            )
            from ..exceptions import APIError as ClientAPIError

            raise ClientAPIError(
                f"Failed to get global player list, API response: {response_data.get('status') if isinstance(response_data, dict) else 'N/A'}",
                response_data=(
                    response_data
                    if isinstance(response_data, dict)
                    else {"raw": response_data}
                ),
            )
        except APIError as e:  # type: ignore
            _LOGGER.error("API error fetching global player list: %s", e)
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error processing global player list response: %s", e
            )
            from ..exceptions import APIError as ClientAPIError

            raise ClientAPIError(f"Unexpected error processing global player list: {e}")

    async def async_add_players(self, players_data: List[str]) -> Dict[str, Any]:
        """
        Adds or updates players in the global list.
        Each string in `players_data` should be in "PlayerName:PlayerXUID" format.

        Corresponds to `POST /api/players/add`.
        Requires authentication.

        Args:
            players_data: A list of player strings to add or update.
                          Example: ["Steve:2535460987654321", "Alex:2535461234567890"]
        Returns: API response dictionary.
        """
        if not isinstance(players_data, list):
            from ..exceptions import InvalidInputError

            raise InvalidInputError("players_data must be a list of strings.")
        # Further validation on format "Name:XUID" could be added here if desired,
        # but API will also validate.

        _LOGGER.info("Adding/updating global players: %s", players_data)
        payload = {"players": players_data}
        return await self._request(
            method="POST",
            path="/players/add",
            json_data=payload,
            authenticated=True,
        )

    async def async_prune_downloads(
        self, directory: str, keep: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Triggers pruning of downloaded server archives in a specified directory.

        Corresponds to `POST /api/downloads/prune`.
        Requires authentication.

        Args:
            directory: The absolute path to the directory to prune.
            keep: The number of newest files to retain. If None, uses server default.
        """
        _LOGGER.info(
            "Triggering download cache prune for directory '%s', keep: %s",
            directory,
            keep if keep is not None else "server default",
        )
        payload: Dict[str, Any] = {"directory": directory}
        if keep is not None:
            payload["keep"] = keep

        return await self._request(
            method="POST",
            path="/downloads/prune",
            json_data=payload,
            authenticated=True,
        )

    async def async_install_new_server(
        self, server_name: str, server_version: str, overwrite: bool = False
    ) -> Dict[str, Any]:
        """
        Requests installation of a new Bedrock server instance.
        The response may indicate success or that confirmation is needed if overwrite is false
        and the server already exists.

        Corresponds to `POST /api/server/install`.
        Requires authentication.

        Args:
            server_name: The desired unique name for the new server.
            server_version: The version to install (e.g., "LATEST", "PREVIEW", "1.20.81.01").
            overwrite: If True, will delete existing server data if a server with the
                       same name already exists. Defaults to False.
        """
        _LOGGER.info(
            "Requesting installation for server '%s', version: '%s', overwrite: %s",
            server_name,
            server_version,
            overwrite,
        )
        payload = {
            "server_name": server_name,
            "server_version": server_version,
            "overwrite": overwrite,
        }

        return await self._request(
            method="POST",
            path="/server/install",
            json_data=payload,
            authenticated=True,
        )
