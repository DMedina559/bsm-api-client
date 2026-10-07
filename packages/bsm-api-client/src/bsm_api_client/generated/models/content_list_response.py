from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.content_list_response_status import ContentListResponseStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContentListResponse")


@_attrs_define
class ContentListResponse:
    """Response model for content listing endpoints.

    Attributes:
        files (Optional[List[str]]): A list of filenames found.

        Attributes:
            status (ContentListResponseStatus):
            files (list[str] | None | Unset):
            message (None | str | Unset):
    """

    status: ContentListResponseStatus
    files: list[str] | None | Unset = UNSET
    message: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        files: list[str] | None | Unset
        if isinstance(self.files, Unset):
            files = UNSET
        elif isinstance(self.files, list):
            files = self.files

        else:
            files = self.files

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
        if files is not UNSET:
            field_dict["files"] = files
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = ContentListResponseStatus(d.pop("status"))

        def _parse_files(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                files_type_0 = cast(list[str], data)

                return files_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        files = _parse_files(d.pop("files", UNSET))

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        content_list_response = cls(
            status=status,
            files=files,
            message=message,
        )

        return content_list_response
