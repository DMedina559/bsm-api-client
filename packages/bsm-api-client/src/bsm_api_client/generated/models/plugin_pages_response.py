from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.plugin_pages_response_status import PluginPagesResponseStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.plugin_pages_response_pages_type_0_item import PluginPagesResponsePagesType0Item


T = TypeVar("T", bound="PluginPagesResponse")


@_attrs_define
class PluginPagesResponse:
    """Response model for plugin native UI pages.

    Attributes:
        status (PluginPagesResponseStatus):
        message (None | str | Unset):
        pages (list[PluginPagesResponsePagesType0Item] | None | Unset):
    """

    status: PluginPagesResponseStatus
    message: None | str | Unset = UNSET
    pages: list[PluginPagesResponsePagesType0Item] | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        pages: list[dict[str, Any]] | None | Unset
        if isinstance(self.pages, Unset):
            pages = UNSET
        elif isinstance(self.pages, list):
            pages = []
            for pages_type_0_item_data in self.pages:
                pages_type_0_item = pages_type_0_item_data.to_dict()
                pages.append(pages_type_0_item)

        else:
            pages = self.pages

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "status": status,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message
        if pages is not UNSET:
            field_dict["pages"] = pages

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.plugin_pages_response_pages_type_0_item import PluginPagesResponsePagesType0Item  # noqa: PLC0415

        d = dict(src_dict)
        status = PluginPagesResponseStatus(d.pop("status"))

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        def _parse_pages(data: object) -> list[PluginPagesResponsePagesType0Item] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                pages_type_0 = []
                _pages_type_0 = data
                for pages_type_0_item_data in _pages_type_0:
                    pages_type_0_item = PluginPagesResponsePagesType0Item.from_dict(pages_type_0_item_data)

                    pages_type_0.append(pages_type_0_item)

                return pages_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[PluginPagesResponsePagesType0Item] | None | Unset, data)

        pages = _parse_pages(d.pop("pages", UNSET))

        plugin_pages_response = cls(
            status=status,
            message=message,
            pages=pages,
        )

        return plugin_pages_response
