from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="InstallationAcceptedResponse")


@_attrs_define
class InstallationAcceptedResponse:
    """
    Attributes:
        message (str):
        server_name (str):
        task_id (str):
        status (Literal['accepted'] | Unset):  Default: 'accepted'.
    """

    message: str
    server_name: str
    task_id: str
    status: Literal["accepted"] | Unset = "accepted"

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        server_name = self.server_name

        task_id = self.task_id

        status = self.status

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "message": message,
                "server_name": server_name,
                "task_id": task_id,
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

        task_id = d.pop("task_id")

        status = cast(Literal["accepted"] | Unset, d.pop("status", UNSET))
        if status != "accepted" and not isinstance(status, Unset):
            raise ValueError(f"status must match const 'accepted', got '{status}'")

        installation_accepted_response = cls(
            message=message,
            server_name=server_name,
            task_id=task_id,
            status=status,
        )

        return installation_accepted_response
