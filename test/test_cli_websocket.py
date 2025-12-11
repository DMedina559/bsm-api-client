import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
import click
from bsm_api_client.cli.server import list_servers
from bsm_api_client.websocket_client import WebSocketClient
from bsm_api_client.cli.decorators import monitor_task


@pytest.fixture
def mock_client():
    client = AsyncMock()
    # Mocking servers response
    server1 = {"name": "server1", "status": "RUNNING", "version": "1.0"}
    client.async_get_servers.return_value = MagicMock(servers=[server1])
    # Mocking task response
    client.async_get_task_status.return_value = {
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

    with patch("click.clear"), patch("click.secho"), patch("click.echo"), patch(
        "asyncio.sleep", side_effect=side_effect_sleep
    ) as mock_sleep:

        with ctx.scope():
            try:
                await list_servers.callback(loop=True, server_name=None)
            except KeyboardInterrupt:
                pass

    mock_client.websocket_connect.assert_called_once()

    mock_ws_client.subscribe.assert_any_call(
        "event:after_server_statuses_updated"
    )
    assert mock_client.async_get_servers.call_count >= 2
    # Verify sleep was called (fallback triggered after WS finished)
    mock_sleep.assert_called()


@pytest.mark.asyncio
async def test_list_servers_fallback(mock_client):
    mock_client.websocket_connect.side_effect = Exception("Connection failed")

    ctx = click.Context(list_servers, obj={"client": mock_client})

    async def side_effect_sleep(seconds):
        raise KeyboardInterrupt("Break loop")

    with patch("click.clear"), patch("click.secho"), patch("click.echo"), patch(
        "asyncio.sleep", side_effect=side_effect_sleep
    ) as mock_sleep:

        with ctx.scope():
            try:
                await list_servers.callback(loop=True, server_name=None)
            except KeyboardInterrupt:
                pass

    mock_client.websocket_connect.assert_called_once()
    mock_sleep.assert_called()
    assert mock_client.async_get_servers.call_count >= 1


@pytest.mark.asyncio
async def test_monitor_task_websocket(mock_client, mock_ws_client):
    mock_client.websocket_connect.return_value = mock_ws_client

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
    mock_client.async_get_task_status.return_value = {
        "status": "success",
        "message": "Done via poll",
    }

    with patch("click.secho") as mock_secho, patch("click.echo"), patch(
        "asyncio.sleep"
    ) as mock_sleep:  # Mock sleep to run immediately
        await monitor_task(mock_client, "123", "Success", "Failure")

    mock_client.websocket_connect.assert_called_once()
    mock_client.async_get_task_status.assert_called_once_with("123")
    mock_secho.assert_any_call(
        "WebSocket monitoring failed (WS Failed), falling back to polling...",
        fg="yellow",
    )
    mock_secho.assert_any_call("Success: Done via poll", fg="green")
