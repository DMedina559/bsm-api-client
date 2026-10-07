from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.server_settings_response_status import ServerSettingsResponseStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.server_setting_item_payload import ServerSettingItemPayload
    from ..models.server_settings_response_settings_type_0 import ServerSettingsResponseSettingsType0


T = TypeVar("T", bound="ServerSettingsResponse")


@_attrs_define
class ServerSettingsResponse:
    """Response model for server settings operations.

    Attributes:
        status (ServerSettingsResponseStatus):
        message (None | str | Unset):
        setting (None | ServerSettingItemPayload | Unset):
        settings (None | ServerSettingsResponseSettingsType0 | Unset):
    """

    status: ServerSettingsResponseStatus
    message: None | str | Unset = UNSET
    setting: None | ServerSettingItemPayload | Unset = UNSET
    settings: None | ServerSettingsResponseSettingsType0 | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.server_setting_item_payload import ServerSettingItemPayload  # noqa: PLC0415
        from ..models.server_settings_response_settings_type_0 import (
            ServerSettingsResponseSettingsType0,  # noqa: PLC0415
        )

        status = self.status.value

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        setting: dict[str, Any] | None | Unset
        if isinstance(self.setting, Unset):
            setting = UNSET
        elif isinstance(self.setting, ServerSettingItemPayload):
            setting = self.setting.to_dict()
        else:
            setting = self.setting

        settings: dict[str, Any] | None | Unset
        if isinstance(self.settings, Unset):
            settings = UNSET
        elif isinstance(self.settings, ServerSettingsResponseSettingsType0):
            settings = self.settings.to_dict()
        else:
            settings = self.settings

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "status": status,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message
        if setting is not UNSET:
            field_dict["setting"] = setting
        if settings is not UNSET:
            field_dict["settings"] = settings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.server_setting_item_payload import ServerSettingItemPayload  # noqa: PLC0415
        from ..models.server_settings_response_settings_type_0 import (
            ServerSettingsResponseSettingsType0,  # noqa: PLC0415
        )

        d = dict(src_dict)
        status = ServerSettingsResponseStatus(d.pop("status"))

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        def _parse_setting(data: object) -> None | ServerSettingItemPayload | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                setting_type_0 = ServerSettingItemPayload.from_dict(data)

                return setting_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ServerSettingItemPayload | Unset, data)

        setting = _parse_setting(d.pop("setting", UNSET))

        def _parse_settings(data: object) -> None | ServerSettingsResponseSettingsType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                settings_type_0 = ServerSettingsResponseSettingsType0.from_dict(data)

                return settings_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ServerSettingsResponseSettingsType0 | Unset, data)

        settings = _parse_settings(d.pop("settings", UNSET))

        server_settings_response = cls(
            status=status,
            message=message,
            setting=setting,
            settings=settings,
        )

        return server_settings_response
