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
        if request.method == "DELETE":
            return web.json_response({"status": "success", "message": "done"})
        return web.json_response(
            {
                "status": "success",
                "message": "done",
                "server_name": "example",
                "outcome": "started",
            }
        )

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
    from bsm_api_client.generated_adapter import operation_module

    start_server = operation_module("start_server")

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


@pytest.mark.asyncio
async def test_expired_token_retry_releases_first_response(local_api):
    """The 401 response must be closed before authentication is attempted."""
    client, _ = local_api
    original_authenticate = client.authenticate
    original_send = client._http_client.send
    unauthorized_response = None

    async def tracked_send(*args, **kwargs):
        nonlocal unauthorized_response
        response = await original_send(*args, **kwargs)
        if response.status_code == 401:
            unauthorized_response = response
        return response

    async def assert_released_before_auth():
        assert unauthorized_response is not None
        assert unauthorized_response.is_closed
        return await original_authenticate()

    client._http_client.send = tracked_send
    client.authenticate = assert_released_before_auth
    result = await client.async_start_server("example")
    assert result.status == "success"


@pytest.mark.asyncio
async def test_dynamic_multipart_accepts_file_stream(local_api, tmp_path):
    client, seen = local_api
    client._jwt_token = "fresh"
    client._discovered_operations = client._index_operations(
        {"paths": {"/extension/upload": {"post": {"operationId": "upload"}}}}
    )
    upload_path = tmp_path / "payload.bin"
    upload_path.write_bytes(b"streamed upload")
    with upload_path.open("rb") as stream:
        result = await client.async_call_operation(
            "upload",
            files={"file": ("payload.bin", stream, "application/octet-stream")},
        )
    assert result == {"uploaded": True}
    assert seen == [("file", "payload.bin", b"streamed upload")]


@pytest.mark.asyncio
async def test_rest_interface_uses_one_contract_and_shared_generated_client(local_api):
    from bsm_api_client.contracts import StartServerResponse
    from bsm_api_client.generated.models.start_server_response import (
        StartServerResponse as GeneratedResponse,
    )

    client, _ = local_api
    assert GeneratedResponse is StartServerResponse
    response = await client.rest.start_server(server_name="example")
    assert isinstance(response, StartServerResponse)
    detailed = await client.rest.start_server_detailed(server_name="example")
    assert detailed.status_code == 200
    assert isinstance(detailed.parsed, StartServerResponse)
    assert "application/json" in detailed.headers["Content-Type"]
    first = await client.async_get_generated_client()
    assert await client.async_get_generated_client() is first
    assert len(client._generated_http_clients) == 2  # authenticated REST and login
    assert client._session is None  # REST does not create a WebSocket session


@pytest.mark.asyncio
async def test_caller_owned_httpx_client_remains_open():
    import httpx

    from bsm_api_client import BedrockServerManagerApi
    from bsm_api_client.exceptions import APIError

    async def respond(request):
        return httpx.Response(200, json={"status": "success", "servers": []})

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as transport:
        client = BedrockServerManagerApi(
            "http://localhost", jwt_token="token", http_client=transport
        )
        response = await client.rest.list_servers()
        assert response.servers == []
        await client.close()
        assert not transport.is_closed
        with pytest.raises(APIError, match="closed"):
            await client.rest.list_servers()


@pytest.mark.asyncio
async def test_generated_login_sends_secret_without_unmasking_model_dumps():
    from urllib.parse import parse_qs

    import httpx

    from bsm_api_client import BedrockServerManagerApi
    from bsm_api_client.contracts import BodyLogin

    body = BodyLogin(username="admin", password="test-password", grant_type="password")
    assert "test-password" not in repr(body)
    assert body.model_dump(mode="json")["password"] != "test-password"

    async def respond(request):
        values = parse_qs(request.content.decode())
        assert values["password"] == ["test-password"]
        return httpx.Response(
            200, json={"access_token": "token", "token_type": "bearer"}
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as transport:
        async with BedrockServerManagerApi(
            "http://localhost", jwt_token="placeholder", http_client=transport
        ) as client:
            response = await client.rest.login(body=body)
            assert response.access_token == "token"


@pytest.mark.asyncio
async def test_generated_rest_respects_proxy_mount_and_custom_api_prefix():
    import httpx

    from bsm_api_client import BedrockServerManagerApi

    async def respond(request):
        assert request.url.path == "/bsm/custom/server/example/start"
        assert request.headers["Authorization"] == "Bearer token"
        return httpx.Response(
            200,
            json={
                "status": "success",
                "message": "Started",
                "outcome": "started",
                "server_name": "example",
            },
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as transport:
        async with BedrockServerManagerApi(
            "http://localhost/bsm",
            base_path="custom",
            jwt_token="token",
            http_client=transport,
        ) as client:
            response = await client.rest.start_server(server_name="example")
            assert response.outcome == "started"
