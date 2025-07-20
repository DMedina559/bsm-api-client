# tests/test_scheduler_methods.py
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch
from bsm_api_client.api_client import BedrockServerManagerApi

@pytest_asyncio.fixture
async def client():
    """Async fixture for a BedrockServerManagerApi instance."""
    client = BedrockServerManagerApi("localhost", "admin", "password")
    yield client
    await client.close()

@pytest.mark.asyncio
async def test_add_server_cron_job(client):
    """Test async_add_server_cron_job method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {"status": "success", "message": "Cron job added."}
        result = await client.async_add_server_cron_job("test-server", "* * * * * command")
        mock_request.assert_called_once_with(
            "POST",
            "/server/test-server/cron_scheduler/add",
            json_data={"new_cron_job": "* * * * * command"},
            authenticated=True,
        )
        assert result["status"] == "success"

@pytest.mark.asyncio
async def test_modify_server_cron_job(client):
    """Test async_modify_server_cron_job method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {"status": "success", "message": "Cron job modified."}
        result = await client.async_modify_server_cron_job(
            "test-server", "* * * * * old_command", "* * * * * new_command"
        )
        mock_request.assert_called_once_with(
            "POST",
            "/server/test-server/cron_scheduler/modify",
            json_data={
                "old_cron_job": "* * * * * old_command",
                "new_cron_job": "* * * * * new_command",
            },
            authenticated=True,
        )
        assert result["status"] == "success"

@pytest.mark.asyncio
async def test_delete_server_cron_job(client):
    """Test async_delete_server_cron_job method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {"status": "success", "message": "Cron job deleted."}
        result = await client.async_delete_server_cron_job("test-server", "* * * * * command")
        mock_request.assert_called_once_with(
            "DELETE",
            "/server/test-server/cron_scheduler/delete",
            params={"cron_string": "* * * * * command"},
            authenticated=True,
        )
        assert result["status"] == "success"

@pytest.mark.asyncio
async def test_add_server_windows_task(client):
    """Test async_add_server_windows_task method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {"status": "success", "message": "Task added."}
        triggers = [{"type": "daily", "time": "12:00"}]
        result = await client.async_add_server_windows_task(
            "test-server", "server start", triggers
        )
        mock_request.assert_called_once_with(
            "POST",
            "/server/test-server/task_scheduler/add",
            json_data={"command": "server start", "triggers": triggers},
            authenticated=True,
        )
        assert result["status"] == "success"

@pytest.mark.asyncio
async def test_modify_server_windows_task(client):
    """Test async_modify_server_windows_task method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {"status": "success", "message": "Task modified."}
        triggers = [{"type": "daily", "time": "13:00"}]
        result = await client.async_modify_server_windows_task(
            "test-server", "test-task", "server stop", triggers
        )
        mock_request.assert_called_once_with(
            "PUT",
            "/server/test-server/task_scheduler/task/test-task",
            json_data={"command": "server stop", "triggers": triggers},
            authenticated=True,
        )
        assert result["status"] == "success"

@pytest.mark.asyncio
async def test_delete_server_windows_task(client):
    """Test async_delete_server_windows_task method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {"status": "success", "message": "Task deleted."}
        result = await client.async_delete_server_windows_task("test-server", "test-task")
        mock_request.assert_called_once_with(
            "DELETE",
            "/server/test-server/task_scheduler/task/test-task",
            authenticated=True,
        )
        assert result["status"] == "success"
