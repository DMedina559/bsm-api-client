from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PlayerPermissionPayload")


@_attrs_define
class PlayerPermissionPayload:
    """Represents a single player's permission data sent from the client.

    Attributes:
        name (str):
        permission_level (str):
        xuid (str):
    """

    name: str
    permission_level: str
    xuid: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        permission_level = self.permission_level

        xuid = self.xuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
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

        player_permission_payload = cls(
            name=name,
            permission_level=permission_level,
            xuid=xuid,
        )

        player_permission_payload.additional_properties = d
        return player_permission_payload

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
