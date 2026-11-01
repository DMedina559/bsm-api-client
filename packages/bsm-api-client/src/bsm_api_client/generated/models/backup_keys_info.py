from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.backup_key_info import BackupKeyInfo





T = TypeVar("T", bound="BackupKeysInfo")



@_attrs_define
class BackupKeysInfo:
    """:ivar active: Value supplied to the operation.
    :ivar keys: Value supplied to the operation."""

    active: None | str
    keys: list[BackupKeyInfo]





    def to_dict(self) -> dict[str, Any]:
        from ..models.backup_key_info import BackupKeyInfo # noqa: PLC0415
        active: None | str
        active = self.active

        keys = []
        for keys_item_data in self.keys:
            keys_item = keys_item_data.to_dict()
            keys.append(keys_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "active": active,
            "keys": keys,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.backup_key_info import BackupKeyInfo # noqa: PLC0415
        d = dict(src_dict)
        def _parse_active(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        active = _parse_active(d.pop("active"))


        keys = []
        _keys = d.pop("keys")
        for keys_item_data in (_keys):
            keys_item = BackupKeyInfo.from_dict(keys_item_data)



            keys.append(keys_item)


        backup_keys_info = cls(
            active=active,
            keys=keys,
        )

        return backup_keys_info

