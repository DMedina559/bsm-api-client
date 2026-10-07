from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.app_info_response_status import AppInfoResponseStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.app_info_response_info_type_0 import AppInfoResponseInfoType0


T = TypeVar("T", bound="AppInfoResponse")


@_attrs_define
class AppInfoResponse:
    """Response model for app/system info.

    Attributes:
        status (AppInfoResponseStatus):
        info (AppInfoResponseInfoType0 | None | Unset):
        message (None | str | Unset):
    """

    status: AppInfoResponseStatus
    info: AppInfoResponseInfoType0 | None | Unset = UNSET
    message: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.app_info_response_info_type_0 import AppInfoResponseInfoType0  # noqa: PLC0415

        status = self.status.value

        info: dict[str, Any] | None | Unset
        if isinstance(self.info, Unset):
            info = UNSET
        elif isinstance(self.info, AppInfoResponseInfoType0):
            info = self.info.to_dict()
        else:
            info = self.info

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
        if info is not UNSET:
            field_dict["info"] = info
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.app_info_response_info_type_0 import AppInfoResponseInfoType0  # noqa: PLC0415

        d = dict(src_dict)
        status = AppInfoResponseStatus(d.pop("status"))

        def _parse_info(data: object) -> AppInfoResponseInfoType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                info_type_0 = AppInfoResponseInfoType0.from_dict(data)

                return info_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AppInfoResponseInfoType0 | None | Unset, data)

        info = _parse_info(d.pop("info", UNSET))

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        app_info_response = cls(
            status=status,
            info=info,
            message=message,
        )

        return app_info_response
