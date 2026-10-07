from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.trigger_event_response_status import TriggerEventResponseStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.trigger_event_response_details_type_0 import TriggerEventResponseDetailsType0


T = TypeVar("T", bound="TriggerEventResponse")


@_attrs_define
class TriggerEventResponse:
    """Response model for triggering a custom plugin event.

    Attributes:
        status (TriggerEventResponseStatus):
        details (None | TriggerEventResponseDetailsType0 | Unset):
        message (None | str | Unset):
    """

    status: TriggerEventResponseStatus
    details: None | TriggerEventResponseDetailsType0 | Unset = UNSET
    message: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.trigger_event_response_details_type_0 import TriggerEventResponseDetailsType0  # noqa: PLC0415

        status = self.status.value

        details: dict[str, Any] | None | Unset
        if isinstance(self.details, Unset):
            details = UNSET
        elif isinstance(self.details, TriggerEventResponseDetailsType0):
            details = self.details.to_dict()
        else:
            details = self.details

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
        if details is not UNSET:
            field_dict["details"] = details
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.trigger_event_response_details_type_0 import TriggerEventResponseDetailsType0  # noqa: PLC0415

        d = dict(src_dict)
        status = TriggerEventResponseStatus(d.pop("status"))

        def _parse_details(data: object) -> None | TriggerEventResponseDetailsType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                details_type_0 = TriggerEventResponseDetailsType0.from_dict(data)

                return details_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TriggerEventResponseDetailsType0 | Unset, data)

        details = _parse_details(d.pop("details", UNSET))

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        trigger_event_response = cls(
            status=status,
            details=details,
            message=message,
        )

        return trigger_event_response
