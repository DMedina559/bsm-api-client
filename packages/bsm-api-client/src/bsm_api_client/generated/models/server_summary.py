from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.player_info import PlayerInfo


T = TypeVar("T", bound="ServerSummary")


@_attrs_define
class ServerSummary:
    """
    Attributes:
        name (str):
        status (str):
        version (str):
        player_count (int | Unset):  Default: 0.
        players (list[PlayerInfo] | Unset):
    """

    name: str
    status: str
    version: str
    player_count: int | Unset = 0
    players: list[PlayerInfo] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        status = self.status

        version = self.version

        player_count = self.player_count

        players: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.players, Unset):
            players = []
            for players_item_data in self.players:
                players_item = players_item_data.to_dict()
                players.append(players_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "status": status,
                "version": version,
            }
        )
        if player_count is not UNSET:
            field_dict["player_count"] = player_count
        if players is not UNSET:
            field_dict["players"] = players

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.player_info import PlayerInfo  # noqa: PLC0415

        d = dict(src_dict)
        name = d.pop("name")

        status = d.pop("status")

        version = d.pop("version")

        player_count = d.pop("player_count", UNSET)

        _players = d.pop("players", UNSET)
        players: list[PlayerInfo] | Unset = UNSET
        if _players is not UNSET:
            players = []
            for players_item_data in _players:
                players_item = PlayerInfo.from_dict(players_item_data)

                players.append(players_item)

        server_summary = cls(
            name=name,
            status=status,
            version=version,
            player_count=player_count,
            players=players,
        )

        return server_summary
