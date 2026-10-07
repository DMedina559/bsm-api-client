from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.trigger_event_payload_payload_type_0 import TriggerEventPayloadPayloadType0


T = TypeVar("T", bound="TriggerEventPayload")


@_attrs_define
class TriggerEventPayload:
    """Request model for triggering a custom plugin event.

    Attributes:
        event_name (str): The namespaced name of the event to trigger (e.g., 'myplugin:myevent').
        payload (None | TriggerEventPayloadPayloadType0 | Unset): Optional dictionary payload for the event.
    """

    event_name: str
    payload: None | TriggerEventPayloadPayloadType0 | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.trigger_event_payload_payload_type_0 import TriggerEventPayloadPayloadType0  # noqa: PLC0415

        event_name = self.event_name

        payload: dict[str, Any] | None | Unset
        if isinstance(self.payload, Unset):
            payload = UNSET
        elif isinstance(self.payload, TriggerEventPayloadPayloadType0):
            payload = self.payload.to_dict()
        else:
            payload = self.payload

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "event_name": event_name,
            }
        )
        if payload is not UNSET:
            field_dict["payload"] = payload

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.trigger_event_payload_payload_type_0 import TriggerEventPayloadPayloadType0  # noqa: PLC0415

        d = dict(src_dict)
        event_name = d.pop("event_name")

        def _parse_payload(data: object) -> None | TriggerEventPayloadPayloadType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                payload_type_0 = TriggerEventPayloadPayloadType0.from_dict(data)

                return payload_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TriggerEventPayloadPayloadType0 | Unset, data)

        payload = _parse_payload(d.pop("payload", UNSET))

        trigger_event_payload = cls(
            event_name=event_name,
            payload=payload,
        )

        trigger_event_payload.additional_properties = d
        return trigger_event_payload

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
