"""Scheduler controls preserve explicit action and revision on the wire."""

import json

import httpx
import pytest

from bsm_api_client import BedrockServerManagerApi


@pytest.mark.asyncio
@pytest.mark.parametrize("action", ["run_now", "pause", "resume", "retry"])
async def test_scheduler_control_serialization(action):
    requests = []

    async def handle(request):
        requests.append(request)
        return httpx.Response(200, json={"status": "success", "message": "Accepted"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handle)) as transport:
        client = BedrockServerManagerApi(
            "http://bsm", jwt_token="test", http_client=transport
        )
        response = await client.scheduler.async_control_schedule(
            "nightly", action, revision="current"
        )
        assert response.status == "success"
        assert requests[0].url.path == "/api/scheduler/schedules/nightly/action"
        assert json.loads(requests[0].content) == {
            "action": action,
            "revision": "current",
        }
        await client.close()
