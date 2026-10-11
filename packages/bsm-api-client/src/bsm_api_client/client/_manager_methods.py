"""Mixin class for manager-level API methods.

This module provides the `ManagerMethodsMixin` class, which includes methods
for interacting with manager-level endpoints of the Bedrock Server Manager API.
These methods handle operations such as getting system information, managing
players, and installing new servers.
"""

import logging
from typing import Any, Dict, cast

from ..generated_adapter import GeneratedOperationMethods
from ..models import (
    AddPlayersPayload,
    AddPlayersResponse,
    AppInfoResponse,
    CustomZipsResponse,
    GetApplicationHealthResponse,
    GetApplicationMetricsResponse,
    InstallServerPayload,
    InstallServerResponse,
    PlayerListResponse,
    PruneDownloadsPayload,
    PruneDownloadsResponse,
    SettingItemResponse,
    SettingsResponse,
    SetupAccountResponse,
    SetupStatusResponse,
    TaskSnapshot,
    ThemeListResponse,
    UserLoginPayload,
)
from ..validation import parse_response

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.manager")


class ManagerMethodsMixin(GeneratedOperationMethods):
    """Mixin for manager-level endpoints."""

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

    async def async_scan_players(self) -> AddPlayersResponse:
        """Triggers a scan of player logs across all servers.

        Returns:
            An `AddPlayersResponse` object containing the result of the scan operation.
        """
        _LOGGER.info("Triggering player log scan")
        response = await self.async_call_generated("scan_players", authenticated=True)
        return cast(AddPlayersResponse, parse_response(AddPlayersResponse, response))

    async def async_get_players(self) -> PlayerListResponse:
        """Gets the global list of known players.

        Returns:
            A `PlayerListResponse` object containing the list of players.
        """
        _LOGGER.debug("Fetching global player list from /players/get")
        response = await self.async_call_generated("list_players", authenticated=True)
        return cast(PlayerListResponse, parse_response(PlayerListResponse, response))

    async def async_add_players(self, payload: AddPlayersPayload) -> AddPlayersResponse:
        """Adds or updates players in the global list.

        Args:
            payload: An `AddPlayersPayload` object containing the players to add.

        Returns:
            An `AddPlayersResponse` object containing the result of the add operation.
        """
        _LOGGER.info("Adding/updating global players: %s", payload.players)
        response = await self.async_call_generated(
            "add_players", body=payload.model_dump(), authenticated=True
        )
        return cast(AddPlayersResponse, parse_response(AddPlayersResponse, response))

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

    async def async_install_new_server(
        self, payload: InstallServerPayload
    ) -> InstallServerResponse:
        """Requests the installation of a new Bedrock server instance.

        Args:
            payload: An `InstallServerPayload` object containing the server details.

        Returns:
            An `InstallServerResponse` object with the result of the installation request.
        """
        _LOGGER.info(
            "Requesting installation for server '%s', version: '%s', overwrite: %s",
            payload.server_name,
            payload.server_version,
            payload.overwrite,
        )
        response = await self.async_call_generated(
            "install_server", body=payload.model_dump(), authenticated=True
        )
        return cast(
            InstallServerResponse, parse_response(InstallServerResponse, response)
        )

    async def async_get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Retrieves the status of a background task.

        Args:
            task_id: The ID of the task.

        Returns:
            A dictionary containing the status of the task.
        """
        _LOGGER.info("Fetching installation status for task ID: %s", task_id)
        result = await self.async_call_generated(
            "get_task_status", parameters={"task_id": task_id}, authenticated=True
        )
        return dict(result)

    async def async_get_task_snapshot(self, task_id: str) -> TaskSnapshot:
        """Return the typed task snapshot from the version-2 backend contract."""
        return cast(
            TaskSnapshot,
            parse_response(TaskSnapshot, await self.async_get_task_status(task_id)),
        )

    async def async_list_tasks(self) -> list[TaskSnapshot]:
        """List typed task snapshots visible to the authenticated user."""
        result = await self.async_call_generated("list_tasks", authenticated=True)
        return [
            cast(TaskSnapshot, parse_response(TaskSnapshot, item)) for item in result
        ]

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
