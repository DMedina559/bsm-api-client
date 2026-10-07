from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.server_process_info_response_status import ServerProcessInfoResponseStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.process_info import ProcessInfo


T = TypeVar("T", bound="ServerProcessInfoResponse")


@_attrs_define
class ServerProcessInfoResponse:
    """Response model for server process info.

    Attributes:
        status (ServerProcessInfoResponseStatus):
        message (None | str | Unset):
        process_info (None | ProcessInfo | Unset):
    """

    status: ServerProcessInfoResponseStatus
    message: None | str | Unset = UNSET
    process_info: None | ProcessInfo | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.process_info import ProcessInfo  # noqa: PLC0415

        status = self.status.value

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        process_info: dict[str, Any] | None | Unset
        if isinstance(self.process_info, Unset):
            process_info = UNSET
        elif isinstance(self.process_info, ProcessInfo):
            process_info = self.process_info.to_dict()
        else:
            process_info = self.process_info

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "status": status,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message
        if process_info is not UNSET:
            field_dict["process_info"] = process_info

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.process_info import ProcessInfo  # noqa: PLC0415

        d = dict(src_dict)
        status = ServerProcessInfoResponseStatus(d.pop("status"))

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        def _parse_process_info(data: object) -> None | ProcessInfo | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                process_info_type_0 = ProcessInfo.from_dict(data)

                return process_info_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ProcessInfo | Unset, data)

        process_info = _parse_process_info(d.pop("process_info", UNSET))

        server_process_info_response = cls(
            status=status,
            message=message,
            process_info=process_info,
        )

        return server_process_info_response
