from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="PlayerPermission")


@_attrs_define
class PlayerPermission:
    """
    Attributes:
        name (str):
        permission_level (str):
        xuid (str):
    """

    name: str
    permission_level: str
    xuid: str

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        permission_level = self.permission_level

        xuid = self.xuid

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "permission_level": permission_level,
                "xuid": xuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        permission_level = d.pop("permission_level")

        xuid = d.pop("xuid")

        player_permission = cls(
            name=name,
            permission_level=permission_level,
            xuid=xuid,
        )

        return player_permission
