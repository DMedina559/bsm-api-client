from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.player_permission_payload import PlayerPermissionPayload


T = TypeVar("T", bound="PermissionsSetPayload")


@_attrs_define
class PermissionsSetPayload:
    """Request model for setting multiple player permissions.

    Attributes:
        permissions (list[PlayerPermissionPayload]): List of player permission entries.
    """

    permissions: list[PlayerPermissionPayload]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        permissions = []
        for permissions_item_data in self.permissions:
            permissions_item = permissions_item_data.to_dict()
            permissions.append(permissions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "permissions": permissions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.player_permission_payload import PlayerPermissionPayload  # noqa: PLC0415

        d = dict(src_dict)
        permissions = []
        _permissions = d.pop("permissions")
        for permissions_item_data in _permissions:
            permissions_item = PlayerPermissionPayload.from_dict(permissions_item_data)

            permissions.append(permissions_item)

        permissions_set_payload = cls(
            permissions=permissions,
        )

        permissions_set_payload.additional_properties = d
        return permissions_set_payload

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
