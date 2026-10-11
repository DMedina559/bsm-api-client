from unittest.mock import AsyncMock, MagicMock, patch

import click
import pytest

from bsm_api_client.websocket_client import WebSocketClient
from bsm_cli.decorators import monitor_task
from bsm_cli.server import list_servers


@pytest.mark.parametrize("status", ["completed", "success"])
def test_typed_task_completion(status):
    from bsm_cli.decorators import _task_finished

    assert _task_finished({"status": status, "message": "Done"}, "Finished", "Failed")


@pytest.mark.parametrize("status", ["failed", "cancelled"])
def test_typed_task_failure(status):
    from bsm_api_client.exceptions import OperationFailedError
    from bsm_cli.decorators import _task_finished

    with pytest.raises(OperationFailedError, match="Server failed") as error:
        _task_finished(
            {
                "status": status,
                "message": "Task failed",
                "error": {"code": "server_error", "message": "Server failed"},
            },
            "Finished",
            "Failed",
        )
    assert error.value.api_code == "server_error"


@pytest.fixture
def mock_client():
    client = AsyncMock()
    # Mocking servers response
    server1 = {"name": "server1", "status": "RUNNING", "version": "1.0"}
    client.servers.async_get_servers.return_value = MagicMock(servers=[server1])
    # Mocking task response
    client.tasks.async_get_task_status.return_value = {
        "status": "success",
        "message": "Task done",
    }
    return client


@pytest.fixture
def mock_ws_client():
    ws_client = AsyncMock(spec=WebSocketClient)
    ws_client.connect.return_value = ws_client
    ws_client.subscribe = AsyncMock()

    # Mock context manager
    ws_client.__aenter__ = AsyncMock(return_value=ws_client)
    ws_client.__aexit__ = AsyncMock()

    return ws_client


@pytest.mark.asyncio
async def test_list_servers_websocket_flow(mock_client, mock_ws_client):
    mock_client.websocket_connect.return_value = mock_ws_client

    # Mock listen to yield one message then stop
    async def listen_mock():
        yield {"event": "status_updated"}

    mock_ws_client.listen.side_effect = listen_mock

    # Create a real Click Context
    ctx = click.Context(list_servers, obj={"client": mock_client})

    # Mock sleep to break the loop after WS finishes
    async def side_effect_sleep(seconds):
        raise KeyboardInterrupt("Break loop")

    with (
        patch("click.clear"),
        patch("click.secho"),
        patch("click.echo"),
        patch("asyncio.sleep", side_effect=side_effect_sleep) as mock_sleep,
    ):

        with ctx.scope():
            try:
                await list_servers.callback(loop=True, server_name=None)
            except KeyboardInterrupt:
                pass

    mock_client.websocket_connect.assert_called_once()

    mock_ws_client.subscribe.assert_any_call("event:after_server_statuses_updated")
    assert mock_client.servers.async_get_servers.call_count >= 2
    # Verify sleep was called (fallback triggered after WS finished)
    mock_sleep.assert_called()


@pytest.mark.asyncio
async def test_list_servers_fallback(mock_client):
    mock_client.websocket_connect.side_effect = Exception("Connection failed")

    ctx = click.Context(list_servers, obj={"client": mock_client})

    async def side_effect_sleep(seconds):
        raise KeyboardInterrupt("Break loop")

    with (
        patch("click.clear"),
        patch("click.secho"),
        patch("click.echo"),
        patch("asyncio.sleep", side_effect=side_effect_sleep) as mock_sleep,
    ):

        with ctx.scope():
            try:
                await list_servers.callback(loop=True, server_name=None)
            except KeyboardInterrupt:
                pass

    mock_client.websocket_connect.assert_called_once()
    mock_sleep.assert_called()
    assert mock_client.servers.async_get_servers.call_count >= 1


@pytest.mark.asyncio
async def test_monitor_task_websocket(mock_client, mock_ws_client):
    mock_client.websocket_connect.return_value = mock_ws_client

    mock_client.tasks.async_get_task_status.return_value = {"status": "running"}
    task_id = "123"
    msg = {
        "type": "task_update",
        "topic": f"task:{task_id}",
        "data": {"status": "success", "message": "Done"},
    }

    async def listen_mock():
        yield msg

    mock_ws_client.listen.side_effect = listen_mock

    with patch("click.secho") as mock_secho, patch("click.echo"):
        await monitor_task(mock_client, task_id, "Success", "Failure")

    mock_client.websocket_connect.assert_called_once()
    mock_secho.assert_called_with("Success: Done", fg="green")


