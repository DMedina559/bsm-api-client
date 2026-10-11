import logging
from typing import Any, Dict, cast

from ..models import TaskSnapshot
from ..validation import parse_response
from .base import Service

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.manager")


class TasksService(Service):

    async def async_get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Retrieves the status of a background task.

        Args:
            task_id: The ID of the task.

        Returns:
            A dictionary containing the status of the task.
        """
        _LOGGER.info("Fetching installation status for task ID: %s", task_id)
        result = await self.async_call_generated(
            "get_task_status", parameters={"task_id": task_id}, authenticated=True
        )
        return dict(result)

    async def async_get_task_snapshot(self, task_id: str) -> TaskSnapshot:
        """Return the typed task snapshot from the version-2 backend contract."""
        return cast(
            TaskSnapshot,
            parse_response(TaskSnapshot, await self.async_get_task_status(task_id)),
        )

    async def async_list_tasks(self) -> list[TaskSnapshot]:
        """List typed task snapshots visible to the authenticated user."""
        result = await self.async_call_generated("list_tasks", authenticated=True)
        return [
            cast(TaskSnapshot, parse_response(TaskSnapshot, item)) for item in result
        ]
