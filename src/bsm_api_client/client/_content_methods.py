# src/bsm_api_client/client/_content_methods.py
"""Mixin class containing content management methods (backups, worlds, addons)."""
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
        ) -> Any:
            ...

    async def async_list_server_backups(
        self, server_name: str, backup_type: str
    ) -> BackupRestoreResponse:
        """
        Lists backup filenames for a specific server and backup type.

        Corresponds to `GET /api/server/{server_name}/backup/list/{backup_type}`.
        Requires authentication.

        Args:
            server_name: The name of the server.
            backup_type: The type of backups to list (e.g., "world", "properties", "allowlist", "permissions", "all").
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
        """
        Handles the API request for selecting a restore type and provides a redirect URL
        to the page where specific backup files of that type can be chosen.

        Corresponds to `POST /api/server/{server_name}/restore/select_backup_type`.
        Requires authentication.
        Request body model: RestoreTypePayload
        Expected response model: BackupRestoreResponse

        Args:
            server_name: The name of the server.
            payload: A RestoreTypePayload object.
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
        """
        Lists available world template files (.mcworld) from the manager's content directory.

        Corresponds to `GET /api/content/worlds`.
        Requires authentication.
        """
        _LOGGER.debug("Fetching available world files from /content/worlds")
        response = await self._request("GET", "/content/worlds", authenticated=True)
        return ContentListResponse.model_validate(response)

    async def async_get_content_addons(self) -> ContentListResponse:
        """
        Lists available addon files (.mcpack, .mcaddon) from the manager's content directory.

        Corresponds to `GET /api/content/addons`.
        Requires authentication.
        """
        _LOGGER.debug("Fetching available addon files from /content/addons")
        response = await self._request("GET", "/content/addons", authenticated=True)
        return ContentListResponse.model_validate(response)

    async def async_trigger_server_backup(
        self, server_name: str, payload: BackupActionPayload
    ) -> BackupRestoreResponse:
        """
        Triggers a backup operation for a specific server.

        Corresponds to `POST /api/server/{server_name}/backup/action`.
        Requires authentication.

        Args:
            server_name: The name of the server to back up.
            payload: A BackupActionPayload object.
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
        """
        Exports the current world of a server to a .mcworld file in the content directory.

        Corresponds to `POST /api/server/{server_name}/world/export`.
        Requires authentication.

        Args:
            server_name: The name of the server whose world to export.
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
        """
        Resets the current world of a server.

        Corresponds to `DELETE /api/server/{server_name}/world/reset`.
        Requires authentication.

        Args:
            server_name: The name of the server whose world to export.
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
        """
        Prunes older backups for a specific server based on server-defined retention policies.
        The new FastAPI endpoint (`POST /api/server/{server_name}/backups/prune`)
        does not accept a request body; retention is solely managed by server-side settings.

        Corresponds to `POST /api/server/{server_name}/backups/prune`.
        Requires authentication.

        Args:
            server_name: The name of the server whose backups to prune.
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
        """
        Restores a server's world or a specific configuration file from a backup.

        Corresponds to `POST /api/server/{server_name}/restore/action`.
        Requires authentication.

        Args:
            server_name: The name of the server.
            payload: A RestoreActionPayload object.
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
        """
        Restores the server's world AND standard configuration files from their latest backups.
        NOTE: This method's behavior was updated for the new API. It now calls the
        generic restore action endpoint (`POST /api/server/{server_name}/restore/action`)
        with a payload of `{"restore_type": "all"}`. The dedicated `/restore/all`
        endpoint from the old API is no longer used.

        Corresponds to `POST /api/server/{server_name}/restore/action` with `{"restore_type": "all"}`.
        Requires authentication.

        Args:
            server_name: The name of the server to restore.
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
        """
        Installs a world from a .mcworld file (from content directory) to a server.

        Corresponds to `POST /api/server/{server_name}/world/install`.
        Requires authentication.

        Args:
            server_name: The name of the server.
            payload: A FileNamePayload object.
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
        """
        Installs an addon (.mcaddon or .mcpack file from content directory) to a server.

        Corresponds to `POST /api/server/{server_name}/addon/install`.
        Requires authentication.

        Args:
            server_name: The name of the server.
            payload: A FileNamePayload object.
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
