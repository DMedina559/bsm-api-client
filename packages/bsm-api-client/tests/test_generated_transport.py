"""Exercise real generated serialization against a local HTTP server."""

import gzip

import pytest
import pytest_asyncio
from aiohttp import web

from bsm_api_client import BedrockServerManagerApi
from bsm_api_client.exceptions import InvalidInputError
from bsm_api_client.models import AllowlistRemovePayload


@pytest_asyncio.fixture
async def local_api():
    seen = []

    async def login(request):
        data = dict(await request.post())
        seen.append(("login", data))
        return web.json_response({"access_token": "fresh", "token_type": "bearer"})

    async def action(request):
        if request.headers.get("Authorization") == "Bearer expired":
            return web.json_response({"detail": "expired"}, status=401)
        body = await request.json() if request.can_read_body else None
        seen.append((request.method, request.match_info["server_name"], body))
        return web.json_response({"status": "success", "message": "done"})

    async def invalid(request):
        return web.json_response(
            {"detail": [{"loc": ["body"], "msg": "invalid"}]}, status=422
        )

    async def panorama(request):
        return web.Response(
            body=gzip.compress(b"\xff\xd8image"),
            headers={"Content-Encoding": "gzip", "Content-Type": "image/jpeg"},
        )

    async def upload(request):
        reader = await request.multipart()
        field = await reader.next()
        seen.append((field.name, field.filename, bytes(await field.read())))
        return web.json_response({"uploaded": True})

    async def query(request):
        return web.json_response(dict(request.query))

    app = web.Application()
    app.router.add_post("/auth/token", login)
    app.router.add_post("/api/server/{server_name}/start", action)
    app.router.add_delete("/api/server/{server_name}/allowlist/remove", action)
    app.router.add_post("/api/server/{server_name}/stop", invalid)
    app.router.add_get("/api/panorama", panorama)
    app.router.add_post("/extension/upload", upload)
    app.router.add_get("/extra/query", query)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 0)
    await site.start()
    port = runner.addresses[0][1]
    try:
        async with BedrockServerManagerApi(
            f"http://127.0.0.1:{port}",
            username="test",
            password="test",
            jwt_token="expired",
        ) as client:
            yield client, seen
    finally:
        await runner.cleanup()


@pytest.mark.asyncio
async def test_generated_start_refreshes_auth_and_preserves_path_encoding(local_api):
    client, seen = local_api
    result = await client.async_start_server("A/B & C")
    assert result.status == "success"
    assert seen[0][0] == "login" and seen[0][1]["username"] == "test"
    assert seen[1] == ("POST", "A/B & C", None)
    assert client._jwt_token == "fresh"


@pytest.mark.asyncio
async def test_generated_adapter_uses_schema_delete_and_body(local_api):
    client, seen = local_api
    client._jwt_token = "fresh"
    await client.async_remove_server_allowlist_players(
        "example", AllowlistRemovePayload(players=["Steve"])
    )
    assert seen == [("DELETE", "example", {"players": ["Steve"]})]


@pytest.mark.asyncio
async def test_generated_and_dynamic_errors_share_hierarchy(local_api):
    client, _ = local_api
    client._jwt_token = "fresh"
    with pytest.raises(InvalidInputError) as error:
        await client.async_stop_server("example")
    assert error.value.status_code == 422


@pytest.mark.asyncio
async def test_binary_response_is_not_decompressed_twice(local_api):
    client, _ = local_api
    assert await client.async_get_panorama_image() == b"\xff\xd8image"


@pytest.mark.asyncio
async def test_dynamic_multipart_and_boolean_query(local_api):
    client, seen = local_api
    client._jwt_token = "fresh"
    client._discovered_operations = client._index_operations(
        {
            "paths": {
                "/extension/upload": {
                    "post": {"operationId": "upload", "x-bsm-plugin": "demo"}
                },
                "/extra/query": {"get": {"operationId": "query"}},
            }
        }
    )
    result = await client.async_call_operation(
        "upload", files={"file": ("test.txt", b"hello", "text/plain")}
    )
    assert result == {"uploaded": True}
    assert seen == [("file", "test.txt", b"hello")]
    assert await client.async_call_operation(
        "query", query={"enabled": True, "missing": None}
    ) == {"enabled": "true"}


@pytest.mark.asyncio
async def test_generated_bridge_uses_shared_transport_and_closes_with_facade(local_api):
    from bsm_api_client.generated.api.server_mannagement import start_server

    client, seen = local_api
    generated = await client.async_get_generated_client()
    await start_server.asyncio(server_name="example", client=generated)
    transport = generated.get_async_httpx_client()
    await client.close()
    assert transport.is_closed
    assert seen[-1][0:2] == ("POST", "example")


@pytest.mark.asyncio
async def test_concurrent_expired_requests_share_one_refresh(local_api):
    import asyncio

    client, seen = local_api
    responses = await asyncio.gather(
        *(client.async_start_server(f"server-{number}") for number in range(5))
    )
    assert all(response.status == "success" for response in responses)
    assert len([entry for entry in seen if entry[0] == "login"]) == 1
