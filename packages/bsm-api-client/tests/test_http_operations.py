"""Public operation workflows against a real HTTP service."""

import asyncio
import copy

import aiohttp
import pytest
import pytest_asyncio
from aiohttp import web

from bsm_api_client import (
    BedrockServerManagerApi,
    compatibility_report,
    schema_fingerprint,
)
from bsm_api_client.exceptions import APIError, AuthError, InvalidInputError

STATE = web.AppKey("state", dict)


async def operation(request):
    state = request.app[STATE]
    state["requests"].append((request.path, request.headers.get("Authorization")))
    if (
        request.path == "/unauthorized"
        or request.headers.get("Authorization") == "Bearer expired"
    ):
        return web.json_response({"detail": "expired"}, status=401)
    if request.path == "/binary":
        return web.Response(
            body=b"0123456789" * 100000, content_type="application/octet-stream"
        )
    if request.path == "/text":
        return web.Response(text="123")
    if request.path == "/invalid":
        return web.Response(text="{invalid", content_type="application/json")
    if request.path == "/redirect":
        raise web.HTTPFound("/text")
    if request.path == "/query":
        return web.json_response(
            {
                "names": request.query.getall("names", []),
                "enabled": request.query.get("enabled"),
            }
        )
    if request.path == "/upload":
        reader = await request.multipart()
        parts = []
        while (part := await reader.next()) is not None:
            parts.append(
                {
                    "name": part.name,
                    "filename": part.filename,
                    "type": part.headers.get("Content-Type"),
                    "data": (await part.read()).decode(),
                }
            )
        return web.json_response(parts)
    return web.json_response(await request.json())


@pytest_asyncio.fixture
async def service():
    state = {"fetches": 0, "logins": 0, "requests": []}
    schema = {
        "openapi": "3.1.0",
        "security": [{"bearer": []}],
        "components": {
            "schemas": {
                "Input": {
                    "type": "object",
                    "required": ["count"],
                    "additionalProperties": False,
                    "properties": {"count": {"type": "integer", "minimum": 1}},
                }
            },
            "requestBodies": {
                "Input": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Input"}
                        }
                    },
                }
            },
        },
        "paths": {
            "/extension": {
                "post": {
                    "operationId": "extension",
                    "x-bsm-plugin": "custom",
                    "requestBody": {"$ref": "#/components/requestBodies/Input"},
                }
            },
            "/binary": {"get": {"operationId": "binary"}},
            "/text": {"get": {"operationId": "text"}},
            "/invalid": {"get": {"operationId": "invalid"}},
            "/redirect": {"get": {"operationId": "redirect"}},
            "/query": {"get": {"operationId": "query"}},
            "/upload": {
                "post": {
                    "operationId": "upload",
                    "requestBody": {
                        "content": {
                            "multipart/form-data": {"schema": {"type": "object"}}
                        }
                    },
                }
            },
            "/unauthorized": {"get": {"operationId": "unauthorized"}},
        },
    }
    schema["paths"]["/auth/token"] = {"post": {"operationId": "login", "security": []}}
    state["schema"] = schema

    async def contract(request):
        state["fetches"] += 1
        await asyncio.sleep(0.01)
        if state.get("broken"):
            return web.json_response({"paths": []})
        return web.json_response(state["schema"])

    async def login(request):
        state["logins"] += 1
        return web.json_response({"access_token": "fresh", "token_type": "bearer"})

    app = web.Application()
    app[STATE] = state
    app.router.add_get("/api/openapi.json", contract)
    app.router.add_post("/auth/token", login)
    for path, item in schema["paths"].items():
        if path == "/auth/token":
            continue
        app.router.add_route(next(iter(item)).upper(), path, operation)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 0)
    await site.start()
    url = f"http://127.0.0.1:{runner.addresses[0][1]}"
    async with BedrockServerManagerApi(
        url, username="admin", password="password", jwt_token="fresh"
    ) as client:
        try:
            yield client, state
        finally:
            await runner.cleanup()


@pytest.mark.asyncio
async def test_discovery_coalesces_refreshes_and_keeps_last_valid_snapshot(service):
    client, state = service
    await asyncio.gather(*(client.async_discover_api() for _ in range(10)))
    assert state["fetches"] == 1
    previous = client.schema_fingerprint
    state["schema"]["info"] = {"version": "2"}
    await asyncio.gather(*(client.async_discover_api(force=True) for _ in range(10)))
    assert state["fetches"] == 2
    assert client.schema_fingerprint != previous
    snapshot = copy.deepcopy(client.schema)
    state["broken"] = True
    with pytest.raises(APIError):
        await client.async_refresh_api()
    assert client.schema == snapshot
    assert "extension" in client.plugin_operations["custom"][0].operation_id


@pytest.mark.asyncio
async def test_nested_referenced_validation_rejects_inputs_before_http(service):
    client, state = service
    await client.async_discover_api()
    for body in [{"count": 0}, {"count": "secret"}, {"count": 1, "extra": True}]:
        with pytest.raises(InvalidInputError) as error:
            await client.async_call_operation("extension", json_data=body)
        assert "secret" not in str(error.value)
    assert not state["requests"]
    assert await client.async_call_operation("extension", json_data={"count": 1}) == {
        "count": 1
    }


@pytest.mark.asyncio
async def test_response_types_repeated_query_and_redirect_policy(service):
    client, _ = service
    assert await client.async_call_operation("text") == "123"
    assert (await client.async_call_operation("binary"))[:10] == b"0123456789"
    assert await client.async_call_operation(
        "query", query={"names": ["a", "b"], "enabled": False}
    ) == {"names": ["a", "b"], "enabled": "false"}
    with pytest.raises(APIError, match="malformed JSON"):
        await client.async_call_operation("invalid")
    with pytest.raises(APIError, match="redirect"):
        await client.async_call_operation("redirect")


