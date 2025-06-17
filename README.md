<div style="text-align: center;">
    <img src="https://raw.githubusercontent.com/dmedina559/bedrock-server-manager/main/src/bedrock_server_manager/web/static/image/icon/favicon.svg" alt="BSM Logo" width="150">
</div>

# bsm-api-client

[![PyPI version](https://img.shields.io/pypi/v/bsm-api-client.svg)](https://pypi.org/project/bsm-api-client/)
[![Python Versions](https://img.shields.io/pypi/pyversions/bsm_api_client.svg)](https://pypi.org/project/bsm-api-client/)
[![License](https://img.shields.io/pypi/l/bsm-api-client.svg)](https://github.com/dmedina559/bsm-api-client/blob/main/LICENSE)

## Introduction

`bsm-api-client` is an asynchronous Python client library for interacting with the Bedrock Server Manager API. It provides a convenient way to manage Minecraft Bedrock Dedicated Servers through the manager's HTTP API.

## Features

*   Fully asynchronous using `asyncio` and `aiohttp`.
*   Context manager support for session management.
*   Handles authentication (JWT) automatically, including token refresh attempts.
*   Provides methods for most BSM API endpoints:
    *   Manager Information & Global Actions
    *   Server Listing, Status & Configuration
    *   Server Actions (Start, Stop, Command, Update, etc.)
    *   Content Management (Backups, Worlds, Addons)
    *   OS-specific Task Scheduling (Cron for Linux, Task Scheduler for Windows)
*   Custom exceptions for specific API errors, providing context like status codes and API messages.
*   Supports connecting via HTTP or HTTPS.

## Installation

Install the library using pip:

```bash
pip install bsm-api-client
```

## Quick Start

Here's a basic example of how to initialize the client and fetch server information:

For a complete list of endpoints and examples, see [API_DOCS.md](https://github.com/DMedina559/bsm-api-client/blob/main/docs/API_DOCS.md)

```python
import asyncio
from bsm_api_client import BedrockServerManagerApi, APIError, CannotConnectError

async def main():
    client = BedrockServerManagerApi(
        host="host",                   # e.g., "127.0.0.1" or "bsm.example.internal"
        username="username",           # Username for BSM login
        password="password",           # Password for BSM login
        port=11325,                    # Optional: Not required for example if using domain such as bsm.example.internal
        use_ssl=False                  # Set to True if your manager uses HTTPS
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
