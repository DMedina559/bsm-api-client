from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.audit_log_response_details_type_0 import AuditLogResponseDetailsType0


T = TypeVar("T", bound="AuditLogResponse")


@_attrs_define
class AuditLogResponse:
    """
    Attributes:
        action (str):
        id (int):
        timestamp (datetime.datetime):
        user_id (int):
        details (AuditLogResponseDetailsType0 | None | Unset):
    """

    action: str
    id: int
    timestamp: datetime.datetime
    user_id: int
    details: AuditLogResponseDetailsType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.audit_log_response_details_type_0 import AuditLogResponseDetailsType0  # noqa: PLC0415

        action = self.action

        id = self.id

        timestamp = self.timestamp.isoformat()

        user_id = self.user_id

        details: dict[str, Any] | None | Unset
        if isinstance(self.details, Unset):
            details = UNSET
        elif isinstance(self.details, AuditLogResponseDetailsType0):
            details = self.details.to_dict()
        else:
            details = self.details

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action": action,
                "id": id,
                "timestamp": timestamp,
                "user_id": user_id,
            }
        )
        if details is not UNSET:
            field_dict["details"] = details

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.audit_log_response_details_type_0 import AuditLogResponseDetailsType0  # noqa: PLC0415

        d = dict(src_dict)
        action = d.pop("action")

        id = d.pop("id")

        timestamp = datetime.datetime.fromisoformat(d.pop("timestamp"))

        user_id = d.pop("user_id")

        def _parse_details(data: object) -> AuditLogResponseDetailsType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                details_type_0 = AuditLogResponseDetailsType0.from_dict(data)

                return details_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AuditLogResponseDetailsType0 | None | Unset, data)

        details = _parse_details(d.pop("details", UNSET))

        audit_log_response = cls(
            action=action,
            id=id,
            timestamp=timestamp,
            user_id=user_id,
            details=details,
        )

        audit_log_response.additional_properties = d
        return audit_log_response

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
