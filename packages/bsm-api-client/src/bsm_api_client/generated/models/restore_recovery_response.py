from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Literal, cast

if TYPE_CHECKING:
  from ..models.restore_recovery_state import RestoreRecoveryState





T = TypeVar("T", bound="RestoreRecoveryResponse")



@_attrs_define
class RestoreRecoveryResponse:
    """:ivar recovery: Value supplied to the operation.
    :ivar message: Value supplied to the operation.
    :ivar status: Default: 'success'."""

    recovery: RestoreRecoveryState
    message: None | str | Unset = UNSET
    status: Literal['success'] | Unset = 'success'





    def to_dict(self) -> dict[str, Any]:
        from ..models.restore_recovery_state import RestoreRecoveryState # noqa: PLC0415
        recovery = self.recovery.to_dict()

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        status = self.status


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "recovery": recovery,
        })
        if message is not UNSET:
            field_dict["message"] = message
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.restore_recovery_state import RestoreRecoveryState # noqa: PLC0415
        d = dict(src_dict)
        recovery = RestoreRecoveryState.from_dict(d.pop("recovery"))




        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))


        status = cast(Literal['success'] | Unset , d.pop("status", UNSET))
        if status != 'success'and not isinstance(status, Unset):
            raise ValueError(f"status must match const 'success', got '{status}'")

        restore_recovery_response = cls(
            recovery=recovery,
            message=message,
            status=status,
        )

        return restore_recovery_response

