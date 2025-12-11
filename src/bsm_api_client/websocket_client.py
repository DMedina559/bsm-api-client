import asyncio
import json
import logging
from typing import AsyncGenerator, List, Dict, Any, Optional

import aiohttp

from .exceptions import APIError, AuthError

_LOGGER = logging.getLogger(__name__)


class WebSocketClient:
    """
    A client for interacting with the Bedrock Server Manager WebSocket API.

    This class handles connecting, authentication, subscribing/unsubscribing to topics,
    and receiving messages.
    """

    def __init__(
        self,
        session: aiohttp.ClientSession,
        url: str,
        token: Optional[str] = None,
    ):
        """
        Initialize the WebSocketClient.

        Args:
            session: The aiohttp ClientSession to use.
            url: The WebSocket URL.
            token: The JWT token for authentication.
        """
        self._session = session
        self._url = url
        self._token = token
        self._ws: Optional[aiohttp.ClientWebSocketResponse] = None

    async def connect(self) -> "WebSocketClient":
        """
        Connect to the WebSocket server.

        Returns:
            self
        """
        # The server expects the token as a query parameter '?token=...'
        # It does not check the Authorization header for WebSockets.
        url = self._url
        if self._token:
            separator = "&" if "?" in url else "?"
            url = f"{url}{separator}token={self._token}"

        try:
            self._ws = await self._session.ws_connect(url)
            _LOGGER.info(f"Connected to WebSocket at {self._url}")
        except aiohttp.ClientResponseError as e:
            if e.status == 401 or e.status == 403:
                raise AuthError(
                    f"Authentication failed: {e.message}", status_code=e.status
                )
            raise APIError(
                f"WebSocket connection failed: {e.message}", status_code=e.status
            )
        except Exception as e:
            raise APIError(f"WebSocket connection failed: {str(e)}")

        return self

    async def disconnect(self):
        """Disconnect from the WebSocket server."""
        if self._ws:
            await self._ws.close()
            self._ws = None
            _LOGGER.info("Disconnected from WebSocket")

    async def subscribe(self, topic: str):
        """
        Subscribe to a topic.

        Args:
            topic: The topic to subscribe to.
        """
        if not self._ws:
            raise APIError("WebSocket is not connected")

        message = {"action": "subscribe", "topic": topic}
        await self._ws.send_json(message)
        _LOGGER.debug(f"Subscribed to {topic}")

    async def unsubscribe(self, topic: str):
        """
        Unsubscribe from a topic.

        Args:
            topic: The topic to unsubscribe from.
        """
        if not self._ws:
            raise APIError("WebSocket is not connected")

        message = {"action": "unsubscribe", "topic": topic}
        await self._ws.send_json(message)
        _LOGGER.debug(f"Unsubscribed from {topic}")

    async def listen(self) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Listen for incoming messages.

        Yields:
            Received messages as dictionaries.
        """
        if not self._ws:
            raise APIError("WebSocket is not connected")

        async for msg in self._ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                try:
                    data = msg.json()
                    yield data
                except json.JSONDecodeError:
                    _LOGGER.warning(f"Received non-JSON message: {msg.data}")
            elif msg.type == aiohttp.WSMsgType.ERROR:
                _LOGGER.error(
                    f"WebSocket connection closed with error: {self._ws.exception()}"
                )
                break
            elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.CLOSING):
                _LOGGER.info("WebSocket connection closed")
                break

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()
