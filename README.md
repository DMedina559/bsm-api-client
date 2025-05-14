# pybedrock-server-manager

An asynchronous Python client library for interacting with the [Bedrock Server Manager](https://github.com/dmedina2018/bedrock-server-manager) API (BSM).

This library provides convenient methods for managing Minecraft Bedrock Edition servers through the BSM web interface's backend API, including starting/stopping servers, sending commands, managing backups, handling allowlists, and more.

**Note:** This library requires the Bedrock Server Manager application to be running and accessible.

## Features

*   Fully asynchronous using `asyncio` and `aiohttp`.
*   Handles authentication (JWT) automatically, including token refresh.
*   Provides methods for most BSM API endpoints:
    *   Manager Information & Global Actions
    *   Server Listing, Status & Configuration
    *   Server Actions (Start, Stop, Command, Update, etc.)
    *   Content Management (Backups, Worlds, Addons)
    *   OS-specific Task Scheduling (Cron for Linux, Task Scheduler for Windows)
*   Custom exceptions for specific API errors.
*   Optional external `aiohttp.ClientSession` support for integration into larger applications (like Home Assistant).

## Installation

Install the package from PyPI (once published):

```bash
pip install pybedrock-server-manager
```

Or, for development, install from source:

```bash
git clone https://github.com/your_username/pybedrock-server-manager.git # Replace with your repo URL
cd pybedrock-server-manager
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
    ServerNotRunningError # Example specific error
)

# --- Configuration ---
BSM_HOST = "your_bsm_host_or_ip"
BSM_PORT = 19135 # Your BSM API port (default for BSM v3 is 19135)
BSM_USERNAME = "your_bsm_username"
BSM_PASSWORD = "your_bsm_password"

# --- Optional: Setup Logging ---
logging.basicConfig(level=logging.INFO)
# Set library logger level for more detail (e.g., during debugging)
logging.getLogger("pybedrock_server_manager").setLevel(logging.DEBUG) # For library's own logs
# For aiohttp's client session logs (can be noisy)
# logging.getLogger("aiohttp.client").setLevel(logging.DEBUG)


async def main():
    """Example usage of the API client."""
    # Use async with for automatic session management if library creates the session
    async with BedrockServerManagerApi(
        host=BSM_HOST,
        port=BSM_PORT,
        username=BSM_USERNAME,
        password=BSM_PASSWORD
    ) as api:
        try:
            # Authentication is handled automatically on the first authenticated call.
            # Or, you can explicitly authenticate:
            # await api.authenticate()

            # --- Example API Calls ---
            print("Fetching manager info...")
            manager_info = await api.async_get_info()
            print(f"Manager Info: {manager_info}")

            print("\nFetching server list...")
            server_list = await api.async_get_servers()
            print(f"Discovered Servers: {server_list}")

            if server_list:
                target_server = server_list[0] # Use the first server for further examples

                print(f"\nFetching status for server: {target_server}...")
                status_info = await api.async_get_server_status_info(target_server)
                print(f"Status Info for {target_server}: {status_info}")

                # Example: Send a command (ensure server is running)
                # print(f"\nSending 'list' command to {target_server}...")
                # try:
                #     command_response = await api.async_send_server_command(target_server, "list")
                #     print(f"Command Response: {command_response}")
                # except ServerNotRunningError as e:
                #     print(f"Could not send command to {target_server}: {e}")

                # Example: Get server properties
                # print(f"\nFetching properties for {target_server}...")
                # properties = await api.async_get_server_properties(target_server)
                # print(f"Properties for {target_server}: {properties.get('properties', {}).get('level-name', 'N/A')}")


        except AuthError as e:
            print(f"Authentication failed: {e}")
        except CannotConnectError as e:
            print(f"Connection failed: {e}")
        except APIError as e:
            print(f"An API error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            logging.exception("Unexpected error in main:") # Log full traceback for unexpected errors

if __name__ == "__main__":
    asyncio.run(main())
```

### Authentication

The library handles JWT authentication automatically. Provide username and password during `BedrockServerManagerApi` initialization. The client will:
1.  Attempt to log in on the first call to an authenticated endpoint (or explicit `api.authenticate()` call).
2.  Store the JWT access token.
3.  Include the token in subsequent requests.
4.  Attempt to re-authenticate and retry once if a `401 Unauthorized` error (e.g., token expired) is received.

### API Client (`BedrockServerManagerApi`)

**Initialization:**

*   `host` (str): BSM hostname or IP.
*   `port` (int): BSM API port.
*   `username` (str): BSM API username.
*   `password` (str): BSM API password.
*   `session` (Optional[`aiohttp.ClientSession`]): External `aiohttp` session. If `None` (default), the library creates and manages its own.
*   `base_path` (str, default=`"/api"`): API base path.
*   `request_timeout` (int, default=`10`): Request timeout in seconds.

**Session Management:**

*   If `session=None` (default), use `async with BedrockServerManagerApi(...)` or call `await api.close()` manually.
*   If providing an external session, manage its lifecycle outside the library.

### Available Methods

All methods are asynchronous and should be `await`ed.

*(Note: `server_name` refers to the unique identifier/directory name of the server instance.)*

**Manager & Global Methods (`_manager_methods.py`):**
*   `async_get_info()`: Get BSM system and application info.
*   `async_scan_players()`: Trigger scan of player logs.
*   `async_get_players()`: Get global list of known players.
*   `async_add_players(players_data: List[str])`: Add players to global list.
*   `async_prune_downloads(directory: str, keep: Optional[int] = None)`: Prune download cache.
*   `async_install_new_server(server_name: str, server_version: str, overwrite: bool = False)`: Install a new server.

**Server Information Methods (`_server_info_methods.py`):**
*   `async_get_servers()`: Get list of all configured server names.
*   `async_get_server_validate(server_name: str)`: Validate if a server exists.
*   `async_get_server_status_info(server_name: str)`: Get runtime process info (PID, CPU, memory).
*   `async_get_server_running_status(server_name: str)`: Get simple running status (true/false).
*   `async_get_server_config_status(server_name: str)`: Get status from server's config file.
*   `async_get_server_version(server_name: str)`: Get installed version of a server.
*   `async_get_server_world_name(server_name: str)`: Get configured world name (`level-name`).
*   `async_get_server_properties(server_name: str)`: Get `server.properties` content.
*   `async_get_server_permissions_data(server_name: str)`: Get `permissions.json` content.
*   `async_get_server_allowlist(server_name: str)`: Get current allowlist.

**Server Action Methods (`_server_action_methods.py`):**
*   `async_start_server(server_name: str)`: Start the server.
*   `async_stop_server(server_name: str)`: Stop the server.
*   `async_restart_server(server_name: str)`: Restart the server.
*   `async_send_server_command(server_name: str, command: str)`: Send a command to the server.
*   `async_update_server(server_name: str)`: Trigger server update process.
*   `async_add_server_allowlist(server_name: str, players: List[str], ignores_player_limit: bool = False)`: Add players to allowlist.
*   `async_remove_server_allowlist_player(server_name: str, player_name: str)`: Remove player from allowlist.
*   `async_set_server_permissions(server_name: str, permissions_dict: Dict[str, str])`: Set player permissions.
*   `async_update_server_properties(server_name: str, properties_dict: Dict[str, Any])`: Update `server.properties`.
*   `async_configure_server_os_service(server_name: str, payload: Dict[str, bool])`: Configure OS service (autostart/autoupdate).
*   `async_delete_server(server_name: str)`: Permanently delete the server.

**Content Management Methods (`_content_methods.py`):**
*   `async_list_server_backups(server_name: str, backup_type: str)`: List backups for a server.
*   `async_get_content_worlds()`: List available `.mcworld` files for installation.
*   `async_get_content_addons()`: List available `.mcpack`/`.mcaddon` files for installation.
*   `async_trigger_server_backup(server_name: str, backup_type: str = "all", file_to_backup: Optional[str] = None)`: Trigger a backup.
*   `async_export_server_world(server_name: str)`: Export server's current world.
*   `async_prune_server_backups(server_name: str, keep: Optional[int] = None)`: Prune old backups.
*   `async_restore_server_backup(server_name: str, restore_type: str, backup_file: str)`: Restore a specific backup.
*   `async_restore_server_latest_all(server_name: str)`: Restore latest 'all' type backup.
*   `async_install_server_world(server_name: str, filename: str)`: Install a `.mcworld` file.
*   `async_install_server_addon(server_name: str, filename: str)`: Install an addon file.

**Scheduler Methods (`_scheduler_methods.py`):**
*   `async_add_server_cron_job(server_name: str, new_cron_job: str)`: Add cron job (Linux).
*   `async_modify_server_cron_job(server_name: str, old_cron_job: str, new_cron_job: str)`: Modify cron job (Linux).
*   `async_delete_server_cron_job(server_name: str, cron_string: str)`: Delete cron job (Linux).
*   `async_add_server_windows_task(server_name: str, command: str, triggers: List[Dict[str, Any]])`: Add Windows scheduled task.
*   `async_get_server_windows_task_details(server_name: str, task_name: str)`: Get Windows task details.
*   `async_modify_server_windows_task(server_name: str, task_name: str, command: str, triggers: List[Dict[str, Any]])`: Modify Windows task.
*   `async_delete_server_windows_task(server_name: str, task_name: str)`: Delete Windows task.

*Refer to the source code or use `help(api_instance.method_name)` for detailed parameters.*

### Error Handling

The library raises specific exceptions inheriting from `APIError`:

*   **`APIError`**: Base for all library API errors.
*   **`AuthError`**: Authentication failures.
*   **`CannotConnectError`**: Network/connection issues, timeouts.
*   **`ServerNotFoundError`**: Target server name not found by API.
*   **`ServerNotRunningError`**: Operation requires a running server, but it's not.

Example:
```python
try:
    await api.async_start_server("my_server")
except ServerNotRunningError as e: # Example, though start usually doesn't throw this one
    print(f"Error: {e}")
except AuthError as e:
    print(f"Auth failed: {e}")
# ... etc.
```