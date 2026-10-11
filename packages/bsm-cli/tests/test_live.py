"""Live terminal projections reject stale revisions and reconnect safely."""

import pytest

from bsm_cli.live import RevisionGate
from bsm_cli.manager import memory


def test_revision_gate_does_not_rewind_or_cross_epochs():
    gate = RevisionGate()
    assert gate.accept({"epoch": "one", "revision": 12})
    assert not gate.accept({"epoch": "one", "revision": 11})
    assert not gate.accept({"epoch": "two", "revision": 13})
    assert not gate.accept({})
    assert gate.accept({"epoch": "one", "revision": 13})
    assert RevisionGate().accept({"epoch": "two", "revision": 1})


def test_memory_units_and_missing_values():
    assert memory(None) == "Unavailable"
    assert memory(1024) == "1.00 GB"
    assert memory(1024**2, "TB") == "1.00 TB"
    assert memory(1024, "MB") == "1024.00 MB"


def test_metrics_with_equal_revision_do_not_rewind_sample_time():
    gate = RevisionGate()
    assert gate.accept({"epoch": "one", "revision": 12, "timestamp": 100})
    assert not gate.accept(
        {"epoch": "one", "revision": 12, "latest": {"timestamp": 99}}
    )
    assert gate.accept({"epoch": "one", "revision": 12, "timestamp": 101})


async def _never():
    import asyncio

    await asyncio.Event().wait()


@pytest.mark.asyncio
async def test_closing_live_view_cancels_pending_listener(monkeypatch):
    from unittest.mock import AsyncMock

    from bsm_api_client.models import ServersListResponse
    from bsm_cli.live import watch_resource

    class Socket:
        def __init__(self):
            self.closed = False
            self.cancelled = False

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            self.closed = True

        async def subscribe(self, topic):
            pass

        async def listen(self):
            try:
                await _never()
                yield {}
            finally:
                self.cancelled = True

    socket = Socket()
    client = AsyncMock()
    client.websocket_connect.return_value = socket
    fetch = AsyncMock(
        return_value=ServersListResponse(
            status="success", servers=[], epoch="one", revision=1
        )
    )
    stream = watch_resource(client, fetch, ("fleet",), interval=0.01)
    assert (await anext(stream))[1] is False
    assert (await anext(stream))[1] is True
    assert (await anext(stream))[1] is True
    await stream.aclose()
    assert socket.closed and socket.cancelled


def test_monitor_renders_backend_server_metrics_and_both_ram_values(capsys):
    from bsm_api_client.models import (
        GetApplicationMetricsResponse,
        MetricsSample,
        ServerMetrics,
    )
    from bsm_cli.manager import render_metrics

    sample = MetricsSample(
        timestamp=100,
        asyncio_task_count=16,
        background_task_count=0,
        loop_lag_ms=3.9,
        sys_ram_mb=8192,
        sys_ram_percent=90.7,
        servers=[ServerMetrics(server_name="alpha", cpu_percent=0.8, memory_mb=156.25)],
    )
    response = GetApplicationMetricsResponse(
        latest=sample, history=[sample], history_limit=60, interval_seconds=3
    )
    render_metrics(response, "auto")
    output = capsys.readouterr().out
    assert "alpha" in output and "0.8%" in output and "156.25 MB" in output
    assert "Ram" in output and "8.00 GB" in output
    assert "Ram usage" in output and "90.7%" in output
