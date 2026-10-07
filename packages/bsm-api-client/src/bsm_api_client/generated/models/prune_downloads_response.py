from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.prune_downloads_response_status import PruneDownloadsResponseStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="PruneDownloadsResponse")


@_attrs_define
class PruneDownloadsResponse:
    """Response model for pruning downloads.

    Attributes:
        status (PruneDownloadsResponseStatus):
        files_deleted (int | None | Unset):
        files_kept (int | None | Unset):
        message (None | str | Unset):
    """

    status: PruneDownloadsResponseStatus
    files_deleted: int | None | Unset = UNSET
    files_kept: int | None | Unset = UNSET
    message: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        files_deleted: int | None | Unset
        if isinstance(self.files_deleted, Unset):
            files_deleted = UNSET
        else:
            files_deleted = self.files_deleted

        files_kept: int | None | Unset
        if isinstance(self.files_kept, Unset):
            files_kept = UNSET
        else:
            files_kept = self.files_kept

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
        if files_deleted is not UNSET:
            field_dict["files_deleted"] = files_deleted
        if files_kept is not UNSET:
            field_dict["files_kept"] = files_kept
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = PruneDownloadsResponseStatus(d.pop("status"))

        def _parse_files_deleted(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        files_deleted = _parse_files_deleted(d.pop("files_deleted", UNSET))

        def _parse_files_kept(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        files_kept = _parse_files_kept(d.pop("files_kept", UNSET))

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        prune_downloads_response = cls(
            status=status,
            files_deleted=files_deleted,
            files_kept=files_kept,
            message=message,
        )

        return prune_downloads_response
