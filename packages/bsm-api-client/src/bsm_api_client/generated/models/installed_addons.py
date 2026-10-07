from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.installed_addon import InstalledAddon


T = TypeVar("T", bound="InstalledAddons")


@_attrs_define
class InstalledAddons:
    """
    Attributes:
        behavior_packs (list[InstalledAddon] | Unset):
        resource_packs (list[InstalledAddon] | Unset):
    """

    behavior_packs: list[InstalledAddon] | Unset = UNSET
    resource_packs: list[InstalledAddon] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        behavior_packs: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.behavior_packs, Unset):
            behavior_packs = []
            for behavior_packs_item_data in self.behavior_packs:
                behavior_packs_item = behavior_packs_item_data.to_dict()
                behavior_packs.append(behavior_packs_item)

        resource_packs: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.resource_packs, Unset):
            resource_packs = []
            for resource_packs_item_data in self.resource_packs:
                resource_packs_item = resource_packs_item_data.to_dict()
                resource_packs.append(resource_packs_item)

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if behavior_packs is not UNSET:
            field_dict["behavior_packs"] = behavior_packs
        if resource_packs is not UNSET:
            field_dict["resource_packs"] = resource_packs

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.installed_addon import InstalledAddon  # noqa: PLC0415

        d = dict(src_dict)
        _behavior_packs = d.pop("behavior_packs", UNSET)
        behavior_packs: list[InstalledAddon] | Unset = UNSET
        if _behavior_packs is not UNSET:
            behavior_packs = []
            for behavior_packs_item_data in _behavior_packs:
                behavior_packs_item = InstalledAddon.from_dict(behavior_packs_item_data)

                behavior_packs.append(behavior_packs_item)

        _resource_packs = d.pop("resource_packs", UNSET)
        resource_packs: list[InstalledAddon] | Unset = UNSET
        if _resource_packs is not UNSET:
            resource_packs = []
            for resource_packs_item_data in _resource_packs:
                resource_packs_item = InstalledAddon.from_dict(resource_packs_item_data)

                resource_packs.append(resource_packs_item)

        installed_addons = cls(
            behavior_packs=behavior_packs,
            resource_packs=resource_packs,
        )

        return installed_addons
