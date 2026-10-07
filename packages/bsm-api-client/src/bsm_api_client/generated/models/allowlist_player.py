from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="AllowlistPlayer")


@_attrs_define
class AllowlistPlayer:
    """
    Attributes:
        name (str):
        ignores_player_limit (bool | Unset):  Default: False.
        xuid (None | str | Unset):
    """

    name: str
    ignores_player_limit: bool | Unset = False
    xuid: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        ignores_player_limit = self.ignores_player_limit

        xuid: None | str | Unset
        if isinstance(self.xuid, Unset):
            xuid = UNSET
        else:
            xuid = self.xuid

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
            }
        )
        if ignores_player_limit is not UNSET:
            field_dict["ignoresPlayerLimit"] = ignores_player_limit
        if xuid is not UNSET:
            field_dict["xuid"] = xuid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        ignores_player_limit = d.pop("ignoresPlayerLimit", UNSET)

        def _parse_xuid(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        xuid = _parse_xuid(d.pop("xuid", UNSET))

        allowlist_player = cls(
            name=name,
            ignores_player_limit=ignores_player_limit,
            xuid=xuid,
        )

        return allowlist_player
