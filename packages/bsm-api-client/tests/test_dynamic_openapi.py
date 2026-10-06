"""Tests for runtime OpenAPI discovery."""

import sys
from types import ModuleType
from unittest.mock import AsyncMock, MagicMock

import pytest

from bsm_api_client.dynamic import DynamicOpenAPIMixin


class DummyClient(DynamicOpenAPIMixin):
    def __init__(self):
        self._default_headers = {"Accept": "application/json"}
        self._jwt_token = "token"
        self._server_root_url = "http://localhost"
        self._request_timeout = 90
        self._session = MagicMock()


def test_indexes_core_and_plugin_operations():
    schema = {
        "paths": {
            "/api/server/{server_name}/start": {
                "post": {"operationId": "start_server", "tags": ["servers"]}
            },
            "/plugins/demo/status": {
                "get": {"operationId": "demo_status", "tags": ["plugin:demo"]}
            },
        }
    }
    operations = DummyClient._index_operations(schema)
    assert operations["start_server"].method == "POST"
    assert operations["demo_status"].path == "/plugins/demo/status"


@pytest.mark.asyncio
async def test_discovery_groups_plugin_routes():
    client = DummyClient()
    client._fetch_openapi_schema = AsyncMock(
        return_value={
            "openapi": "3.1.0",
            "paths": {
                "/plugins/demo/status": {
                    "get": {
                        "operationId": "demo_status",
                        "tags": ["plugin:demo"],
                    }
                }
            },
        }
    )
    await client.async_discover_api()
    assert client.schema_fingerprint
    assert client.plugins["demo"][0].operation_id == "demo_status"


@pytest.mark.asyncio
async def test_dynamic_operation_renders_path_and_forwards_payload():
    client = DummyClient()
    client._fetch_openapi_schema = AsyncMock(
        return_value={
            "paths": {
                "/plugins/demo/server/{server_name}": {
                    "post": {
                        "operationId": "demo_server_action",
                        "tags": ["plugin:demo"],
                    }
                }
            }
        }
    )
    client._dynamic_request = AsyncMock(return_value={"status": "success"})
    result = await client.async_call_operation(
        "demo_server_action",
        path_params={"server_name": "My Server"},
        query={"force": True},
        json_data={"value": 1},
    )
    assert result == {"status": "success"}
    client._dynamic_request.assert_awaited_once_with(
        "POST",
        "/plugins/demo/server/My%20Server",
        query={"force": True},
        json_data={"value": 1},
        headers=None,
        authenticated=True,
    )


def test_missing_path_parameter_is_rejected():
    with pytest.raises(ValueError, match="server_name"):
        DummyClient._render_path("/server/{server_name}/start", {})


@pytest.mark.asyncio
async def test_openapi_discovery_uses_configured_api_base_path():
    client = DummyClient()
    client._base_url = "http://localhost/custom-api"
    response = AsyncMock()
    response.status = 200
    response.ok = True
    response.json = AsyncMock(return_value={"paths": {}})
    context = AsyncMock()
    context.__aenter__.return_value = response
    context.__aexit__.return_value = None
    client._session.get.return_value = context

    schema = await client._fetch_openapi_schema()

    assert schema == {"paths": {}}
    client._session.get.assert_called_once_with(
        "http://localhost/custom-api/openapi.json",
        headers={"Accept": "application/json", "Authorization": "Bearer token"},
        timeout=90,
    )


@pytest.mark.asyncio
async def test_generated_client_bridge_reuses_token(monkeypatch):
    client = DummyClient()
    client._verify_ssl = False
    captured = {}

    class GeneratedClient:
        def __init__(self, **kwargs):
            captured.update(kwargs)

    generated = ModuleType("bsm_api_client.generated")
    generated.AuthenticatedClient = GeneratedClient
    monkeypatch.setitem(sys.modules, "bsm_api_client.generated", generated)

    result = await client.async_get_generated_client()

    assert isinstance(result, GeneratedClient)
    assert captured == {
        "base_url": "http://localhost",
        "token": "token",
        "verify_ssl": False,
    }


@pytest.mark.asyncio
async def test_compat_request_uses_openapi_transport():
    from bsm_api_client.api_client import BedrockServerManagerApi

    client = BedrockServerManagerApi("http://localhost", jwt_token="token")
    try:
        client._dynamic_request = AsyncMock(return_value={"status": "success"})
        result = await client._request(
            "POST",
            "/server/example/start",
            json_data={"force": True},
            params={"wait": "1"},
        )
        assert result == {"status": "success"}
        client._dynamic_request.assert_awaited_once_with(
            "POST",
            "/api/server/example/start",
            query={"wait": "1"},
            json_data={"force": True},
            headers=None,
            authenticated=True,
            is_retry=False,
        )
    finally:
        await client.close()
