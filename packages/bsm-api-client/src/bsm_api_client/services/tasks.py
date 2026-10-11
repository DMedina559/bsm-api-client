"""Background task snapshots."""

from typing import cast

from ..models import TaskSnapshot
from ..validation import parse_response
from .base import Service


class TasksService(Service):
    async def async_get_task_status(self, task_id: str) -> TaskSnapshot:
        """Return the current typed snapshot of a background task.

        :param task_id: The task identifier.

        :returns: `TaskSnapshot`.
        """
        result = await self.async_call_generated(
            "get_task_status",
            parameters={"task_id": task_id},
            authenticated=True,
            typed=True,
        )
        return parse_response(TaskSnapshot, result)

    async def async_list_tasks(self) -> list[TaskSnapshot]:
        """List task snapshots visible to the authenticated user.

        :returns: `list[TaskSnapshot]`.
        """
        result = await self.async_call_generated(
            "list_tasks",
            authenticated=True,
            typed=True,
        )
        return cast(list[TaskSnapshot], result)
