from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="InstallServerPayload")


@_attrs_define
class InstallServerPayload:
    """Request model for installing a new server.

    Attributes:
        server_name (str): Name for the new server.
        overwrite (bool | None | Unset): If True, confirm overwriting an existing installation. Default: False.
        server_version (str | Unset): Version to install (e.g., 'LATEST', '1.20.10.01', 'CUSTOM'). Default: 'LATEST'.
        server_zip_path (None | str | Unset): Path to a custom ZIP file, if 'CUSTOM' version is selected.
    """

    server_name: str
    overwrite: bool | None | Unset = False
    server_version: str | Unset = "LATEST"
    server_zip_path: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        server_name = self.server_name

        overwrite: bool | None | Unset
        if isinstance(self.overwrite, Unset):
            overwrite = UNSET
        else:
            overwrite = self.overwrite

        server_version = self.server_version

        server_zip_path: None | str | Unset
        if isinstance(self.server_zip_path, Unset):
            server_zip_path = UNSET
        else:
            server_zip_path = self.server_zip_path

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "server_name": server_name,
            }
        )
        if overwrite is not UNSET:
            field_dict["overwrite"] = overwrite
        if server_version is not UNSET:
            field_dict["server_version"] = server_version
        if server_zip_path is not UNSET:
            field_dict["server_zip_path"] = server_zip_path

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        server_name = d.pop("server_name")

        def _parse_overwrite(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        overwrite = _parse_overwrite(d.pop("overwrite", UNSET))

        server_version = d.pop("server_version", UNSET)

        def _parse_server_zip_path(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        server_zip_path = _parse_server_zip_path(d.pop("server_zip_path", UNSET))

        install_server_payload = cls(
            server_name=server_name,
            overwrite=overwrite,
            server_version=server_version,
            server_zip_path=server_zip_path,
        )

        install_server_payload.additional_properties = d
        return install_server_payload

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
