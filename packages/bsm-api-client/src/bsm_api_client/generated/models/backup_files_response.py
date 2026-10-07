from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.backup_files_response_backups_type_1 import BackupFilesResponseBackupsType1


T = TypeVar("T", bound="BackupFilesResponse")


@_attrs_define
class BackupFilesResponse:
    """
    Attributes:
        backups (BackupFilesResponseBackupsType1 | list[str]):
        message (None | str | Unset):
        status (Literal['success'] | Unset):  Default: 'success'.
    """

    backups: BackupFilesResponseBackupsType1 | list[str]
    message: None | str | Unset = UNSET
    status: Literal["success"] | Unset = "success"

    def to_dict(self) -> dict[str, Any]:
        backups: dict[str, Any] | list[str]
        if isinstance(self.backups, list):
            backups = self.backups

        else:
            backups = self.backups.to_dict()

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        status = self.status

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "backups": backups,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.backup_files_response_backups_type_1 import BackupFilesResponseBackupsType1  # noqa: PLC0415

        d = dict(src_dict)

        def _parse_backups(data: object) -> BackupFilesResponseBackupsType1 | list[str]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                backups_type_0 = cast(list[str], data)

                return backups_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            backups_type_1 = BackupFilesResponseBackupsType1.from_dict(data)

            return backups_type_1

        backups = _parse_backups(d.pop("backups"))

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        status = cast(Literal["success"] | Unset, d.pop("status", UNSET))
        if status != "success" and not isinstance(status, Unset):
            raise ValueError(f"status must match const 'success', got '{status}'")

        backup_files_response = cls(
            backups=backups,
            message=message,
            status=status,
        )

        return backup_files_response