@pytest.mark.asyncio
async def test_monitor_task_fallback(mock_client):
    mock_client.websocket_connect.side_effect = Exception("WS Failed")
    mock_client.tasks.async_get_task_status.return_value = {
        "status": "success",
        "message": "Done via poll",
    }

    with (
        patch("click.secho") as mock_secho,
        patch("click.echo"),
        patch("asyncio.sleep"),
    ):  # Mock sleep to run immediately
        await monitor_task(mock_client, "123", "Success", "Failure")

    mock_client.websocket_connect.assert_called_once()
    mock_client.tasks.async_get_task_status.assert_called_once_with("123")
    mock_secho.assert_any_call(
        "WebSocket monitoring failed (WS Failed), falling back to polling...",
        fg="yellow",
    )
    mock_secho.assert_any_call("Success: Done via poll", fg="green")


@pytest.mark.asyncio
async def test_monitor_task_propagates_failed_background_result(mock_client):
    from bsm_api_client.exceptions import OperationFailedError

    mock_client.websocket_connect.side_effect = Exception("WS Failed")
    mock_client.tasks.async_get_task_status.return_value = {
        "status": "success",
        "message": "Task completed",
        "result": {"status": "error", "message": "Install failed"},
    }
    with pytest.raises(OperationFailedError, match="Install failed"):
        await monitor_task(mock_client, "123", "Success", "Failure")


@pytest.mark.asyncio
async def test_task_already_finished_at_subscription(mock_client, mock_ws_client):
    mock_client.websocket_connect.return_value = mock_ws_client
    await monitor_task(mock_client, "123", "Success", "Failure")
    mock_ws_client.subscribe.assert_awaited_once_with("task:123")
    mock_client.tasks.async_get_task_status.assert_awaited_once_with("123")
    mock_ws_client.listen.assert_not_called()


@pytest.mark.asyncio
async def test_idle_task_socket_falls_back_to_rest(
    mock_client, mock_ws_client, monkeypatch
):
    import asyncio

    mock_client.websocket_connect.return_value = mock_ws_client
    mock_client.tasks.async_get_task_status.side_effect = [
        {"status": "running", "message": "Running"},
        {"status": "completed", "message": "Done"},
    ]

    async def listen():
        await asyncio.Event().wait()
        yield {}

    async def timeout(awaitable, timeout):
        awaitable.close()
        raise TimeoutError()

    mock_ws_client.listen.side_effect = listen
    monkeypatch.setattr("bsm_cli.decorators.asyncio.wait_for", timeout)
    await monitor_task(mock_client, "123", "Success", "Failure")
    assert mock_client.tasks.async_get_task_status.await_count == 2
    mock_ws_client.__aexit__.assert_awaited_once()


@pytest.mark.asyncio
async def test_task_poll_recovers_after_connection_loss(mock_client, monkeypatch):
    from bsm_api_client.exceptions import CannotConnectError

    mock_client.websocket_connect.side_effect = CannotConnectError("disconnected")
    mock_client.tasks.async_get_task_status.side_effect = [
        CannotConnectError("disconnected"),
        {"status": "completed", "message": "Installed"},
    ]
    monkeypatch.setattr("bsm_cli.decorators.asyncio.sleep", AsyncMock())
    await monitor_task(mock_client, "task-123", "Installed", "Failed")
    assert mock_client.tasks.async_get_task_status.await_count == 2


@pytest.mark.asyncio
async def test_task_poll_reports_unknown_outcome_on_disconnect(
    mock_client, monkeypatch
):
    from bsm_api_client.exceptions import CannotConnectError

    mock_client.websocket_connect.side_effect = CannotConnectError("disconnected")
    mock_client.tasks.async_get_task_status.side_effect = CannotConnectError(
        "disconnected"
    )
    monkeypatch.setattr("bsm_cli.decorators.asyncio.sleep", AsyncMock())
    with pytest.raises(CannotConnectError, match="Task task-123 was submitted"):
        await monitor_task(mock_client, "task-123", "Installed", "Failed")
    assert mock_client.tasks.async_get_task_status.await_count == 3
