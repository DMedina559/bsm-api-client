from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.custom_zips_response_status import CustomZipsResponseStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomZipsResponse")


@_attrs_define
class CustomZipsResponse:
    """Response model for custom zips list.

    Attributes:
        custom_zips (list[str]):
        status (CustomZipsResponseStatus):
        message (None | str | Unset):
    """

    custom_zips: list[str]
    status: CustomZipsResponseStatus
    message: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        custom_zips = self.custom_zips

        status = self.status.value

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "custom_zips": custom_zips,
                "status": status,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        custom_zips = cast(list[str], d.pop("custom_zips"))

        status = CustomZipsResponseStatus(d.pop("status"))

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        custom_zips_response = cls(
            custom_zips=custom_zips,
            status=status,
            message=message,
        )

        return custom_zips_response
