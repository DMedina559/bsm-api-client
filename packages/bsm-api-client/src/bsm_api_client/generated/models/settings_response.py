from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.settings_response_status import SettingsResponseStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.setting_item_response import SettingItemResponse
    from ..models.settings_response_settings_type_0 import SettingsResponseSettingsType0


T = TypeVar("T", bound="SettingsResponse")


@_attrs_define
class SettingsResponse:
    """Response model for settings operations.

    Attributes:
        status (SettingsResponseStatus):
        message (None | str | Unset):
        setting (None | SettingItemResponse | Unset):
        settings (None | SettingsResponseSettingsType0 | Unset):
    """

    status: SettingsResponseStatus
    message: None | str | Unset = UNSET
    setting: None | SettingItemResponse | Unset = UNSET
    settings: None | SettingsResponseSettingsType0 | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.setting_item_response import SettingItemResponse  # noqa: PLC0415
        from ..models.settings_response_settings_type_0 import SettingsResponseSettingsType0  # noqa: PLC0415

        status = self.status.value

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        setting: dict[str, Any] | None | Unset
        if isinstance(self.setting, Unset):
            setting = UNSET
        elif isinstance(self.setting, SettingItemResponse):
            setting = self.setting.to_dict()
        else:
            setting = self.setting

        settings: dict[str, Any] | None | Unset
        if isinstance(self.settings, Unset):
            settings = UNSET
        elif isinstance(self.settings, SettingsResponseSettingsType0):
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
        from ..models.setting_item_response import SettingItemResponse  # noqa: PLC0415
        from ..models.settings_response_settings_type_0 import SettingsResponseSettingsType0  # noqa: PLC0415

        d = dict(src_dict)
        status = SettingsResponseStatus(d.pop("status"))

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        def _parse_setting(data: object) -> None | SettingItemResponse | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                setting_type_0 = SettingItemResponse.from_dict(data)

                return setting_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SettingItemResponse | Unset, data)

        setting = _parse_setting(d.pop("setting", UNSET))

        def _parse_settings(data: object) -> None | SettingsResponseSettingsType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                settings_type_0 = SettingsResponseSettingsType0.from_dict(data)

                return settings_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SettingsResponseSettingsType0 | Unset, data)

        settings = _parse_settings(d.pop("settings", UNSET))

        settings_response = cls(
            status=status,
            message=message,
            setting=setting,
            settings=settings,
        )

        return settings_response
