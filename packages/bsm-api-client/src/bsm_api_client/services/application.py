import logging
from typing import cast

from ..models import (
    CustomZipsResponse,
    GetAllGlobalSettingsResponse,
    GetApplicationHealthResponse,
    GetApplicationMetricsResponse,
    GetSystemAndAppInfoResponse,
    PruneDownloadCacheResponse,
    PruneDownloadsPayload,
    ReloadGlobalSettingsResponse,
    RuntimeStatus,
    SetGlobalSettingResponse,
    SettingItemPayload,
    SetupStatusResponse,
    ShutdownResponse,
    ThemeListResponse,
    TokenResponse,
    UserLoginPayload,
)
from ..validation import parse_response
from .base import Service

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.manager")


class ApplicationService(Service):
    """Service for manager-level endpoints."""

    async def async_get_info(self) -> GetSystemAndAppInfoResponse:
        """Gets system and application information from the manager.

        The response exposes OS, application version, splash text, and the IANA
        display and scheduling timezone directly. Timestamp instants remain UTC.

        :returns: `GetSystemAndAppInfoResponse`.
        """
        _LOGGER.debug("Fetching manager system and application information from /info")
        response = await self.async_call_generated(
            "get_system_info", authenticated=False, typed=True
        )
        return cast(
            GetSystemAndAppInfoResponse,
            parse_response(GetSystemAndAppInfoResponse, response),
        )

    async def async_get_custom_zips(self) -> CustomZipsResponse:
        """Retrieves a list of available custom server ZIP files.

        :returns: `CustomZipsResponse`.
        """
        _LOGGER.info("Fetching list of custom zips.")
        response = await self.async_call_generated(
            "list_downloads", authenticated=True, typed=True
        )
        return cast(CustomZipsResponse, parse_response(CustomZipsResponse, response))

    async def async_get_themes(self) -> ThemeListResponse:
        """Retrieves a list of available themes.

        :returns: `ThemeListResponse`.
        """
        _LOGGER.info("Fetching list of available themes.")
        result = await self.async_call_generated(
            "list_themes", authenticated=True, typed=True
        )
        return cast(ThemeListResponse, parse_response(ThemeListResponse, result))

    async def async_get_all_settings(self) -> GetAllGlobalSettingsResponse:
        """Retrieve all global application settings.

        :returns: `GetAllGlobalSettingsResponse`.
        """
        _LOGGER.info("Fetching all global application settings.")
        response = await self.async_call_generated(
            "get_settings", authenticated=True, typed=True
        )
        return cast(
            GetAllGlobalSettingsResponse,
            parse_response(GetAllGlobalSettingsResponse, response),
        )

    async def async_set_setting(
        self, payload: SettingItemPayload
    ) -> SetGlobalSettingResponse:
        """Sets a specific global application setting.

        :param payload: The SettingItemPayload request model.

        :returns: `SetGlobalSettingResponse`.
        """
        _LOGGER.debug("Updating global application setting '%s'", payload.key)
        response = await self.async_call_generated(
            "set_setting", body=payload.model_dump(), authenticated=True, typed=True
        )
        return cast(
            SetGlobalSettingResponse, parse_response(SetGlobalSettingResponse, response)
        )

    async def async_reload_settings(self) -> ReloadGlobalSettingsResponse:
        """Forces a reload of global application settings and logging configuration.

        :returns: `ReloadGlobalSettingsResponse`.
        """
        _LOGGER.info("Requesting reload of global settings and logging configuration.")
        response = await self.async_call_generated(
            "reload_settings", authenticated=True, typed=True
        )
        return cast(
            ReloadGlobalSettingsResponse,
            parse_response(ReloadGlobalSettingsResponse, response),
        )

    async def async_get_panorama_image(self) -> bytes:
        """Retrieves the panorama background image.

        :returns: `bytes`.
        """
        response = await self.async_call_generated(
            "get_panorama", authenticated=False, detailed=True
        )
        return cast(bytes, response.content)

    async def async_prune_downloads(
        self, payload: PruneDownloadsPayload
    ) -> PruneDownloadCacheResponse:
        """Triggers pruning of downloaded server archives.

        :param payload: The PruneDownloadsPayload request model.

        :returns: `PruneDownloadCacheResponse`.
        """
        _LOGGER.info(
            "Triggering download cache prune for directory '%s', keep: %s",
            payload.directory,
            payload.keep if payload.keep is not None else "server default",
        )
        response = await self.async_call_generated(
            "prune_downloads", body=payload.model_dump(), authenticated=True, typed=True
        )
        return cast(
            PruneDownloadCacheResponse,
            parse_response(PruneDownloadCacheResponse, response),
        )

    async def async_get_application_health(self) -> GetApplicationHealthResponse:
        """Return manager lifecycle and component health checks.

        :returns: `GetApplicationHealthResponse`.
        """
        return parse_response(
            GetApplicationHealthResponse,
            await self.async_call_generated(
                "get_application_health", authenticated=True, typed=True
            ),
        )

    async def async_get_application_metrics(self) -> GetApplicationMetricsResponse:
        """Return application and system samples with their bounded history.

        :returns: `GetApplicationMetricsResponse`.
        """
        return parse_response(
            GetApplicationMetricsResponse,
            await self.async_call_generated(
                "get_application_metrics", authenticated=True, typed=True
            ),
        )

    async def async_get_setup_status(self) -> SetupStatusResponse:
        """Check whether the backend needs its first administrator.

        :returns: `SetupStatusResponse`.
        """
        return parse_response(
            SetupStatusResponse,
            await self.async_call_generated(
                "get_setup_status", authenticated=False, typed=True
            ),
        )

    async def async_create_first_user(self, payload: UserLoginPayload) -> TokenResponse:
        """Create the initial administrator on an unconfigured backend.

        :param payload: The UserLoginPayload request model.

        :returns: `TokenResponse`.
        """
        return parse_response(
            TokenResponse,
            await self.async_call_generated(
                "create_first_user",
                body=payload.model_dump(mode="json"),
                authenticated=False,
                typed=True,
            ),
        )

    async def async_get_web_runtime(self) -> RuntimeStatus:
        """Inspect the web host's phase and shutdown state as an administrator."""
        return parse_response(
            RuntimeStatus,
            await self.async_call_generated(
                "get_web_runtime", authenticated=True, typed=True
            ),
        )

    async def async_shutdown_web_runtime(self) -> ShutdownResponse:
        """Request graceful host shutdown; acceptance does not confirm completion."""
        return parse_response(
            ShutdownResponse,
            await self.async_call_generated(
                "shutdown_web_runtime", body={}, authenticated=True, typed=True
            ),
        )
