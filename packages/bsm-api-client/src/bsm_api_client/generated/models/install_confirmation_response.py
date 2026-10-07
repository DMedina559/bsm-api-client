from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="InstallConfirmationResponse")


@_attrs_define
class InstallConfirmationResponse:
    """
    Attributes:
        message (str):
        server_name (str):
        status (Literal['confirm_needed'] | Unset):  Default: 'confirm_needed'.
    """

    message: str
    server_name: str
    status: Literal["confirm_needed"] | Unset = "confirm_needed"

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        server_name = self.server_name

        status = self.status

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "message": message,
                "server_name": server_name,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message = d.pop("message")

        server_name = d.pop("server_name")

        status = cast(Literal["confirm_needed"] | Unset, d.pop("status", UNSET))
        if status != "confirm_needed" and not isinstance(status, Unset):
            raise ValueError(f"status must match const 'confirm_needed', got '{status}'")

        install_confirmation_response = cls(
            message=message,
            server_name=server_name,
            status=status,
        )

        return install_confirmation_response
