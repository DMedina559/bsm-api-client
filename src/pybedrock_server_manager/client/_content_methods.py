# src/pybedrock_server_manager/client/_content_methods.py
"""Mixin class containing content management methods (backups, worlds, addons)."""
import logging
from typing import Any, Dict, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client_base import ClientBase

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.content")

# Define allowed types for validation to avoid magic strings
ALLOWED_BACKUP_LIST_TYPES = ["world", "config"]
ALLOWED_BACKUP_ACTION_TYPES = ["world", "config", "all"]
ALLOWED_RESTORE_TYPES = ["world", "config"]


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
    ) -> Dict[str, Any]:
        """
        Lists backup filenames for a specific server and backup type.

        Corresponds to `GET /api/server/{server_name}/backups/list/{backup_type}`.
        Requires authentication.

        Args:
            server_name: The name of the server.
            backup_type: The type of backups to list (e.g., "world", "config").
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

        return await self._request(
            "GET",
            f"/server/{server_name}/backups/list/{bt_lower}",
            authenticated=True,
        )

    async def async_get_content_worlds(self) -> Dict[str, Any]:
        """
        Lists available world template files (.mcworld) from the manager's content directory.

        Corresponds to `GET /api/content/worlds`.
        Requires authentication.
        """
        _LOGGER.debug("Fetching available world files from /content/worlds")
        return await self._request("GET", "/content/worlds", authenticated=True)

    async def async_get_content_addons(self) -> Dict[str, Any]:
        """
        Lists available addon files (.mcpack, .mcaddon) from the manager's content directory.

        Corresponds to `GET /api/content/addons`.
        Requires authentication.
        """
        _LOGGER.debug("Fetching available addon files from /content/addons")
        return await self._request("GET", "/content/addons", authenticated=True)

    async def async_trigger_server_backup(
        self,
        server_name: str,
        backup_type: str = "all",
        file_to_backup: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Triggers a backup operation for a specific server.

        Corresponds to `POST /api/server/{server_name}/backup/action`.
        Requires authentication.

        Args:
            server_name: The name of the server to back up.
            backup_type: Type of backup ("world", "config", "all"). Defaults to "all".
            file_to_backup: Required if backup_type is "config". Specifies the config file.
        """
        bt_lower = backup_type.lower()
        if bt_lower not in ALLOWED_BACKUP_ACTION_TYPES:
            _LOGGER.error(
                "Invalid backup_type '%s' for triggering backup. Allowed: %s",
                backup_type,
                ALLOWED_BACKUP_ACTION_TYPES,
            )
            raise ValueError(
                f"Invalid backup_type '{backup_type}' provided. Allowed types are: {', '.join(ALLOWED_BACKUP_ACTION_TYPES)}"
            )

        _LOGGER.info(
            "Triggering backup for server '%s', type: %s, file: %s",
            server_name,
            bt_lower,
            file_to_backup or "N/A",
        )
        payload: Dict[str, str] = {"backup_type": bt_lower}
        if bt_lower == "config":
            if not file_to_backup:
                raise ValueError(
                    "file_to_backup is required when backup_type is 'config'"
                )
            payload["file_to_backup"] = file_to_backup
        elif file_to_backup:
            _LOGGER.warning(
                "file_to_backup ('%s') provided but will be ignored for backup_type '%s'",
                file_to_backup,
                bt_lower,
            )

        return await self._request(
            "POST",
            f"/server/{server_name}/backup/action",
            json_data=payload,
            authenticated=True,
        )

    async def async_export_server_world(self, server_name: str) -> Dict[str, Any]:
        """
        Exports the current world of a server to a .mcworld file in the content directory.

        Corresponds to `POST /api/server/{server_name}/world/export`.
        Requires authentication.

        Args:
            server_name: The name of the server whose world to export.
        """
        _LOGGER.info("Triggering world export for server '%s'", server_name)
        return await self._request(
            "POST",
            f"/server/{server_name}/world/export",
            json_data=None,
            authenticated=True,
        )

    async def async_prune_server_backups(
        self, server_name: str, keep: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Prunes older backups for a specific server.

        Corresponds to `POST /api/server/{server_name}/backups/prune`.
        Requires authentication.

        Args:
            server_name: The name of the server whose backups to prune.
            keep: The number of recent backups of each type to retain.
                  If None, uses the manager's default setting.
        """
        _LOGGER.info(
            "Triggering backup pruning for server '%s', keep: %s",
            server_name,
            keep if keep is not None else "manager default",
        )
        payload: Optional[Dict[str, Any]] = None
        if keep is not None:
            if not isinstance(keep, int) or keep < 0:
                raise ValueError("keep must be a non-negative integer if provided.")
            payload = {"keep": keep}

        return await self._request(
            "POST",
            f"/server/{server_name}/backups/prune",
            json_data=payload,
            authenticated=True,
        )

    async def async_restore_server_backup(
        self, server_name: str, restore_type: str, backup_file: str
    ) -> Dict[str, Any]:
        """
        Restores a server's world or a specific configuration file from a backup.

        Corresponds to `POST /api/server/{server_name}/restore/action`.
        Requires authentication.

        Args:
            server_name: The name of the server.
            restore_type: Type of restore ("world" or "config").
            backup_file: The filename of the backup to restore (relative to server's backup dir).
        """
        rt_lower = restore_type.lower()
        if rt_lower not in ALLOWED_RESTORE_TYPES:
            _LOGGER.error(
                "Invalid restore_type '%s'. Allowed: %s",
                restore_type,
                ALLOWED_RESTORE_TYPES,
            )
            raise ValueError(
                f"Invalid restore_type '{restore_type}' provided. Allowed types are: {', '.join(ALLOWED_RESTORE_TYPES)}"
            )

        _LOGGER.info(
            "Requesting restore for server '%s', type: %s, file: '%s'",
            server_name,
            rt_lower,
            backup_file,
        )
        payload = {"restore_type": rt_lower, "backup_file": backup_file}

        return await self._request(
            "POST",
            f"/server/{server_name}/restore/action",
            json_data=payload,
            authenticated=True,
        )

    async def async_restore_server_latest_all(self, server_name: str) -> Dict[str, Any]:
        """
        Restores the server's world AND standard configuration files from their latest backups.

        Corresponds to `POST /api/server/{server_name}/restore/all`.
        Requires authentication.

        Args:
            server_name: The name of the server to restore.
        """
        _LOGGER.info(
            "Requesting restore of latest 'all' backup for server '%s'", server_name
        )
        return await self._request(
            "POST",
            f"/server/{server_name}/restore/all",
            json_data=None,
            authenticated=True,
        )

    async def async_install_server_world(
        self, server_name: str, filename: str
    ) -> Dict[str, Any]:
        """
        Installs a world from a .mcworld file (from content directory) to a server.

        Corresponds to `POST /api/server/{server_name}/world/install`.
        Requires authentication.

        Args:
            server_name: The name of the server.
            filename: The name of the .mcworld file (relative to content/worlds dir).
        """
        _LOGGER.info(
            "Requesting world install for server '%s' from file '%s'",
            server_name,
            filename,
        )
        payload = {"filename": filename}

        return await self._request(
            "POST",
            f"/server/{server_name}/world/install",
            json_data=payload,
            authenticated=True,
        )

    async def async_install_server_addon(
        self, server_name: str, filename: str
    ) -> Dict[str, Any]:
        """
        Installs an addon (.mcaddon or .mcpack file from content directory) to a server.

        Corresponds to `POST /api/server/{server_name}/addon/install`.
        Requires authentication.

        Args:
            server_name: The name of the server.
            filename: The name of the addon file (relative to content/addons dir).
        """
        _LOGGER.info(
            "Requesting addon install for server '%s' from file '%s'",
            server_name,
            filename,
        )
        payload = {"filename": filename}

        return await self._request(
            "POST",
            f"/server/{server_name}/addon/install",
            json_data=payload,
            authenticated=True,
        )
