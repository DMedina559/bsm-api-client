# src/bsm_api_client/client/_manager_methods.py
"""Mixin class for manager-level API methods.

This module provides the `ManagerMethodsMixin` class, which includes methods
for interacting with manager-level endpoints of the Bedrock Server Manager API.
These methods handle operations such as getting system information, managing
players, and installing new servers.
"""
import logging
from typing import Any, Dict, Optional, List, TYPE_CHECKING
from ..models import (
    AddPlayersPayload,
    SettingItem,
    PruneDownloadsPayload,
    InstallServerPayload,
    InstallServerResponse,
    GeneralApiResponse,
    SettingsResponse,
)

if TYPE_CHECKING:
    from ..client_base import ClientBase

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.manager")


class ManagerMethodsMixin:
    """Mixin for manager-level endpoints."""

    _request: callable
    if TYPE_CHECKING:

        async def _request(
            self: "ClientBase",
            method: str,
            path: str,
            json_data: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None,
            authenticated: bool = True,
            is_retry: bool = False,
        ) -> Any: ...

    async def async_get_info(self) -> GeneralApiResponse:
        """Gets system and application information from the manager.

        Returns:
            A `GeneralApiResponse` object containing system and application information.
        """
        _LOGGER.debug("Fetching manager system and application information from /info")
        response = await self._request(method="GET", path="/info", authenticated=False)
        return GeneralApiResponse.model_validate(response)

    async def async_scan_players(self) -> Dict[str, Any]:
        """Triggers a scan of player logs across all servers.

        Returns:
            A dictionary containing the result of the scan operation.
        """
        _LOGGER.info("Triggering player log scan")
        return await self._request(
            method="POST", path="/players/scan", authenticated=True
        )

    async def async_get_players(self) -> Dict[str, Any]:
        """Gets the global list of known players.

        Returns:
            A dictionary containing the list of players.
        """
        _LOGGER.debug("Fetching global player list from /players/get")
        return await self._request(
            method="GET", path="/players/get", authenticated=True
        )

    async def async_add_players(self, payload: AddPlayersPayload) -> Dict[str, Any]:
        """Adds or updates players in the global list.

        Args:
            payload: An `AddPlayersPayload` object containing the players to add.

        Returns:
            A dictionary containing the result of the add operation.
        """
        _LOGGER.info("Adding/updating global players: %s", payload.players)
        return await self._request(
            method="POST",
            path="/players/add",
            json_data=payload.model_dump(),
            authenticated=True,
        )

    async def async_get_custom_zips(self) -> Dict[str, Any]:
        """Retrieves a list of available custom server ZIP files.

        Returns:
            A dictionary containing the list of custom ZIP files.
        """
        _LOGGER.info("Fetching list of custom zips.")
        return await self._request(
            method="GET", path="/downloads/list", authenticated=True
        )

    async def async_get_themes(self) -> Dict[str, Any]:
        """Retrieves a list of available themes.

        Returns:
            A dictionary containing the list of themes.
        """
        _LOGGER.info("Fetching list of available themes.")
        return await self._request(method="GET", path="/themes", authenticated=True)

    async def async_get_all_settings(self) -> Dict[str, Any]:
        """Retrieve all global application settings.

        Returns:
            A dictionary containing all settings.
        """
        _LOGGER.info("Fetching all global application settings.")
        return await self._request(method="GET", path="/settings", authenticated=True)

    async def async_set_setting(self, payload: SettingItem) -> Dict[str, Any]:
        """Sets a specific global application setting.

        Args:
            payload: A `SettingItem` object containing the setting to set.

        Returns:
            A dictionary containing the result of the set operation.
        """
        _LOGGER.info(
            "Setting global application setting '%s' to: %s", payload.key, payload.value
        )
        return await self._request(
            method="POST",
            path="/settings",
            json_data=payload.model_dump(),
            authenticated=True,
        )

    async def async_reload_settings(self) -> Dict[str, Any]:
        """Forces a reload of global application settings and logging configuration.

        Returns:
            A dictionary containing the result of the reload operation.
        """
        _LOGGER.info("Requesting reload of global settings and logging configuration.")
        return await self._request(
            method="POST", path="/settings/reload", authenticated=True
        )

    async def async_get_panorama_image(self) -> bytes:
        """Retrieves the panorama background image.

        Returns:
            The raw bytes of the panorama image.

        Raises:
            CannotConnectError: If a connection to the server cannot be established.
            APIError: For any other API-related errors.
        """
        _LOGGER.info("Fetching panorama image.")
        # This request might return non-JSON data.
        # The _request method expects JSON or handleable errors.
        # We need to make a raw request or adapt _request.
        # For now, let's assume _request can handle non-JSON if status is OK
        # by returning the raw response object or its content.
        # However, current _request tries to parse JSON.
        # A direct session call is safer for binary data.

        url = f"{self._server_root_url}/api/panorama"  # Assuming /api prefix is appropriate here
        if "/api" not in self._api_base_segment:  # If base_path was not /api
            url = f"{self._base_url}/panorama"

        _LOGGER.debug("Request: GET %s for panorama image", url)
        try:
            async with self._session.get(
                url,
                headers={"Accept": "image/jpeg, */*"},  # Accept jpeg primarily
                timeout=aiohttp.ClientTimeout(total=self._request_timeout),
            ) as response:
                _LOGGER.debug("Response Status for GET %s: %s", url, response.status)
                if not response.ok:
                    await self._handle_api_error(response, "/api/panorama")
                    # Should be unreachable
                    raise APIError(
                        f"Panorama image request failed with status {response.status}"
                    )
                return await response.read()  # Returns bytes
        except aiohttp.ClientError as e:
            _LOGGER.error("AIOHTTP client error fetching panorama: %s", e)
            raise CannotConnectError(
                f"AIOHTTP Client Error fetching panorama: {e}", original_exception=e
            ) from e
        except APIError:  # Re-raise APIError from _handle_api_error
            raise
        except Exception as e:
            _LOGGER.exception("Unexpected error fetching panorama: %s", e)
            raise APIError(
                f"An unexpected error occurred fetching panorama: {e}"
            ) from e

    async def async_prune_downloads(
        self, payload: PruneDownloadsPayload
    ) -> Dict[str, Any]:
        """Triggers pruning of downloaded server archives.

        Args:
            payload: A `PruneDownloadsPayload` object containing the prune options.

        Returns:
            A dictionary containing the result of the prune operation.
        """
        _LOGGER.info(
            "Triggering download cache prune for directory '%s', keep: %s",
            payload.directory,
            payload.keep if payload.keep is not None else "server default",
        )

        return await self._request(
            method="POST",
            path="/downloads/prune",
            json_data=payload.model_dump(),
            authenticated=True,
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

        response = await self._request(
            method="POST",
            path="/server/install",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return InstallServerResponse.model_validate(response)

    async def async_get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Retrieves the status of a background task.

        Args:
            task_id: The ID of the task.

        Returns:
            A dictionary containing the status of the task.
        """
        _LOGGER.info("Fetching installation status for task ID: %s", task_id)
        return await self._request(
            method="GET",
            path=f"/tasks/status/{task_id}",
            authenticated=True,
        )
        return InstallServerResponse.model_validate(response)
