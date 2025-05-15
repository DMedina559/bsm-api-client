# pybedrock-server-manager

[![PyPI version](https://img.shields.io/pypi/v/pybedrock-server-manager.svg)](https://pypi.org/project/pybedrock-server-manager/)
[![Python Versions](https://img.shields.io/pypi/pyversions/pybedrock-server-manager.svg)](https://pypi.org/project/pybedrock-server-manager/)
[![License](https://img.shields.io/pypi/l/pybedrock-server-manager.svg)](https://github.com/dmedina559/bsm-api-client/blob/main/LICENSE)

An asynchronous Python client library for interacting with the [Bedrock Server Manager](https://github.com/dmedina2018/bedrock-server-manager) API (BSM).

This library provides convenient methods for managing Minecraft Bedrock Edition servers through the BSM web interface's backend API, including starting/stopping servers, sending commands, managing backups, handling allowlists, and more.

**Note:** This library requires the Bedrock Server Manager application to be running and accessible.

## Features

*   Fully asynchronous using `asyncio` and `aiohttp`.
*   Handles authentication (JWT) automatically, including token refresh attempts.
*   Provides methods for most BSM API endpoints:
    *   Manager Information & Global Actions
    *   Server Listing, Status & Configuration
    *   Server Actions (Start, Stop, Command, Update, etc.)
    *   Content Management (Backups, Worlds, Addons)
    *   OS-specific Task Scheduling (Cron for Linux, Task Scheduler for Windows)
*   Custom exceptions for specific API errors, providing context like status codes and API messages.
*   Optional external `aiohttp.ClientSession` support for integration into larger applications.
*   Supports connecting via HTTP or HTTPS.

## Installation

Install the package from PyPI:

```bash
pip install pybedrock-server-manager
```

Or, for development, install from source:

```bash
git clone https://github.com/dmedina559/bsm-api-client.git
cd bsm-api-client
pip install -e .
```

## Usage

### Quick Start

```python
import asyncio
import logging

from pybedrock_server_manager import (
    BedrockServerManagerApi,
    APIError,
    AuthError,
    CannotConnectError,
    ServerNotFoundError, # Example specific error
    ServerNotRunningError
)

# --- Configuration ---
BSM_HOST = "your_bsm_host_or_ip"  # e.g., "localhost" or "bsm.example.com"
BSM_PORT = 11325                  # Default BSM API port. Adjust if different
BSM_USERNAME = "your_bsm_username"
BSM_PASSWORD = "your_bsm_password"
BSM_USE_SSL = False               # Set to True if BSM is served over HTTPS
BSM_VERIFY_SSL = True                   # Set to False if using HTTPS with a self-signed cert

# --- Optional: Setup Logging ---
# Basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# For more detailed library logs during development/debugging:
logging.getLogger("pybedrock_server_manager").setLevel(logging.DEBUG)

# For aiohttp's own client session logs (can be very verbose):
# logging.getLogger("aiohttp.client").setLevel(logging.DEBUG)


async def main():
    """Example usage of the API client."""
    # Use async with for automatic session management if the library creates the session
    async with BedrockServerManagerApi(
        host=BSM_HOST,
        port=BSM_PORT,
        username=BSM_USERNAME,
        password=BSM_PASSWORD,
        use_ssl=BSM_USE_SSL,
        verify_ssl=BSM_VERIFY_SSL
    ) as api:
        try:
            # Authentication is handled automatically on the first authenticated call.
            # You can also explicitly authenticate if needed:
            # await api.authenticate() # This will raise AuthError on failure

            print("Fetching manager info (this call does not require authentication)...")
            manager_info = await api.async_get_info()
            print(f"Manager Info: OS Type = {manager_info.get('data', {}).get('os_type')}, App Version = {manager_info.get('data', {}).get('app_version')}")

            print("\nFetching server names...")
            server_names = await api.async_get_server_names() # Gets a list of server name strings
            print(f"Discovered Server Names: {server_names}")

            # For full server details (name, status, version):
            # server_details_list = await api.async_get_servers_details()
            # print(f"Discovered Servers (Details): {server_details_list}")

            if server_names:
                target_server = server_names[0] # Use the first server for further examples

                print(f"\nFetching status for server: {target_server}...")
                status_info = await api.async_get_server_status_info(target_server)
                print(f"Status Info for {target_server}: {status_info.get('process_info') or 'Not Running'}")

                # Example: Send a command (ensure server is running)
                # print(f"\nSending 'list' command to {target_server}...")
                # try:
                #     # Ensure the server is actually running before sending a command
                #     running_status = await api.async_get_server_running_status(target_server)
                #     if running_status.get("is_running"):
                #         command_response = await api.async_send_server_command(target_server, "list")
                #         print(f"Command Response: {command_response}")
                #     else:
                #         print(f"Server {target_server} is not running. Cannot send command.")
                # except ServerNotRunningError as e: # API might also return this if it tries and fails
                #     print(f"Could not send command to {target_server}: {e}")
                # except ServerNotFoundError:
                #     print(f"Server {target_server} not found.")


                # Example: Get server properties
                # print(f"\nFetching properties for {target_server}...")
                # properties_response = await api.async_get_server_properties(target_server)
                # if properties_response.get("status") == "success":
                #     level_name = properties_response.get('properties', {}).get('level-name', 'N/A')
                #     print(f"World name for {target_server}: {level_name}")
                # else:
                #     print(f"Could not fetch properties for {target_server}: {properties_response.get('message')}")

        except AuthError as e:
            print(f"Authentication failed: {e} (Status: {e.status_code}, API Message: {e.api_message}, Details: {e.api_errors})")
        except CannotConnectError as e:
            print(f"Connection failed: {e}")
        except ServerNotFoundError as e:
            print(f"Server not found: {e}")
        except APIError as e: # Catch other specific API errors after more specific ones
            print(f"An API error occurred: {e} (Status: {e.status_code}, API Message: {e.api_message}, Details: {e.api_errors})")
        except Exception as e: # Catch-all for unexpected errors
            print(f"An unexpected error occurred: {e}")
            logging.exception("Unexpected error in main example:")

if __name__ == "__main__":
    asyncio.run(main())
```

### Authentication

The library handles JWT authentication automatically. Provide `username` and `password` during `BedrockServerManagerApi` initialization. The client will:
1.  Attempt to log in on the first call to an endpoint requiring authentication (or if `await api.authenticate()` is called explicitly).
2.  Store the JWT access token upon successful login.
3.  Include this token in the `Authorization` header for subsequent authenticated requests.
4.  If a `401 Unauthorized` error is received (e.g., due to token expiry), it will attempt to re-authenticate once and retry the original request with the new token.

### API Client (`BedrockServerManagerApi`)

**Initialization:**

*   `host` (str): BSM hostname or IP address (e.g., `"localhost"`, `"192.168.1.100"`).
*   `port` (int): BSM API port (e.g., `11325`).
*   `username` (str): BSM API username.
*   `password` (str): BSM API password.
*   `use_ssl` (bool, default=`False`): Set to `True` to use `https` for the API connection.
*   `session` (Optional[`aiohttp.ClientSession`]): An optional, externally managed `aiohttp.ClientSession`. If `None` (default), the library creates and manages its own session.
*   `base_path` (str, default=`"/api"`): The base path for all API endpoints (e.g., `"/api"`).
*   `request_timeout` (int, default=`10`): Default timeout in seconds for API requests.

**Session Management:**

*   If you let the library create its own session (by not providing the `session` argument), it's recommended to use the client as an asynchronous context manager (`async with BedrockServerManagerApi(...) as api:`). This ensures the session is properly closed.
*   Alternatively, if not using `async with`, you must manually call `await api.close()` when done to close the internally created session.
*   If you provide an external session, you are responsible for managing its lifecycle (creation and closure).

### Available Methods

All methods are asynchronous and should be `await`ed. Server-specific methods typically require a `server_name` argument, which is the unique identifier (directory name) of the server instance.

**Manager & Global Methods:**
*   `async_get_info()`: Get BSM system (OS type) and application version. (No Auth)
*   `async_scan_players()`: Trigger a scan of all server log files to update the global player list.
*   `async_get_players()`: Get the global list of known players (name and XUID).
*   `async_add_players(players_data: List[str])`: Add or update players in the global list (format: `"PlayerName:PlayerXUID"`).
*   `async_prune_downloads(directory: str, keep: Optional[int] = None)`: Prune downloaded server archives in a specified directory.
*   `async_install_new_server(server_name: str, server_version: str, overwrite: bool = False)`: Install a new server instance.

**Server Information Methods:**
*   `async_get_servers_details()`: Get a list of all configured servers with details (name, status, version).
*   `async_get_server_names()`: Get a simplified list of all configured server names.
*   `async_get_server_validate(server_name: str)`: Validate if a server's directory and executable exist.
*   `async_get_server_status_info(server_name: str)`: Get runtime process info (PID, CPU, memory, uptime).
*   `async_get_server_running_status(server_name: str)`: Get simple running status (`{"is_running": true/false}`).
*   `async_get_server_config_status(server_name: str)`: Get status from the server's manager-specific config file.
*   `async_get_server_version(server_name: str)`: Get the installed Bedrock version of a server.
*   `async_get_server_world_name(server_name: str)`: Get the configured world name (`level-name`) from `server.properties`.
*   `async_get_server_properties(server_name: str)`: Get the full content of `server.properties`.
*   `async_get_server_permissions_data(server_name: str)`: Get player permission levels from `permissions.json`.
*   `async_get_server_allowlist(server_name: str)`: Get the current player allowlist from `allowlist.json`.

**Server Action Methods:**
*   `async_start_server(server_name: str)`: Start the server.
*   `async_stop_server(server_name: str)`: Stop the server.
*   `async_restart_server(server_name: str)`: Restart the server.
*   `async_send_server_command(server_name: str, command: str)`: Send a command to the server console.
*   `async_update_server(server_name: str)`: Trigger the server update process.
*   `async_add_server_allowlist(server_name: str, players: List[str], ignores_player_limit: bool = False)`: Add players to the server's allowlist.
*   `async_remove_server_allowlist_player(server_name: str, player_name: str)`: Remove a player from the server's allowlist.
*   `async_set_server_permissions(server_name: str, permissions_dict: Dict[str, str])`: Set player permission levels (XUID to level mapping).
*   `async_update_server_properties(server_name: str, properties_dict: Dict[str, Any])`: Update `server.properties` with specified key-value pairs.
*   `async_configure_server_os_service(server_name: str, service_config: Dict[str, bool])`: Configure OS-specific service settings (e.g., autostart, autoupdate).
*   `async_delete_server(server_name: str)`: **Permanently delete all data for the server instance.** Use with caution.

**Content Management Methods (Backups, Worlds, Addons):**
*   `async_list_server_backups(server_name: str, backup_type: str)`: List backup filenames for a server ("world" or "config" type).
*   `async_get_content_worlds()`: List available `.mcworld` files from the manager's content directory for installation.
*   `async_get_content_addons()`: List available `.mcpack`/`.mcaddon` files from the manager's content directory for installation.
*   `async_trigger_server_backup(server_name: str, backup_type: str = "all", file_to_backup: Optional[str] = None)`: Trigger a backup (world, config, or all).
*   `async_export_server_world(server_name: str)`: Export the server's current world to the manager's content directory.
*   `async_prune_server_backups(server_name: str, keep: Optional[int] = None)`: Prune older backups for a server.
*   `async_restore_server_backup(server_name: str, restore_type: str, backup_file: str)`: Restore a specific backup file (world or config).
*   `async_restore_server_latest_all(server_name: str)`: Restore the latest "all" type backup (world and standard configs).
*   `async_install_server_world(server_name: str, filename: str)`: Install a `.mcworld` file from the content directory to a server.
*   `async_install_server_addon(server_name: str, filename: str)`: Install an addon file from the content directory to a server.

**OS Scheduler Methods:**
*   `async_add_server_cron_job(server_name: str, new_cron_job: str)`: Add a cron job (Linux Only).
*   `async_modify_server_cron_job(server_name: str, old_cron_job: str, new_cron_job: str)`: Modify an existing cron job (Linux Only).
*   `async_delete_server_cron_job(server_name: str, cron_string: str)`: Delete a cron job (Linux Only).
*   `async_add_server_windows_task(server_name: str, command: str, triggers: List[Dict[str, Any]])`: Add a Windows scheduled task.
*   `async_get_server_windows_task_details(server_name: str, task_name: str)`: Get details of a Windows scheduled task.
*   `async_modify_server_windows_task(server_name: str, task_name: str, command: str, triggers: List[Dict[str, Any]])`: Modify/replace a Windows task.
*   `async_delete_server_windows_task(server_name: str, task_name: str)`: Delete a Windows scheduled task.

*For detailed parameters, potential return values, and specific error conditions, refer to the method docstrings in the source code or use `help(api_instance.method_name)` in a Python interpreter after importing.*

### Error Handling

The library raises specific exceptions that inherit from `APIError`. This allows for granular error catching. All custom API exceptions provide `status_code` (Optional[int]), `api_message` (str), and `api_errors` (dict) attributes for more context from the API response.

*   **`APIError`**: Base class for errors originating from the API or client interaction.
*   **`AuthError`**: For authentication failures (e.g., bad credentials, invalid/expired token - HTTP 401, 403).
*   **`CannotConnectError`**: For network issues, DNS failures, or connection timeouts. Wraps the original `aiohttp` exception.
*   **`InvalidInputError`**: For client-side input errors that would result in an API error (e.g., HTTP 400 Bad Request from API due to bad payload).
*   **`NotFoundError`**: General resource not found (HTTP 404).
    *   **`ServerNotFoundError`**: A specific `NotFoundError` when a target server name is not found by the API.
*   **`ServerNotRunningError`**: When an operation requires the Bedrock server to be running, but it's not. (May be inferred from API error messages).
*   **`OperationFailedError`**: For general API operation failures not covered by other exceptions (e.g., HTTP 501 Not Implemented).
*   **`APIServerSideError`**: Indicates an error on the BSM API server itself (HTTP 5xx).

Example:
```python
try:
    # Example: Attempting to send a command to a server that might not exist or be running
    server_name = "my_test_server"
    if await api.async_get_server_validate(server_name): # Check if server exists first (optional)
        await api.async_send_server_command(server_name, "say Hello from pyBSM!")
    else:
        print(f"Server {server_name} does not seem to exist for validation.")

except ServerNotFoundError as e:
    print(f"Operation failed because server was not found: {e.api_message or e}")
except ServerNotRunningError as e:
    print(f"Operation failed because server is not running: {e.api_message or e}")
except AuthError as e:
    print(f"Authentication error: {e.api_message or e}")
except APIError as e:
    print(f"A generic API error occurred: Status {e.status_code}, Message: {e.api_message or e}, Details: {e.api_errors}")
```