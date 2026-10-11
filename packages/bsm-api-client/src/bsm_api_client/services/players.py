import logging
from typing import cast

from ..models import AddPlayersPayload, AddPlayersResponse, PlayerListResponse
from ..validation import parse_response
from .base import Service

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.manager")


class PlayersService(Service):

    async def async_scan_players(self) -> AddPlayersResponse:
        """Triggers a scan of player logs across all servers.

        Returns:
            An `AddPlayersResponse` object containing the result of the scan operation.
        """
        _LOGGER.info("Triggering player log scan")
        response = await self.async_call_generated("scan_players", authenticated=True)
        return cast(AddPlayersResponse, parse_response(AddPlayersResponse, response))

    async def async_get_players(self) -> PlayerListResponse:
        """Gets the global list of known players.

        Returns:
            A `PlayerListResponse` object containing the list of players.
        """
        _LOGGER.debug("Fetching global player list from /players/get")
        response = await self.async_call_generated("list_players", authenticated=True)
        return cast(PlayerListResponse, parse_response(PlayerListResponse, response))

    async def async_add_players(self, payload: AddPlayersPayload) -> AddPlayersResponse:
        """Adds or updates players in the global list.

        Args:
            payload: An `AddPlayersPayload` object containing the players to add.

        Returns:
            An `AddPlayersResponse` object containing the result of the add operation.
        """
        _LOGGER.info("Adding/updating global players: %s", payload.players)
        response = await self.async_call_generated(
            "add_players", body=payload.model_dump(), authenticated=True
        )
        return cast(AddPlayersResponse, parse_response(AddPlayersResponse, response))
