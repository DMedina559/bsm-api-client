# tests/test_manager_methods.py
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch
from bsm_api_client.api_client import BedrockServerManagerApi
from bsm_api_client.models import (
    AddPlayersPayload,
    SettingItem,
    PruneDownloadsPayload,
    InstallServerPayload,
)


@pytest_asyncio.fixture
async def client():
    """Async fixture for a BedrockServerManagerApi instance."""
    client = BedrockServerManagerApi("localhost", "admin", "password")
    yield client
    await client.close()


@pytest.mark.asyncio
async def test_get_info(client):
    """Test async_get_info method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {"status": "success", "info": {"version": "1.0.0"}}
        result = await client.async_get_info()
        mock_request.assert_called_once_with(
            method="GET", path="/info", authenticated=False
        )
        assert result["info"]["version"] == "1.0.0"


@pytest.mark.asyncio
async def test_scan_players(client):
    """Test async_scan_players method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {"status": "success", "message": "Scan complete."}
        result = await client.async_scan_players()
        mock_request.assert_called_once_with(
            method="POST", path="/players/scan", authenticated=True
        )
        assert result["status"] == "success"


@pytest.mark.asyncio
async def test_get_players(client):
    """Test async_get_players method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {
            "status": "success",
            "players": [{"name": "player1", "xuid": "123"}],
        }
        result = await client.async_get_players()
        mock_request.assert_called_once_with(
            method="GET", path="/players/get", authenticated=True
        )
        assert len(result["players"]) == 1
        assert result["players"][0]["name"] == "player1"


@pytest.mark.asyncio
async def test_add_players(client):
    """Test async_add_players method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        payload = AddPlayersPayload(players=["player1:123", "player2:456"])
        mock_request.return_value = {"status": "success", "message": "Players added."}
        result = await client.async_add_players(payload)
        mock_request.assert_called_once_with(
            method="POST",
            path="/players/add",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        assert result["status"] == "success"


@pytest.mark.asyncio
async def test_get_all_settings(client):
    """Test async_get_all_settings method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {
            "status": "success",
            "settings": {"web": {"port": 8080}},
        }
        result = await client.async_get_all_settings()
        mock_request.assert_called_once_with(
            method="GET", path="/settings", authenticated=True
        )
        assert result["settings"]["web"]["port"] == 8080


@pytest.mark.asyncio
async def test_set_setting(client):
    """Test async_set_setting method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        payload = SettingItem(key="web.port", value=8081)
        mock_request.return_value = {"status": "success", "message": "Setting updated."}
        result = await client.async_set_setting(payload)
        mock_request.assert_called_once_with(
            method="POST",
            path="/settings",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        assert result["status"] == "success"


@pytest.mark.asyncio
async def test_reload_settings(client):
    """Test async_reload_settings method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {
            "status": "success",
            "message": "Settings reloaded.",
        }
        result = await client.async_reload_settings()
        mock_request.assert_called_once_with(
            method="POST", path="/settings/reload", authenticated=True
        )
        assert result["status"] == "success"


@pytest.mark.asyncio
async def test_prune_downloads(client):
    """Test async_prune_downloads method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        payload = PruneDownloadsPayload(directory="stable", keep=2)
        mock_request.return_value = {
            "status": "success",
            "message": "Downloads pruned.",
        }
        result = await client.async_prune_downloads(payload)
        mock_request.assert_called_once_with(
            method="POST",
            path="/downloads/prune",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        assert result["status"] == "success"


@pytest.mark.asyncio
async def test_install_new_server(client):
    """Test async_install_new_server method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        payload = InstallServerPayload(
            server_name="test-server", server_version="LATEST", overwrite=True
        )
        mock_request.return_value = {
            "status": "success",
            "message": "Server installed.",
        }
        result = await client.async_install_new_server(payload)
        mock_request.assert_called_once_with(
            method="POST",
            path="/server/install",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        assert result["status"] == "success"
