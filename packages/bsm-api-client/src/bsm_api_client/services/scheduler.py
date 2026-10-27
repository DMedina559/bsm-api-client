"""Typed administrator scheduler configuration and run metadata."""

from ..models import ListSchedulesResponse, ScheduledTask, SuccessResponse
from ..validation import parse_response
from .base import Service


class SchedulerService(Service):
    """Manage independent backup, verification, and plugin-provided schedules."""

    async def async_list_schedules(
        self, server_name: str | None = None
    ) -> ListSchedulesResponse:
        """Read schedules, task availability, and recent execution attempts.

        :param server_name: Optional server filter.
        :returns: Durable schedules and bounded run history.
        """
        return parse_response(
            ListSchedulesResponse,
            await self.async_call_generated(
                "list_schedules",
                parameters=(
                    {"server_name": server_name} if server_name is not None else {}
                ),
                authenticated=True,
                typed=True,
            ),
        )

    async def async_save_schedule(
        self, schedule_id: str, configuration: ScheduledTask
    ) -> SuccessResponse:
        """Create or replace a schedule. New definitions start at the next occurrence.

        If the configuration omits ``timezone``, supporting backends use the
        application default for a new job and preserve an existing job's timezone.
        Set the field explicitly when a job must use a particular timezone.

        :param schedule_id: Stable schedule identifier.
        :param configuration: Validated task, timing, server, and task options.
        :returns: Save confirmation.
        """
        return parse_response(
            SuccessResponse,
            await self.async_call_generated(
                "save_schedule",
                parameters={"schedule_id": schedule_id},
                body=configuration,
                authenticated=True,
                typed=True,
            ),
        )

    async def async_delete_schedule(self, schedule_id: str) -> SuccessResponse:
        """Remove a schedule without deleting its server's backup archives.

        :param schedule_id: Stable schedule identifier.
        :returns: Removal confirmation.
        """
        return parse_response(
            SuccessResponse,
            await self.async_call_generated(
                "delete_schedule",
                parameters={"schedule_id": schedule_id},
                authenticated=True,
                typed=True,
            ),
        )
