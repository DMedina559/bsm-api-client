from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PruneDownloadsPayload")


@_attrs_define
class PruneDownloadsPayload:
    """Request model for pruning the download cache.

    Attributes:
        directory (str): The subdirectory within the main download cache to prune (e.g., 'stable' or 'preview').
        keep (int | None | Unset): Number of most recent files to keep. Defaults to config if omitted.
    """

    directory: str
    keep: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        directory = self.directory

        keep: int | None | Unset
        if isinstance(self.keep, Unset):
            keep = UNSET
        else:
            keep = self.keep

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "directory": directory,
            }
        )
        if keep is not UNSET:
            field_dict["keep"] = keep

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        directory = d.pop("directory")

        def _parse_keep(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        keep = _parse_keep(d.pop("keep", UNSET))

        prune_downloads_payload = cls(
            directory=directory,
            keep=keep,
        )

        prune_downloads_payload.additional_properties = d
        return prune_downloads_payload

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
