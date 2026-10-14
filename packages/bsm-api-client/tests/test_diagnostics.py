"""Typed diagnostics against real generated HTTP serialization and backend models."""

import httpx
import pytest
from bedrock_server_manager.diagnostics import models as backend

from bsm_api_client import BedrockServerManagerApi
from bsm_api_client.exceptions import AuthError, InvalidInputError
from bsm_api_client.models import CompareDiagnosticSnapshotsRequest, DiagnosticSnapshot


def snapshot():
    return backend.DiagnosticSnapshot(
        instance_id="a" * 32,
        snapshot_id="snapshot",
        collected_at=100,
        sections=[
            backend.DiagnosticSection(
                name="runtime",
                status="ok",
                collected_at=100,
                data=backend.RuntimeDiagnostics(
                    ready=True,
                    phase="ready",
                    pid=123,
                    uptime_seconds=10,
                    version="4.0",
                    python_version="3.14",
                ),
            )
        ],
        summary=backend.DiagnosticSummary(
            status="ok", ready=True, counts_by_status={"ok": 1}
        ),
        registry=backend.RegistryDiagnostics(
            registered=9, pending=0, max_providers=128, max_providers_per_owner=8
        ),
        environment=backend.DiagnosticEnvironment(
            backend_version="4.0", python_version="3.14", operating_system="Test"
        ),
        persistence=backend.PersistenceDiagnostics(
            queued=0,
            queue_limit=256,
            dropped=0,
            write_failures=0,
            accepting=True,
            history_limit=1000,
            retention_days=7,
        ),
    )


@pytest.mark.asyncio
async def test_diagnostics_round_trip_queries_partial_sources_and_comparison():
    observed = snapshot()
    history = backend.DiagnosticHistory(records=[], available=False, truncated=False)
    responses = {
        "/api/diagnostics": observed,
        "/api/diagnostics/runtime": observed,
        "/api/diagnostics/history": history,
        "/api/diagnostics/runs": backend.DiagnosticRuns(
            runs=[], available=False, truncated=False
        ),
        "/api/diagnostics/trace/trace": backend.DiagnosticTrace(
            correlation_id="trace",
            events=None,
            tasks=[],
            tasks_available=True,
            history=history,
        ),
        "/api/diagnostics/report": backend.DiagnosticReport(
            snapshot=observed, history=history
        ),
        "/api/diagnostics/compare": backend.DiagnosticComparison(
            before_snapshot_id="snapshot",
            after_snapshot_id="snapshot",
            same_instance=True,
            elapsed_seconds=0,
            changes=[],
        ),
    }
    seen = []

    def handler(request):
        assert request.headers["Authorization"] == "Bearer test"
        seen.append(request)
        return httpx.Response(
            200, json=responses[request.url.path].model_dump(mode="json")
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        async with BedrockServerManagerApi(
            "http://backend", jwt_token="test", http_client=http
        ) as client:
            current = await client.diagnostics.async_get_application_diagnostics()
            assert isinstance(current, DiagnosticSnapshot)
            assert current.sections[0].data.ready is True
            assert current.sections[0].data.stage_started_at is None
            assert (
                await client.diagnostics.async_get_subsystem_diagnostics("runtime")
            ).sections[0].data.pid == 123
            page = await client.diagnostics.async_get_diagnostic_history(
                limit=2,
                owner="plugin:example",
                cursor="next",
                outcome="failed",
                operation_id="operation",
            )
            assert not page.available and not page.records
            assert dict(seen[-1].url.params) == {
                "limit": "2",
                "owner": "plugin:example",
                "cursor": "next",
                "outcome": "failed",
                "operation_id": "operation",
            }
            assert not (
                await client.diagnostics.async_get_diagnostic_runs(limit=5)
            ).available
            trace = await client.diagnostics.async_get_diagnostic_trace(
                "trace", limit=3, cursor="next"
            )
            assert (
                not trace.events_available
                and trace.events is None
                and trace.tasks_available
            )
            assert seen[-1].url.params["cursor"] == "next"
            report = await client.diagnostics.async_get_diagnostic_report()
            assert report.snapshot.instance_id == current.instance_id
            payload = CompareDiagnosticSnapshotsRequest(before=current, after=current)
            assert (
                await client.diagnostics.async_compare_diagnostic_snapshots(payload)
            ).same_instance
            import json

            assert (
                json.loads(seen[-1].content)["before"]["snapshot_id"]
                == current.snapshot_id
            )
            assert seen[-1].method == "POST"
            requests = len(seen)
            with pytest.raises(InvalidInputError):
                await client.diagnostics.async_get_diagnostic_history(limit=0)
            with pytest.raises(InvalidInputError):
                await client.diagnostics.async_get_diagnostic_runs(limit=51)
            assert len(seen) == requests


@pytest.mark.asyncio
async def test_diagnostics_preserve_administrator_errors_without_retrying():
    seen = []

    def handler(request):
        seen.append(request)
        return httpx.Response(
            403,
            json={
                "error": {
                    "code": "forbidden",
                    "message": "Administrator required",
                    "details": {},
                }
            },
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        async with BedrockServerManagerApi(
            "http://backend", jwt_token="test", http_client=http
        ) as client:
            with pytest.raises(AuthError) as failure:
                await client.diagnostics.async_get_application_diagnostics()
            assert failure.value.status_code == 403
            assert len(seen) == 1
