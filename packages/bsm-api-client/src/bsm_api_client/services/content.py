import logging
from typing import Any, Dict, cast

from ..dynamic import DynamicOpenAPIMixin
from ..models import (
    AddonActionPayload,
    AddonListResponse,
    AddonReorderPayload,
    AddonSubpackPayload,
    BackupActionPayload,
    BackupFilesResponse,
    ContentListResponse,
    FileNamePayload,
    ListAvailableAddonsResponse,
    RestoreActionPayload,
    TaskAcceptedResponse,
)
from ..validation import parse_response
from .base import Service

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.content")
ALLOWED_BACKUP_LIST_TYPES = ["world", "properties", "allowlist", "permissions"]


class ContentService(Service):
    """Service for content management endpoints (backups, worlds, addons)."""

    async def async_list_server_backups(
        self, server_name: str, backup_type: str
    ) -> BackupFilesResponse:
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
        response = await self.async_call_generated(
            "list_server_backups",
            parameters={"server_name": server_name, "backup_type": bt_lower},
            authenticated=True,
        )
        return cast(BackupFilesResponse, parse_response(BackupFilesResponse, response))

    async def async_get_server_addons(self, server_name: str) -> AddonListResponse:
        """Retrieves a list of addons installed on a server's active world.

        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_get_server_addons('MyServer')
        """
        _LOGGER.debug("Fetching addons for server '%s'", server_name)
        response = await self.async_call_generated(
            "list_server_addons",
            parameters={"server_name": server_name},
            authenticated=True,
        )
        return cast(AddonListResponse, parse_response(AddonListResponse, response))

    async def async_enable_server_addon(
        self, server_name: str, payload: AddonActionPayload
    ) -> TaskAcceptedResponse:
        """Enables an addon on a server.

        .. rubric:: Example:
        .. code-block:: python

            payload = ...
            response = await client.async_enable_server_addon(payload)
        """
        _LOGGER.info(
            "Enabling addon '%s' for server '%s'", payload.pack_uuid, server_name
        )
        response = await self.async_call_generated(
            "enable_addon",
            parameters={"server_name": server_name},
            body=payload.model_dump(),
            authenticated=True,
        )
        return cast(
            TaskAcceptedResponse, parse_response(TaskAcceptedResponse, response)
        )

    async def async_disable_server_addon(
        self, server_name: str, payload: AddonActionPayload
    ) -> TaskAcceptedResponse:
        """Disables an addon on a server.

        .. rubric:: Example:
        .. code-block:: python

            payload = ...
            response = await client.async_disable_server_addon(payload)
        """
        _LOGGER.info(
            "Disabling addon '%s' for server '%s'", payload.pack_uuid, server_name
        )
        response = await self.async_call_generated(
            "disable_addon",
            parameters={"server_name": server_name},
            body=payload.model_dump(),
            authenticated=True,
        )
        return cast(
            TaskAcceptedResponse, parse_response(TaskAcceptedResponse, response)
        )

    async def async_update_server_addon_subpack(
        self, server_name: str, payload: AddonSubpackPayload
    ) -> TaskAcceptedResponse:
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
        response = await self.async_call_generated(
            "update_addon_subpack",
            parameters={"server_name": server_name},
            body=payload.model_dump(),
            authenticated=True,
        )
        return cast(
            TaskAcceptedResponse, parse_response(TaskAcceptedResponse, response)
        )

    async def async_uninstall_server_addon(
        self, server_name: str, payload: AddonActionPayload
    ) -> TaskAcceptedResponse:
        """Uninstalls an addon on a server.

        .. rubric:: Example:
        .. code-block:: python

            payload = ...
            response = await client.async_uninstall_server_addon(payload)
        """
        _LOGGER.info(
            "Uninstalling addon '%s' for server '%s'", payload.pack_uuid, server_name
        )
        response = await self.async_call_generated(
            "uninstall_addon",
            parameters={"server_name": server_name},
            body=payload.model_dump(),
            authenticated=True,
        )
        return cast(
            TaskAcceptedResponse, parse_response(TaskAcceptedResponse, response)
        )

    async def async_reorder_server_addon(
        self, server_name: str, payload: AddonReorderPayload
    ) -> TaskAcceptedResponse:
        """Reorders active addons on a server.

        .. rubric:: Example:
        .. code-block:: python

            payload = ...
            response = await client.async_reorder_server_addon(payload)
        """
        _LOGGER.info(
            "Reordering %s packs for server '%s'", payload.pack_type, server_name
        )
        response = await self.async_call_generated(
            "reorder_addons",
            parameters={"server_name": server_name},
            body=payload.model_dump(),
            authenticated=True,
        )
        return cast(
            TaskAcceptedResponse, parse_response(TaskAcceptedResponse, response)
        )

    async def async_get_content_worlds(self) -> ContentListResponse:
        """Lists available world template files (.mcworld).

        :returns: A `ContentListResponse` object containing the list of world files.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_get_content_worlds()
        """
        _LOGGER.debug("Fetching available world files from /content/worlds")
        response = await self.async_call_generated(
            "list_available_worlds", authenticated=True
        )
        return cast(ContentListResponse, parse_response(ContentListResponse, response))

    async def async_get_content_addons(self) -> ListAvailableAddonsResponse:
        """Lists available addon files (.mcpack, .mcaddon).

        :returns: A `ContentListResponse` object containing the list of addon files.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_get_content_addons()
        """
        _LOGGER.debug("Fetching available addon files from /content/addons")
        response = await self.async_call_generated(
            "list_available_addons", authenticated=True
        )
        return cast(
            ListAvailableAddonsResponse,
            parse_response(ListAvailableAddonsResponse, response),
        )

    async def async_trigger_server_backup(
        self, server_name: str, payload: BackupActionPayload
    ) -> TaskAcceptedResponse:
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
        response = await self.async_call_generated(
            "create_backup",
            parameters={"server_name": server_name},
            body=payload.model_dump(),
            authenticated=True,
        )
        return cast(
            TaskAcceptedResponse, parse_response(TaskAcceptedResponse, response)
        )

    async def async_export_server_world(self, server_name: str) -> TaskAcceptedResponse:
        """Exports the current world of a server to a .mcworld file.

        :param server_name: The name of the server whose world to export.

        :returns: An `ActionResponse` object confirming the export action.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_export_server_world('MyServer')
        """
        _LOGGER.info("Triggering world export for server '%s'", server_name)
        response = await self.async_call_generated(
            "export_world",
            parameters={"server_name": server_name},
            body=None,
            authenticated=True,
        )
        return cast(
            TaskAcceptedResponse, parse_response(TaskAcceptedResponse, response)
        )

    async def async_upload_content(self, file_path: str) -> Dict[str, Any]:
        """Uploads a content file (e.g., .mcworld, .mcaddon) to the server.

        :param file_path: The local path to the file to upload.

        :returns: A dictionary containing the API response.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_upload_content()
        """
        from pathlib import Path

        from ..exceptions import NotFoundError

        dynamic = cast("DynamicOpenAPIMixin", self._owner)
        await dynamic.async_discover_api()
        if "upload_content" not in dynamic.operations:
            raise NotFoundError(
                "This server does not advertise an upload_content operation in OpenAPI."
            )
        path = Path(file_path)
        with path.open("rb") as handle:
            response = await dynamic.async_call_operation(
                "upload_content",
                files={"file": (path.name, handle.read(), "application/octet-stream")},
            )
        return cast(Dict[str, Any], response)

    async def async_reset_server_world(self, server_name: str) -> TaskAcceptedResponse:
        """Resets the current world of a server.

        :param server_name: The name of the server whose world to reset.

        :returns: An `ActionResponse` object confirming the reset action.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_reset_server_world('MyServer')
        """
        _LOGGER.warning("Triggering world reset for server '%s'", server_name)
        response = await self.async_call_generated(
            "reset_world",
            parameters={"server_name": server_name},
            body=None,
            authenticated=True,
        )
        return cast(
            TaskAcceptedResponse, parse_response(TaskAcceptedResponse, response)
        )

    async def async_prune_server_backups(
        self, server_name: str
    ) -> TaskAcceptedResponse:
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
        response = await self.async_call_generated(
            "prune_backups",
            parameters={"server_name": server_name},
            body=None,
            authenticated=True,
        )
        return cast(
            TaskAcceptedResponse, parse_response(TaskAcceptedResponse, response)
        )

    async def async_restore_server_backup(
        self, server_name: str, payload: RestoreActionPayload
    ) -> TaskAcceptedResponse:
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
        response = await self.async_call_generated(
            "restore_backup",
            parameters={"server_name": server_name},
            body=payload.model_dump(),
            authenticated=True,
        )
        return cast(
            TaskAcceptedResponse, parse_response(TaskAcceptedResponse, response)
        )

    async def async_restore_server_latest_all(
        self, server_name: str
    ) -> TaskAcceptedResponse:
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
        response = await self.async_call_generated(
            "restore_backup",
            parameters={"server_name": server_name},
            body=payload,
            authenticated=True,
        )
        return cast(
            TaskAcceptedResponse, parse_response(TaskAcceptedResponse, response)
        )

    async def async_install_server_world(
        self, server_name: str, payload: FileNamePayload
    ) -> TaskAcceptedResponse:
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
        response = await self.async_call_generated(
            "install_world",
            parameters={"server_name": server_name},
            body=payload.model_dump(),
            authenticated=True,
        )
        return cast(
            TaskAcceptedResponse, parse_response(TaskAcceptedResponse, response)
        )

    async def async_install_server_addon(
        self, server_name: str, payload: FileNamePayload
    ) -> TaskAcceptedResponse:
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
        response = await self.async_call_generated(
            "install_addon",
            parameters={"server_name": server_name},
            body=payload.model_dump(),
            authenticated=True,
        )
        return cast(
            TaskAcceptedResponse, parse_response(TaskAcceptedResponse, response)
        )
