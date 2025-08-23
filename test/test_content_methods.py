# tests/test_content_methods.py
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from bsm_api_client.api_client import BedrockServerManagerApi
from bsm_api_client.models import (
    RestoreTypePayload,
    BackupActionPayload,
    RestoreActionPayload,
    FileNamePayload,
)


@pytest_asyncio.fixture
async def client():
    """Async fixture for a BedrockServerManagerApi instance."""
    client = BedrockServerManagerApi("http://localhost", "admin", "password")
    yield client
    await client.close()


@pytest.mark.asyncio
async def test_list_server_backups(client):
    """Test async_list_server_backups method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {"status": "success", "backups": ["backup1.zip"]}
        result = await client.async_list_server_backups("test-server", "world")
        mock_request.assert_called_once_with(
            "GET", "/server/test-server/backup/list/world", authenticated=True
        )
        assert len(result.backups) == 1


@pytest.mark.asyncio
async def test_restore_select_backup_type(client):
    """Test async_restore_select_backup_type method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        payload = RestoreTypePayload(restore_type="world")
        mock_request.return_value = {"status": "success", "redirect_url": "/some/url"}
        result = await client.async_restore_select_backup_type("test-server", payload)
        mock_request.assert_called_once_with(
            method="POST",
            path="/server/test-server/restore/select_backup_type",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        assert result.redirect_url == "/some/url"


@pytest.mark.asyncio
async def test_get_content_worlds(client):
    """Test async_get_content_worlds method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {"status": "success", "files": ["world1.mcworld"]}
        result = await client.async_get_content_worlds()
        mock_request.assert_called_once_with(
            "GET", "/content/worlds", authenticated=True
        )
        assert len(result.files) == 1


@pytest.mark.asyncio
async def test_get_content_addons(client):
    """Test async_get_content_addons method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {"status": "success", "files": ["addon1.mcaddon"]}
        result = await client.async_get_content_addons()
        mock_request.assert_called_once_with(
            "GET", "/content/addons", authenticated=True
        )
        assert len(result.files) == 1


@pytest.mark.asyncio
async def test_trigger_server_backup(client):
    """Test async_trigger_server_backup method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        payload = BackupActionPayload(backup_type="all")
        mock_request.return_value = {
            "status": "success",
            "message": "Backup triggered.",
        }
        result = await client.async_trigger_server_backup("test-server", payload)
        mock_request.assert_called_once_with(
            "POST",
            "/server/test-server/backup/action",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        assert result.status == "success"


@pytest.mark.skip(reason="Content uploader is a disabled-by-default plugin")
@pytest.mark.skip(reason="Content uploader is a disabled-by-default plugin")
@pytest.mark.asyncio
async def test_upload_content(client):
    """Test async_upload_content method."""
    with patch("aiohttp.FormData", new_callable=MagicMock) as mock_form_data:
        with patch.object(client, "_session") as mock_session:
            mock_session.post.return_value.__aenter__.return_value.status = 200
            mock_session.post.return_value.__aenter__.return_value.json = AsyncMock(
                return_value={"status": "success"}
            )

            with patch("builtins.open", new_callable=MagicMock) as mock_open:
                with patch("os.path.basename", return_value="test.zip"):
                    result = await client.async_upload_content("/fake/path/test.zip")
                    assert result["status"] == "success"
                    mock_session.post.assert_called_once()


@pytest.mark.asyncio
async def test_export_server_world(client):
    """Test async_export_server_world method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {
            "status": "success",
            "message": "Export triggered.",
        }
        result = await client.async_export_server_world("test-server")
        mock_request.assert_called_once_with(
            "POST",
            "/server/test-server/world/export",
            json_data=None,
            authenticated=True,
        )
        assert result.status == "success"


@pytest.mark.asyncio
async def test_reset_server_world(client):
    """Test async_reset_server_world method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {"status": "success", "message": "Reset triggered."}
        result = await client.async_reset_server_world("test-server")
        mock_request.assert_called_once_with(
            "DELETE",
            "/server/test-server/world/reset",
            json_data=None,
            authenticated=True,
        )
        assert result.status == "success"


@pytest.mark.asyncio
async def test_prune_server_backups(client):
    """Test async_prune_server_backups method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {
            "status": "success",
            "message": "Pruning triggered.",
        }
        result = await client.async_prune_server_backups("test-server")
        mock_request.assert_called_once_with(
            "POST",
            "/server/test-server/backups/prune",
            json_data=None,
            authenticated=True,
        )
        assert result.status == "success"


@pytest.mark.asyncio
async def test_restore_server_backup(client):
    """Test async_restore_server_backup method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        payload = RestoreActionPayload(restore_type="world", backup_file="backup1.zip")
        mock_request.return_value = {
            "status": "success",
            "message": "Restore triggered.",
        }
        result = await client.async_restore_server_backup("test-server", payload)
        mock_request.assert_called_once_with(
            "POST",
            "/server/test-server/restore/action",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        assert result.status == "success"


@pytest.mark.asyncio
async def test_restore_server_latest_all(client):
    """Test async_restore_server_latest_all method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {
            "status": "success",
            "message": "Restore triggered.",
        }
        result = await client.async_restore_server_latest_all("test-server")
        mock_request.assert_called_once_with(
            "POST",
            "/server/test-server/restore/action",
            json_data={"restore_type": "all"},
            authenticated=True,
        )
        assert result.status == "success"


@pytest.mark.asyncio
async def test_install_server_world(client):
    """Test async_install_server_world method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        payload = FileNamePayload(filename="world1.mcworld")
        mock_request.return_value = {
            "status": "success",
            "message": "Install triggered.",
        }
        result = await client.async_install_server_world("test-server", payload)
        mock_request.assert_called_once_with(
            "POST",
            "/server/test-server/world/install",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        assert result.status == "success"


@pytest.mark.asyncio
async def test_install_server_addon(client):
    """Test async_install_server_addon method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        payload = FileNamePayload(filename="addon1.mcaddon")
        mock_request.return_value = {
            "status": "success",
            "message": "Install triggered.",
        }
        result = await client.async_install_server_addon("test-server", payload)
        mock_request.assert_called_once_with(
            "POST",
            "/server/test-server/addon/install",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        assert result.status == "success"
