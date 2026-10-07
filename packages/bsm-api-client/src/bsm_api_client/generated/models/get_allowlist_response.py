from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.allowlist_player import AllowlistPlayer


T = TypeVar("T", bound="GetAllowlistResponse")


@_attrs_define
class GetAllowlistResponse:
    """
    Attributes:
        players (list[AllowlistPlayer]):
        message (None | str | Unset):
        status (Literal['success'] | Unset):  Default: 'success'.
    """

    players: list[AllowlistPlayer]
    message: None | str | Unset = UNSET
    status: Literal["success"] | Unset = "success"

    def to_dict(self) -> dict[str, Any]:
        players = []
        for players_item_data in self.players:
            players_item = players_item_data.to_dict()
            players.append(players_item)

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        status = self.status

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "players": players,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.allowlist_player import AllowlistPlayer  # noqa: PLC0415

        d = dict(src_dict)
        players = []
        _players = d.pop("players")
        for players_item_data in _players:
            players_item = AllowlistPlayer.from_dict(players_item_data)

            players.append(players_item)

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        status = cast(Literal["success"] | Unset, d.pop("status", UNSET))
        if status != "success" and not isinstance(status, Unset):
            raise ValueError(f"status must match const 'success', got '{status}'")

        get_allowlist_response = cls(
            players=players,
            message=message,
            status=status,
        )

        return get_allowlist_response
