"""Compatibility with the backend's version-2 HTTP contract."""

from unittest.mock import AsyncMock

import pytest
from aiohttp import web

from bsm_api_client import BedrockServerManagerApi, InvalidInputError
from bsm_api_client.models import StartServerResponse, TaskSnapshot
from bsm_api_client.openapi import serialize_headers, serialize_query


@pytest.mark.asyncio
async def test_dynamic_binary_prefix_headers_and_typed_errors():
    app = web.Application()

    async def response(request):
        if request.path.endswith("image"):
            return web.Response(body=b"\x89PNG\xff", content_type="image/png")
        if request.path.endswith("invalid"):
            return web.json_response(
                {
                    "error": {
                        "code": "validation_error",
                        "message": "Invalid request.",
                        "details": {"field": "name"},
                    }
                },
                status=422,
            )
        return web.json_response({"count": request.headers["X-Count"]})

    app.router.add_get("/prefix/api/{kind}", response)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 0)
    await site.start()
    try:
        async with BedrockServerManagerApi(
            f"http://127.0.0.1:{runner.addresses[0][1]}",
            jwt_token="token",
            base_path="prefix/api",
        ) as client:
            client._discovered_operations = client._index_operations(
                {
                    "paths": {
                        f"/api/{name}": {"get": {"operationId": name}}
                        for name in ("image", "headers", "invalid")
                    }
                }
            )
            assert await client.async_call_operation("image") == b"\x89PNG\xff"
            assert await client.async_call_operation(
                "headers", headers={"X-Count": 3}
            ) == {"count": "3"}
            with pytest.raises(InvalidInputError, match="Invalid request") as error:
                await client.async_call_operation("invalid")
            assert error.value.api_code == "validation_error"
            assert error.value.api_details == {"field": "name"}
    finally:
        await runner.cleanup()


def test_boolean_query_array_serialization():
    assert serialize_headers(
        ({"name": "X-Flags", "in": "header"},), {"X-Flags": [True, False]}
    ) == {"X-Flags": "true,false"}
    assert serialize_query(
        ({"name": "flags", "in": "query", "explode": False},), {"flags": [True, False]}
    ) == {"flags": "true,false"}


@pytest.mark.asyncio
async def test_lifecycle_and_task_fields_are_preserved():
    async with BedrockServerManagerApi("http://localhost", jwt_token="token") as client:
        client.async_call_generated = AsyncMock(
            return_value={
                "status": "success",
                "server_name": "example",
                "outcome": "already_running",
                "message": "Already running.",
            }
        )
        response = await client.async_start_server("example")
        assert isinstance(response, StartServerResponse)
        assert response.outcome == "already_running"
        assert response.server_name == "example"
        client.async_call_generated.return_value = {
            "id": "task",
            "status": "failed",
            "message": "Failed.",
            "error": {"code": "server_error", "message": "Server failed."},
        }
        task = await client.async_get_task_snapshot("task")
        assert isinstance(task, TaskSnapshot)
        assert task.error.code == "server_error"
