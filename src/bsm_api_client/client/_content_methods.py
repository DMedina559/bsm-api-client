# src/bsm_api_client/client/_content_methods.py
"""Mixin class for content management methods.

This module provides the `ContentMethodsMixin` class, which includes methods
for managing server content such as backups, worlds, and addons.
"""
import logging
from typing import Any, Dict, Optional, List, TYPE_CHECKING
from ..models import (
    RestoreTypePayload,
    BackupActionPayload,
    RestoreActionPayload,
    FileNamePayload,
    BackupRestoreResponse,
    ContentListResponse,
    ActionResponse,
)

if TYPE_CHECKING:
    from ..client_base import ClientBase

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.content")

# Define allowed types for validation to avoid magic strings
ALLOWED_BACKUP_LIST_TYPES = ["world", "properties", "allowlist", "permissions"]
ALLOWED_BACKUP_ACTION_TYPES = ["world", "config", "all"]
ALLOWED_RESTORE_TYPES = ["world", "properties", "allowlist", "permissions"]


class ContentMethodsMixin:
    """Mixin for content management endpoints (backups, worlds, addons)."""

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

    async def async_list_server_backups(
        self, server_name: str, backup_type: str
    ) -> BackupRestoreResponse:
        """Lists backup files for a specific server and backup type.

        Args:
            server_name: The name of the server.
            backup_type: The type of backups to list (e.g., "world", "properties").

        Returns:
            A `BackupRestoreResponse` object containing the list of backups.

        Raises:
            ValueError: If an invalid `backup_type` is provided.
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
        return BackupRestoreResponse.model_validate(response)

    async def async_restore_select_backup_type(
        self, server_name: str, payload: RestoreTypePayload
    ) -> BackupRestoreResponse:
        """Selects a restore type and gets a redirect URL for choosing a backup file.

        Args:
            server_name: The name of the server.
            payload: A `RestoreTypePayload` object specifying the restore type.

        Returns:
            A `BackupRestoreResponse` object, typically containing a redirect URL.
        """
        _LOGGER.info(
            "Selecting restore backup type '%s' for server '%s'",
            payload.restore_type,
            server_name,
        )
        response = await self._request(
            method="POST",
            path=f"/server/{server_name}/restore/select_backup_type",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return BackupRestoreResponse.model_validate(response)

    async def async_get_content_worlds(self) -> ContentListResponse:
        """Lists available world template files (.mcworld).

        Returns:
            A `ContentListResponse` object containing the list of world files.
        """
        _LOGGER.debug("Fetching available world files from /content/worlds")
        response = await self._request("GET", "/content/worlds", authenticated=True)
        return ContentListResponse.model_validate(response)

    async def async_get_content_addons(self) -> ContentListResponse:
        """Lists available addon files (.mcpack, .mcaddon).

        Returns:
            A `ContentListResponse` object containing the list of addon files.
        """
        _LOGGER.debug("Fetching available addon files from /content/addons")
        response = await self._request("GET", "/content/addons", authenticated=True)
        return ContentListResponse.model_validate(response)

    async def async_trigger_server_backup(
        self, server_name: str, payload: BackupActionPayload
    ) -> BackupRestoreResponse:
        """Triggers a backup operation for a specific server.

        Args:
            server_name: The name of the server to back up.
            payload: A `BackupActionPayload` object specifying the backup details.

        Returns:
            A `BackupRestoreResponse` object confirming the backup action.
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
        return BackupRestoreResponse.model_validate(response)

    async def async_export_server_world(self, server_name: str) -> ActionResponse:
        """Exports the current world of a server to a .mcworld file.

        Args:
            server_name: The name of the server whose world to export.

        Returns:
            An `ActionResponse` object confirming the export action.
        """
        _LOGGER.info("Triggering world export for server '%s'", server_name)
        response = await self._request(
            "POST",
            f"/server/{server_name}/world/export",
            json_data=None,
            authenticated=True,
        )
        return ActionResponse.model_validate(response)

    async def async_reset_server_world(self, server_name: str) -> ActionResponse:
        """Resets the current world of a server.

        Args:
            server_name: The name of the server whose world to reset.

        Returns:
            An `ActionResponse` object confirming the reset action.
        """
        _LOGGER.warning("Triggering world reset for server '%s'", server_name)
        response = await self._request(
            "DELETE",
            f"/server/{server_name}/world/reset",
            json_data=None,
            authenticated=True,
        )
        return ActionResponse.model_validate(response)

    async def async_prune_server_backups(
        self, server_name: str
    ) -> BackupRestoreResponse:
        """Prunes old backups for a server based on its retention policies.

        Args:
            server_name: The name of the server whose backups to prune.

        Returns:
            A `BackupRestoreResponse` object confirming the prune action.
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
        return BackupRestoreResponse.model_validate(response)

    async def async_restore_server_backup(
        self, server_name: str, payload: RestoreActionPayload
    ) -> BackupRestoreResponse:
        """Restores a server's world or configuration from a backup.

        Args:
            server_name: The name of the server.
            payload: A `RestoreActionPayload` object specifying the restore details.

        Returns:
            A `BackupRestoreResponse` object confirming the restore action.
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
        return BackupRestoreResponse.model_validate(response)

    async def async_restore_server_latest_all(
        self, server_name: str
    ) -> BackupRestoreResponse:
        """Restores a server from the latest 'all' backup.

        This restores the server's world and standard configuration files from
        their most recent backups.

        Args:
            server_name: The name of the server to restore.

        Returns:
            A `BackupRestoreResponse` object confirming the restore action.
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
        return BackupRestoreResponse.model_validate(response)

    async def async_install_server_world(
        self, server_name: str, payload: FileNamePayload
    ) -> ActionResponse:
        """Installs a world to a server from a .mcworld file.

        Args:
            server_name: The name of the server.
            payload: A `FileNamePayload` object with the name of the .mcworld file.

        Returns:
            An `ActionResponse` object confirming the installation.
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
        return ActionResponse.model_validate(response)

    async def async_install_server_addon(
        self, server_name: str, payload: FileNamePayload
    ) -> ActionResponse:
        """Installs an addon to a server from a .mcaddon or .mcpack file.

        Args:
            server_name: The name of the server.
            payload: A `FileNamePayload` object with the name of the addon file.

        Returns:
            An `ActionResponse` object confirming the installation.
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
        return ActionResponse.model_validate(response)
