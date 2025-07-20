# tests/test_api_client.py
import pytest
from unittest.mock import AsyncMock, patch
from bsm_api_client.api_client import BedrockServerManagerApi
from bsm_api_client.exceptions import APIError, CannotConnectError
from bsm_api_client.models import (
    InstallServerPayload,
    PropertiesPayload,
    PermissionsSetPayload,
    PlayerPermissionItem,
)

import pytest_asyncio


@pytest_asyncio.fixture
async def client():
    """Async fixture for a BedrockServerManagerApi instance."""
    client = BedrockServerManagerApi("localhost", "admin", "password")
    yield client
    await client.close()


@pytest.mark.asyncio
async def test_get_custom_zips(client):
    """Test get_custom_zips method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {
            "status": "success",
            "files": ["zip1.zip", "zip2.zip"],
        }
        result = await client.async_get_custom_zips()
        mock_request.assert_called_once_with(
            method="GET", path="/downloads/list", authenticated=True
        )
        assert result["files"] == ["zip1.zip", "zip2.zip"]


@pytest.mark.asyncio
async def test_get_themes(client):
    """Test get_themes method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {
            "status": "success",
            "themes": {"dark": "dark.css"},
        }
        result = await client.async_get_themes()
        mock_request.assert_called_once_with(
            method="GET", path="/themes", authenticated=True
        )
        assert result["themes"] == {"dark": "dark.css"}


@pytest.mark.asyncio
async def test_prune_server_backups(client):
    """Test async_prune_server_backups method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {
            "status": "success",
            "message": "Pruning initiated.",
        }
        result = await client.async_prune_server_backups("test-server")
        mock_request.assert_called_once_with(
            "POST",
            "/server/test-server/backups/prune",
            json_data=None,
            authenticated=True,
        )
        assert result["status"] == "success"


@pytest.mark.asyncio
async def test_set_server_permissions(client):
    """Test async_set_server_permissions method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        permissions = [
            PlayerPermissionItem(xuid="123", name="player1", permission_level="member"),
            PlayerPermissionItem(
                xuid="456", name="player2", permission_level="operator"
            ),
        ]
        payload = PermissionsSetPayload(permissions=permissions)
        mock_request.return_value = {
            "status": "success",
            "message": "Permissions updated.",
        }
        result = await client.async_set_server_permissions("test-server", payload)
        mock_request.assert_called_once_with(
            "PUT",
            "/server/test-server/permissions/set",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        assert result["status"] == "success"


@pytest.mark.asyncio
async def test_update_server_properties(client):
    """Test async_update_server_properties method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        properties = {"level-name": "new-world", "gamemode": "survival"}
        payload = PropertiesPayload(properties=properties)
        mock_request.return_value = {
            "status": "success",
            "message": "Properties updated.",
        }
        result = await client.async_update_server_properties("test-server", payload)
        mock_request.assert_called_once_with(
            "POST",
            "/server/test-server/properties/set",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        assert result["status"] == "success"


@pytest.mark.asyncio
async def test_reload_plugins(client):
    """Test async_reload_plugins method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {
            "status": "success",
            "message": "Plugins reloaded.",
        }
        result = await client.async_reload_plugins()
        mock_request.assert_called_once_with(
            method="PUT", path="/plugins/reload", authenticated=True
        )
        assert result["status"] == "success"
