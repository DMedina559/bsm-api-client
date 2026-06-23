# src/bsm_api_client/client/_content_methods.py
"""Mixin class for content management methods.

This module provides the `ContentMethodsMixin` class, which includes methods
for managing server content such as backups, worlds, and addons.
"""

import logging
from typing import Any, Callable, Dict, Optional, cast

import aiohttp

from ..models import (
    ActionResponse,
    AddonActionPayload,
    AddonListResponse,
    AddonReorderPayload,
    AddonSubpackPayload,
    BackupActionPayload,
    ContentListResponse,
    FileNamePayload,
    RestoreActionPayload,
)

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.content")

# Define allowed types for validation to avoid magic strings
ALLOWED_BACKUP_LIST_TYPES = ["world", "properties", "allowlist", "permissions"]
ALLOWED_BACKUP_ACTION_TYPES = ["world", "config", "all"]
ALLOWED_RESTORE_TYPES = ["world", "properties", "allowlist", "permissions"]


class ContentMethodsMixin:
    """Mixin for content management endpoints (backups, worlds, addons)."""

    _request: Callable[..., Any]
    _server_root_url: str
    _jwt_token: Optional[str]
    _session: aiohttp.ClientSession
    _is_retrying: bool
    _authenticate: Callable[..., Any]
    _handle_api_error: Callable[..., Any]

    async def async_list_server_backups(
        self, server_name: str, backup_type: str
    ) -> ActionResponse:
        """Lists backup files for a specific server and backup type.

        :param server_name: The name of the server.
        :param backup_type: The type of backups to list (e.g., "world", "properties").

        :returns: An `ActionResponse` object containing the list of backups.

        :raises ValueError: If an invalid `backup_type` is provided.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_list_server_backups('MyServer')
        """
        bt_lower = backup_type.lower()
        if bt_lower not in ALLOWED_BACKUP_LIST_TYPES:
            _LOGGER.error(
                "Invalid backup_type '%s' for listing backups. Allowed: %s",
                backup_type,
                ALLOWED_BACKUP_LIST_TYPES,
            )
            raise ValueError(
                f"Invalid backup_type '{backup_type}' provided. Allowed types are: {', '.join(ALLOWED_BACKUP_LIST_TYPES)}"
            )
        _LOGGER.debug(
            "Fetching '%s' backups list for server '%s'", bt_lower, server_name
        )

        response = await self._request(
            "GET",
            f"/server/{server_name}/backup/list/{bt_lower}",
            authenticated=True,
        )
        return cast(ActionResponse, ActionResponse.model_validate(response))

    async def async_get_server_addons(self, server_name: str) -> AddonListResponse:
        """Retrieves a list of addons installed on a server's active world.

        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_get_server_addons('MyServer')
        """
        _LOGGER.debug("Fetching addons for server '%s'", server_name)
        response = await self._request(
            "GET", f"/server/{server_name}/addons", authenticated=True
        )
        return cast(AddonListResponse, AddonListResponse.model_validate(response))

    async def async_enable_server_addon(
        self, server_name: str, payload: AddonActionPayload
    ) -> ActionResponse:
        """Enables an addon on a server.

        .. rubric:: Example:
        .. code-block:: python

            payload = ...
            response = await client.async_enable_server_addon(payload)
        """
        _LOGGER.info(
            "Enabling addon '%s' for server '%s'", payload.pack_uuid, server_name
        )
        response = await self._request(
            "POST",
            f"/server/{server_name}/addon/enable",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return cast(ActionResponse, ActionResponse.model_validate(response))

    async def async_disable_server_addon(
        self, server_name: str, payload: AddonActionPayload
    ) -> ActionResponse:
        """Disables an addon on a server.

        .. rubric:: Example:
        .. code-block:: python

            payload = ...
            response = await client.async_disable_server_addon(payload)
        """
        _LOGGER.info(
            "Disabling addon '%s' for server '%s'", payload.pack_uuid, server_name
        )
        response = await self._request(
            "POST",
            f"/server/{server_name}/addon/disable",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return cast(ActionResponse, ActionResponse.model_validate(response))

    async def async_update_server_addon_subpack(
        self, server_name: str, payload: AddonSubpackPayload
    ) -> ActionResponse:
        """Updates an addon's active subpack.

        .. rubric:: Example:
        .. code-block:: python

            payload = ...
            response = await client.async_update_server_addon_subpack(payload)
        """
        _LOGGER.info(
            "Updating subpack for addon '%s' on server '%s'",
            payload.pack_uuid,
            server_name,
        )
        response = await self._request(
            "POST",
            f"/server/{server_name}/addon/subpack",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return cast(ActionResponse, ActionResponse.model_validate(response))

    async def async_uninstall_server_addon(
        self, server_name: str, payload: AddonActionPayload
    ) -> ActionResponse:
        """Uninstalls an addon on a server.

        .. rubric:: Example:
        .. code-block:: python

            payload = ...
            response = await client.async_uninstall_server_addon(payload)
        """
        _LOGGER.info(
            "Uninstalling addon '%s' for server '%s'", payload.pack_uuid, server_name
        )
        response = await self._request(
            "DELETE",
            f"/server/{server_name}/addon/uninstall",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return cast(ActionResponse, ActionResponse.model_validate(response))

    async def async_reorder_server_addon(
        self, server_name: str, payload: AddonReorderPayload
    ) -> ActionResponse:
        """Reorders active addons on a server.

        .. rubric:: Example:
        .. code-block:: python

            payload = ...
            response = await client.async_reorder_server_addon(payload)
        """
        _LOGGER.info(
            "Reordering %s packs for server '%s'", payload.pack_type, server_name
        )
        response = await self._request(
            "POST",
            f"/server/{server_name}/addon/reorder",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return cast(ActionResponse, ActionResponse.model_validate(response))

    async def async_get_content_worlds(self) -> ContentListResponse:
        """Lists available world template files (.mcworld).

        :returns: A `ContentListResponse` object containing the list of world files.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_get_content_worlds()
        """
        _LOGGER.debug("Fetching available world files from /content/worlds")
        response = await self._request("GET", "/content/worlds", authenticated=True)
        return cast(ContentListResponse, ContentListResponse.model_validate(response))

    async def async_get_content_addons(self) -> ContentListResponse:
        """Lists available addon files (.mcpack, .mcaddon).

        :returns: A `ContentListResponse` object containing the list of addon files.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_get_content_addons()
        """
        _LOGGER.debug("Fetching available addon files from /content/addons")
        response = await self._request("GET", "/content/addons", authenticated=True)
        return cast(ContentListResponse, ContentListResponse.model_validate(response))

    async def async_trigger_server_backup(
        self, server_name: str, payload: BackupActionPayload
    ) -> ActionResponse:
        """Triggers a backup operation for a specific server.

        :param server_name: The name of the server to back up.
        :param payload: A `BackupActionPayload` object specifying the backup details.

        :returns: An `ActionResponse` object confirming the backup action.


        .. rubric:: Example:
        .. code-block:: python

            payload = ...
            response = await client.async_trigger_server_backup(payload)
        """
        _LOGGER.info(
            "Triggering backup for server '%s', type: %s, file: %s",
            server_name,
            payload.backup_type,
            payload.file_to_backup or "N/A",
        )

        response = await self._request(
            "POST",
            f"/server/{server_name}/backup/action",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return cast(ActionResponse, ActionResponse.model_validate(response))

    async def async_export_server_world(self, server_name: str) -> ActionResponse:
        """Exports the current world of a server to a .mcworld file.

        :param server_name: The name of the server whose world to export.

        :returns: An `ActionResponse` object confirming the export action.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_export_server_world('MyServer')
        """
        _LOGGER.info("Triggering world export for server '%s'", server_name)
        response = await self._request(
            "POST",
            f"/server/{server_name}/world/export",
            json_data=None,
            authenticated=True,
        )
        return cast(ActionResponse, ActionResponse.model_validate(response))

    async def async_upload_content(self, file_path: str) -> Dict[str, Any]:
        """Uploads a content file (e.g., .mcworld, .mcaddon) to the server.

        :param file_path: The local path to the file to upload.

        :returns: A dictionary containing the API response.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_upload_content()
        """
        import os

        import aiohttp

        _LOGGER.info("Uploading content file: %s", file_path)
        data = aiohttp.FormData()
        data.add_field(
            "file",
            open(file_path, "rb"),
            filename=os.path.basename(file_path),
            content_type="application/octet-stream",
        )

        # Note: aiohttp requires direct session usage for multipart/form-data
        # We bypass the generic _request helper here.
        url = f"{self._server_root_url}/api/content/upload"
        headers = {}
        if self._jwt_token:
            headers["Authorization"] = f"Bearer {self._jwt_token}"

        async with self._session.post(url, data=data, headers=headers) as response:
            if response.status == 401 and not self._is_retrying:
                _LOGGER.info("Token expired, attempting to refresh and retry.")
                self._is_retrying = True
                await self._authenticate()
                # Clear the flag before retrying
                self._is_retrying = False
                return await self.async_upload_content(file_path)

            await self._handle_api_error(response, "/api/content/upload")
            result = await response.json()
            return dict(result)

    async def async_reset_server_world(self, server_name: str) -> ActionResponse:
        """Resets the current world of a server.

        :param server_name: The name of the server whose world to reset.

        :returns: An `ActionResponse` object confirming the reset action.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_reset_server_world('MyServer')
        """
        _LOGGER.warning("Triggering world reset for server '%s'", server_name)
        response = await self._request(
            "DELETE",
            f"/server/{server_name}/world/reset",
            json_data=None,
            authenticated=True,
        )
        return cast(ActionResponse, ActionResponse.model_validate(response))

    async def async_prune_server_backups(self, server_name: str) -> ActionResponse:
        """Prunes old backups for a server based on its retention policies.

        :param server_name: The name of the server whose backups to prune.

        :returns: An `ActionResponse` object confirming the prune action.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_prune_server_backups('MyServer')
        """
        _LOGGER.info(
            "Triggering backup pruning for server '%s' (using server-defined retention)",
            server_name,
        )
        response = await self._request(
            "POST",
            f"/server/{server_name}/backups/prune",
            json_data=None,
            authenticated=True,
        )
        return cast(ActionResponse, ActionResponse.model_validate(response))

    async def async_restore_server_backup(
        self, server_name: str, payload: RestoreActionPayload
    ) -> ActionResponse:
        """Restores a server's world or configuration from a backup.

        :param server_name: The name of the server.
        :param payload: A `RestoreActionPayload` object specifying the restore details.

        :returns: An `ActionResponse` object confirming the restore action.


        .. rubric:: Example:
        .. code-block:: python

            payload = ...
            response = await client.async_restore_server_backup(payload)
        """
        _LOGGER.info(
            "Requesting restore for server '%s', type: %s, file: '%s'",
            server_name,
            payload.restore_type,
            payload.backup_file,
        )

        response = await self._request(
            "POST",
            f"/server/{server_name}/restore/action",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return cast(ActionResponse, ActionResponse.model_validate(response))

    async def async_restore_server_latest_all(self, server_name: str) -> ActionResponse:
        """Restores a server from the latest 'all' backup.

        This restores the server's world and standard configuration files from
        their most recent backups.

        :param server_name: The name of the server to restore.

        :returns: An `ActionResponse` object confirming the restore action.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_restore_server_latest_all('MyServer')
        """
        _LOGGER.info(
            "Requesting restore of latest 'all' backup for server '%s'", server_name
        )
        payload = {"restore_type": "all"}
        response = await self._request(
            "POST",
            f"/server/{server_name}/restore/action",  # Path targets the generic restore action endpoint
            json_data=payload,
            authenticated=True,
        )
        return cast(ActionResponse, ActionResponse.model_validate(response))

    async def async_install_server_world(
        self, server_name: str, payload: FileNamePayload
    ) -> ActionResponse:
        """Installs a world to a server from a .mcworld file.

        :param server_name: The name of the server.
        :param payload: A `FileNamePayload` object with the name of the .mcworld file.

        :returns: An `ActionResponse` object confirming the installation.


        .. rubric:: Example:
        .. code-block:: python

            payload = ...
            response = await client.async_install_server_world(payload)
        """
        _LOGGER.info(
            "Requesting world install for server '%s' from file '%s'",
            server_name,
            payload.filename,
        )

        response = await self._request(
            "POST",
            f"/server/{server_name}/world/install",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return cast(ActionResponse, ActionResponse.model_validate(response))

    async def async_install_server_addon(
        self, server_name: str, payload: FileNamePayload
    ) -> ActionResponse:
        """Installs an addon to a server from a .mcaddon or .mcpack file.

        :param server_name: The name of the server.
        :param payload: A `FileNamePayload` object with the name of the addon file.

        :returns: An `ActionResponse` object confirming the installation.


        .. rubric:: Example:
        .. code-block:: python

            payload = ...
            response = await client.async_install_server_addon(payload)
        """
        _LOGGER.info(
            "Requesting addon install for server '%s' from file '%s'",
            server_name,
            payload.filename,
        )

        response = await self._request(
            "POST",
            f"/server/{server_name}/addon/install",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return cast(ActionResponse, ActionResponse.model_validate(response))
