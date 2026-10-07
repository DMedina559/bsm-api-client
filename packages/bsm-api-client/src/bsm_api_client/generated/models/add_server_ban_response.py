from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.add_server_ban_response_status import AddServerBanResponseStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="AddServerBanResponse")


@_attrs_define
class AddServerBanResponse:
    """
    Attributes:
        message (str):
        status (AddServerBanResponseStatus | Unset):  Default: AddServerBanResponseStatus.SUCCESS.
    """

    message: str
    status: AddServerBanResponseStatus | Unset = AddServerBanResponseStatus.SUCCESS

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "message": message,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message = d.pop("message")

        _status = d.pop("status", UNSET)
        status: AddServerBanResponseStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = AddServerBanResponseStatus(_status)

        add_server_ban_response = cls(
            message=message,
            status=status,
        )

        return add_server_ban_response
