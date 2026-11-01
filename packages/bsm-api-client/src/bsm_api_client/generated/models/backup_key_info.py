from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="BackupKeyInfo")



@_attrs_define
class BackupKeyInfo:
    """:ivar created_at: Value supplied to the operation.
    :ivar key_id: Value supplied to the operation."""

    created_at: str
    key_id: str





    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        key_id = self.key_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "created_at": created_at,
            "key_id": key_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = d.pop("created_at")

        key_id = d.pop("key_id")

        backup_key_info = cls(
            created_at=created_at,
            key_id=key_id,
        )

        return backup_key_info

