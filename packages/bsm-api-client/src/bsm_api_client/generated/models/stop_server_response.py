from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define

from ..models.stop_server_response_outcome import StopServerResponseOutcome
from ..types import UNSET, Unset

T = TypeVar("T", bound="StopServerResponse")


@_attrs_define
class StopServerResponse:
    """
    Attributes:
        message (str):
        outcome (StopServerResponseOutcome):
        server_name (str):
        status (Literal['success'] | Unset):  Default: 'success'.
    """

    message: str
    outcome: StopServerResponseOutcome
    server_name: str
    status: Literal["success"] | Unset = "success"

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        outcome = self.outcome.value

        server_name = self.server_name

        status = self.status

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "message": message,
                "outcome": outcome,
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

        outcome = StopServerResponseOutcome(d.pop("outcome"))

        server_name = d.pop("server_name")

        status = cast(Literal["success"] | Unset, d.pop("status", UNSET))
        if status != "success" and not isinstance(status, Unset):
            raise ValueError(f"status must match const 'success', got '{status}'")

        stop_server_response = cls(
            message=message,
            outcome=outcome,
            server_name=server_name,
            status=status,
        )

        return stop_server_response
