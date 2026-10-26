from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field
import json
from .. import types

from ..types import UNSET, Unset

from ..types import File, FileTypes
from ..types import UNSET, Unset
from io import BytesIO
from typing import cast






T = TypeVar("T", bound="BodyImportServerSnapshot")



@_attrs_define
class BodyImportServerSnapshot:
    """:ivar file: Value supplied to the operation.
    :ivar recovery_key: Value supplied to the operation."""

    file: File
    recovery_key: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        file = self.file.to_tuple()


        recovery_key: None | str | Unset
        if isinstance(self.recovery_key, Unset):
            recovery_key = UNSET
        else:
            recovery_key = self.recovery_key


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "file": file,
        })
        if recovery_key is not UNSET:
            field_dict["recovery_key"] = recovery_key

        return field_dict


    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("file", self.file.to_tuple()))



        if not isinstance(self.recovery_key, Unset):
            if isinstance(self.recovery_key, str):

                files.append(("recovery_key", (None, str(self.recovery_key).encode(), "text/plain")))
            else:
                files.append(("recovery_key", (None, str(self.recovery_key).encode(), "text/plain")))



        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))



        return files


    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file = File(
             payload = BytesIO(d.pop("file"))
        )




        def _parse_recovery_key(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        recovery_key = _parse_recovery_key(d.pop("recovery_key", UNSET))


        body_import_server_snapshot = cls(
            file=file,
            recovery_key=recovery_key,
        )


        body_import_server_snapshot.additional_properties = d
        return body_import_server_snapshot

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
