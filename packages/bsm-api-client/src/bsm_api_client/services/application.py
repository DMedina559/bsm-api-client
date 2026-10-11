import logging
from typing import cast

from ..models import (
    AppInfoResponse,
    CustomZipsResponse,
    GetApplicationHealthResponse,
    GetApplicationMetricsResponse,
    PruneDownloadsPayload,
    PruneDownloadsResponse,
    SettingItemResponse,
    SettingsResponse,
    SetupAccountResponse,
    SetupStatusResponse,
    ThemeListResponse,
    UserLoginPayload,
)
from ..validation import parse_response
from .base import Service

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.manager")


class ApplicationService(Service):
    """Service for manager-level endpoints."""

    async def async_get_info(self) -> AppInfoResponse:
        """Gets system and application information from the manager.

        Returns:
            An `AppInfoResponse` object containing system and application information.
        """
        _LOGGER.debug("Fetching manager system and application information from /info")
        response = await self.async_call_generated(
            "get_system_info", authenticated=False
        )
        return cast(AppInfoResponse, parse_response(AppInfoResponse, response))

    async def async_get_custom_zips(self) -> CustomZipsResponse:
        """Retrieves a list of available custom server ZIP files.

        Returns:
            A `CustomZipsResponse` object containing the list of custom ZIP files.
        """
        _LOGGER.info("Fetching list of custom zips.")
        response = await self.async_call_generated("list_downloads", authenticated=True)
        return cast(CustomZipsResponse, parse_response(CustomZipsResponse, response))

    async def async_get_themes(self) -> ThemeListResponse:
        """Retrieves a list of available themes.

        Returns:
            A `ThemeListResponse` containing the list of themes.
        """
        _LOGGER.info("Fetching list of available themes.")
        result = await self.async_call_generated("list_themes", authenticated=True)
        return cast(ThemeListResponse, parse_response(ThemeListResponse, result))

    async def async_get_all_settings(self) -> SettingsResponse:
        """Retrieve all global application settings.

        Returns:
            A `SettingsResponse` object containing all settings.
        """
        _LOGGER.info("Fetching all global application settings.")
        response = await self.async_call_generated("get_settings", authenticated=True)
        return cast(SettingsResponse, parse_response(SettingsResponse, response))

    async def async_set_setting(self, payload: SettingItemResponse) -> SettingsResponse:
        """Sets a specific global application setting.

        Args:
            payload: A `SettingItemResponse` object containing the setting to set.

        Returns:
            A `SettingsResponse` object containing the result of the set operation.
        """
        _LOGGER.debug("Updating global application setting '%s'", payload.key)
        response = await self.async_call_generated(
            "set_setting", body=payload.model_dump(), authenticated=True
        )
        return cast(SettingsResponse, parse_response(SettingsResponse, response))

    async def async_reload_settings(self) -> SettingsResponse:
        """Forces a reload of global application settings and logging configuration.

        Returns:
            A `SettingsResponse` object containing the result of the reload operation.
        """
        _LOGGER.info("Requesting reload of global settings and logging configuration.")
        response = await self.async_call_generated(
            "reload_settings", authenticated=True
        )
        return cast(SettingsResponse, parse_response(SettingsResponse, response))

    async def async_get_panorama_image(self) -> bytes:
        """Retrieves the panorama background image.

        Returns:
            The raw bytes of the panorama image.

        Raises:
            CannotConnectError: If a connection to the server cannot be established.
            APIError: For any other API-related errors.
        """
        response = await self.async_call_generated(
            "get_panorama", authenticated=False, detailed=True
        )
        return cast(bytes, response.content)

    async def async_prune_downloads(
        self, payload: PruneDownloadsPayload
    ) -> PruneDownloadsResponse:
        """Triggers pruning of downloaded server archives.

        Args:
            payload: A `PruneDownloadsPayload` object containing the prune options.

        Returns:
            A `PruneDownloadsResponse` object containing the result of the prune operation.
        """
        _LOGGER.info(
            "Triggering download cache prune for directory '%s', keep: %s",
            payload.directory,
            payload.keep if payload.keep is not None else "server default",
        )
        response = await self.async_call_generated(
            "prune_downloads", body=payload.model_dump(), authenticated=True
        )
        return cast(
            PruneDownloadsResponse, parse_response(PruneDownloadsResponse, response)
        )

    async def async_get_application_health(self) -> GetApplicationHealthResponse:
        """Return manager lifecycle and component health checks."""
        return parse_response(
            GetApplicationHealthResponse,
            await self.async_call_generated(
                "get_application_health", authenticated=True
            ),
        )

    async def async_get_application_metrics(self) -> GetApplicationMetricsResponse:
        """Return application and system samples with their bounded history."""
        return parse_response(
            GetApplicationMetricsResponse,
            await self.async_call_generated(
                "get_application_metrics", authenticated=True
            ),
        )

    async def async_get_setup_status(self) -> SetupStatusResponse:
        """Check whether the backend needs its first administrator."""
        return parse_response(
            SetupStatusResponse,
            await self.async_call_generated("get_setup_status", authenticated=False),
        )

    async def async_create_first_user(
        self, payload: UserLoginPayload
    ) -> SetupAccountResponse:
        """Create the initial administrator on an unconfigured backend."""
        return parse_response(
            SetupAccountResponse,
            await self.async_call_generated(
                "create_first_user",
                body=payload.model_dump(mode="json"),
                authenticated=False,
            ),
        )
