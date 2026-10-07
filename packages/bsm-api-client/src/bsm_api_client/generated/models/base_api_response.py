from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.base_api_response_status import BaseApiResponseStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="BaseApiResponse")


@_attrs_define
class BaseApiResponse:
    """
    Attributes:
        status (BaseApiResponseStatus):
        message (None | str | Unset):
    """

    status: BaseApiResponseStatus
    message: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

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
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = BaseApiResponseStatus(d.pop("status"))

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        base_api_response = cls(
            status=status,
            message=message,
        )

        return base_api_response
