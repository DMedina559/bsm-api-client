# src/pybedrock_server_manager/client/_scheduler_methods.py
"""Mixin class containing OS-specific task scheduler methods."""
import logging
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from urllib.parse import quote  # For URL encoding path parameters

if TYPE_CHECKING:
    from ..client_base import ClientBase  # For type hinting _request

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.scheduler")

# Define allowed commands for Windows tasks for client-side validation
ALLOWED_WINDOWS_TASK_COMMANDS = [
    "update-server",
    "backup-all",
    "start-server",
    "stop-server",
    "restart-server",
    "scan-players",
]


class SchedulerMethodsMixin:
    """Mixin for OS-specific task scheduler endpoints."""

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

    async def async_add_server_cron_job(
        self, server_name: str, new_cron_job: str
    ) -> Dict[str, Any]:
        """
        Adds a new cron job to the crontab of the user running the manager.
        **Linux Only.**

        Corresponds to `POST /api/server/{server_name}/cron_scheduler/add`.
        Requires authentication.

        Args:
            server_name: The server context for the request.
            new_cron_job: The complete cron job line string to add.
        """
        _LOGGER.info("Adding cron job for server '%s': '%s'", server_name, new_cron_job)
        payload = {"new_cron_job": new_cron_job}

        return await self._request(
            "POST",
            f"/server/{server_name}/cron_scheduler/add",
            json_data=payload,
            authenticated=True,
        )

    async def async_modify_server_cron_job(
        self, server_name: str, old_cron_job: str, new_cron_job: str
    ) -> Dict[str, Any]:
        """
        Modifies an existing cron job by exact match.
        **Linux Only.**

        Corresponds to `POST /api/server/{server_name}/cron_scheduler/modify`.
        Requires authentication.

        Args:
            server_name: The server context.
            old_cron_job: The exact existing cron job line to replace.
            new_cron_job: The new cron job line.
        """
        _LOGGER.info(
            "Modifying cron job for server '%s'. Old: '%s', New: '%s'",
            server_name,
            old_cron_job,
            new_cron_job,
        )
        payload = {"old_cron_job": old_cron_job, "new_cron_job": new_cron_job}

        return await self._request(
            "POST",
            f"/server/{server_name}/cron_scheduler/modify",
            json_data=payload,
            authenticated=True,
        )

    async def async_delete_server_cron_job(
        self, server_name: str, cron_string: str
    ) -> Dict[str, Any]:
        """
        Deletes a cron job by exact string match.
        **Linux Only.** The `cron_string` will be URL-encoded by the HTTP client.

        Corresponds to `DELETE /api/server/{server_name}/cron_scheduler/delete`.
        Requires authentication.

        Args:
            server_name: The server context.
            cron_string: The exact cron job line to delete.
        """
        _LOGGER.info(
            "Deleting cron job for server '%s': '%s'", server_name, cron_string
        )

        return await self._request(
            "DELETE",
            f"/server/{server_name}/cron_scheduler/delete",
            params={"cron_string": cron_string},  # aiohttp handles query param encoding
            authenticated=True,
        )

    async def async_add_server_windows_task(
        self, server_name: str, command: str, triggers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Adds a new scheduled task in Windows Task Scheduler.
        **Windows Only.**

        Corresponds to `POST /api/server/{server_name}/task_scheduler/add`.
        Requires authentication.

        Args:
            server_name: The server context for the task.
            command: The manager command to execute (e.g., "backup-all").
            triggers: A list of trigger definition objects. See API docs for structure.
        """
        if command not in ALLOWED_WINDOWS_TASK_COMMANDS:
            _LOGGER.error(
                "Invalid command '%s' for Windows task. Allowed: %s",
                command,
                ALLOWED_WINDOWS_TASK_COMMANDS,
            )
            raise ValueError(
                f"Invalid command '{command}' provided. Allowed commands are: {', '.join(ALLOWED_WINDOWS_TASK_COMMANDS)}"
            )

        _LOGGER.info(
            "Adding Windows task for server '%s', command: '%s'", server_name, command
        )
        payload = {"command": command, "triggers": triggers}

        return await self._request(
            "POST",
            f"/server/{server_name}/task_scheduler/add",
            json_data=payload,
            authenticated=True,
        )

    async def async_get_server_windows_task_details(
        self, server_name: str, task_name: str
    ) -> Dict[str, Any]:
        """
        Retrieves details of a specific Windows scheduled task.
        **Windows Only.**

        Corresponds to `POST /api/server/{server_name}/task_scheduler/details`.
        Requires authentication.

        Args:
            server_name: The server context.
            task_name: The full name of the task.
        """
        _LOGGER.info(
            "Getting Windows task details for server '%s', task: '%s'",
            server_name,
            task_name,
        )
        payload = {"task_name": task_name}

        return await self._request(
            "POST",
            f"/server/{server_name}/task_scheduler/details",
            json_data=payload,
            authenticated=True,
        )

    async def async_modify_server_windows_task(
        self,
        server_name: str,
        task_name: str,
        command: str,
        triggers: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Modifies an existing Windows scheduled task by replacing it.
        **Windows Only.** The `task_name` in the path will be URL-encoded.

        Corresponds to `PUT /api/server/{server_name}/task_scheduler/task/{task_name}`.
        Requires authentication.

        Args:
            server_name: The server context.
            task_name: The current full name of the task to replace.
            command: The new manager command for the task.
            triggers: A list of new trigger definitions for the task.
        """
        if command not in ALLOWED_WINDOWS_TASK_COMMANDS:
            _LOGGER.error(
                "Invalid command '%s' for Windows task modification. Allowed: %s",
                command,
                ALLOWED_WINDOWS_TASK_COMMANDS,
            )
            raise ValueError(
                f"Invalid command '{command}' provided. Allowed commands are: {', '.join(ALLOWED_WINDOWS_TASK_COMMANDS)}"
            )

        _LOGGER.info(
            "Modifying Windows task '%s' for server '%s', new command: '%s'",
            task_name,
            server_name,
            command,
        )
        payload = {"command": command, "triggers": triggers}
        encoded_task_name = quote(task_name)  # Basic URL encoding for path segment

        return await self._request(
            "PUT",
            f"/server/{server_name}/task_scheduler/task/{encoded_task_name}",
            json_data=payload,
            authenticated=True,
        )

    async def async_delete_server_windows_task(
        self, server_name: str, task_name: str
    ) -> Dict[str, Any]:
        """
        Deletes an existing Windows scheduled task.
        **Windows Only.** The `task_name` in the path will be URL-encoded.

        Corresponds to `DELETE /api/server/{server_name}/task_scheduler/task/{task_name}`.
        Requires authentication.

        Args:
            server_name: The server context.
            task_name: The full name of the task to delete.
        """
        _LOGGER.info(
            "Deleting Windows task '%s' for server '%s'", task_name, server_name
        )
        encoded_task_name = quote(task_name)  # Basic URL encoding for path segment

        return await self._request(
            "DELETE",
            f"/server/{server_name}/task_scheduler/task/{encoded_task_name}",
            authenticated=True,
        )
