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


@pytest.mark.asyncio
async def test_global_activity_round_trip_filters_operations_and_listener_details():
    from bedrock_server_manager.events import EventSubscriptionInfo, EventSubscriptions
    from bedrock_server_manager.operations import OperationActivity, OperationSnapshot

    from bsm_api_client.models import DiagnosticActivity

    result = backend.DiagnosticActivity(
        operations=OperationActivity(
            recent=[
                OperationSnapshot(
                    operation_id="operation",
                    sequence_id="sequence",
                    root_operation_id="root",
                    parent_operation_id="root",
                    correlation_id="trace",
                    name="server.start",
                    server_name="alpha",
                    status="finished",
                    outcome="started",
                    started_at=100,
                    finished_at=101,
                )
            ]
        ),
        subscriptions=EventSubscriptions(
            total=1,
            items=[
                EventSubscriptionInfo(
                    subscription_id="subscription",
                    listener_id="plugin:listener",
                    name="before_server_start",
                    owner="plugin:example",
                    kind="hook",
                    priority=100,
                    once=False,
                    active=True,
                    after=("other:listener",),
                    unresolved_after=("other:listener",),
                    calls=2,
                )
            ],
        ),
        truncated=True,
    )
    requests = []

    def handler(request):
        requests.append(request)
        assert request.headers["Authorization"] == "Bearer test"
        assert request.url.path == "/api/diagnostics/activity"
        return httpx.Response(200, json=result.model_dump(mode="json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        async with BedrockServerManagerApi(
            "http://backend", jwt_token="test", http_client=http
        ) as client:
            observed = await client.diagnostics.async_get_diagnostic_activity(
                server_name="alpha",
                sequence_id="sequence",
                operation_id="operation",
                phase="before",
                limit=5,
            )
            assert isinstance(observed, DiagnosticActivity)
            assert observed.operations.recent[0].parent_operation_id == "root"
            assert observed.operations.recent[0].outcome == "started"
            assert observed.subscriptions.items[0].unresolved_after == [
                "other:listener"
            ]
            assert observed.truncated
            assert dict(requests[-1].url.params) == {
                "server_name": "alpha",
                "sequence_id": "sequence",
                "operation_id": "operation",
                "phase": "before",
                "limit": "5",
            }
            with pytest.raises(InvalidInputError):
                await client.diagnostics.async_get_diagnostic_activity(limit=201)
    assert len(requests) == 1


@pytest.mark.asyncio
async def test_older_trace_without_operation_metadata_remains_readable():
    body = {
        "correlation_id": "old",
        "events": None,
        "events_available": False,
        "tasks": [],
        "tasks_available": False,
        "history": {"records": [], "available": True, "truncated": False},
    }
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(200, json=body))
    ) as http:
        async with BedrockServerManagerApi(
            "http://backend", jwt_token="test", http_client=http
        ) as client:
            trace = await client.diagnostics.async_get_diagnostic_trace("old")
            assert not trace.operations_available and trace.operations is None


@pytest.mark.asyncio
async def test_event_activity_supports_operation_sequence_server_and_phase_filters():
    from bedrock_server_manager.events import EventBus

    observed = []

    def handler(request):
        observed.append(request)
        return httpx.Response(
            200, json=EventBus().diagnostics().model_dump(mode="json")
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        async with BedrockServerManagerApi(
            "http://backend", jwt_token="test", http_client=http
        ) as client:
            await client.events.async_get_event_activity(
                server_name="alpha",
                source="plugin:probe",
                operation_name="server.start",
                operation_id="op",
                sequence_id="seq",
                phase="before",
                limit=5,
            )
    assert observed[0].url.path == "/api/events/activity"
    assert dict(observed[0].url.params) == {
        "server_name": "alpha",
        "source": "plugin:probe",
        "operation_name": "server.start",
        "operation_id": "op",
        "sequence_id": "seq",
        "phase": "before",
        "limit": "5",
    }
