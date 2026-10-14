# WebSocket notifications

REST and WebSocket connections share SDK credentials but have separate transports. Open a WebSocket explicitly and consume it within its context:

```python
websocket = await client.websocket_connect()
try:
    await websocket.subscribe("application-metrics")
    async for message in websocket.listen():
        print(message)
finally:
    await websocket.disconnect()
```

Authentication and subscription success must be interpreted from incoming messages; sending a frame is not proof that the server accepted it. Topic permissions come from the backend. The low-level `WebSocketClient` does not automatically reconnect or replay subscriptions; integrations own reconnect policy.

After reconnecting, fetch HTTP state again before applying further changes. Compare revisions only within the same resource and backend epoch. Do not let delayed frames from an old connection replace the current epoch. Task completion and operation outcomes are separate concepts.

The SDK's event service exposes administrative catalog/activity operations. Diagnostic snapshots remain HTTP reads; a diagnostic change notification protocol is not implemented.
