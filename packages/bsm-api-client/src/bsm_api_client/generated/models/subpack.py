from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="Subpack")


@_attrs_define
class Subpack:
    """
    Attributes:
        folder_name (str):
        memory_tier (int | None | Unset):
        name (None | str | Unset):
    """

    folder_name: str
    memory_tier: int | None | Unset = UNSET
    name: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        folder_name = self.folder_name

        memory_tier: int | None | Unset
        if isinstance(self.memory_tier, Unset):
            memory_tier = UNSET
        else:
            memory_tier = self.memory_tier

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "folder_name": folder_name,
            }
        )
        if memory_tier is not UNSET:
            field_dict["memory_tier"] = memory_tier
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        folder_name = d.pop("folder_name")

        def _parse_memory_tier(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        memory_tier = _parse_memory_tier(d.pop("memory_tier", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        subpack = cls(
            folder_name=folder_name,
            memory_tier=memory_tier,
            name=name,
        )

        return subpack
