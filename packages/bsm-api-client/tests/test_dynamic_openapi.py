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
        form_data=None,
        authenticated=True,
    )


def test_missing_path_parameter_is_rejected():
    with pytest.raises(ValueError, match="server_name"):
        DummyClient._render_path("/server/{server_name}/start", {})


@pytest.mark.asyncio
async def test_openapi_discovery_uses_configured_api_base_path():
    client = DummyClient()
    client._base_url = "http://localhost/custom-api"
    client._api_base_segment = "/custom-api"
    client._dynamic_request = AsyncMock(return_value={"paths": {}})
    schema = await client._fetch_openapi_schema()
    assert schema == {"paths": {}}
    client._dynamic_request.assert_awaited_once_with(
        "GET", "/custom-api/openapi.json", authenticated=True
    )


@pytest.mark.asyncio
async def test_generated_client_bridge_reuses_token(monkeypatch):
    client = DummyClient()
    client._verify_ssl = False
    captured = {}

    class GeneratedClient:
        def __init__(self, **kwargs):
            captured.update(kwargs)

        def set_async_httpx_client(self, transport):
            self.transport = transport

    generated = ModuleType("bsm_api_client.generated")
    generated.AuthenticatedClient = GeneratedClient
    monkeypatch.setitem(sys.modules, "bsm_api_client.generated", generated)

    result = await client.async_get_generated_client()

    assert isinstance(result, GeneratedClient)
    await result.transport.aclose()
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
