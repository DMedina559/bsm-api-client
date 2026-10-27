"""Content overrides survive SDK validation and HTTP serialization."""

import json

import httpx
import pytest

from bsm_api_client import BedrockServerManagerApi


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mode,components",
    [("world", None), ("full", None), ("selected", ["world", "server.properties"])],
)
async def test_backup_content_http_serialization(mode, components):
    seen = []

    def handler(request):
        seen.append(request)
        return httpx.Response(
            202, json={"status": "accepted", "task_id": "task", "message": "Queued"}
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as transport:
        async with BedrockServerManagerApi(
            "http://test", jwt_token="test", http_client=transport
        ) as client:
            result = await client.backups.async_create(
                "alpha", mode=mode, components=components
            )
    assert result["task_id"] == "task"
    assert seen[0].url.path == "/api/server/alpha/backups"
    assert json.loads(seen[0].content)["mode"] == mode
    assert json.loads(seen[0].content)["components"] == components
