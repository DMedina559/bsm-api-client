from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RestoreActionPayload")


@_attrs_define
class RestoreActionPayload:
    """Request model for triggering a restore action.

    Attributes:
        restore_type (str): Type of restore: 'world', 'properties', 'allowlist', 'permissions', or 'all'.
        backup_file (None | str | Unset): Name of the backup file (basename) to restore from (required if not 'all').
    """

    restore_type: str
    backup_file: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        restore_type = self.restore_type

        backup_file: None | str | Unset
        if isinstance(self.backup_file, Unset):
            backup_file = UNSET
        else:
            backup_file = self.backup_file

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "restore_type": restore_type,
            }
        )
        if backup_file is not UNSET:
            field_dict["backup_file"] = backup_file

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        restore_type = d.pop("restore_type")

        def _parse_backup_file(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        backup_file = _parse_backup_file(d.pop("backup_file", UNSET))

        restore_action_payload = cls(
            restore_type=restore_type,
            backup_file=backup_file,
        )

        restore_action_payload.additional_properties = d
        return restore_action_payload

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
