"""Typed administrative access to event declarations and delivery diagnostics."""

from typing import Literal

from ..models import EventCatalog, EventDiagnostics
from ..validation import parse_response
from .base import Service


class EventService(Service):
    async def async_list_application_events(self) -> EventCatalog:
        """List event declarations and payload schemas; requires an administrator."""
        return parse_response(
            EventCatalog,
            await self.async_call_generated(
                "list_application_events", authenticated=True, typed=True
            ),
        )

    async def async_get_event_activity(
        self,
        *,
        name: str | None = None,
        owner: str | None = None,
        correlation_id: str | None = None,
        status: (
            Literal["dispatching", "completed", "partial", "cancelled", "suppressed"]
            | None
        ) = None,
        limit: int = 200,
    ) -> EventDiagnostics:
        """Read bounded metadata without event payloads; requires an administrator."""
        parameters = {
            key: value
            for key, value in {
                "name": name,
                "owner": owner,
                "correlation_id": correlation_id,
                "status": status,
                "limit": limit,
            }.items()
            if value is not None
        }
        return parse_response(
            EventDiagnostics,
            await self.async_call_generated(
                "get_event_activity",
                parameters=parameters,
                authenticated=True,
                typed=True,
            ),
        )
