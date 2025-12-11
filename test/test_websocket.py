import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock
from bsm_api_client.websocket_client import WebSocketClient
from bsm_api_client.exceptions import APIError, AuthError
import aiohttp


@pytest.fixture
def mock_session():
    session = AsyncMock(spec=aiohttp.ClientSession)
    # Explicitly make ws_connect an AsyncMock so it returns a coroutine when called
    session.ws_connect = AsyncMock()
    return session


@pytest.fixture
def mock_ws_response():
    ws = AsyncMock(spec=aiohttp.ClientWebSocketResponse)
    ws.close = AsyncMock()
    ws.send_json = AsyncMock()
    return ws


@pytest.mark.asyncio
async def test_websocket_connect(mock_session, mock_ws_response):
    # Configure ws_connect to return the mock_ws_response when awaited
    mock_session.ws_connect.return_value = mock_ws_response

    url = "ws://localhost:8000/ws"
    token = "fake_token"
    client = WebSocketClient(mock_session, url, token)

    await client.connect()

    mock_session.ws_connect.assert_called_once_with(
        url, headers={"Authorization": "Bearer fake_token"}
    )
    assert client._ws == mock_ws_response


@pytest.mark.asyncio
async def test_websocket_connect_auth_error(mock_session):
    # Side effect should be an exception raised when awaited
    mock_session.ws_connect.side_effect = aiohttp.ClientResponseError(
        request_info=MagicMock(), history=(), status=401, message="Unauthorized"
    )

    url = "ws://localhost:8000/ws"
    client = WebSocketClient(mock_session, url, "token")

    with pytest.raises(AuthError):
        await client.connect()


@pytest.mark.asyncio
async def test_websocket_subscribe(mock_session, mock_ws_response):
    mock_session.ws_connect.return_value = mock_ws_response
    client = WebSocketClient(mock_session, "ws://url")
    await client.connect()

    await client.subscribe("test:topic")

    mock_ws_response.send_json.assert_called_once_with(
        {"action": "subscribe", "topic": "test:topic"}
    )


@pytest.mark.asyncio
async def test_websocket_unsubscribe(mock_session, mock_ws_response):
    mock_session.ws_connect.return_value = mock_ws_response
    client = WebSocketClient(mock_session, "ws://url")
    await client.connect()

    await client.unsubscribe("test:topic")

    mock_ws_response.send_json.assert_called_once_with(
        {"action": "unsubscribe", "topic": "test:topic"}
    )


@pytest.mark.asyncio
async def test_websocket_listen(mock_session, mock_ws_response):
    mock_session.ws_connect.return_value = mock_ws_response

    # Mocking iteration over messages
    msg1 = MagicMock()
    msg1.type = aiohttp.WSMsgType.TEXT
    msg1.json.return_value = {"event": "test"}

    msg2 = MagicMock()
    msg2.type = aiohttp.WSMsgType.CLOSED

    async def msg_iter():
        yield msg1
        yield msg2

    mock_ws_response.__aiter__.side_effect = msg_iter

    client = WebSocketClient(mock_session, "ws://url")
    await client.connect()

    received = []
    async for msg in client.listen():
        received.append(msg)

    assert received == [{"event": "test"}]


@pytest.mark.asyncio
async def test_context_manager(mock_session, mock_ws_response):
    mock_session.ws_connect.return_value = mock_ws_response

    async with WebSocketClient(mock_session, "ws://url") as client:
        assert client._ws == mock_ws_response

    mock_ws_response.close.assert_called_once()
