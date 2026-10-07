from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.addon_list_response_status import AddonListResponseStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.installed_addons import InstalledAddons


T = TypeVar("T", bound="AddonListResponse")


@_attrs_define
class AddonListResponse:
    """Response model for retrieving all addons on a server.

    Attributes:
        status (AddonListResponseStatus):
        addons (InstalledAddons | None | Unset):
        message (None | str | Unset):
    """

    status: AddonListResponseStatus
    addons: InstalledAddons | None | Unset = UNSET
    message: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.installed_addons import InstalledAddons  # noqa: PLC0415

        status = self.status.value

        addons: dict[str, Any] | None | Unset
        if isinstance(self.addons, Unset):
            addons = UNSET
        elif isinstance(self.addons, InstalledAddons):
            addons = self.addons.to_dict()
        else:
            addons = self.addons

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "status": status,
            }
        )
        if addons is not UNSET:
            field_dict["addons"] = addons
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.installed_addons import InstalledAddons  # noqa: PLC0415

        d = dict(src_dict)
        status = AddonListResponseStatus(d.pop("status"))

        def _parse_addons(data: object) -> InstalledAddons | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                addons_type_0 = InstalledAddons.from_dict(data)

                return addons_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(InstalledAddons | None | Unset, data)

        addons = _parse_addons(d.pop("addons", UNSET))

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        addon_list_response = cls(
            status=status,
            addons=addons,
            message=message,
        )

        return addon_list_response
