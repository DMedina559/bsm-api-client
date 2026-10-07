from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AddonActionPayload")


@_attrs_define
class AddonActionPayload:
    """Request model for modifying a specific addon (e.g. enable, disable, uninstall).

    Attributes:
        pack_type (str): The type of the pack: 'behavior' or 'resource'.
        pack_uuid (str): The UUID of the pack.
    """

    pack_type: str
    pack_uuid: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pack_type = self.pack_type

        pack_uuid = self.pack_uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pack_type": pack_type,
                "pack_uuid": pack_uuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pack_type = d.pop("pack_type")

        pack_uuid = d.pop("pack_uuid")

        addon_action_payload = cls(
            pack_type=pack_type,
            pack_uuid=pack_uuid,
        )

        addon_action_payload.additional_properties = d
        return addon_action_payload

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
