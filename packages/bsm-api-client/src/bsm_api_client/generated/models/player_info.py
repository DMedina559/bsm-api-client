from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="PlayerInfo")


@_attrs_define
class PlayerInfo:
    """
    Attributes:
        name (str):
        xuid (str):
    """

    name: str
    xuid: str

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        xuid = self.xuid

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "xuid": xuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        xuid = d.pop("xuid")

        player_info = cls(
            name=name,
            xuid=xuid,
        )

        return player_info
