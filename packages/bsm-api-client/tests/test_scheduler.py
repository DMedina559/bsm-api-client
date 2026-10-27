"""Generated serialization and public scheduler service coverage."""

import json

import httpx
import pytest

from bsm_api_client import BedrockServerManagerApi
from bsm_api_client.models import ScheduledTask


@pytest.mark.asyncio
async def test_schedule_crud():
    seen = []

    def handler(request):
        seen.append(request)
        assert request.headers["authorization"] == "Bearer test"
        if request.url.path == "/api/scheduler/schedules":
            return httpx.Response(
                200,
                json={
                    "schedules": [],
                    "task_types": ["backup", "verify"],
                    "timezones": ["UTC", "America/Los_Angeles"],
                    "timezone_database_available": True,
                    "host_timezone": "UTC",
                },
            )
        return httpx.Response(200, json={"status": "success", "message": "Saved"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as transport:
        async with BedrockServerManagerApi(
            "http://test", jwt_token="test", http_client=transport
        ) as client:
            result = await client.scheduler.async_list_schedules("alpha")
            assert result.task_types == ["backup", "verify"]
            assert result.timezone_database_available
            assert "America/Los_Angeles" in result.timezones
            assert seen[-1].url.params["server_name"] == "alpha"
            config = ScheduledTask(task="verify", server_name="alpha", enabled=False)
            await client.scheduler.async_save_schedule("weekly", config)
            assert seen[-1].method == "PUT"
            assert json.loads(seen[-1].content)["task"] == "verify"
            assert "timezone" not in json.loads(seen[-1].content)
            await client.scheduler.async_save_schedule(
                "weekly", config.model_copy(update={"timezone": "America/Los_Angeles"})
            )
            assert json.loads(seen[-1].content)["timezone"] == "America/Los_Angeles"
            await client.scheduler.async_delete_schedule("weekly")
            assert seen[-1].method == "DELETE"
