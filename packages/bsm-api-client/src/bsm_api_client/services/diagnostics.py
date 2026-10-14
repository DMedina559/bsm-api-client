"""Typed administrative diagnostics through the shared SDK transport."""

from typing import Literal

from ..models import (
    CompareDiagnosticSnapshotsRequest,
    DiagnosticComparison,
    DiagnosticHistory,
    DiagnosticReport,
    DiagnosticRuns,
    DiagnosticSnapshot,
    DiagnosticTrace,
)
from ..validation import parse_response
from .base import Service


class DiagnosticsService(Service):
    """Inspect bounded observations, retained records and snapshot differences."""

    async def async_get_application_diagnostics(self) -> DiagnosticSnapshot:
        """Collect application observations; requires an administrator."""
        return parse_response(
            DiagnosticSnapshot,
            await self.async_call_generated(
                "get_application_diagnostics", authenticated=True, typed=True
            ),
        )

    async def async_get_subsystem_diagnostics(
        self, subsystem: str
    ) -> DiagnosticSnapshot:
        """Inspect one registered subsystem without inventing missing readings."""
        return parse_response(
            DiagnosticSnapshot,
            await self.async_call_generated(
                "get_subsystem_diagnostics",
                parameters={"subsystem": subsystem},
                authenticated=True,
                typed=True,
            ),
        )

    async def async_get_diagnostic_history(
        self,
        *,
        limit: int = 100,
        subsystem: str | None = None,
        instance_id: str | None = None,
        correlation_id: str | None = None,
        cursor: str | None = None,
        owner: str | None = None,
        code: str | None = None,
        outcome: Literal["completed", "failed", "cancelled"] | None = None,
        operation_id: str | None = None,
    ) -> DiagnosticHistory:
        """Read one filtered history page; pass its next cursor for continuation."""
        parameters = {
            key: value
            for key, value in {
                "limit": limit,
                "subsystem": subsystem,
                "instance_id": instance_id,
                "correlation_id": correlation_id,
                "cursor": cursor,
                "owner": owner,
                "code": code,
                "outcome": outcome,
                "operation_id": operation_id,
            }.items()
            if value is not None
        }
        return parse_response(
            DiagnosticHistory,
            await self.async_call_generated(
                "get_diagnostic_history",
                parameters=parameters,
                authenticated=True,
                typed=True,
            ),
        )

    async def async_get_diagnostic_runs(self, *, limit: int = 20) -> DiagnosticRuns:
        """Read bounded summaries of retained application instances."""
        return parse_response(
            DiagnosticRuns,
            await self.async_call_generated(
                "get_diagnostic_runs",
                parameters={"limit": limit},
                authenticated=True,
                typed=True,
            ),
        )

    async def async_get_diagnostic_trace(
        self, correlation_id: str, *, limit: int = 100, cursor: str | None = None
    ) -> DiagnosticTrace:
        """Inspect correlated records with independent source availability."""
        parameters = {"correlation_id": correlation_id, "limit": limit}
        if cursor is not None:
            parameters["cursor"] = cursor
        return parse_response(
            DiagnosticTrace,
            await self.async_call_generated(
                "get_diagnostic_trace",
                parameters=parameters,
                authenticated=True,
                typed=True,
            ),
        )

    async def async_get_diagnostic_report(self) -> DiagnosticReport:
        """Collect a support report; review metadata before sharing."""
        return parse_response(
            DiagnosticReport,
            await self.async_call_generated(
                "get_diagnostic_report", authenticated=True, typed=True
            ),
        )

    async def async_compare_diagnostic_snapshots(
        self, payload: CompareDiagnosticSnapshotsRequest
    ) -> DiagnosticComparison:
        """Compare validated snapshots; counter deltas depend on instance identity."""
        return parse_response(
            DiagnosticComparison,
            await self.async_call_generated(
                "compare_diagnostic_snapshots",
                body=payload,
                authenticated=True,
                typed=True,
            ),
        )
