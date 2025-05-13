# src/pybedrock_server_manager/client/_content_methods.py
"""Mixin class containing content management methods (backups, worlds, addons)."""
import logging
from typing import Any, Dict, Optional, List

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.content")


class ContentMethodsMixin:
    """Mixin for content management endpoints."""

    async def async_list_server_backups(
        self, server_name: str, backup_type: str
    ) -> Dict[str, Any]:
        """Lists backup filenames for a server and type. Calls GET /api/server/{server_name}/backups/list/{backup_type}."""
        if backup_type not in ["world", "config", "all"]:
            _LOGGER.error("Invalid backup_type '%s' for listing backups.", backup_type)
            raise ValueError(f"Invalid backup_type '{backup_type}' provided.")
        _LOGGER.debug(
            "Fetching '%s' backups list for server '%s'", backup_type, server_name
        )
        return await self._request(
            "GET",
            f"{self._base_path}/server/{server_name}/backups/list/{backup_type}",
            authenticated=True,
        )

    async def async_get_content_worlds(self) -> Dict[str, Any]:
        """Lists available .mcworld files. Calls GET /api/content/worlds."""
        _LOGGER.debug("Fetching available world files from /api/content/worlds")
        return await self._request(
            "GET", f"{self._base_path}/content/worlds", authenticated=True
        )

    async def async_get_content_addons(self) -> Dict[str, Any]:
        """Lists available .mcpack/.mcaddon files. Calls GET /api/content/addons."""
        _LOGGER.debug("Fetching available addon files from /api/content/addons")
        return await self._request(
            "GET", f"{self._base_path}/content/addons", authenticated=True
        )

    async def async_trigger_server_backup(
        self,
        server_name: str,
        backup_type: str = "all",
        file_to_backup: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Triggers a backup operation. Calls POST /api/server/{server_name}/backup/action."""
        _LOGGER.info(
            "Triggering backup for server '%s', type: %s, file: %s",
            server_name,
            backup_type,
            file_to_backup or "N/A",
        )
        payload: Dict[str, str] = {"backup_type": backup_type}
        if backup_type.lower() == "config":
            if not file_to_backup:
                raise ValueError(
                    "file_to_backup is required when backup_type is 'config'"
                )
            payload["file_to_backup"] = file_to_backup
        elif file_to_backup:
            _LOGGER.warning(
                "file_to_backup ('%s') provided but ignored for backup_type '%s'",
                file_to_backup,
                backup_type,
            )
        return await self._request(
            "POST",
            f"{self._base_path}/server/{server_name}/backup/action",
            data=payload,
            authenticated=True,
        )

    async def async_export_server_world(self, server_name: str) -> Dict[str, Any]:
        """Triggers world export for a server. Calls POST /api/server/{server_name}/world/export."""
        _LOGGER.info("Triggering world export for server '%s'", server_name)
        return await self._request(
            "POST",
            f"{self._base_path}/server/{server_name}/world/export",
            data=None,
            authenticated=True,
        )

    async def async_prune_server_backups(
        self, server_name: str, keep: Optional[int] = None
    ) -> Dict[str, Any]:
        """Triggers backup pruning for a server. Calls POST /api/server/{server_name}/backups/prune."""
        _LOGGER.info(
            "Triggering backup pruning for server '%s', keep: %s",
            server_name,
            keep if keep is not None else "manager default",
        )
        payload: Optional[Dict[str, Any]] = None
        if keep is not None:
            payload = {"keep": keep}
        return await self._request(
            "POST",
            f"{self._base_path}/server/{server_name}/backups/prune",
            data=payload,
            authenticated=True,
        )

    async def async_restore_server_backup(
        self, server_name: str, restore_type: str, backup_file: str
    ) -> Dict[str, Any]:
        """Restores a specific backup file. Calls POST /api/server/{server_name}/restore/action."""
        _LOGGER.info(
            "Requesting restore for server '%s', type: %s, file: %s",
            server_name,
            restore_type,
            backup_file,
        )
        payload = {"restore_type": restore_type, "backup_file": backup_file}
        return await self._request(
            "POST",
            f"{self._base_path}/server/{server_name}/restore/action",
            data=payload,
            authenticated=True,
        )

    async def async_restore_server_latest_all(self, server_name: str) -> Dict[str, Any]:
        """Restores the latest 'all' backup. Calls POST /api/server/{server_name}/restore/all."""
        _LOGGER.info("Requesting restore latest all for server '%s'", server_name)
        return await self._request(
            "POST",
            f"{self._base_path}/server/{server_name}/restore/all",
            data=None,
            authenticated=True,
        )

    async def async_install_server_world(
        self, server_name: str, filename: str
    ) -> Dict[str, Any]:
        """Installs a world from a .mcworld file. Calls POST /api/server/{server_name}/world/install."""
        _LOGGER.info(
            "Requesting world install for server '%s' from file '%s'",
            server_name,
            filename,
        )
        payload = {"filename": filename}
        return await self._request(
            "POST",
            f"{self._base_path}/server/{server_name}/world/install",
            data=payload,
            authenticated=True,
        )

    async def async_install_server_addon(
        self, server_name: str, filename: str
    ) -> Dict[str, Any]:
        """Installs an addon (.mcaddon or .mcpack) file. Calls POST /api/server/{server_name}/addon/install."""
        _LOGGER.info(
            "Requesting addon install for server '%s' from file '%s'",
            server_name,
            filename,
        )
        payload = {"filename": filename}
        return await self._request(
            "POST",
            f"{self._base_path}/server/{server_name}/addon/install",
            data=payload,
            authenticated=True,
        )
