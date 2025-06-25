# src/bsm_api_client/client/_scheduler_methods.py
"""Mixin class containing OS-specific task scheduler methods."""
import logging
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from urllib.parse import quote

if TYPE_CHECKING:
    from ..client_base import ClientBase
    from ..exceptions import InvalidInputError  # For type hinting

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.scheduler")

# Updated based on API documentation for POST /api/server/{server_name}/task_scheduler/add
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
        Returns: API response dictionary.
        """
        if not server_name or not isinstance(server_name, str):
            from ..exceptions import InvalidInputError

            raise InvalidInputError("server_name must be a non-empty string.")
        if not new_cron_job or not isinstance(new_cron_job, str):
            from ..exceptions import InvalidInputError

            raise InvalidInputError("new_cron_job must be a non-empty string.")

        _LOGGER.info("Adding cron job for server '%s': '%s'", server_name, new_cron_job)
        payload = {"new_cron_job": new_cron_job}
        encoded_server_name = quote(server_name)
        return await self._request(
            "POST",
            f"/server/{encoded_server_name}/cron_scheduler/add",
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
        Returns: API response dictionary.
        """
        if not server_name or not isinstance(server_name, str):
            from ..exceptions import InvalidInputError

            raise InvalidInputError("server_name must be a non-empty string.")
        if not old_cron_job or not isinstance(old_cron_job, str):
            from ..exceptions import InvalidInputError

            raise InvalidInputError("old_cron_job must be a non-empty string.")
        if not new_cron_job or not isinstance(new_cron_job, str):
            from ..exceptions import InvalidInputError

            raise InvalidInputError("new_cron_job must be a non-empty string.")

        _LOGGER.info(
            "Modifying cron job for server '%s'. Old: '%s', New: '%s'",
            server_name,
            old_cron_job,
            new_cron_job,
        )
        payload = {"old_cron_job": old_cron_job, "new_cron_job": new_cron_job}
        encoded_server_name = quote(server_name)
        return await self._request(
            "POST",
            f"/server/{encoded_server_name}/cron_scheduler/modify",
            json_data=payload,
            authenticated=True,
        )

    async def async_delete_server_cron_job(
        self, server_name: str, cron_string: str
    ) -> Dict[str, Any]:
        """
        Deletes a cron job by exact string match.
        **Linux Only.**

        Corresponds to `DELETE /api/server/{server_name}/cron_scheduler/delete`.
        Requires authentication.

        Args:
            server_name: The server context.
            cron_string: The exact cron job line to delete.
        Returns: API response dictionary.
        """
        if not server_name or not isinstance(server_name, str):
            from ..exceptions import InvalidInputError

            raise InvalidInputError("server_name must be a non-empty string.")
        if not cron_string or not isinstance(cron_string, str):
            from ..exceptions import InvalidInputError

            raise InvalidInputError("cron_string must be a non-empty string.")

        _LOGGER.info(
            "Deleting cron job for server '%s': '%s'", server_name, cron_string
        )
        encoded_server_name = quote(server_name)
        return await self._request(
            "DELETE",
            f"/server/{encoded_server_name}/cron_scheduler/delete",
            params={"cron_string": cron_string},
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
            command: The manager command to execute. See API docs for allowed values.
            triggers: A list of trigger definition objects. See API docs for structure.
        Returns: API response dictionary.
        """
        if not server_name or not isinstance(server_name, str):
            from ..exceptions import InvalidInputError

            raise InvalidInputError("server_name must be a non-empty string.")
        if command not in ALLOWED_WINDOWS_TASK_COMMANDS:
            from ..exceptions import InvalidInputError

            raise InvalidInputError(
                f"Invalid command '{command}' provided. Allowed commands are: {', '.join(ALLOWED_WINDOWS_TASK_COMMANDS)}"
            )
        if not isinstance(triggers, list) or not triggers:
            from ..exceptions import InvalidInputError

            raise InvalidInputError(
                "triggers must be a non-empty list of trigger objects."
            )
        # Further validation of trigger structure can be added here or rely on API validation.

        _LOGGER.info(
            "Adding Windows task for server '%s', command: '%s'", server_name, command
        )
        payload = {"command": command, "triggers": triggers}
        encoded_server_name = quote(server_name)
        return await self._request(
            "POST",
            f"/server/{encoded_server_name}/task_scheduler/add",
            json_data=payload,
            authenticated=True,
        )

    async def async_get_server_windows_task_details(
        self, server_name: str, task_name: str
    ) -> Dict[str, Any]:
        """
        Retrieves details of a specific Windows scheduled task.
        The actual details are under the "task_details" key in the response.
        **Windows Only.**

        Corresponds to `POST /api/server/{server_name}/task_scheduler/details`.
        Requires authentication.

        Args:
            server_name: The server context.
            task_name: The full name of the task.
        Returns:
            API response dictionary. The main data is under "task_details".
        """
        if not server_name or not isinstance(server_name, str):
            from ..exceptions import InvalidInputError

            raise InvalidInputError("server_name must be a non-empty string.")
        if not task_name or not isinstance(task_name, str):
            from ..exceptions import InvalidInputError

            raise InvalidInputError("task_name must be a non-empty string.")

        _LOGGER.info(
            "Getting Windows task details for server '%s', task: '%s'",
            server_name,
            task_name,
        )
        payload = {"task_name": task_name}
        encoded_server_name = quote(server_name)
        # This method returns the full response, the caller can access response_data.get("task_details")
        return await self._request(
            "POST",
            f"/server/{encoded_server_name}/task_scheduler/details",
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
        **Windows Only.**

        Corresponds to `PUT /api/server/{server_name}/task_scheduler/task/{task_name}`.
        Requires authentication.

        Args:
            server_name: The server context.
            task_name: The current full name of the task to replace.
            command: The new manager command for the task.
            triggers: A list of new trigger definitions for the task.
        Returns: API response dictionary.
        """
        if not server_name or not isinstance(server_name, str):
            from ..exceptions import InvalidInputError

            raise InvalidInputError("server_name must be a non-empty string.")
        if not task_name or not isinstance(task_name, str):
            from ..exceptions import InvalidInputError

            raise InvalidInputError("task_name must be a non-empty string.")
        if command not in ALLOWED_WINDOWS_TASK_COMMANDS:
            from ..exceptions import InvalidInputError

            raise InvalidInputError(
                f"Invalid command '{command}' provided. Allowed commands are: {', '.join(ALLOWED_WINDOWS_TASK_COMMANDS)}"
            )
        if not isinstance(triggers, list) or not triggers:
            from ..exceptions import InvalidInputError

            raise InvalidInputError(
                "triggers must be a non-empty list of trigger objects."
            )

        _LOGGER.info(
            "Modifying Windows task '%s' for server '%s', new command: '%s'",
            task_name,
            server_name,
            command,
        )
        payload = {"command": command, "triggers": triggers}
        encoded_server_name = quote(server_name)
        encoded_task_name = quote(task_name)

        return await self._request(
            "PUT",
            f"/server/{encoded_server_name}/task_scheduler/task/{encoded_task_name}",
            json_data=payload,
            authenticated=True,
        )

    async def async_delete_server_windows_task(
        self, server_name: str, task_name: str
    ) -> Dict[str, Any]:
        """
        Deletes an existing Windows scheduled task.
        **Windows Only.**

        Corresponds to `DELETE /api/server/{server_name}/task_scheduler/task/{task_name}`.
        Requires authentication.

        Args:
            server_name: The server context.
            task_name: The full name of the task to delete.
        Returns: API response dictionary.
        """
        if not server_name or not isinstance(server_name, str):
            from ..exceptions import InvalidInputError

            raise InvalidInputError("server_name must be a non-empty string.")
        if not task_name or not isinstance(task_name, str):
            from ..exceptions import InvalidInputError

            raise InvalidInputError("task_name must be a non-empty string.")

        _LOGGER.info(
            "Deleting Windows task '%s' for server '%s'", task_name, server_name
        )
        encoded_server_name = quote(server_name)
        encoded_task_name = quote(task_name)

        return await self._request(
            "DELETE",
            f"/server/{encoded_server_name}/task_scheduler/task/{encoded_task_name}",
            authenticated=True,
        )
