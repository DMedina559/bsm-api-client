from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.player_list_response_status import PlayerListResponseStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.player_info import PlayerInfo


T = TypeVar("T", bound="PlayerListResponse")


@_attrs_define
class PlayerListResponse:
    """Response model for player lists.

    Attributes:
        status (PlayerListResponseStatus):
        message (None | str | Unset):
        players (list[PlayerInfo] | None | Unset):
    """

    status: PlayerListResponseStatus
    message: None | str | Unset = UNSET
    players: list[PlayerInfo] | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        players: list[dict[str, Any]] | None | Unset
        if isinstance(self.players, Unset):
            players = UNSET
        elif isinstance(self.players, list):
            players = []
            for players_type_0_item_data in self.players:
                players_type_0_item = players_type_0_item_data.to_dict()
                players.append(players_type_0_item)

        else:
            players = self.players

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "status": status,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message
        if players is not UNSET:
            field_dict["players"] = players

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.player_info import PlayerInfo  # noqa: PLC0415

        d = dict(src_dict)
        status = PlayerListResponseStatus(d.pop("status"))

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        def _parse_players(data: object) -> list[PlayerInfo] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                players_type_0 = []
                _players_type_0 = data
                for players_type_0_item_data in _players_type_0:
                    players_type_0_item = PlayerInfo.from_dict(players_type_0_item_data)

                    players_type_0.append(players_type_0_item)

                return players_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[PlayerInfo] | None | Unset, data)

        players = _parse_players(d.pop("players", UNSET))

        player_list_response = cls(
            status=status,
            message=message,
            players=players,
        )

        return player_list_response
