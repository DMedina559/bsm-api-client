import logging
from typing import cast

from ..models import (
    AddPlayersManuallyResponse,
    AddPlayersPayload,
    GetAllKnownPlayersResponse,
    ScanAndUpdatePlayerDbResponse,
)
from ..validation import parse_response
from .base import Service

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.manager")


class PlayersService(Service):

    async def async_scan_players(self) -> ScanAndUpdatePlayerDbResponse:
        """Triggers a scan of player logs across all servers.

        :returns: `ScanAndUpdatePlayerDbResponse`.
        """
        _LOGGER.info("Triggering player log scan")
        response = await self.async_call_generated(
            "scan_players", authenticated=True, typed=True
        )
        return cast(
            ScanAndUpdatePlayerDbResponse,
            parse_response(ScanAndUpdatePlayerDbResponse, response),
        )

    async def async_get_players(self) -> GetAllKnownPlayersResponse:
        """Gets the global list of known players.

        :returns: `GetAllKnownPlayersResponse`.
        """
        _LOGGER.debug("Fetching global player list from /players/get")
        response = await self.async_call_generated(
            "list_players", authenticated=True, typed=True
        )
        return cast(
            GetAllKnownPlayersResponse,
            parse_response(GetAllKnownPlayersResponse, response),
        )

    async def async_add_players(
        self, payload: AddPlayersPayload
    ) -> AddPlayersManuallyResponse:
        """Adds or updates players in the global list.

        :param payload: The AddPlayersPayload request model.

        :returns: `AddPlayersManuallyResponse`.
        """
        _LOGGER.info("Adding/updating global players: %s", payload.players)
        response = await self.async_call_generated(
            "add_players", body=payload.model_dump(), authenticated=True, typed=True
        )
        return cast(
            AddPlayersManuallyResponse,
            parse_response(AddPlayersManuallyResponse, response),
        )
