from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.plugin_statuses_response_status import PluginStatusesResponseStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.plugin_statuses_response_plugins_type_0 import PluginStatusesResponsePluginsType0


T = TypeVar("T", bound="PluginStatusesResponse")


@_attrs_define
class PluginStatusesResponse:
    """Response model for plugin statuses.

    Attributes:
        status (PluginStatusesResponseStatus):
        message (None | str | Unset):
        plugins (None | PluginStatusesResponsePluginsType0 | Unset):
    """

    status: PluginStatusesResponseStatus
    message: None | str | Unset = UNSET
    plugins: None | PluginStatusesResponsePluginsType0 | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.plugin_statuses_response_plugins_type_0 import PluginStatusesResponsePluginsType0  # noqa: PLC0415

        status = self.status.value

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        plugins: dict[str, Any] | None | Unset
        if isinstance(self.plugins, Unset):
            plugins = UNSET
        elif isinstance(self.plugins, PluginStatusesResponsePluginsType0):
            plugins = self.plugins.to_dict()
        else:
            plugins = self.plugins

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "status": status,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message
        if plugins is not UNSET:
            field_dict["plugins"] = plugins

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.plugin_statuses_response_plugins_type_0 import PluginStatusesResponsePluginsType0  # noqa: PLC0415

        d = dict(src_dict)
        status = PluginStatusesResponseStatus(d.pop("status"))

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        def _parse_plugins(data: object) -> None | PluginStatusesResponsePluginsType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                plugins_type_0 = PluginStatusesResponsePluginsType0.from_dict(data)

                return plugins_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PluginStatusesResponsePluginsType0 | Unset, data)

        plugins = _parse_plugins(d.pop("plugins", UNSET))

        plugin_statuses_response = cls(
            status=status,
            message=message,
            plugins=plugins,
        )

        return plugin_statuses_response
