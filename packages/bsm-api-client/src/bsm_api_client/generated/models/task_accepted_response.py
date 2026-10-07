from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="TaskAcceptedResponse")


@_attrs_define
class TaskAcceptedResponse:
    """
    Attributes:
        message (str):
        task_id (str):
        status (Literal['accepted'] | Unset):  Default: 'accepted'.
    """

    message: str
    task_id: str
    status: Literal["accepted"] | Unset = "accepted"

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        task_id = self.task_id

        status = self.status

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "message": message,
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

        task_id = d.pop("task_id")

        status = cast(Literal["accepted"] | Unset, d.pop("status", UNSET))
        if status != "accepted" and not isinstance(status, Unset):
            raise ValueError(f"status must match const 'accepted', got '{status}'")

        task_accepted_response = cls(
            message=message,
            task_id=task_id,
            status=status,
        )

        return task_accepted_response
