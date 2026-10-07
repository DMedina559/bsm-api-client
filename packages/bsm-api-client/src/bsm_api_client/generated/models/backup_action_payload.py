from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BackupActionPayload")


@_attrs_define
class BackupActionPayload:
    """Request model for triggering a backup action.

    Attributes:
        backup_type (str): Type of backup: 'world', 'config', or 'all'.
        file_to_backup (None | str | Unset): Name of config file if backup_type is 'config' (e.g., 'server.properties').
    """

    backup_type: str
    file_to_backup: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        backup_type = self.backup_type

        file_to_backup: None | str | Unset
        if isinstance(self.file_to_backup, Unset):
            file_to_backup = UNSET
        else:
            file_to_backup = self.file_to_backup

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "backup_type": backup_type,
            }
        )
        if file_to_backup is not UNSET:
            field_dict["file_to_backup"] = file_to_backup

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        backup_type = d.pop("backup_type")

        def _parse_file_to_backup(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        file_to_backup = _parse_file_to_backup(d.pop("file_to_backup", UNSET))

        backup_action_payload = cls(
            backup_type=backup_type,
            file_to_backup=file_to_backup,
        )

        backup_action_payload.additional_properties = d
        return backup_action_payload

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
