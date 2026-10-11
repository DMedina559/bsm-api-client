<div style="text-align: center;">
    <img src="https://raw.githubusercontent.com/DMedina559/bsm-frontend/main/frontend/public/image/icon/favicon.svg" alt="BSM Logo" width="150">
</div>

# bsm-api-client

<p align="center">
  <a href="https://github.com/DMedina559/bsm-api-client/releases">
    <img alt="Stable" src="https://img.shields.io/github/v/release/DMedina559/bsm-api-client?label=Stable&color=blue">
  </a>
  <a href="https://github.com/DMedina559/bsm-api-client/releases">
    <img alt="Pre-Release" src="https://img.shields.io/github/v/release/DMedina559/bsm-api-client?include_prereleases&label=Pre-Release&color=red">
  </a>
  <a href="https://github.com/DMedina559/bsm-api-client/actions">
    <img alt="Tests" src="https://img.shields.io/github/actions/workflow/status/DMedina559/bsm-api-client/build-test.yml?label=Tests&event=push">
  </a>
</p>

## Introduction

`bsm-api-client` is an asynchronous Python client library for interacting with the Bedrock Server Manager API. It provides a convenient way to manage Minecraft Bedrock Dedicated Servers through the manager's HTTP API.

## Features

*   Fully asynchronous with generated OpenAPI operations, Pydantic contracts, persistent HTTPX REST transport, and aiohttp WebSockets.
*   Context manager support for session management.
*   Handles authentication (JWT) automatically, including token refresh attempts.
*   Generates the typed REST surface from BSM 4.x FastAPI OpenAPI at release time.
*   Discovers new core and plugin FastAPI endpoints at runtime without waiting for a client release.
*   Provides typed domain services for BSM workflows:
    *   Manager Information & Global Actions
    *   Server Listing, Status & Configuration
    *   Server Actions (Start, Stop, Command, Update, etc.)
    *   Content Management (Backups, Worlds, Addons)
*   Custom exceptions for specific API errors, providing context like status codes and API messages.
*   Supports connecting via HTTP or HTTPS.

## Installation

Install the library using pip:

```bash
pip install bsm-api-client
```

## Quick Start

Here's a basic example of how to initialize the client and fetch server information:

For a complete list of endpoints and examples, see [API_DOCS.md](../../docs/API_DOCS.md)

```python
import asyncio

from bsm_api_client import APIError, BedrockServerManagerApi


async def main():
    try:
        async with BedrockServerManagerApi(
            base_url="http://127.0.0.1:11325",
            username="username",
            password="password",
        ) as client:
            info = await client.application.async_get_info()
            print(info.info)

            fleet = await client.servers.async_get_servers()
            for server in fleet.servers or []:
                print(server.name, server.status, server.version)
    except APIError as error:
        print(f"API request failed: {error}")


if __name__ == "__main__":
    asyncio.run(main())
```


## Generated and dynamic API

BSM 4.x is the source of truth for the REST contract. Generated code is committed,
reviewed, and shipped in both wheels and source archives; installation does not
run code generation. Endpoint request and response models are the same public
Pydantic contracts exposed by `bsm_api_client.models`.

Use the generated operation-ID interface for ordinary REST operations:

```python
result = await client.rest.start_server(server_name="MyServer")
detailed = await client.rest.start_server_detailed(server_name="MyServer")
print(detailed.status_code, detailed.headers, detailed.parsed)
```

Services organize SDK workflows under `client.servers`, `client.application`,
`client.tasks`, `client.players`, `client.plugins`, `client.users`, `client.account`,
and `client.content`. Root-level domain methods have been removed; use the
corresponding service or the generated operation-ID interface.
Runtime plugin contracts are available through `client.discovery`. Plugin
operation groups previously exposed as `client.plugins` are now
`client.discovery.plugins` (also available as `client.plugin_operations`).

REST uses a persistent HTTPX client with shared authentication, token refresh,
timeouts, and error translation. Pass `http_client=httpx.AsyncClient(...)` to use
caller-owned transport settings; closing the SDK leaves that client open.
The `session=` argument supplies only the WebSocket aiohttp session. The SDK
creates an internal WebSocket session lazily and closes only sessions it owns.

For endpoints added after the installed client was released (including plugin
FastAPI routers), discover and invoke them at runtime:

```python
operations = await client.discovery.discover()
for operation_id, operation in operations.items():
    print(operation_id, operation.method, operation.path)

result = await client.discovery.call(
    "some_operation_id",
    path_params={"server_name": "MyServer"},
)
```

Call `await client.discovery.refresh()` after plugins are reloaded to detect a
changed schema. WebSocket routes remain handled by `WebSocketClient`, because
OpenAPI describes HTTP operations rather than WebSocket routes.


Inspect `client.capabilities.has("start_server")`, `client.capabilities.plugins`,
and `client.capabilities.runtime_only` after discovery. `client.api_diff()` compares
against the schema shipped in the client, including referenced model changes.
`ApiOperation` supplies the same metadata to the CLI and Python callers.

Generated calls use the facade's shared authentication/retry/error transport:

```python
response = await client.async_call_generated(
    "start_server", parameters={"server_name": "MyServer"}, detailed=True
)
print(response.parsed)  # Generated typed response
```

See [generation](../../docs/OPENAPI_GENERATION.md) and
[contract conventions](../../docs/OPENAPI_CONTRACT.md) for development and plugins.

## File operations and runtime discovery

Multipart operations support repeated files and fields. File tuples contain the
filename, bytes or readable stream, and content type. Streams start at their
current position; use your own file context manager.

```python
await client.async_call_operation(
    "plugin_upload", form_data={"enabled": True},
    files={"files": [("first.mcpack", first_stream, "application/zip"),
                     ("second.mcpack", second_stream, "application/zip")]},
)

async with client.async_stream_operation("plugin_download") as response:
    with open("download.zip", "wb") as output:
        async for chunk in response.aiter_bytes(65536):
            output.write(chunk)
```

Streaming supports discovered GET operations and releases the connection on exit,
including partial reads and cancellation. Regular operation calls buffer responses.
JSON, text and binary content are interpreted by the advertised response media type;
malformed JSON raises `APIError`. Set `authenticated=False` for public operations.
Streaming defaults to the operation's advertised security requirements.

```python
from bsm_api_client import compatibility_report
report = compatibility_report(previous_schema, client.schema)
```

See [contract conventions](../../docs/OPENAPI_CONTRACT.md) for retry policy,
validation, supported serialization and compatibility-report limitations.

## Migrating to the service API

Root-level domain methods have been removed. Use `client.servers`, `client.application`,
`client.content`, `client.tasks`, `client.players`, `client.plugins`, `client.account`, or
`client.users`, or call operation-ID methods through `client.rest`. For example, replace
`client.async_start_server(name)` with `client.servers.async_start_server(name)`.
Task status and ban methods return Pydantic models; `client.tasks.async_get_task_status(id)`
returns `TaskSnapshot`. Use `.model_dump(mode="json")` when a dictionary is needed.

Pass `remember_me=True` when creating the SDK to request the backend-configured
longer token lifetime on login and reauthentication. The default is `False`.
This option does not extend an existing JWT supplied through `jwt_token`.
