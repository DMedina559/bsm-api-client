from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.theme_list_response_status import ThemeListResponseStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ThemeListResponse")


@_attrs_define
class ThemeListResponse:
    """Response model for theme lists.

    Attributes:
        status (ThemeListResponseStatus):
        message (None | str | Unset):
        themes (list[str] | None | Unset):
    """

    status: ThemeListResponseStatus
    message: None | str | Unset = UNSET
    themes: list[str] | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        themes: list[str] | None | Unset
        if isinstance(self.themes, Unset):
            themes = UNSET
        elif isinstance(self.themes, list):
            themes = self.themes

        else:
            themes = self.themes

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "status": status,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message
        if themes is not UNSET:
            field_dict["themes"] = themes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = ThemeListResponseStatus(d.pop("status"))

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        def _parse_themes(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                themes_type_0 = cast(list[str], data)

                return themes_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        themes = _parse_themes(d.pop("themes", UNSET))

        theme_list_response = cls(
            status=status,
            message=message,
            themes=themes,
        )

        return theme_list_response