@pytest.mark.asyncio
async def test_streaming_release_and_shared_authentication(service):
    client, state = service
    await client.async_discover_api()
    client._jwt_token = "expired"
    async with client.async_stream_operation("binary") as response:
        assert (await anext(response.aiter_bytes()))[:10] == b"0123456789"
    assert response.is_closed
    assert state["logins"] == 1
    assert await client.async_call_operation("text") == "123"
    with pytest.raises(InvalidInputError, match="GET"):
        async with client.async_stream_operation("extension"):
            pass


@pytest.mark.asyncio
async def test_authentication_retries_once_and_never_replays_uploads(service):
    client, state = service
    await client.async_discover_api()
    with pytest.raises(AuthError):
        await client.async_call_operation("unauthorized")
    assert state["logins"] == 1
    assert len(state["requests"]) == 2
    client._jwt_token = "expired"
    with pytest.raises(AuthError):
        await client.async_call_operation(
            "upload", files={"files": ("one.txt", b"one", "text/plain")}
        )
    assert state["logins"] == 1
    assert len(state["requests"]) == 3


@pytest.mark.asyncio
async def test_multiple_files_and_form_fields_preserve_metadata_and_stream_position(
    service, tmp_path
):
    client, _ = service
    path = tmp_path / "test.txt"
    path.write_bytes(b"skipremaining")
    with path.open("rb") as stream:
        stream.seek(4)
        result = await client.async_call_operation(
            "upload",
            form_data={"enabled": True},
            files={
                "files": [
                    ("first.txt", stream, "text/plain"),
                    ("second.bin", b"two", "application/octet-stream"),
                ]
            },
        )
    assert result[0]["data"] == "true"
    assert result[1]["data"] == "remaining"
    assert result[1]["filename"] == "first.txt"
    assert result[2]["type"] == "application/octet-stream"


@pytest.mark.asyncio
async def test_external_session_remains_open_on_client_close(service):
    client, _ = service
    async with aiohttp.ClientSession() as session:
        borrowed = BedrockServerManagerApi(
            client._server_root_url, jwt_token="fresh", session=session
        )
        await borrowed.async_call_path("GET", "/text")
        await borrowed.close()
        await borrowed.close()
        assert not session.closed


def test_compatibility_classifies_add_remove_metadata_and_model_changes():
    before = {"paths": {"/one": {"get": {"operationId": "one", "summary": "old"}}}}
    after = copy.deepcopy(before)
    after["paths"]["/one"]["get"]["summary"] = "new"
    assert (
        compatibility_report(before, after)["changes"][0]["severity"] == "informational"
    )
    after["paths"]["/one"]["get"]["security"] = [{"bearer": []}]
    assert not compatibility_report(before, after)["compatible"]
    assert (
        compatibility_report({"paths": {}}, before)["changes"][0]["severity"]
        == "additive"
    )
    assert not compatibility_report(before, {"paths": {}})["compatible"]
    assert schema_fingerprint(before) == schema_fingerprint(
        dict(reversed(list(before.items())))
    )


@pytest.mark.asyncio
async def test_form_only_multipart_uses_advertised_encoding(service):
    client, _ = service
    result = await client.async_call_operation(
        "upload", form_data={"enabled": True, "names": ["a", "b"]}
    )
    assert [part["data"] for part in result] == ["true", "a", "b"]


@pytest.mark.asyncio
async def test_cli_download_streams_and_preserves_destination_on_failure(
    service, tmp_path
):
    import json
    import os
    import sys

    client, _ = service
    output = tmp_path / "download.bin"
    env = {
        **os.environ,
        "BSM_BASE_URL": client._server_root_url,
        "BSM_JWT_TOKEN": "fresh",
    }

    async def run(identifier):
        process = await asyncio.create_subprocess_exec(
            sys.executable,
            "-m",
            "bsm_cli",
            "--json",
            "api",
            "download",
            identifier,
            str(output),
            env=env,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(process.communicate(), 15)
        return process.returncode, stdout, stderr

    code, stdout, stderr = await run("binary")
    assert code == 0, stderr
    assert json.loads(stdout)["bytes"] == 1000000
    assert output.read_bytes() == b"0123456789" * 100000
    code, stdout, stderr = await run("unauthorized")
    assert code == 3, stderr
    assert not stdout
    assert output.stat().st_size == 1000000
    assert not list(tmp_path.glob(".bsm-download-*"))


@pytest.mark.parametrize(
    "content_type,expected",
    [
        ("text/plain", "123"),
        ("application/octet-stream", b"123"),
        ("application/json", 123),
    ],
)
def test_generated_response_decoding_matches_dynamic_content_types(
    content_type, expected
):
    from types import SimpleNamespace

    from bsm_api_client.generated_adapter import response_value

    assert (
        response_value(
            SimpleNamespace(
                content=b"123", headers={"content-type": content_type}, status_code=200
            )
        )
        == expected
    )


@pytest.mark.asyncio
async def test_concurrent_401s_share_refresh_even_when_server_reissues_identical_token(
    service,
):
    client, state = service
    await client.async_discover_api()
    results = await asyncio.gather(
        *(client.async_call_operation("unauthorized") for _ in range(5)),
        return_exceptions=True,
    )
    assert all(isinstance(result, AuthError) for result in results)
    assert state["logins"] == 1
    assert len(state["requests"]) == 10
