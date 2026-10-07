from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.server_running_status_response_status import ServerRunningStatusResponseStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ServerRunningStatusResponse")


@_attrs_define
class ServerRunningStatusResponse:
    """Response model for server running status.

    Attributes:
        status (ServerRunningStatusResponseStatus):
        message (None | str | Unset):
        running (bool | None | Unset):
    """

    status: ServerRunningStatusResponseStatus
    message: None | str | Unset = UNSET
    running: bool | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        running: bool | None | Unset
        if isinstance(self.running, Unset):
            running = UNSET
        else:
            running = self.running

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "status": status,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message
        if running is not UNSET:
            field_dict["running"] = running

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = ServerRunningStatusResponseStatus(d.pop("status"))

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        def _parse_running(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        running = _parse_running(d.pop("running", UNSET))

        server_running_status_response = cls(
            status=status,
            message=message,
            running=running,
        )

        return server_running_status_response
