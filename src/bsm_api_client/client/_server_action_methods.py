# src/bsm_api_client/client/_server_action_methods.py
"""Mixin class containing server action and backup/restore methods."""
import logging
from typing import Any, Dict, Optional, List, TYPE_CHECKING, Union
from urllib.parse import quote

if TYPE_CHECKING:
    from ..client_base import ClientBase
    from ..exceptions import APIError, InvalidInputError

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.server_actions")


class ServerActionMethodsMixin:
    """Mixin for server action and backup/restore endpoints."""

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

    async def async_start_server(self, server_name: str) -> Dict[str, Any]:
        """
        Starts the specified Bedrock server instance.

        Corresponds to `POST /api/server/{server_name}/start`.
        Requires authentication.

        Args:
            server_name: The unique name of the server instance to start.
        Returns:
            API response dictionary.
        """
        _LOGGER.info("Requesting start for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        return await self._request(
            "POST",
            f"/server/{encoded_server_name}/start",
            authenticated=True,
        )

    async def async_stop_server(self, server_name: str) -> Dict[str, Any]:
        """
        Stops the specified running Bedrock server instance.

        Corresponds to `POST /api/server/{server_name}/stop`.
        Requires authentication.

        Args:
            server_name: The unique name of the server instance to stop.
        Returns:
            API response dictionary.
        """
        _LOGGER.info("Requesting stop for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        return await self._request(
            "POST",
            f"/server/{encoded_server_name}/stop",
            authenticated=True,
        )

    async def async_restart_server(self, server_name: str) -> Dict[str, Any]:
        """
        Restarts the specified Bedrock server instance.

        Corresponds to `POST /api/server/{server_name}/restart`.
        Requires authentication.

        Args:
            server_name: The unique name of the server instance to restart.
        Returns:
            API response dictionary.
        """
        _LOGGER.info("Requesting restart for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        return await self._request(
            "POST",
            f"/server/{encoded_server_name}/restart",
            authenticated=True,
        )

    async def async_send_server_command(
        self, server_name: str, command: str
    ) -> Dict[str, Any]:
        """
        Sends a command string to the specified server's console.

        Corresponds to `POST /api/server/{server_name}/send_command`.
        Requires authentication.

        Args:
            server_name: The unique name of the target server instance.
            command: The command string to send.
        Returns:
            API response dictionary.
        """
        if not command or command.isspace():
            # Consider using InvalidInputError from .exceptions
            from ..exceptions import InvalidInputError  # Local import for clarity

            raise InvalidInputError("Command cannot be empty or just whitespace.")
        _LOGGER.info("Sending command to server '%s': '%s'", server_name, command)
        payload = {"command": command}
        encoded_server_name = quote(server_name)
        return await self._request(
            "POST",
            f"/server/{encoded_server_name}/send_command",
            json_data=payload,
            authenticated=True,
        )

    async def async_update_server(self, server_name: str) -> Dict[str, Any]:
        """
        Checks for and applies updates to the specified server instance.
        The response indicates if an update was performed and the new version.
        E.g., {"status": "success", "updated": true, "new_version": "1.20.81.01", "message": "..."}

        Corresponds to `POST /api/server/{server_name}/update`.
        Requires authentication.

        Args:
            server_name: The unique name of the server instance to update.
        Returns:
            API response dictionary, including 'updated' (bool) and 'new_version' (str).
        """
        _LOGGER.info("Requesting update for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        return await self._request(
            "POST",
            f"/server/{encoded_server_name}/update",
            authenticated=True,
        )

    async def async_delete_server(self, server_name: str) -> Dict[str, Any]:
        """
        Permanently deletes all data associated with the specified server instance.
        **USE WITH EXTREME CAUTION: This action is irreversible.**

        Corresponds to `DELETE /api/server/{server_name}/delete`.
        Requires authentication.

        Args:
            server_name: The unique name of the server instance to delete.
        Returns:
            API response dictionary.
        """
        _LOGGER.warning(
            "Requesting DELETION of server '%s'. THIS IS IRREVERSIBLE.", server_name
        )
        encoded_server_name = quote(server_name)
        return await self._request(
            "DELETE",
            f"/server/{encoded_server_name}/delete",
            authenticated=True,
        )

    # --- Backup & Restore Methods ---

    async def async_prune_server_backups(
        self, server_name: str, keep: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Prunes older backups for a specific server.

        Corresponds to `POST /api/server/{server_name}/backups/prune`.
        Requires authentication.

        Args:
            server_name: The server whose backups to prune.
            keep: Optional. Number of recent backups of each type to retain.
                  If None, API uses server-side default.
        Returns:
            API response dictionary.
        """
        _LOGGER.info(
            "Requesting backup pruning for server '%s', keep: %s", server_name, keep
        )
        payload: Dict[str, Any] = {}
        if keep is not None:
            if not isinstance(keep, int) or keep < 0:
                from ..exceptions import InvalidInputError

                raise InvalidInputError("Keep must be a non-negative integer.")
            payload["keep"] = keep

        encoded_server_name = quote(server_name)
        return await self._request(
            "POST",
            f"/server/{encoded_server_name}/backups/prune",
            json_data=payload if payload else None,  # Send empty body if keep is None
            authenticated=True,
        )

    async def async_list_server_backups(
        self, server_name: str, backup_type: str
    ) -> List[str]:
        """
        Lists available backup filenames for a server and backup type.

        Corresponds to `GET /api/server/{server_name}/backups/list/{backup_type}`.
        Requires authentication.

        Args:
            server_name: The server for which to list backups.
            backup_type: Type of backups ("world" or "config").

        Returns:
            A list of backup filenames (basenames).

        Raises:
            InvalidInputError: if backup_type is invalid.
            APIError: For other API communication or processing errors.
        """
        if backup_type not in ["world", "config"]:
            from ..exceptions import InvalidInputError

            raise InvalidInputError("backup_type must be 'world' or 'config'.")
        _LOGGER.debug("Listing '%s' backups for server '%s'", backup_type, server_name)

        encoded_server_name = quote(server_name)
        encoded_backup_type = quote(backup_type)

        try:
            response_data = await self._request(
                "GET",
                f"/server/{encoded_server_name}/backups/list/{encoded_backup_type}",
                authenticated=True,
            )
            if (
                isinstance(response_data, dict)
                and response_data.get("status") == "success"
                and isinstance(response_data.get("backups"), list)
            ):
                # Ensure all items in backups list are strings
                return [str(b) for b in response_data["backups"] if isinstance(b, str)]

            _LOGGER.error(
                "Received non-success or unexpected structure for backup list: %s",
                response_data,
            )
            from ..exceptions import APIError  # Local import

            raise APIError(  # type: ignore
                f"Failed to list backups, API response: {response_data.get('status') if isinstance(response_data, dict) else 'N/A'}",
                response_data=(
                    response_data
                    if isinstance(response_data, dict)
                    else {"raw": response_data}
                ),
            )
        except APIError as e:
            _LOGGER.error(
                "API error listing backups for '%s' (type %s): %s",
                server_name,
                backup_type,
                e,
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error processing backup list for '%s': %s", server_name, e
            )
            from ..exceptions import APIError  # Local import

            raise APIError(f"Unexpected error processing backup list for '{server_name}': {e}")  # type: ignore

    async def async_trigger_server_backup(
        self,
        server_name: str,
        backup_type: str,
        file_to_backup: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Triggers a backup operation for the specified server.

        Corresponds to `POST /api/server/{server_name}/backup/action`.
        Requires authentication.

        Args:
            server_name: The server to back up.
            backup_type: Type of backup ("world", "config", "all").
            file_to_backup: Required if backup_type is "config". Relative path of the config file.

        Returns:
            API response dictionary.
        """
        _LOGGER.info("Triggering '%s' backup for server '%s'", backup_type, server_name)
        if backup_type not in ["world", "config", "all"]:
            from ..exceptions import InvalidInputError

            raise InvalidInputError("backup_type must be 'world', 'config', or 'all'.")

        payload: Dict[str, Any] = {"backup_type": backup_type}
        if backup_type == "config":
            if not file_to_backup or not isinstance(file_to_backup, str):
                from ..exceptions import InvalidInputError

                raise InvalidInputError(
                    "'file_to_backup' is required for 'config' backup type."
                )
            payload["file_to_backup"] = file_to_backup
            _LOGGER.info("Config file to backup: %s", file_to_backup)

        encoded_server_name = quote(server_name)
        return await self._request(
            "POST",
            f"/server/{encoded_server_name}/backup/action",
            json_data=payload,
            authenticated=True,
        )

    async def async_trigger_server_restore(
        self,
        server_name: str,
        restore_type: str,
        backup_file: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Triggers a restore operation for the specified server.

        Corresponds to `POST /api/server/{server_name}/restore/action`.
        Requires authentication.

        Args:
            server_name: The server to restore to.
            restore_type: Type of restore ("world", "config", "all").
            backup_file: Required if restore_type is "world" or "config".
                         The relative path to the backup file.

        Returns:
            API response dictionary.
        """
        _LOGGER.info(
            "Triggering '%s' restore for server '%s'", restore_type, server_name
        )
        if restore_type not in ["world", "config", "all"]:
            from ..exceptions import InvalidInputError

            raise InvalidInputError("restore_type must be 'world', 'config', or 'all'.")

        payload: Dict[str, Any] = {"restore_type": restore_type}
        if restore_type in ["world", "config"]:
            if not backup_file or not isinstance(backup_file, str):
                from ..exceptions import InvalidInputError

                raise InvalidInputError(
                    "'backup_file' is required for 'world' or 'config' restore type."
                )
            payload["backup_file"] = backup_file
            _LOGGER.info("Backup file to restore: %s", backup_file)

        encoded_server_name = quote(server_name)
        return await self._request(
            "POST",
            f"/server/{encoded_server_name}/restore/action",
            json_data=payload,
            authenticated=True,
        )
