# src/pybedrock_server_manager/client/_manager_methods.py
"""Mixin class containing manager-level API methods."""
import logging
from typing import Any, Dict, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client_base import ClientBase

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.manager")


class ManagerMethodsMixin:
    """Mixin for manager-level endpoints."""

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

    async def async_get_info(self) -> Dict[str, Any]:
        """
        Gets system and application information from the manager.

        Corresponds to `GET /api/info`.
        Requires no authentication.
        """
        _LOGGER.debug("Fetching manager system and application information from /info")
        return await self._request(method="GET", path="/info", authenticated=False)

    async def async_scan_players(self) -> Dict[str, Any]:
        """
        Triggers scanning of player logs across all servers.

        Corresponds to `POST /api/players/scan`.
        Requires authentication.
        """
        _LOGGER.info("Triggering player log scan")
        return await self._request(
            method="POST", path="/players/scan", authenticated=True
        )

    async def async_get_players(self) -> Dict[str, Any]:
        """
        Gets the global list of known players (name and XUID).

        Corresponds to `GET /api/players/get`.
        Requires authentication.
        """
        _LOGGER.debug("Fetching global player list from /players/get")
        return await self._request(
            method="GET", path="/players/get", authenticated=True
        )

    async def async_add_players(self, players_data: List[str]) -> Dict[str, Any]:
        """
        Adds or updates players in the global list.
        Each string in `players_data` should be in "PlayerName:PlayerXUID" format.

        Corresponds to `POST /api/players/add`.
        Requires authentication.

        Args:
            players_data: A list of player strings to add or update.
                          Example: ["Steve:2535460987654321", "Alex:2535461234567890"]
        """
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
