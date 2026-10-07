from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.task_snapshot_status import TaskSnapshotStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.api_error_response import APIErrorResponse


T = TypeVar("T", bound="TaskSnapshot")


@_attrs_define
class TaskSnapshot:
    """
    Attributes:
        id (str):
        message (str):
        status (TaskSnapshotStatus):
        error (APIErrorResponse | None | Unset):
        result (Any | Unset):
    """

    id: str
    message: str
    status: TaskSnapshotStatus
    error: APIErrorResponse | None | Unset = UNSET
    result: Any | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.api_error_response import APIErrorResponse  # noqa: PLC0415

        id = self.id

        message = self.message

        status = self.status.value

        error: dict[str, Any] | None | Unset
        if isinstance(self.error, Unset):
            error = UNSET
        elif isinstance(self.error, APIErrorResponse):
            error = self.error.to_dict()
        else:
            error = self.error

        result = self.result

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "message": message,
                "status": status,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error
        if result is not UNSET:
            field_dict["result"] = result

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.api_error_response import APIErrorResponse  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        message = d.pop("message")

        status = TaskSnapshotStatus(d.pop("status"))

        def _parse_error(data: object) -> APIErrorResponse | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                error_type_0 = APIErrorResponse.from_dict(data)

                return error_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(APIErrorResponse | None | Unset, data)

        error = _parse_error(d.pop("error", UNSET))

        result = d.pop("result", UNSET)

        task_snapshot = cls(
            id=id,
            message=message,
            status=status,
            error=error,
            result=result,
        )

        return task_snapshot
