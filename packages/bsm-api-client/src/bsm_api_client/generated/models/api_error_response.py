from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..models.api_error_response_code import APIErrorResponseCode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.api_error_response_details import APIErrorResponseDetails


T = TypeVar("T", bound="APIErrorResponse")


@_attrs_define
class APIErrorResponse:
    """Safe transport representation; Python API callers receive exceptions.

    Attributes:
        code (APIErrorResponseCode):
        message (str):
        details (APIErrorResponseDetails | Unset):
    """

    code: APIErrorResponseCode
    message: str
    details: APIErrorResponseDetails | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        code = self.code.value

        message = self.message

        details: dict[str, Any] | Unset = UNSET
        if not isinstance(self.details, Unset):
            details = self.details.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "code": code,
                "message": message,
            }
        )
        if details is not UNSET:
            field_dict["details"] = details

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.api_error_response_details import APIErrorResponseDetails  # noqa: PLC0415

        d = dict(src_dict)
        code = APIErrorResponseCode(d.pop("code"))

        message = d.pop("message")

        _details = d.pop("details", UNSET)
        details: APIErrorResponseDetails | Unset
        if isinstance(_details, Unset):
            details = UNSET
        else:
            details = APIErrorResponseDetails.from_dict(_details)

        api_error_response = cls(
            code=code,
            message=message,
            details=details,
        )

        return api_error_response
