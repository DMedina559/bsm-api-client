from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="BanInfo")


@_attrs_define
class BanInfo:
    """
    Attributes:
        player_name (str):
        xuid (str):
        banned_at (None | str | Unset):
        reason (None | str | Unset):
    """

    player_name: str
    xuid: str
    banned_at: None | str | Unset = UNSET
    reason: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        player_name = self.player_name

        xuid = self.xuid

        banned_at: None | str | Unset
        if isinstance(self.banned_at, Unset):
            banned_at = UNSET
        else:
            banned_at = self.banned_at

        reason: None | str | Unset
        if isinstance(self.reason, Unset):
            reason = UNSET
        else:
            reason = self.reason

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "player_name": player_name,
                "xuid": xuid,
            }
        )
        if banned_at is not UNSET:
            field_dict["banned_at"] = banned_at
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        player_name = d.pop("player_name")

        xuid = d.pop("xuid")

        def _parse_banned_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        banned_at = _parse_banned_at(d.pop("banned_at", UNSET))

        def _parse_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reason = _parse_reason(d.pop("reason", UNSET))

        ban_info = cls(
            player_name=player_name,
            xuid=xuid,
            banned_at=banned_at,
            reason=reason,
        )

        return ban_info
