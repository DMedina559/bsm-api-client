from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PluginInfo")


@_attrs_define
class PluginInfo:
    """
    Attributes:
        enabled (bool):
        author (str | Unset):  Default: ''.
        description (str | Unset):  Default: ''.
        status (str | Unset):  Default: 'UNKNOWN'.
        version (str | Unset):  Default: 'N/A'.
    """

    enabled: bool
    author: str | Unset = ""
    description: str | Unset = ""
    status: str | Unset = "UNKNOWN"
    version: str | Unset = "N/A"

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        author = self.author

        description = self.description

        status = self.status

        version = self.version

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "enabled": enabled,
            }
        )
        if author is not UNSET:
            field_dict["author"] = author
        if description is not UNSET:
            field_dict["description"] = description
        if status is not UNSET:
            field_dict["status"] = status
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enabled = d.pop("enabled")

        author = d.pop("author", UNSET)

        description = d.pop("description", UNSET)

        status = d.pop("status", UNSET)

        version = d.pop("version", UNSET)

        plugin_info = cls(
            enabled=enabled,
            author=author,
            description=description,
            status=status,
            version=version,
        )

        return plugin_info
