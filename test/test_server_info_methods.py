# tests/test_server_info_methods.py
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch
from bsm_api_client.api_client import BedrockServerManagerApi
from bsm_api_client.exceptions import ServerNotFoundError


@pytest_asyncio.fixture
async def client():
    """Async fixture for a BedrockServerManagerApi instance."""
    client = BedrockServerManagerApi("http://localhost", "admin", "password")
    yield client
    await client.close()


@pytest.mark.asyncio
async def test_get_servers(client):
    """Test async_get_servers method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {
            "status": "success",
            "servers": [
                {"name": "server1", "status": "RUNNING", "version": "1.0.0"},
                {"name": "server2", "status": "STOPPED", "version": "1.0.1"},
            ],
        }
        result = await client.async_get_servers()
        mock_request.assert_called_once_with("GET", "/servers", authenticated=True)
        assert len(result.servers) == 2
        assert result.servers[0]["name"] == "server1"


@pytest.mark.asyncio
async def test_get_server_names(client):
    """Test async_get_server_names method."""
    with patch.object(
        client, "async_get_servers", new_callable=AsyncMock
    ) as mock_details:
        mock_details.return_value.servers = [
            {"name": "server2", "status": "STOPPED", "version": "1.0.1"},
            {"name": "server1", "status": "RUNNING", "version": "1.0.0"},
        ]
        result = await client.async_get_server_names()
        assert result == ["server1", "server2"]


@pytest.mark.asyncio
async def test_get_server_validate_success(client):
    """Test async_get_server_validate method for a successful validation."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {"status": "success"}
        result = await client.async_get_server_validate("test-server")
        mock_request.assert_called_once_with(
            "GET", "/server/test-server/validate", authenticated=True
        )
        assert result is True


@pytest.mark.asyncio
async def test_get_server_validate_not_found(client):
    """Test async_get_server_validate method for a server that is not found."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.side_effect = ServerNotFoundError("Server not found")
        with pytest.raises(ServerNotFoundError):
            await client.async_get_server_validate("unknown-server")


@pytest.mark.asyncio
async def test_get_server_process_info(client):
    """Test async_get_server_process_info method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {
            "status": "success",
            "data": {"process_info": {"pid": 123}},
        }
        result = await client.async_get_server_process_info("test-server")
        mock_request.assert_called_once_with(
            "GET", "/server/test-server/process_info", authenticated=True
        )
        assert result.data["process_info"]["pid"] == 123


@pytest.mark.asyncio
async def test_get_server_running_status(client):
    """Test async_get_server_running_status method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {"status": "success", "data": {"running": True}}
        result = await client.async_get_server_running_status("test-server")
        mock_request.assert_called_once_with(
            "GET", "/server/test-server/status", authenticated=True
        )
        assert result.data["running"] is True


@pytest.mark.asyncio
async def test_get_server_config_status(client):
    """Test async_get_server_config_status method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {
            "status": "success",
            "data": {"config_status": "RUNNING"},
        }
        result = await client.async_get_server_config_status("test-server")
        mock_request.assert_called_once_with(
            "GET", "/server/test-server/config_status", authenticated=True
        )
        assert result.data["config_status"] == "RUNNING"


@pytest.mark.asyncio
async def test_get_server_version(client):
    """Test async_get_server_version method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {"status": "success", "data": {"version": "1.0.0"}}
        result = await client.async_get_server_version("test-server")
        mock_request.assert_called_once_with(
            "GET", "/server/test-server/version", authenticated=True
        )
        assert result.data["version"] == "1.0.0"


@pytest.mark.asyncio
async def test_get_server_properties(client):
    """Test async_get_server_properties method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {
            "status": "success",
            "properties": {"level-name": "world"},
        }
        result = await client.async_get_server_properties("test-server")
        mock_request.assert_called_once_with(
            "GET", "/server/test-server/properties/get", authenticated=True
        )
        assert result.properties["level-name"] == "world"


@pytest.mark.asyncio
async def test_get_server_permissions_data(client):
    """Test async_get_server_permissions_data method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {"status": "success", "data": {"permissions": []}}
        result = await client.async_get_server_permissions_data("test-server")
        mock_request.assert_called_once_with(
            "GET", "/server/test-server/permissions/get", authenticated=True
        )
        assert result.data["permissions"] == []


@pytest.mark.asyncio
async def test_get_server_allowlist(client):
    """Test async_get_server_allowlist method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {"status": "success", "players": []}
        result = await client.async_get_server_allowlist("test-server")
        mock_request.assert_called_once_with(
            "GET", "/server/test-server/allowlist/get", authenticated=True
        )
        assert result.players == []
