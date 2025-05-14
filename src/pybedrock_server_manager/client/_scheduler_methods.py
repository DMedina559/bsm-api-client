# src/pybedrock_server_manager/client/_scheduler_methods.py
"""Mixin class containing OS-specific task scheduler methods."""
import logging
from typing import Any, Dict, List, Optional

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.scheduler")


class SchedulerMethodsMixin:
    """Mixin for OS-specific task scheduler endpoints."""

    async def async_add_server_cron_job(
        self, server_name: str, new_cron_job: str
    ) -> Dict[str, Any]:
        """Adds a new cron job (Linux Only). Calls POST /api/server/{server_name}/cron_scheduler/add."""
        _LOGGER.info("Adding cron job for server '%s': %s", server_name, new_cron_job)
        payload = {"new_cron_job": new_cron_job}

        return await self._request(
            "POST",
            f"/server/{server_name}/cron_scheduler/add",
            data=payload,
            authenticated=True,
        )

    async def async_modify_server_cron_job(
        self, server_name: str, old_cron_job: str, new_cron_job: str
    ) -> Dict[str, Any]:
        """Modifies an existing cron job (Linux Only). Calls POST /api/server/{server_name}/cron_scheduler/modify."""
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
            data=payload,
            authenticated=True,
        )

    async def async_delete_server_cron_job(
        self, server_name: str, cron_string: str
    ) -> Dict[str, Any]:
        """Deletes a cron job (Linux Only). Calls DELETE /api/server/{server_name}/cron_scheduler/delete."""
        _LOGGER.info("Deleting cron job for server '%s': %s", server_name, cron_string)

        return await self._request(
            "DELETE",
            f"/server/{server_name}/cron_scheduler/delete",
            params={"cron_string": cron_string},
            authenticated=True,
        )

    async def async_add_server_windows_task(
        self, server_name: str, command: str, triggers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Adds a new Windows scheduled task. Calls POST /api/server/{server_name}/task_scheduler/add."""
        _LOGGER.info(
            "Adding Windows task for server '%s', command: '%s'", server_name, command
        )
        payload = {"command": command, "triggers": triggers}

        return await self._request(
            "POST",
            f"/server/{server_name}/task_scheduler/add",
            data=payload,
            authenticated=True,
        )

    async def async_get_server_windows_task_details(
        self, server_name: str, task_name: str
    ) -> Dict[str, Any]:
        """Gets details of a Windows scheduled task. Calls POST /api/server/{server_name}/task_scheduler/details."""
        _LOGGER.info(
            "Getting Windows task details for server '%s', task: '%s'",
            server_name,
            task_name,
        )
        payload = {"task_name": task_name}

        return await self._request(
            "POST",  # Assuming POST is correct as per API docs, though GET seems more logical for "get details"
            f"/server/{server_name}/task_scheduler/details",
            data=payload,
            authenticated=True,
        )

    async def async_modify_server_windows_task(
        self,
        server_name: str,
        task_name: str,
        command: str,
        triggers: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Modifies a Windows scheduled task. Calls PUT /api/server/{server_name}/task_scheduler/task/{task_name}."""
        _LOGGER.info(
            "Modifying Windows task '%s' for server '%s', new command: '%s'",
            task_name,
            server_name,
            command,
        )
        payload = {"command": command, "triggers": triggers}

        return await self._request(
            "PUT",
            f"/server/{server_name}/task_scheduler/task/{task_name}",
            data=payload,
            authenticated=True,
        )

    async def async_delete_server_windows_task(
        self, server_name: str, task_name: str
    ) -> Dict[str, Any]:
        """Deletes a Windows scheduled task. Calls DELETE /api/server/{server_name}/task_scheduler/task/{task_name}."""
        _LOGGER.info(
            "Deleting Windows task '%s' for server '%s'", task_name, server_name
        )

        return await self._request(
            "DELETE",
            f"/server/{server_name}/task_scheduler/task/{task_name}",
            authenticated=True,
        )
