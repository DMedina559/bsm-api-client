from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.api_error_response import APIErrorResponse


T = TypeVar("T", bound="ErrorEnvelope")


@_attrs_define
class ErrorEnvelope:
    """
    Attributes:
        error (APIErrorResponse): Safe transport representation; Python API callers receive exceptions.
    """

    error: APIErrorResponse

    def to_dict(self) -> dict[str, Any]:
        error = self.error.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "error": error,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.api_error_response import APIErrorResponse  # noqa: PLC0415

        d = dict(src_dict)
        error = APIErrorResponse.from_dict(d.pop("error"))

        error_envelope = cls(
            error=error,
        )

        return error_envelope
