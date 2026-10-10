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

*   Fully asynchronous with a generated OpenAPI client plus an `aiohttp` compatibility/WebSocket transport.
*   Context manager support for session management.
*   Handles authentication (JWT) automatically, including token refresh attempts.
*   Generates the typed REST surface from BSM 4.x FastAPI OpenAPI at release time.
*   Discovers new core and plugin FastAPI endpoints at runtime without waiting for a client release.
*   Provides compatibility methods for the established BSM client API:
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
from bsm_api_client import BedrockServerManagerApi, APIError, CannotConnectError

async def main():
    client = BedrockServerManagerApi(
        base_url="http://host:port",    # e.g., "http://127.0.0.1:11325" or "https://bsm.example.internal"
        username="username",           # Username for BSM login
        password="password",           # Password for BSM login
        verify_ssl=True                # Set to False if using HTTPS with a self-signed cert
    )

    try:
        async with client: # Handles session and token management
            # Get manager info (no auth needed for this specific call, but client handles it)
            manager_info = await client.async_get_info()
            print(f"Manager OS: {manager_info.get('data', {}).get('os_type')}, Version: {manager_info.get('data', {}).get('app_version')}")

            # Get list of all servers
            servers = await client.async_get_servers_details()
            if servers:
                print("\nManaged Servers:")
                for server in servers:
                    print(f"  - Name: {server['name']}, Status: {server['status']}, Version: {server['version']}")
            else:
                print("No servers found.")

            # Example: Start a specific server (replace 'MyServer' with an actual server name)
            # server_name_to_start = "MyServer"
            # if any(s['name'] == server_name_to_start for s in servers):
            #     print(f"\nAttempting to start server: {server_name_to_start}")
            #     start_response = await client.async_start_server(server_name_to_start)
            #     print(f"Start response: {start_response.get('message')}")
            # else:
            #     print(f"\nServer '{server_name_to_start}' not found, cannot start.")

    except AuthError as e:
        print(f"Authentication Error: {e}")
    except ServerNotFoundError as e:
        print(f"Server Not Found Error: {e}")
    except APIError as e:
        print(f"An API Error occurred: {e}")
        print(f"  Status Code: {e.status_code}")
        print(f"  API Message: {e.api_message}")
        print(f"  API Errors: {e.api_errors}")
    except CannotConnectError as e:
        print(f"Connection Error: {e}")
    except ValueError as e:
        print(f"Input Error: {e}")
    finally:
        # The `async with client:` block handles closing the session.
        # If not using context manager, you would call:
        # await client.close()
        pass

if __name__ == "__main__":
    asyncio.run(main())
```


## Generated and dynamic API

BSM 4.x is the source of truth for the REST contract. Release builds export
`/api/openapi.json` from the pinned BSM typed-contract revision and generate
`bsm_api_client.generated`. The existing `BedrockServerManagerApi` methods
are compatibility adapters that invoke generated operations by stable ID.

For endpoints added after the installed client was released (including plugin
FastAPI routers), discover and invoke them at runtime:

```python
operations = await client.async_discover_api()
for operation_id, operation in operations.items():
    print(operation_id, operation.method, operation.path)

result = await client.async_call_operation(
    "some_operation_id",
    path_params={"server_name": "MyServer"},
)
```

Call `await client.async_refresh_api()` after plugins are reloaded to detect a
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

## File operations and compatibility

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
        async for chunk in response.content.iter_chunked(65536):
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
