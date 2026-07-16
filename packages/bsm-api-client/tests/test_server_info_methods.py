# tests/test_server_info_methods.py
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio

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
                {
                    "name": "server1",
                    "status": "RUNNING",
                    "version": "1.0.0",
                    "player_count": 0,
                },
                {
                    "name": "server2",
                    "status": "STOPPED",
                    "version": "1.0.1",
                    "player_count": 0,
                },
            ],
        }
        result = await client.async_get_servers()
        mock_request.assert_called_once_with("GET", "/servers", authenticated=True)
        assert len(result.servers) == 2
        assert result.servers[0].name == "server1"


@pytest.mark.asyncio
async def test_get_server_names(client):
    """Test async_get_server_names method."""
    with patch.object(
        client, "async_get_servers", new_callable=AsyncMock
    ) as mock_details:
        from collections import namedtuple

        ServerMock = namedtuple(
            "ServerMock", ["name", "status", "version", "player_count"]
        )
        mock_details.return_value.servers = [
            ServerMock(
                name="server2", status="STOPPED", version="1.0.1", player_count=0
            ),
            ServerMock(
                name="server1", status="RUNNING", version="1.0.0", player_count=0
            ),
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
async def test_get_server_summary(client):
    """Test async_get_server_summary method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {
            "name": "server1",
            "status": "RUNNING",
            "version": "1.0.0",
            "player_count": 5,
            "players": [{"name": "player1", "xuid": "123"}],
        }
        result = await client.async_get_server_summary("server1")
        mock_request.assert_called_once_with(
            "GET", "/server/server1/summary", authenticated=True
        )
        assert result.name == "server1"
        assert result.status == "RUNNING"
        assert result.player_count == 5


@pytest.mark.asyncio
async def test_get_server_process_info(client):
    """Test async_get_server_process_info method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {
            "status": "success",
            "process_info": {"pid": 123},
        }
        result = await client.async_get_server_process_info("test-server")
        mock_request.assert_called_once_with(
            "GET", "/server/test-server/process_info", authenticated=True
        )
        assert result.process_info["pid"] == 123


@pytest.mark.asyncio
async def test_get_server_running_status(client):
    """Test async_get_server_running_status method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {"status": "success", "running": True}
        result = await client.async_get_server_running_status("test-server")
        mock_request.assert_called_once_with(
            "GET", "/server/test-server/status", authenticated=True
        )
        assert result.running is True


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
        mock_request.return_value = {"status": "success", "permissions": []}
        result = await client.async_get_server_permissions_data("test-server")
        mock_request.assert_called_once_with(
            "GET", "/server/test-server/permissions/get", authenticated=True
        )
        assert result.permissions == []


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
