# src/pybedrock_server_manager/client/_manager_methods.py
"""Mixin class containing manager-level API methods."""
import logging
from typing import Any, Dict, Optional, List

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.manager")


class ManagerMethodsMixin:
    """Mixin for manager-level endpoints."""

    async def async_get_info(self) -> Dict[str, Any]:
        """Gets system and application information from the manager. Calls GET /api/info."""
        _LOGGER.debug("Fetching manager system and application information from /info")

        return await self._request(method="GET", path="/info", authenticated=False)

    async def async_scan_players(self) -> Dict[str, Any]:
        """Triggers scanning of player logs. Calls POST /api/players/scan."""
        _LOGGER.info("Triggering player log scan")

        return await self._request("POST", path="/players/scan", authenticated=True)

    async def async_get_players(self) -> Dict[str, Any]:
        """Gets the global list of known players. Calls GET /api/players/get."""
        _LOGGER.debug(
            "Fetching global player list from /players/get"
        )  # Updated log message

        return await self._request("GET", path="/players/get", authenticated=True)

    async def async_add_players(self, players_data: List[str]) -> Dict[str, Any]:
        """Adds players to the global list. Calls POST /api/players/add."""
        _LOGGER.info("Adding/updating global players: %s", players_data)
        payload = {"players": players_data}

        return await self._request(
            "POST",
            path="/players/add",
            data=payload,
            authenticated=True,
        )

    async def async_prune_downloads(
        self, directory: str, keep: Optional[int] = None
    ) -> Dict[str, Any]:
        """Triggers pruning of the global download cache. Calls POST /api/downloads/prune."""
        _LOGGER.info(
            "Triggering download cache prune for dir '%s', keep: %s",
            directory,
            keep if keep is not None else "default",
        )
        payload: Dict[str, Any] = {"directory": directory}
        if keep is not None:
            payload["keep"] = keep

        return await self._request(
            "POST",
            path="/downloads/prune",
            data=payload,
            authenticated=True,
        )

    async def async_install_new_server(
        self, server_name: str, server_version: str, overwrite: bool = False
    ) -> Dict[str, Any]:
        """Requests installation of a new server instance. Calls POST /api/server/install."""
        _LOGGER.info(
            "Requesting install for server '%s', version: %s, overwrite: %s",
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
            "POST",
            path="/server/install",
            data=payload,
            authenticated=True,
        )
