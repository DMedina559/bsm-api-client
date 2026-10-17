"""Exercise real generated serialization against a local HTTP server."""

import gzip
import threading
from pathlib import Path

import pytest
import pytest_asyncio
from aiohttp import web

from bsm_api_client import BedrockServerManagerApi
from bsm_api_client.exceptions import InvalidInputError
from bsm_api_client.models import AllowlistRemovePayload


@pytest.mark.asyncio
async def test_generated_metadata_reads_run_outside_event_loop(local_api, monkeypatch):
    """Cold endpoint resolution and body validation never read JSON on the loop."""
    from bsm_api_client.generated_adapter import _operation_registry, operation_module

    _operation_registry.cache_clear()
    operation_module.cache_clear()
    loop_thread = threading.get_ident()
    reads = []
    original = Path.read_text

    def read_text(path, *args, **kwargs):
        if path.name in {"operations.json", "openapi.json"}:
            assert threading.get_ident() != loop_thread
            reads.append(path.name)
        return original(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", read_text)
    client, _ = local_api
    await client.rest.start_server("example")
    await client.servers.async_remove_server_allowlist_players(
        "example", AllowlistRemovePayload(players=["Alex"])
    )
    assert "operations.json" in reads
    assert "openapi.json" in reads
    assert reads.count("operations.json") == 1


def _add_runtime_routes(app, seen):
    async def runtime(request):
        seen.append(("runtime", request.headers.get("Authorization")))
        return web.json_response(
            {
                "instance_id": "test-instance",
                "pid": 123,
                "phase": "ready",
                "shutdown_requested": False,
            }
        )

    async def shutdown(request):
        body = await request.json()
        seen.append(("shutdown", body, request.headers.get("X-BSM-Shutdown-Token")))
        return web.json_response(
            {
                "instance_id": "test-instance",
                "pid": 123,
                "phase": "stopping",
                "shutdown_requested": True,
                "shutdown_reason": "administrator",
                "status": "accepted",
            },
            status=202,
        )

    async def events(request):
        return web.json_response({"events": []})

    async def activity(request):
        seen.append(("activity", dict(request.query)))
        return web.json_response(
            {
                "accepting": True,
                "emitted": 2,
                "suppressed": 0,
                "failed_listeners": 0,
                "subscriptions": 1,
                "active": [],
                "recent": [],
                "pending_workers": 0,
            }
        )

    app.router.add_get("/api/runtime", runtime)
    app.router.add_post("/api/runtime/shutdown", shutdown)
    app.router.add_get("/api/events", events)
    app.router.add_get("/api/events/activity", activity)


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
            return web.json_response(
                {
                    "status": "success",
                    "message": "done",
                    "details": {"removed": body["players"], "not_found": []},
                }
            )
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
    _add_runtime_routes(app, seen)
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
    result = await client.servers.async_start_server("A/B & C")
    assert result.status == "success"
    assert seen[0][0] == "login" and seen[0][1]["username"] == "test"
    assert seen[1] == ("POST", "A/B & C", None)
    assert client._jwt_token == "fresh"


@pytest.mark.asyncio
async def test_generated_adapter_uses_schema_delete_and_body(local_api):
    client, seen = local_api
    client._jwt_token = "fresh"
    await client.servers.async_remove_server_allowlist_players(
        "example", AllowlistRemovePayload(players=["Steve"])
    )
    assert seen == [("DELETE", "example", {"players": ["Steve"]})]


@pytest.mark.asyncio
async def test_generated_and_dynamic_errors_share_hierarchy(local_api):
    client, _ = local_api
    client._jwt_token = "fresh"
    with pytest.raises(InvalidInputError) as error:
        await client.servers.async_stop_server("example")
    assert error.value.status_code == 422


@pytest.mark.asyncio
async def test_binary_response_is_not_decompressed_twice(local_api):
    client, _ = local_api
    assert await client.application.async_get_panorama_image() == b"\xff\xd8image"


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
        *(client.servers.async_start_server(f"server-{number}") for number in range(5))
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
    result = await client.servers.async_start_server("example")
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


@pytest.mark.asyncio
async def test_content_service_streams_upload_in_bounded_chunks(
    local_api, tmp_path, monkeypatch
):
    from pathlib import Path

    client, seen = local_api
    document = {
        "paths": {
            "/extension/upload": {
                "post": {"operationId": "upload_content", "x-bsm-plugin": "demo"}
            }
        }
    }
    client._openapi_schema = document
    client._discovered_operations = client._index_operations(document)
    client._jwt_token = "fresh"
    path = tmp_path / "world.mcworld"
    payload = b"world" * 40000
    path.write_bytes(payload)
    original_open = Path.open
    reads = []
    handles = []

    class BoundedFile:
        def __init__(self, handle):
            self.handle = handle

        def read(self, size=-1):
            assert size > 0, "Uploads must not read the entire file at once"
            reads.append(size)
            return self.handle.read(size)

        def __getattr__(self, name):
            return getattr(self.handle, name)

        def __enter__(self):
            return self

        def __exit__(self, *args):
            self.handle.close()

    def open_file(selected, *args, **kwargs):
        handle = original_open(selected, *args, **kwargs)
        if selected == path:
            handles.append(handle)
            return BoundedFile(handle)
        return handle

    monkeypatch.setattr(Path, "open", open_file)
    assert await client.content.async_upload_content(str(path)) == {"uploaded": True}
    assert seen == [("file", "world.mcworld", payload)]
    assert len(reads) > 1
    assert all(handle.closed for handle in handles)


@pytest.mark.asyncio
async def test_shutdown_attempts_all_owned_transports_after_failure():
    from unittest.mock import AsyncMock

    import httpx

    client = BedrockServerManagerApi("http://localhost", jwt_token="token")
    http_close = client._http_client.aclose
    client._generated_http_clients = [
        AsyncMock(aclose=AsyncMock(side_effect=RuntimeError("close failed")))
    ]
    websocket = AsyncMock()
    websocket.closed = False
    client._session = websocket
    with pytest.raises(RuntimeError, match="close failed"):
        await client.close()
    assert client._http_client.is_closed
    websocket.close.assert_awaited_once()
    await client.close()
    await http_close()
    with pytest.raises(AttributeError):
        getattr(client, "async_start_server")
    assert isinstance(client._http_client, httpx.AsyncClient)


@pytest.mark.parametrize("remember_me", [False, True])
@pytest.mark.asyncio
async def test_login_and_reauthentication_preserve_remember_me(local_api, remember_me):
    original, seen = local_api
    options = {"remember_me": True} if remember_me else {}
    async with BedrockServerManagerApi(
        original._server_root_url, username="test", password="test", **options
    ) as client:
        await client.authenticate()
        client._jwt_token = "expired"
        await client.rest.start_server("example")
    logins = [entry[1] for entry in seen if entry[0] == "login"]
    assert len(logins) == 2
    assert all(data["remember_me"] == str(remember_me).lower() for data in logins)


@pytest.mark.asyncio
async def test_password_change_preserves_secret_values_on_the_wire():
    import httpx

    from bsm_api_client.models import ChangePasswordPayload

    payload = ChangePasswordPayload(
        current_password="old-secret", new_password="new-secret"
    )
    assert "old-secret" not in repr(payload)
    assert "new-secret" not in payload.model_dump_json()

    async def respond(request):
        import json

        assert json.loads(request.content) == {
            "current_password": "old-secret",
            "new_password": "new-secret",
        }
        return httpx.Response(
            200, json={"status": "success", "message": "Password changed."}
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as transport:
        async with BedrockServerManagerApi(
            "http://localhost", jwt_token="token", http_client=transport
        ) as client:
            response = await client.account.async_change_password(payload)
            assert response.status == "success"


def test_incomplete_account_error_preserves_committed_outcome():
    from bsm_api_client import APIServerSideError

    result = {"committed": True, "action": "change_password", "resource": "account"}
    error = APIServerSideError(
        "Operation incomplete.",
        status_code=500,
        response_data={
            "error": {
                "code": "operation_incomplete",
                "message": "Operation incomplete.",
                "details": {"result": result},
            }
        },
    )
    assert error.operation_result == result
    assert error.committed is True
    assert "change was saved" in str(error)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status,code,committed",
    [(503, "unavailable", False), (500, "operation_incomplete", True)],
)
async def test_generated_transport_preserves_structured_failures_without_retries(
    status, code, committed
):
    import httpx

    from bsm_api_client import APIServerSideError

    calls = []
    result = (
        {"committed": True, "action": "update_account", "resource": "account"}
        if committed
        else None
    )

    async def respond(request):
        calls.append(request)
        return httpx.Response(
            status,
            json={
                "error": {
                    "code": code,
                    "message": "Operation unavailable or incomplete.",
                    "details": {"result": result} if result else {},
                }
            },
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as transport:
        async with BedrockServerManagerApi(
            "http://localhost", jwt_token="token", http_client=transport
        ) as client:
            with pytest.raises(APIServerSideError) as error:
                await client.rest.get_settings()
            assert error.value.api_code == code
            assert error.value.operation_result == result
            assert error.value.committed is committed
    assert len(calls) == 1


@pytest.mark.asyncio
async def test_event_catalog_filters_and_shutdown_receipt_use_generated_contracts(
    local_api,
):
    from bsm_api_client.models import (
        EventCatalog,
        EventDiagnostics,
        RuntimeStatus,
        ShutdownResponse,
    )

    client, seen = local_api
    assert isinstance(await client.events.async_list_application_events(), EventCatalog)
    activity = await client.events.async_get_event_activity(
        owner="plugin:example", correlation_id="operation-1", status="partial", limit=5
    )
    assert isinstance(activity, EventDiagnostics)
    assert (
        "activity",
        {
            "owner": "plugin:example",
            "correlation_id": "operation-1",
            "status": "partial",
            "limit": "5",
        },
    ) in seen
    assert isinstance(await client.application.async_get_web_runtime(), RuntimeStatus)
    receipt = await client.application.async_shutdown_web_runtime()
    assert isinstance(receipt, ShutdownResponse)
    assert receipt.status == "accepted" and receipt.phase == "stopping"
    assert ("shutdown", {}, None) in seen
    assert not hasattr(receipt, "task_id")


@pytest.mark.asyncio
@pytest.mark.parametrize("interface", ["rest", "application"])
@pytest.mark.parametrize("instance_id,ready", [("runtime-1", True), (None, False)])
async def test_health_response_preserves_process_identity(
    interface, instance_id, ready
):
    import httpx

    from bsm_api_client.models import GetApplicationHealthResponse

    payload = {
        "pid": 123,
        "instance_id": instance_id,
        "version": "4.0.0b8",
        "ready": ready,
        "lifecycle": "ready" if ready else "stopping",
        "health": "healthy" if ready else "degraded",
        "checks": {"lifecycle": {"healthy": ready, "message": "Lifecycle check"}},
        "checked_at": 1.0,
    }

    async def respond(request):
        assert request.url.path == "/api/health"
        assert request.headers["Authorization"] == "Bearer token"
        assert "X-BSM-Readiness-Token" not in request.headers
        return httpx.Response(200, json=payload)

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as transport:
        async with BedrockServerManagerApi(
            "http://localhost", jwt_token="token", http_client=transport
        ) as client:
            response = (
                await client.rest.get_application_health()
                if interface == "rest"
                else await client.application.async_get_application_health()
            )
            assert isinstance(response, GetApplicationHealthResponse)
            assert response.pid == 123
            assert response.instance_id == instance_id
            assert response.version == "4.0.0b8"
            assert response.ready is ready
            assert response.checks["lifecycle"].healthy is ready
