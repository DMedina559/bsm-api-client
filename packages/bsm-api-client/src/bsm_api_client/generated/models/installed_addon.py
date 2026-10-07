from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.installed_addon_status import InstalledAddonStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.subpack import Subpack


T = TypeVar("T", bound="InstalledAddon")


@_attrs_define
class InstalledAddon:
    """
    Attributes:
        name (str):
        status (InstalledAddonStatus):
        uuid (str):
        version (list[int]):
        active_subpack (None | str | Unset):
        icon (None | str | Unset):
        path (None | str | Unset):
        subpacks (list[Subpack] | Unset):
    """

    name: str
    status: InstalledAddonStatus
    uuid: str
    version: list[int]
    active_subpack: None | str | Unset = UNSET
    icon: None | str | Unset = UNSET
    path: None | str | Unset = UNSET
    subpacks: list[Subpack] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        status = self.status.value

        uuid = self.uuid

        version = self.version

        active_subpack: None | str | Unset
        if isinstance(self.active_subpack, Unset):
            active_subpack = UNSET
        else:
            active_subpack = self.active_subpack

        icon: None | str | Unset
        if isinstance(self.icon, Unset):
            icon = UNSET
        else:
            icon = self.icon

        path: None | str | Unset
        if isinstance(self.path, Unset):
            path = UNSET
        else:
            path = self.path

        subpacks: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.subpacks, Unset):
            subpacks = []
            for subpacks_item_data in self.subpacks:
                subpacks_item = subpacks_item_data.to_dict()
                subpacks.append(subpacks_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "status": status,
                "uuid": uuid,
                "version": version,
            }
        )
        if active_subpack is not UNSET:
            field_dict["active_subpack"] = active_subpack
        if icon is not UNSET:
            field_dict["icon"] = icon
        if path is not UNSET:
            field_dict["path"] = path
        if subpacks is not UNSET:
            field_dict["subpacks"] = subpacks

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.subpack import Subpack  # noqa: PLC0415

        d = dict(src_dict)
        name = d.pop("name")

        status = InstalledAddonStatus(d.pop("status"))

        uuid = d.pop("uuid")

        version = cast(list[int], d.pop("version"))

        def _parse_active_subpack(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        active_subpack = _parse_active_subpack(d.pop("active_subpack", UNSET))

        def _parse_icon(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        icon = _parse_icon(d.pop("icon", UNSET))

        def _parse_path(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        path = _parse_path(d.pop("path", UNSET))

        _subpacks = d.pop("subpacks", UNSET)
        subpacks: list[Subpack] | Unset = UNSET
        if _subpacks is not UNSET:
            subpacks = []
            for subpacks_item_data in _subpacks:
                subpacks_item = Subpack.from_dict(subpacks_item_data)

                subpacks.append(subpacks_item)

        installed_addon = cls(
            name=name,
            status=status,
            uuid=uuid,
            version=version,
            active_subpack=active_subpack,
            icon=icon,
            path=path,
            subpacks=subpacks,
        )

        return installed_addon
