from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.permissions_update_response_status import PermissionsUpdateResponseStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.permissions_update_response_errors_type_0 import PermissionsUpdateResponseErrorsType0


T = TypeVar("T", bound="PermissionsUpdateResponse")


@_attrs_define
class PermissionsUpdateResponse:
    """Response model for permissions update.

    Attributes:
        status (PermissionsUpdateResponseStatus):
        errors (None | PermissionsUpdateResponseErrorsType0 | Unset):
        message (None | str | Unset):
    """

    status: PermissionsUpdateResponseStatus
    errors: None | PermissionsUpdateResponseErrorsType0 | Unset = UNSET
    message: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.permissions_update_response_errors_type_0 import (
            PermissionsUpdateResponseErrorsType0,  # noqa: PLC0415
        )

        status = self.status.value

        errors: dict[str, Any] | None | Unset
        if isinstance(self.errors, Unset):
            errors = UNSET
        elif isinstance(self.errors, PermissionsUpdateResponseErrorsType0):
            errors = self.errors.to_dict()
        else:
            errors = self.errors

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
        if errors is not UNSET:
            field_dict["errors"] = errors
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.permissions_update_response_errors_type_0 import (
            PermissionsUpdateResponseErrorsType0,  # noqa: PLC0415
        )

        d = dict(src_dict)
        status = PermissionsUpdateResponseStatus(d.pop("status"))

        def _parse_errors(data: object) -> None | PermissionsUpdateResponseErrorsType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                errors_type_0 = PermissionsUpdateResponseErrorsType0.from_dict(data)

                return errors_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PermissionsUpdateResponseErrorsType0 | Unset, data)

        errors = _parse_errors(d.pop("errors", UNSET))

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        permissions_update_response = cls(
            status=status,
            errors=errors,
            message=message,
        )

        return permissions_update_response
