"""Serialize terminal refreshes and reject stale resource revisions."""

import asyncio
from contextlib import aclosing, suppress

from bsm_api_client.exceptions import AuthError


class RevisionGate:
    """A connection owns one epoch; reconnects establish a new baseline."""

    def __init__(self):
        self.epoch = None
        self.revision = -1
        self.timestamp = float("-inf")

    def accept(self, value):
        epoch = value.get("epoch")
        revision = value.get("revision")
        if epoch is None or revision is None:
            return self.epoch is None
        if self.epoch is not None and epoch != self.epoch:
            return False
        if revision < self.revision:
            return False
        latest = value.get("latest") or {}
        timestamp = value.get("timestamp", latest.get("timestamp"))
        if (
            timestamp is not None
            and revision == self.revision
            and timestamp < self.timestamp
        ):
            return False
        if timestamp is not None:
            self.timestamp = timestamp
        self.epoch, self.revision = epoch, revision
        return True


async def _fresh_snapshot(fetch, gate):
    fresh = await fetch()
    if gate.epoch and fresh.epoch and fresh.epoch != gate.epoch:
        raise ConnectionError("Backend epoch changed")
    return fresh if gate.accept(fresh.model_dump()) else None


async def _apply_message(message, current, fetch, gate, topics, transform):
    if message.get("type") == "error":
        raise AuthError(message.get("message", "WebSocket authentication failed"))
    if message.get("topic") not in topics:
        return None
    if transform and message.get("type") == "resource_update":
        data = message.get("data", {})
        return transform(current, data) if gate.accept(data) else None
    return await _fresh_snapshot(fetch, gate)


async def _listen_resource(socket, fetch, topics, interval, transform):
    for topic in topics:
        await socket.subscribe(topic)
    gate = RevisionGate()
    current = await fetch()
    gate.accept(current.model_dump())
    yield current
    messages = socket.listen().__aiter__()
    pending = asyncio.create_task(anext(messages))
    try:
        while True:
            done, _ = await asyncio.wait({pending}, timeout=interval)
            if done:
                message = pending.result()
                pending = asyncio.create_task(anext(messages))
                fresh = await _apply_message(
                    message, current, fetch, gate, topics, transform
                )
            else:
                fresh = await _fresh_snapshot(fetch, gate)
            if fresh is not None:
                current = fresh
                yield current
    finally:
        pending.cancel()
        with suppress(asyncio.CancelledError, Exception):
            await pending


async def watch_resource(client, fetch, topics, *, interval=3, transform=None):
    """Subscribe before fetching; serialize snapshots and live updates.

    Periodic HTTP snapshots reconcile missed events. Disconnections retain HTTP
    fallback while retrying the socket. A new session resets the revision baseline.
    """
    yield await fetch(), False
    while True:
        try:
            socket = await client.websocket_connect()
            async with socket:
                async with aclosing(
                    _listen_resource(socket, fetch, topics, interval, transform)
                ) as stream:
                    async for current in stream:
                        yield current, True
        except AuthError:
            await client.authenticate()
        except Exception:
            # HTTP refresh errors surface below rather than being swallowed.
            pass
        yield await fetch(), False
        await asyncio.sleep(interval)
