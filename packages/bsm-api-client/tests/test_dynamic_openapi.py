"""Tests for runtime OpenAPI discovery."""

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
