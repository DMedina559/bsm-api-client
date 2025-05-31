<div style="text-align: center;">
    <img src="https://raw.githubusercontent.com/dmedina559/bedrock-server-manager/main/bedrock_server_manager/web/static/image/icon/favicon.svg" alt="BSM Logo" width="150">
</div>

# pybedrock_server_manager - API Documentation & Examples

API documentation and examples for the `pybedrock_server_manager` library.

**Doc Version:** `0.6.0`

## Table of Contents
- [Asynchronous Nature](#asynchronous-nature)
- [Client Initialization (`BedrockServerManagerApi`)](#client-initialization-bedrockservermanagerapi)
- [Authentication](#authentication)
- [Error Handling](#error-handling)
  - [Custom Exceptions](#custom-exceptions)
- [API Reference](#api-reference)
  - [Manager Methods](#manager-methods)
    - [`async_get_info()`](#async_get_info)
    - [`async_scan_players()`](#async_scan_players)
    - [`async_get_players()`](#async_get_players)
    - [`async_add_players(players_data)`](#async_add_playersplayers_data)
    - [`async_prune_downloads(directory, keep)`](#async_prune_downloadsdirectory-keep)
    - [`async_install_new_server(server_name, server_version, overwrite)`](#async_install_new_serverserver_name-server_version-overwrite)
  - [Server Information Methods](#server-information-methods)
    - [`async_get_servers_details()`](#async_get_servers_details)
    - [`async_get_server_names()`](#async_get_server_names)
    - [`async_get_server_validate(server_name)`](#async_get_server_validateserver_name)
    - [`async_get_server_status_info(server_name)`](#async_get_server_status_infoserver_name)
    - [`async_get_server_running_status(server_name)`](#async_get_server_running_statusserver_name)
    - [`async_get_server_config_status(server_name)`](#async_get_server_config_statusserver_name)
    - [`async_get_server_version(server_name)`](#async_get_server_versionserver_name)
    - [`async_get_server_world_name(server_name)`](#async_get_server_world_nameserver_name)
    - [`async_get_server_properties(server_name)`](#async_get_server_propertiesserver_name)
    - [`async_get_server_permissions_data(server_name)`](#async_get_server_permissions_dataserver_name)
    - [`async_get_server_allowlist(server_name)`](#async_get_server_allowlistserver_name)
  - [Server Action Methods](#server-action-methods)
    - [`async_start_server(server_name)`](#async_start_serverserver_name)
    - [`async_stop_server(server_name)`](#async_stop_serverserver_name)
    - [`async_restart_server(server_name)`](#async_restart_serverserver_name)
    - [`async_send_server_command(server_name, command)`](#async_send_server_commandserver_name-command)
    - [`async_update_server(server_name)`](#async_update_serverserver_name)
    - [`async_add_server_allowlist(server_name, players, ignores_player_limit)`](#async_add_server_allowlistserver_name-players-ignores_player_limit)
    - [`async_remove_server_allowlist_player(server_name, player_name)`](#async_remove_server_allowlist_playerserver_name-player_name)
    - [`async_set_server_permissions(server_name, permissions_dict)`](#async_set_server_permissionsserver_name-permissions_dict)
    - [`async_update_server_properties(server_name, properties_dict)`](#async_update_server_propertiesserver_name-properties_dict)
    - [`async_configure_server_os_service(server_name, service_config)`](#async_configure_server_os_serviceserver_name-service_config)
    - [`async_delete_server(server_name)`](#async_delete_serverserver_name)
  - [Content Management Methods](#content-management-methods)
    - [`async_list_server_backups(server_name, backup_type)`](#async_list_server_backupsserver_name-backup_type)
    - [`async_get_content_worlds()`](#async_get_content_worlds)
    - [`async_get_content_addons()`](#async_get_content_addons)
    - [`async_trigger_server_backup(server_name, backup_type, file_to_backup)`](#async_trigger_server_backupserver_name-backup_type-file_to_backup)
    - [`async_export_server_world(server_name)`](#async_export_server_worldserver_name)
    - [`async_reset_server_world(server_name)`](#async_reset_server_worldserver_name)
    - [`async_prune_server_backups(server_name, keep)`](#async_prune_server_backupsserver_name-keep)
    - [`async_restore_server_backup(server_name, restore_type, backup_file)`](#async_restore_server_backupserver_name-restore_type-backup_file)
    - [`async_restore_server_latest_all(server_name)`](#async_restore_server_latest_allserver_name)
    - [`async_install_server_world(server_name, filename)`](#async_install_server_worldserver_name-filename)
    - [`async_install_server_addon(server_name, filename)`](#async_install_server_addonserver_name-filename)
  - [Scheduler Methods](#scheduler-methods)
    - [Linux Cron Scheduler](#linux-cron-scheduler)
      - [`async_add_server_cron_job(server_name, new_cron_job)`](#async_add_server_cron_jobserver_name-new_cron_job)
      - [`async_modify_server_cron_job(server_name, old_cron_job, new_cron_job)`](#async_modify_server_cron_jobserver_name-old_cron_job-new_cron_job)
      - [`async_delete_server_cron_job(server_name, cron_string)`](#async_delete_server_cron_jobserver_name-cron_string)
    - [Windows Task Scheduler](#windows-task-scheduler)
      - [`async_add_server_windows_task(server_name, command, triggers)`](#async_add_server_windows_taskserver_name-command-triggers)
      - [`async_get_server_windows_task_details(server_name, task_name)`](#async_get_server_windows_task_detailsserver_name-task_name)
      - [`async_modify_server_windows_task(server_name, task_name, command, triggers)`](#async_modify_server_windows_taskserver_name-task_name-command-triggers)
      - [`async_delete_server_windows_task(server_name, task_name)`](#async_delete_server_windows_taskserver_name-task_name)

## Asynchronous Nature

All API interaction methods in this library are `async` and must be `await`ed. This makes the library suitable for use in asynchronous applications (e.g., those built with `asyncio`, `FastAPI`, etc.). Ensure your application runs an asyncio event loop.

## Client Initialization (`BedrockServerManagerApi`)

The main entry point to the library is the `BedrockServerManagerApi` class.

```python
from pybedrock_server_manager import BedrockServerManagerApi

client = BedrockServerManagerApi(
    host="host",                   # e.g., "127.0.0.1" or "bsm.example.internal"
    username="username",           # Username for BSM login
    password="password",           # Password for BSM login
    port=11325,                    # Optional: Not required for example if using domain such as bsm.example.internal
    session=None,                  # Optional: Pass an existing aiohttp.ClientSession
    base_path="/api",              # Default API base path
    request_timeout=10,            # Seconds
    use_ssl=False                  # Set to True for HTTPS
    verify_ssl=True                # Set to False to disable SSL cert verification (HTTPS only)
)
```

### Constructor Parameters

*   **`host`** (*str*, required): The hostname or IP address of the Bedrock Server Manager.
*   **`username`** (*str*, required): The username for API authentication.
*   **`password`** (*str*, required): The password for API authentication.
*   **`port`** (*int*, Optional): The port number on which the Bedrock Server Manager API is listening.
*   **`session`** (*Optional[aiohttp.ClientSession]*, optional): An optional, pre-existing `aiohttp.ClientSession` to use for requests. If `None` (default), the client will create and manage its own session.
*   **`base_path`** (*str*, optional): The base path for the API endpoints on the server. Defaults to `"/api"`.
*   **`request_timeout`** (*int*, optional): The timeout in seconds for API requests. Defaults to `10`.
*   **`use_ssl`** (*bool*, optional): Set to `True` if the Bedrock Server Manager API is served over HTTPS. Defaults to `False`.
*   **`verify_ssl` (*bool*, optional): If use_ssl is `True`, this flag determines whether the SSL certificate of the server is verified. Defaults to `True` (verify certificate). Set to `False` to disable SSL certificate verification (e.g., for self-signed certificates). Disabling SSL verification is insecure and not recommended for production environments. If an external session is provided, this parameter is ignored, and the SSL verification behavior of the provided session will be used.

### Context Manager Usage

The client supports the asynchronous context manager protocol, which is the recommended way to ensure the underlying `aiohttp.ClientSession` is properly closed:

```python
async with BedrockServerManagerApi(...) as client:
    # Use client methods
    await client.async_get_info()
# Session is automatically closed here
```

### `close()` Method

If not using the client as an asynchronous context manager, you should explicitly close the session when done:

```python
client = BedrockServerManagerApi(...)
try:
    # Use client methods
    await client.async_get_info()
finally:
    await client.close()
```

## Authentication

The `BedrockServerManagerApi` client handles authentication automatically. Upon the first authenticated request (or if a token expires), it will:
1.  Internally call its `authenticate()` method to send a `POST` request to the `/api/login` endpoint with the provided `username` and `password`.
2.  Store the received JWT (JSON Web Token).
3.  Include this JWT in the `Authorization: Bearer <token>` header for all subsequent authenticated requests.

If an authenticated request returns a `401 Unauthorized` status, the client will assume the token has expired, clear the stored token, re-authenticate, and then retry the original request **once**. If authentication still fails, an `AuthError` will be raised.

The `/api/login` endpoint itself is exempt from CSRF protection on the server side.

## Error Handling

The client library raises custom exceptions to indicate various error conditions encountered during API interactions or client-side issues. All API-related exceptions inherit from `APIError`.

When an API error occurs, the `_request` method in `ClientBase` attempts to parse the JSON error response from the server. The `APIError` (and its subclasses) will contain:

*   `message`: The primary error message.
*   `status_code`: The HTTP status code of the API response (e.g., `400`, `401`, `404`, `500`).
*   `response_data`: The full parsed JSON dictionary from the API error response.
*   `api_message`: A convenience attribute, typically `response_data.get("message", "")`.
*   `api_errors`: A convenience attribute, typically `response_data.get("errors", {})`, which might contain field-specific validation errors from the API.

### Custom Exceptions

The following custom exceptions are defined in `pybedrock_server_manager.exceptions`:

*   **`APIError(Exception)`**:
    Generic base exception for errors originating from or related to the Bedrock Server Manager API.

*   **`CannotConnectError(APIError)`**:
    Raised when the client cannot connect to the Bedrock Server Manager API host (e.g., network issues, host down, DNS failure). This typically wraps a lower-level connection error from `aiohttp` (e.g., `aiohttp.ClientConnectionError`).
    *   `original_exception`: Contains the underlying exception from `aiohttp`.

*   **`AuthError(APIError)`**:
    Indicates an authentication or authorization failure (e.g., HTTP `401 Unauthorized`, `403 Forbidden`, or bad credentials during login).

*   **`NotFoundError(APIError)`**:
    Raised when a requested resource is not found (e.g., HTTP `404 Not Found` for a generic path).

*   **`ServerNotFoundError(NotFoundError)`**:
    A more specific "not found" error, raised when a specific server instance (by `server_name`) cannot be found by the API. Typically corresponds to an HTTP `404 Not Found` on a server-specific endpoint.

*   **`ServerNotRunningError(APIError)`**:
    Raised when an operation is attempted that requires the Bedrock server process to be running, but it is not. This can be inferred from specific API error messages even if the HTTP status is, for example, `500` or `200` with an error status in the JSON payload.

*   **`InvalidInputError(APIError)`**:
    Indicates that the input provided to an API endpoint was invalid, typically corresponding to an HTTP `400 Bad Request`. The `api_errors` attribute may contain specific details about which fields failed validation.

*   **`OperationFailedError(APIError)`**:
    A general error for API operations that fail for reasons not covered by other more specific exceptions. This can include HTTP `501 Not Implemented` or other specific operational failures reported by the API.

*   **`APIServerSideError(APIError)`**:
    Indicates that an unexpected error occurred on the API server side during request processing, typically corresponding to an HTTP `500 Internal Server Error` or other `5xx` statuses.

In addition to these, client methods may raise standard Python exceptions like `ValueError` or `TypeError` for invalid arguments passed to the client methods themselves *before* an API call is made.

## API Reference

The following methods are available on an instance of `BedrockServerManagerApi`. All methods are `async` and must be `await`ed.

---

### Manager Methods

These methods interact with manager-level endpoints, generally not specific to a single server instance.

#### `async_get_info()`

Retrieves basic system information (OS type) and the current version of the Bedrock Server Manager application.

*   **Corresponds to:** `GET /api/info`
*   **Authentication:** None required.
*   **Arguments:** None.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary containing the API response. On success, this includes a `data` key with `os_type` and `app_version`.
        ```json
        {
            "status": "success",
            "data": {
                "os_type": "Linux", // or "Windows"
                "app_version": "3.2.1"
            }
        }
        ```
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `APIServerSideError`: If the API encounters an internal error retrieving the info.
    *   `APIError`: For other unexpected API response issues.
*   **Example:**
    ```python
    info = await client.async_get_info()
    print(f"OS: {info['data']['os_type']}, App Version: {info['data']['app_version']}")
    ```

---
#### `async_scan_players()`

Triggers a scan of all server log files (`server_output.txt`) to find player connection entries and update the central `players.json` file.

*   **Corresponds to:** `POST /api/players/scan`
*   **Authentication:** Required.
*   **Arguments:** None.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary confirming the scan initiation or completion status.
        ```json
        {
            "status": "success",
            "players_found": true, // boolean
            "message": "Player scan completed and data saved."
        }
        ```
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `APIServerSideError`: If the API encounters an internal error during the scan or save process.
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    response = await client.async_scan_players()
    print(response['message'])
    ```

---
#### `async_get_players()`

Retrieves the global list of all known players (name and XUID) from the manager's central `players.json` file.

*   **Corresponds to:** `GET /api/players/get`
*   **Authentication:** Required.
*   **Arguments:** None.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary containing the list of players.
        ```json
        {
            "status": "success",
            "players": [
                {"name": "PlayerOne", "xuid": "253..."},
                {"name": "PlayerTwo", "xuid": "253..."}
            ]
            // "message": "Player file not found." if applicable
        }
        ```
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `APIServerSideError`: If the API has issues reading/parsing `players.json`.
    *   `APIError`: For other API response issues (e.g., invalid JSON format from API).
*   **Example:**
    ```python
    player_data = await client.async_get_players()
    for player in player_data.get('players', []):
        print(f"Name: {player['name']}, XUID: {player['xuid']}")
    ```

---
#### `async_add_players(players_data)`

Adds one or more players to the central `players.json` file. If a player with the same XUID already exists, their information (e.g., name) will be updated.

*   **Corresponds to:** `POST /api/players/add`
*   **Authentication:** Required.
*   **Arguments:**
    *   `players_data` (*List[str]*, required): A list of player strings. Each string must be in the format `"PlayerName:PlayerXUID"`. Example: `["Steve:2535460987654321", "Alex:2535461234567890"]`.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary confirming the operation.
        ```json
        {
            "status": "success",
            "message": "Players added successfully."
        }
        ```
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `InvalidInputError`: If the `players_data` format is invalid as per API validation.
    *   `APIServerSideError`: If the API has issues writing/updating `players.json`.
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    new_players = ["TestPlayer1:12345", "TestPlayer2:67890"]
    response = await client.async_add_players(new_players)
    print(response['message'])
    ```

---
#### `async_prune_downloads(directory, keep)`

Triggers pruning of older downloaded server archives (e.g., `bedrock-server-*.zip`) from a specified directory on the manager host.

*   **Corresponds to:** `POST /api/downloads/prune`
*   **Authentication:** Required.
*   **Arguments:**
    *   `directory` (*str*, required): The reliative path on the manager server to the directory containing download files to be pruned.
    *   `keep` (*Optional[int]*, optional): The number of the most recent files to retain. If `None`, the manager's default setting (`DOWNLOAD_KEEP`) will be used.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary confirming the pruning operation.
        ```json
        {
            "status": "success",
            "message": "Download cache pruned successfully for '/path/to/downloafs'."
        }
        ```
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `InvalidInputError`: If `directory` is missing or `keep` is invalid as per API validation.
    *   `APIServerSideError`: If the API encounters errors accessing the directory or deleting files.
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    response = await client.async_prune_downloads(directory="stable", keep=3)
    print(response['message'])
    ```

---
#### `async_install_new_server(server_name, server_version, overwrite)`

Requests the installation of a new Bedrock server instance on the manager.

*   **Corresponds to:** `POST /api/server/install`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The desired unique name for the new server.
    *   `server_version` (*str*, required): The version to install (e.g., `"LATEST"`, `"PREVIEW"`, `"1.20.81.01"`).
    *   `overwrite` (*bool*, optional): If `True` and a server with the same name exists, its data will be deleted before installation. Defaults to `False`.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary indicating the result.
        *   On successful installation (HTTP 201):
            ```json
            {
                "status": "success",
                "server_name": "UniqueServerName",
                "version": "1.20.81.01", // Actual version installed
                "message": "Server 'UniqueServerName' installed successfully...",
                "next_step_url": "/server/UniqueServerName/configure_properties?new_install=true"
            }
            ```
        *   If server exists and `overwrite` is `False` (HTTP 200):
            ```json
            {
                "status": "confirm_needed",
                "message": "Server 'ExistingServer' already exists. Overwrite existing data and reinstall?",
                "server_name": "ExistingServer",
                "server_version": "LATEST" // Original requested version
            }
            ```
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `InvalidInputError`: If `server_name` or `server_version` is invalid as per API validation.
    *   `APIServerSideError`: If any step of the installation process fails on the server (download, extraction, config).
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    try:
        response = await client.async_install_new_server(
            server_name="MyNewServer",
            server_version="LATEST",
            overwrite=False
        )
        if response.get("status") == "confirm_needed":
            print(f"Confirmation needed: {response['message']}")
            # Optionally, resend with overwrite=True
            # response = await client.async_install_new_server("MyNewServer", "LATEST", overwrite=True)
        elif response.get("status") == "success":
            print(f"Install successful: {response['message']}")
    except APIError as e:
        print(f"Install failed: {e}")
    ```

---

### Server Information Methods

These methods retrieve information and status details about specific server instances or all servers.

#### `async_get_servers_details()`

Fetches a list of all detected Bedrock server instances managed by the application, along with their last known status and installed version.

*   **Corresponds to:** `GET /api/servers`
*   **Authentication:** Required.
*   **Arguments:** None.
*   **Returns:**
    *   *Type:* `List[Dict[str, Any]]`
    *   *Description:* A list of dictionaries. Each dictionary represents a server and contains the keys:
        *   `name` (*str*): The unique name of the server instance.
        *   `status` (*str*): The last known status from the server's config file (e.g., "RUNNING", "STOPPED").
        *   `version` (*str*): The installed version from the server's config file (e.g., "1.20.40.01").
        The method processes the raw API response to return this list directly. If the API reports partial errors (e.g., "Completed with errors..."), a warning is logged, but successfully parsed servers are still returned.
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `APIServerSideError`: If the API encounters a fundamental issue accessing directories.
    *   `APIError`: If the response structure is unexpected or malformed.
*   **Example:**
    ```python
    servers = await client.async_get_servers_details()
    for server in servers:
        print(f"Name: {server['name']}, Status: {server['status']}, Version: {server['version']}")
    ```

---
#### `async_get_server_names()`

A convenience method that fetches a simplified, sorted list of just server names. It internally calls `async_get_servers_details()`.

*   **Corresponds to:** (Uses `GET /api/servers` internally)
*   **Authentication:** Required.
*   **Arguments:** None.
*   **Returns:**
    *   *Type:* `List[str]`
    *   *Description:* A sorted list of server names.
*   **Raises:** (Same as `async_get_servers_details()`)
    *   `CannotConnectError`, `AuthError`, `APIServerSideError`, `APIError`.
*   **Example:**
    ```python
    server_names = await client.async_get_server_names()
    print("Available server names:", server_names)
    ```

---
#### `async_get_server_validate(server_name)`

Validates if the server directory and the main executable (`bedrock_server`) exist for the specified server name.

*   **Corresponds to:** `GET /api/server/{server_name}/validate`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The unique name of the server instance to validate.
*   **Returns:**
    *   *Type:* `bool`
    *   *Description:* `True` if the server is found and considered valid by the API (API returns HTTP 200 with `{"status": "success", ...}`).
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `ServerNotFoundError`: If the API returns HTTP 404, indicating the server directory or executable was not found.
    *   `InvalidInputError`: If `server_name` is invalid (e.g. empty string) as per API validation.
    *   `APIServerSideError`: If the API has configuration issues preventing validation.
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    server_to_check = "MyExistingServer"
    try:
        is_valid = await client.async_get_server_validate(server_to_check)
        if is_valid:
            print(f"Server '{server_to_check}' is valid.")
    except ServerNotFoundError:
        print(f"Server '{server_to_check}' not found or invalid.")
    ```

---
#### `async_get_server_status_info(server_name)`

Retrieves runtime status information for a specific server process, including running state and basic resource usage (PID, CPU, Memory, Uptime) if the process is active.

*   **Corresponds to:** `GET /api/server/{server_name}/status_info`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The unique name of the server instance.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary containing the server's process information.
        *   If server is running:
            ```json
            {
                "status": "success",
                "process_info": {
                    "pid": 12345,
                    "cpu_percent": 10.5,
                    "memory_mb": 512.5,
                    "uptime": "1:00:00"
                }
            }
            ```
        *   If server is not running:
            ```json
            {
                "status": "success",
                "process_info": null,
                "message": "Server '<server_name>' is not running."
            }
            ```
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `ServerNotFoundError`: If the API determines the server itself doesn't exist (pre-request validation).
    *   `InvalidInputError`: If `server_name` is invalid.
    *   `APIServerSideError`: If the API has configuration issues (e.g., `BASE_DIR` missing) or errors with `psutil`.
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    status_info = await client.async_get_server_status_info("MyServer")
    if status_info.get("process_info"):
        print(f"PID: {status_info['process_info']['pid']}")
    else:
        print(status_info.get("message", "Server not running or info unavailable."))
    ```

---
#### `async_get_server_running_status(server_name)`

Checks if the Bedrock server process for the specified server instance is currently running.

*   **Corresponds to:** `GET /api/server/{server_name}/running_status`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The unique name of the server instance.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary indicating the running status.
        ```json
        {
            "status": "success",
            "is_running": true // or false
        }
        ```
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `ServerNotFoundError`: If the API determines the server itself doesn't exist.
    *   `InvalidInputError`: If `server_name` is invalid.
    *   `APIServerSideError`: If the API has configuration or `psutil` issues.
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    running_status = await client.async_get_server_running_status("MyServer")
    print(f"Server is running: {running_status.get('is_running')}")
    ```

---
#### `async_get_server_config_status(server_name)`

Gets the status string stored within the server's specific configuration file (e.g., "Installed", "Stopped").

*   **Corresponds to:** `GET /api/server/{server_name}/config_status`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The unique name of the server instance.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary containing the config status.
        ```json
        {
            "status": "success",
            "config_status": "Installed" // Example status
        }
        ```
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `ServerNotFoundError`: If the API determines the server itself doesn't exist.
    *   `InvalidInputError`: If `server_name` is invalid.
    *   `APIServerSideError`: If the API cannot access or read the server's config file.
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    config_stat = await client.async_get_server_config_status("MyServer")
    print(f"Config status: {config_stat.get('config_status')}")
    ```

---
#### `async_get_server_version(server_name)`

Gets the installed Bedrock server version string stored within the server's specific configuration file.

*   **Corresponds to:** `GET /api/server/{server_name}/version`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The unique name of the server instance.
*   **Returns:**
    *   *Type:* `Optional[str]`
    *   *Description:* The installed version string (e.g., `"1.20.81.01"`) if found and the API call is successful. Returns `None` if the version cannot be determined (e.g., API error, "installed_version" key missing or null in response).
*   **Raises:** (Note: This method catches `APIError` and returns `None` instead. `CannotConnectError` would still propagate if it occurs before `_request` completes.)
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails (would be caught and result in `None`).
*   **Example:**
    ```python
    version = await client.async_get_server_version("MyServer")
    if version:
        print(f"Installed version: {version}")
    else:
        print("Could not retrieve server version.")
    ```

---
#### `async_get_server_world_name(server_name)`

Gets the configured world name (`level-name` property) from the `server.properties` file for the specified server.

*   **Corresponds to:** `GET /api/server/{server_name}/world_name`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The unique name of the server instance.
*   **Returns:**
    *   *Type:* `Optional[str]`
    *   *Description:* The world name string (e.g., `"Bedrock level"`) if found and the API call is successful. Returns `None` if the world name cannot be determined (e.g., API error, "world_name" key missing or null in response).
*   **Raises:** (Note: Catches `APIError` and returns `None`. `CannotConnectError` would still propagate.)
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails (would be caught and result in `None`).
*   **Example:**
    ```python
    world_name = await client.async_get_server_world_name("MyServer")
    if world_name:
        print(f"World name: {world_name}")
    else:
        print("Could not retrieve world name.")
    ```

---
#### `async_get_server_properties(server_name)`

Retrieves the parsed content of the server's `server.properties` file.

*   **Corresponds to:** `GET /api/server/{server_name}/read_properties`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The unique name of the server instance.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary representing the API response. The actual server properties are within the `properties` key of this dictionary.
        ```json
        {
            "status": "success",
            "properties": {
                "server-name": "My Bedrock Server",
                "gamemode": "survival",
                // ... other properties
            }
        }
        ```
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `ServerNotFoundError`: If the API determines the server itself or its `server.properties` file doesn't exist.
    *   `InvalidInputError`: If `server_name` is invalid.
    *   `APIServerSideError`: If the API has issues reading the file.
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    response = await client.async_get_server_properties("MyServer")
    server_props = response.get("properties", {})
    print(f"Max players: {server_props.get('max-players')}")
    ```

---
#### `async_get_server_permissions_data(server_name)`

Retrieves player permissions from the server's `permissions.json` file, optionally enriched with names from the global `players.json`.

*   **Corresponds to:** `GET /api/server/{server_name}/permissions_data`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The unique name of the server instance.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary representing the API response. The player permissions list is within `data.permissions`.
        ```json
        {
            "status": "success",
            "data": {
                "permissions": [
                    {"xuid": "...", "name": "...", "permission_level": "operator"},
                    // ... more players
                ]
            },
            "message": "Successfully retrieved server permissions." // Optional
        }
        ```
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `ServerNotFoundError`: If the API determines the server directory doesn't exist.
    *   `InvalidInputError`: If `server_name` is invalid.
    *   `APIServerSideError`: If the API has issues reading or parsing `permissions.json`.
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    response = await client.async_get_server_permissions_data("MyServer")
    permissions_list = response.get("data", {}).get("permissions", [])
    for p_data in permissions_list:
        print(f"{p_data['name']} ({p_data['xuid']}): {p_data['permission_level']}")
    ```

---
#### `async_get_server_allowlist(server_name)`

Retrieves the current list of players from the server's `allowlist.json` file.

*   **Corresponds to:** `GET /api/server/{server_name}/allowlist`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The unique name of the server instance.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary representing the API response. The allowlist players are within the `existing_players` key.
        ```json
        {
            "status": "success",
            "existing_players": [
                {"ignoresPlayerLimit": false, "name": "PlayerOne"},
                // ... more players
            ],
            "message": "Successfully retrieved X players from allowlist."
        }
        ```
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `ServerNotFoundError`: If the API determines the server directory doesn't exist.
    *   `InvalidInputError`: If `server_name` is invalid.
    *   `APIServerSideError`: If the API has issues reading or parsing `allowlist.json`.
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    response = await client.async_get_server_allowlist("MyServer")
    allowlisted_players = response.get("existing_players", [])
    for player in allowlisted_players:
        print(f"Allowlisted: {player['name']}")
    ```

---

### Server Action Methods

These methods perform actions on specific server instances, such as starting, stopping, or configuring them.

#### `async_start_server(server_name)`

Starts the specified Bedrock server instance.

*   **Corresponds to:** `POST /api/server/{server_name}/start`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The unique name of the server instance to start.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary confirming the action.
        ```json
        {
            "status": "success",
            "message": "Server '<server_name>' started successfully."
        }
        ```
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `ServerNotFoundError`: If the server executable is not found by the API.
    *   `InvalidInputError`: If `server_name` is invalid.
    *   `APIServerSideError`: If the server is already running, fails to start (OS issues, timeout), or if there are configuration errors.
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    response = await client.async_start_server("MyServer")
    print(response['message'])
    ```

---
#### `async_stop_server(server_name)`

Stops the specified running Bedrock server instance.

*   **Corresponds to:** `POST /api/server/{server_name}/stop`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The unique name of the server instance to stop.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary confirming the action.
        ```json
        {
            "status": "success",
            "message": "Server '<server_name>' stopped successfully." // or "...was already stopped."
        }
        ```
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `ServerNotFoundError`: If the server executable is missing (though process might be found).
    *   `InvalidInputError`: If `server_name` is invalid.
    *   `APIServerSideError`: If sending the stop command fails, the server fails to stop within timeout, or OS-specific errors occur.
    *   `OperationFailedError`: If stopping is attempted on an unsupported OS (e.g., for graceful shutdown command).
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    response = await client.async_stop_server("MyServer")
    print(response['message'])
    ```

---
#### `async_restart_server(server_name)`

Restarts the specified Bedrock server instance.

*   **Corresponds to:** `POST /api/server/{server_name}/restart`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The unique name of the server instance to restart.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary confirming the action.
        ```json
        {
            "status": "success",
            "message": "Server '<server_name>' restarted successfully." // or "...was not running and was started."
        }
        ```
*   **Raises:** (Can raise errors related to both stop and start phases)
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `ServerNotFoundError`: If server executable is missing.
    *   `InvalidInputError`: If `server_name` is invalid.
    *   `APIServerSideError`: If the stop or start phase fails due to various reasons (timeout, OS errors, config issues).
    *   `OperationFailedError`: If underlying stop/start is attempted on an unsupported OS.
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    response = await client.async_restart_server("MyServer")
    print(response['message'])
    ```

---
#### `async_send_server_command(server_name, command)`

Sends a command string to the specified running Bedrock server instance's console input.

*   **Corresponds to:** `POST /api/server/{server_name}/send_command`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The unique name of the target server instance.
    *   `command` (*str*, required): The command string to be sent to the server console.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary confirming the command was sent.
        ```json
        {
            "status": "success",
            "message": "Command '<command>' sent successfully."
        }
        ```
*   **Raises:**
    *   `ValueError`: If `command` is empty or whitespace only (client-side validation).
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `ServerNotFoundError`: If the server executable is missing.
    *   `ServerNotRunningError`: If the API indicates the server is not running or cannot be communicated with (e.g., screen session/pipe not found).
    *   `InvalidInputError`: If `server_name` is invalid or JSON body is malformed by API's standards.
    *   `APIServerSideError`: If the command sending process fails (e.g., screen/pipe error, config issues).
    *   `OperationFailedError`: If sending commands is attempted on an unsupported OS or `pywin32` is missing on Windows.
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    try:
        response = await client.async_send_server_command("MyServer", "say Hello from API!")
        print(response['message'])
    except ValueError as e:
        print(f"Input Error: {e}")
    ```

---
#### `async_update_server(server_name)`

Checks for the latest Bedrock Dedicated Server version and updates the specified server instance if a newer version is available or if the installed version is unknown.

*   **Corresponds to:** `POST /api/server/{server_name}/update`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The unique name of the server instance to update.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary indicating the outcome of the update process.
        *   If update performed: `{"status": "success", "updated": true, "new_version": "1.x.y.z", "message": "..."}`
        *   If already up-to-date: `{"status": "success", "updated": false, "new_version": "1.x.y.z", "message": "..."}`
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `ServerNotFoundError`: If the server itself doesn't exist.
    *   `InvalidInputError`: If `server_name` is invalid.
    *   `APIServerSideError`: If any step of the update process fails (config errors, internet connectivity, download, extraction, backup, server stop/start).
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    response = await client.async_update_server("MyServer")
    print(response['message'])
    if response.get('updated'):
        print(f"Updated to version: {response.get('new_version')}")
    ```

---
#### `async_add_server_allowlist(server_name, players, ignores_player_limit)`

Adds players to the server's `allowlist.json` file.

*   **Corresponds to:** `POST /api/server/{server_name}/allowlist/add`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The name of the server instance.
    *   `players` (*List[str]*, required): A list of player names (Gamertags) to add.
    *   `ignores_player_limit` (*bool*, optional): Sets the `ignoresPlayerLimit` flag for all players being added. Defaults to `False`.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary confirming the action.
        ```json
        {
            "status": "success",
            "message": "Allowlist saved successfully with X player(s)." // Or "No new players..."
        }
        ```
*   **Raises:**
    *   `TypeError`: If `players` is not a list (client-side validation).
    *   `ValueError`: If any player name in `players` is not a non-empty string (client-side validation).
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `ServerNotFoundError`: If the server directory doesn't exist.
    *   `InvalidInputError`: If `server_name` is invalid or JSON body is malformed (e.g., `ignoresPlayerLimit` not boolean).
    *   `APIServerSideError`: If reading/writing `allowlist.json` fails on the server.
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    try:
        response = await client.async_add_server_allowlist("MyServer", ["NewPlayer1", "VIP_User"], ignores_player_limit=True)
        print(response['message'])
    except (TypeError, ValueError) as e:
        print(f"Input error: {e}")
    ```

---
#### `async_remove_server_allowlist_player(server_name, player_name)`

Removes a specific player from the server's `allowlist.json` file. Player name matching is case-insensitive on the API side.

*   **Corresponds to:** `DELETE /api/server/{server_name}/allowlist/player/{player_name}`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The unique name of the server instance.
    *   `player_name` (*str*, required): The name of the player to remove. This will be URL-encoded.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary confirming the action.
        *   If player removed: `{"status": "success", "message": "Player '<player_name>' removed..."}`
        *   If player not found: `{"status": "success", "message": "Player '<player_name>' not found..."}`
*   **Raises:**
    *   `ValueError`: If `player_name` is empty or whitespace (client-side validation).
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `ServerNotFoundError`: If the server directory doesn't exist.
    *   `InvalidInputError`: If `server_name` or `player_name` is invalid as per API.
    *   `APIServerSideError`: If reading/writing `allowlist.json` fails on the server.
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    try:
        response = await client.async_remove_server_allowlist_player("MyServer", "OldPlayer")
        print(response['message'])
    except ValueError as e:
        print(f"Input error: {e}")
    ```

---
#### `async_set_server_permissions(server_name, permissions_dict)`

Updates permission levels for one or more players in the server's `permissions.json` file.

*   **Corresponds to:** `PUT /api/server/{server_name}/permissions`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The name of the server instance.
    *   `permissions_dict` (*Dict[str, str]*, required): A dictionary mapping player XUIDs (strings) to desired permission level strings (`"visitor"`, `"member"`, or `"operator"`). Invalid levels will cause a `ValueError`.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary confirming the action.
        ```json
        {
            "status": "success",
            "message": "Permissions updated successfully for X player(s)..." // Or "No valid permission changes..."
        }
        ```
*   **Raises:**
    *   `TypeError`: If `permissions_dict` is not a dictionary (client-side).
    *   `ValueError`: If any permission level in `permissions_dict` is invalid (client-side).
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `ServerNotFoundError`: If the server directory doesn't exist.
    *   `InvalidInputError`: If the API rejects the input (e.g., malformed JSON, `server_name` invalid, or server-side validation of levels if different from client).
    *   `APIServerSideError`: If reading/writing `permissions.json` fails on the server.
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    permissions_to_set = {
        "2535416409681153": "operator",
        "2535457894355891": "member"
    }
    try:
        response = await client.async_set_server_permissions("MyServer", permissions_to_set)
        print(response['message'])
    except (TypeError, ValueError) as e:
        print(f"Input error: {e}")
    ```

---
#### `async_update_server_properties(server_name, properties_dict)`

Updates specified key-value pairs in the `server.properties` file for the given server. Only properties present in a predefined API allowlist can be modified.

*   **Corresponds to:** `POST /api/server/{server_name}/properties`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The name of the server instance.
    *   `properties_dict` (*Dict[str, Any]*, required): A dictionary where keys are `server.properties` keys and values are their new desired values. Values are typically strings, but numbers are accepted by the API for relevant fields.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary confirming the action.
        ```json
        {
            "status": "success",
            "message": "Server properties for '<server_name>' updated successfully." // Or "No valid properties..."
        }
        ```
*   **Raises:**
    *   `TypeError`: If `properties_dict` is not a dictionary (client-side).
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `ServerNotFoundError`: If the server's `server.properties` file is not found.
    *   `InvalidInputError`: If `server_name` is invalid, or if API validation fails for any property value (type, range, format). The `api_errors` attribute of the exception may detail specific failures.
    *   `APIServerSideError`: If reading/writing `server.properties` fails on the server.
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    properties_to_update = {
        "max-players": "15",
        "difficulty": "hard",
        "level-name": "My Awesome World" # API will clean this to "My_Awesome_World"
    }
    try:
        response = await client.async_update_server_properties("MyServer", properties_to_update)
        print(response['message'])
    except TypeError as e:
        print(f"Input error: {e}")
    ```

---
#### `async_configure_server_os_service(server_name, service_config)`

Configures OS-specific service settings for the server instance (e.g., systemd on Linux, `autoupdate` flag in config on Windows).

*   **Corresponds to:** `POST /api/server/{server_name}/service`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The name of the server instance.
    *   `service_config` (*Dict[str, bool]*, required): A dictionary with OS-specific boolean flags.
        *   **Linux:** `{"autoupdate": bool, "autostart": bool}`
        *   **Windows:** `{"autoupdate": bool}`
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary confirming the action, with OS-specific message.
        *   Linux: `{"status": "success", "message": "Systemd service created and enabled successfully."}`
        *   Windows: `{"status": "success", "message": "Autoupdate setting for '<server_name>' updated to true."}`
*   **Raises:**
    *   `TypeError`: If `service_config` is not a dictionary (client-side).
    *   `ValueError`: If any value in `service_config` is not a boolean (client-side).
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `InvalidInputError`: If `server_name` is invalid, JSON body is malformed, or keys/values are not boolean as per API.
    *   `OperationFailedError` (HTTP 403/500 from API): If called on an unsupported OS by the manager.
    *   `APIServerSideError`: If underlying OS operations fail (e.g., `systemctl` errors, config file write errors).
    *   `APIError`: For other API response issues.
*   **Example (assuming manager is on Linux):**
    ```python
    linux_service_config = {"autoupdate": True, "autostart": True}
    try:
        response = await client.async_configure_server_os_service("MyLinuxServer", linux_service_config)
        print(response['message'])
    except (TypeError, ValueError) as e:
        print(f"Input error: {e}")
    ```

---
#### `async_delete_server(server_name)`

Permanently deletes all data associated with the specified server instance (installation, config, backups). **This action is irreversible.**

*   **Corresponds to:** `DELETE /api/server/{server_name}/delete`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The unique name of the server instance to delete.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary confirming the deletion.
        ```json
        {
            "status": "success",
            "message": "All data for server '<server_name>' deleted successfully."
        }
        ```
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `ServerNotFoundError`: If the server does not exist.
    *   `InvalidInputError`: If `server_name` is invalid.
    *   `APIServerSideError`: If stopping the server before deletion fails, or if deleting directories fails (permissions, files in use).
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    # USE WITH EXTREME CAUTION!
    # confirm_delete = input("Are you sure you want to delete 'MyServerToDelete'? (yes/no): ")
    # if confirm_delete.lower() == 'yes':
    #     response = await client.async_delete_server("MyServerToDelete")
    #     print(response['message'])
    ```

---

### Content Management Methods

These methods deal with managing server content like backups, worlds, and addons.

#### `async_list_server_backups(server_name, backup_type)`

Lists available backup filenames (basenames only) for a specified server and backup type.

*   **Corresponds to:** `GET /api/server/{server_name}/backups/list/{backup_type}`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The name of the server.
    *   `backup_type` (*str*, required): The type of backups to list. Must be `"world"`, `"properties"`, `"allowlist"`, `"permissions"`, or `"all"` (case-insensitive).
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary containing the list of backup filenames.
        * If `backup_type` is `"world"`, `"properties"`, `"allowlist"`, or `"permissions"`, the `backups` key will contain a `List[str]` of filenames:
            ```json
            {
                "status": "success",
                "backups": [
                    "world_backup_20231027103000.mcworld",
                    // ... more filenames
                ]
            }
            ```
            Returns `{"status": "success", "backups": []}` if no backups of the specified type are found.
        * If `backup_type` is `"all"`, the `backups` key will contain a `Dict[str, List[str]]` with categorized filenames. Categories will only be included if files are found for them:
            ```json
            {
                "status": "success",
                "backups": {
                    "allowlist_backups": [
                        "allowlist_backup_20240115080000.json",
                        "allowlist_backup_20231201120000.json"
                    ],
                    "permissions_backups": [
                        "permissions_backup_20240115080000.json"
                    ],
                    "properties_backups": [
                        "server_backup_20240115080000.properties",
                        "server_backup_20231201120000.properties"
                    ],
                    "world_backups": [
                        "my_world.mcworld",
                        "my_other_world.mcworld"
                    ]
                }
            }
            ```
            Returns `{"status": "success", "backups": {}}` if `backup_type="all"` but no backups of any type are found.
*   **Raises:**
    *   `ValueError`: If `backup_type` is not one of the allowed values (client-side).
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `ServerNotFoundError`: If the server does not exist.
    *   `InvalidInputError`: If `server_name` is invalid.
    *   `APIServerSideError`: If the API has issues accessing the backup directory.
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    try:
        response = await client.async_list_server_backups("MyServer", "world")
        print("World backups:", response.get("backups", []))
    except ValueError as e:
        print(f"Input error: {e}")
    ```

---
#### `async_get_content_worlds()`

Lists available world template files (`.mcworld`) found in the manager's configured `content/worlds` directory.

*   **Corresponds to:** `GET /api/content/worlds`
*   **Authentication:** Required.
*   **Arguments:** None.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary containing a list of world filenames.
        ```json
        {
            "status": "success",
            "files": [
                "MyAwesomeWorld.mcworld",
                // ... more filenames
            ]
            // "message": "No matching files found." if applicable
        }
        ```
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `NotFoundError`: If the API reports the content directory itself is not found.
    *   `APIServerSideError`: If `CONTENT_DIR` is not configured or inaccessible on the manager.
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    response = await client.async_get_content_worlds()
    print("Available world templates:", response.get("files", []))
    ```

---
#### `async_get_content_addons()`

Lists available addon files (`.mcpack`, `.mcaddon`) found in the manager's configured `content/addons` directory.

*   **Corresponds to:** `GET /api/content/addons`
*   **Authentication:** Required.
*   **Arguments:** None.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary containing a list of addon filenames.
        ```json
        {
            "status": "success",
            "files": [
                "AwesomeBehaviorPack.mcpack",
                // ... more filenames
            ]
            // "message": "No matching files found." if applicable
        }
        ```
*   **Raises:** (Similar to `async_get_content_worlds()`)
    *   `CannotConnectError`, `AuthError`, `NotFoundError`, `APIServerSideError`, `APIError`.
*   **Example:**
    ```python
    response = await client.async_get_content_addons()
    print("Available addon files:", response.get("files", []))
    ```

---
#### `async_trigger_server_backup(server_name, backup_type, file_to_backup)`

Triggers a backup operation (world, specific config file, or all) for the specified server.

*   **Corresponds to:** `POST /api/server/{server_name}/backup/action`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The name of the server to back up.
    *   `backup_type` (*str*, optional): Type of backup. Must be `"world"`, `"config"`, or `"all"` (case-insensitive). Defaults to `"all"`.
    *   `file_to_backup` (*Optional[str]*, optional): Required if `backup_type` is `"config"`. Specifies the relative path of the configuration file to back up within the server's directory (e.g., `"server.properties"`).
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary confirming the backup operation.
        ```json
        {
            "status": "success",
            "message": "World backup completed successfully for server '<server_name>'." // Message varies
        }
        ```
*   **Raises:**
    *   `ValueError`: If `backup_type` is invalid, or if `backup_type` is "config" and `file_to_backup` is not provided (client-side).
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `ServerNotFoundError`: If the server or the `file_to_backup` does not exist.
    *   `InvalidInputError`: If `server_name` is invalid or other payload issues.
    *   `APIServerSideError`: If the backup operation fails on the server (config errors, file system errors, server stop/start issues).
    *   `APIError`: For other API response issues.
*   **Example (backup all):**
    ```python
    response = await client.async_trigger_server_backup("MyServer", backup_type="all")
    print(response['message'])
    ```
*   **Example (backup specific config):**
    ```python
    try:
        response = await client.async_trigger_server_backup("MyServer", backup_type="config", file_to_backup="server.properties")
        print(response['message'])
    except ValueError as e:
        print(f"Input error: {e}")
    ```

---
#### `async_export_server_world(server_name)`

Exports the currently active world directory of the specified server into a `.mcworld` archive file, saved in the manager's `content/worlds` directory.

*   **Corresponds to:** `POST /api/server/{server_name}/world/export`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The name of the server instance whose world should be exported.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary confirming the export and providing the path to the exported file.
        ```json
        {
            "status": "success",
            "message": "World for server '<server_name>' exported successfully as '<file.mcworld>'.",
            "export_file": "/full/path/to/content/worlds/<file.mcworld>"
        }
        ```
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `ServerNotFoundError`: If the server does not exist.
    *   `InvalidInputError`: If `server_name` is invalid.
    *   `APIServerSideError`: If the export process fails (config errors, cannot determine world name, world directory not found, archive creation error).
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    response = await client.async_export_server_world("MyServer")
    print(response['message'])
    ```

---
#### `async_reset_server_world(server_name)`

Resets the currently active world directory of the specified server.

*   **Corresponds to:** `DELETE /api/server/{server_name}/world/reset`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The name of the server instance whose world should be reset.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary confirming the reset.
        ```json
        {
            "status": "success",
            "message": "World for server '<server_name>' reset successfully."
        }
        ```
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `ServerNotFoundError`: If the server does not exist.
    *   `InvalidInputError`: If `server_name` is invalid.
    *   `APIServerSideError`: If the resett process fails (config errors, cannot determine world name, world directory not found).
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    response = await client.async_reset_server_world("MyServer")
    print(response['message'])
    ```

---
#### `async_prune_server_backups(server_name, keep)`

Deletes older backups for a specific server from its subdirectory within the configured `BACKUP_DIR`.

*   **Corresponds to:** `POST /api/server/{server_name}/backups/prune`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The name of the server whose backups to prune.
    *   `keep` (*Optional[int]*, optional): The number of the most recent backups of *each type* (world, properties, json) to retain. If `None`, the manager's default setting (`BACKUP_KEEP`) is used. Must be a non-negative integer if provided.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary confirming the pruning operation.
        ```json
        {
            "status": "success",
            "message": "Backup pruning completed for server '<server_name>'."
            // Or "No backup directory found, nothing to prune."
        }
        ```
*   **Raises:**
    *   `ValueError`: If `keep` is provided but is not a non-negative integer (client-side).
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `ServerNotFoundError`: If the server does not exist.
    *   `InvalidInputError`: If `server_name` is invalid or the `keep` value is invalid as per API.
    *   `APIServerSideError`: If the pruning process fails (config errors, backup directory issues, file system errors).
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    try:
        response = await client.async_prune_server_backups("MyServer", keep=5)
        print(response['message'])
    except ValueError as e:
        print(f"Input error: {e}")
    ```

---
#### `async_restore_server_backup(server_name, restore_type, backup_file)`

Restores a server's world or a specific configuration file from a specified backup file. **Warning: This overwrites current files.**

*   **Corresponds to:** `POST /api/server/{server_name}/restore/action`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The name of the server instance to restore to.
    *   `restore_type` (*str*, required): Type of restore. Must be `"world"` or `"config"` (case-insensitive).
    *   `backup_file` (*str*, required): The filename of the backup to restore (relative to the server's backup subdirectory within `BACKUP_DIR`).
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary confirming the restore operation.
        ```json
        {
            "status": "success",
            "message": "Restoration from '<backup_file>' (type: <type>) completed successfully."
        }
        ```
*   **Raises:**
    *   `ValueError`: If `restore_type` is invalid (client-side).
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `ServerNotFoundError`: If the server does not exist.
    *   `NotFoundError`: If the specified `backup_file` is not found by the API.
    *   `InvalidInputError`: If `server_name` is invalid, payload is malformed, or `backup_file` path is outside allowed directory.
    *   `APIServerSideError`: If the restore operation fails (config errors, server stop/start issues, unzipping/import errors, file copy errors).
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    try:
        response = await client.async_restore_server_backup("MyServer", "world", "world_backup_xyz.mcworld")
        print(response['message'])
    except ValueError as e:
        print(f"Input error: {e}")
    ```

---
#### `async_restore_server_latest_all(server_name)`

Restores the server's world AND standard configuration files (`server.properties`, `allowlist.json`, `permissions.json`) from their respective *latest* available backups. **Warning: This overwrites current files.**

*   **Corresponds to:** `POST /api/server/{server_name}/restore/all`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The name of the server instance to restore.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary confirming the restore operation.
        ```json
        {
            "status": "success",
            "message": "Restore all completed successfully for server '<server_name>'."
        }
        ```
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `ServerNotFoundError`: If the server does not exist.
    *   `InvalidInputError`: If `server_name` is invalid.
    *   `APIServerSideError`: If any part of the restore (world or any config file) fails.
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    response = await client.async_restore_server_latest_all("MyServer")
    print(response['message'])
    ```

---
#### `async_install_server_world(server_name, filename)`

Installs a world from a `.mcworld` file (located in the manager's `content/worlds` directory) into the specified server, replacing the existing world. **Warning: This overwrites the server's current world.**

*   **Corresponds to:** `POST /api/server/{server_name}/world/install`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The name of the server instance.
    *   `filename` (*str*, required): The path to the `.mcworld` file, relative to the manager's `content/worlds` directory (e.g., `"MyCoolWorld.mcworld"` or `"user_uploads/MyCoolWorld.mcworld"`).
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary confirming the world installation.
        ```json
        {
            "status": "success",
            "message": "World '<filename>' installed successfully for server '<server_name>'."
        }
        ```
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `ServerNotFoundError`: If the server does not exist.
    *   `NotFoundError`: If the specified `filename` (world file) is not found by the API.
    *   `InvalidInputError`: If `server_name` is invalid, payload is malformed, or `filename` path is invalid (e.g., path traversal).
    *   `APIServerSideError`: If the world installation fails (config errors, server stop/start issues, world name determination error, world extraction error).
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    response = await client.async_install_server_world("MyServer", "MyDownloadedWorld.mcworld")
    print(response['message'])
    ```

---
#### `async_install_server_addon(server_name, filename)`

Installs an addon pack (`.mcaddon` or `.mcpack`) from the manager's `content/addons` directory into the specified server. This involves extracting and activating behavior/resource packs.

*   **Corresponds to:** `POST /api/server/{server_name}/addon/install`
*   **Authentication:** Required.
*   **Arguments:**
    *   `server_name` (*str*, required): The name of the server instance.
    *   `filename` (*str*, required): The path to the `.mcaddon` or `.mcpack` file, relative to the manager's `content/addons` directory (e.g., `"CoolBehaviorPack.mcpack"`).
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary confirming the addon installation.
        ```json
        {
            "status": "success",
            "message": "Addon '<filename>' installed successfully for server '<server_name>'."
        }
        ```
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `ServerNotFoundError`: If the server does not exist.
    *   `NotFoundError`: If the specified `filename` (addon file) is not found by the API.
    *   `InvalidInputError`: If `server_name` is invalid, payload is malformed, `filename` path is invalid, addon file has unsupported extension, or manifest issues.
    *   `APIServerSideError`: If the addon installation fails (config errors, server stop/start, world name determination, file extraction, corrupted addon file, file system errors during pack installation/activation).
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    response = await client.async_install_server_addon("MyServer", "AwesomeAddonCollection.mcaddon")
    print(response['message'])
    ```

---

### Scheduler Methods

These methods interact with the host OS's native task scheduling system (Linux `cron` or Windows Task Scheduler) via the Bedrock Server Manager API. **Availability and behavior depend on the operating system where the Bedrock Server Manager is running.**

---
#### Linux Cron Scheduler

These methods are **Linux Only**. They will raise an `OperationFailedError` (typically from a 403 Forbidden or 500 error from the API) if the Bedrock Server Manager is not running on Linux.

##### `async_add_server_cron_job(server_name, new_cron_job)`

Adds a new cron job entry to the crontab of the user running the Bedrock Server Manager process.

*   **Corresponds to:** `POST /api/server/{server_name}/cron_scheduler/add`
*   **Authentication:** Required.
*   **Platform:** Linux Only.
*   **Arguments:**
    *   `server_name` (*str*, required): The server context for the request (used for logging/authorization by API).
    *   `new_cron_job` (*str*, required): The complete, raw cron job line string to be added.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary confirming the addition.
        ```json
        {
            "status": "success",
            "message": "Cron job added successfully."
        }
        ```
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `InvalidInputError`: If `new_cron_job` is empty or `server_name` is invalid.
    *   `OperationFailedError` (HTTP 403/500 from API): If manager is not on Linux.
    *   `APIServerSideError`: If `crontab` command not found or crontab write fails on manager.
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    cron_line = "0 3 * * * /path/to/manager backup-all --server MyServer"
    response = await client.async_add_server_cron_job("MyServer", cron_line)
    print(response['message'])
    ```

---
##### `async_modify_server_cron_job(server_name, old_cron_job, new_cron_job)`

Modifies an existing cron job entry by exact match.

*   **Corresponds to:** `POST /api/server/{server_name}/cron_scheduler/modify`
*   **Authentication:** Required.
*   **Platform:** Linux Only.
*   **Arguments:**
    *   `server_name` (*str*, required): The server context.
    *   `old_cron_job` (*str*, required): The exact, complete, existing cron job line to find and replace.
    *   `new_cron_job` (*str*, required): The new, complete cron job line to replace the old one.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary confirming the modification.
        ```json
        {
            "status": "success",
            "message": "Cron job modified successfully." // Or "No modification needed..."
        }
        ```
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `InvalidInputError`: If cron job strings are empty or `server_name` is invalid.
    *   `NotFoundError`: If `old_cron_job` is not found in the crontab.
    *   `OperationFailedError` (HTTP 403/500 from API): If manager is not on Linux.
    *   `APIServerSideError`: If `crontab` command not found or crontab write fails.
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    old_cron = "0 3 * * * /old/cmd"
    new_cron = "0 4 * * * /new/cmd"
    response = await client.async_modify_server_cron_job("MyServer", old_cron, new_cron)
    print(response['message'])
    ```

---
##### `async_delete_server_cron_job(server_name, cron_string)`

Deletes a specific cron job line from the user's crontab by exact string match.

*   **Corresponds to:** `DELETE /api/server/{server_name}/cron_scheduler/delete`
*   **Authentication:** Required.
*   **Platform:** Linux Only.
*   **Arguments:**
    *   `server_name` (*str*, required): The server context.
    *   `cron_string` (*str*, required): The exact, complete cron job line to find and delete. This string will be URL-encoded by `aiohttp` when sent as a query parameter.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary confirming the deletion attempt.
        ```json
        {
            "status": "success",
            "message": "Cron job deleted successfully (if it existed)."
        }
        ```
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `InvalidInputError`: If `cron_string` is empty or `server_name` is invalid.
    *   `OperationFailedError` (HTTP 403/500 from API): If manager is not on Linux.
    *   `APIServerSideError`: If `crontab` command not found or crontab write fails.
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    cron_to_delete = "0 4 * * * /new/cmd"
    response = await client.async_delete_server_cron_job("MyServer", cron_to_delete)
    print(response['message'])
    ```

---
#### Windows Task Scheduler

These methods are **Windows Only**. They will raise an `OperationFailedError` (typically from a 403 Forbidden or 500 error from the API) if the Bedrock Server Manager is not running on Windows.

##### `async_add_server_windows_task(server_name, command, triggers)`

Creates a new scheduled task in the Windows Task Scheduler.

*   **Corresponds to:** `POST /api/server/{server_name}/task_scheduler/add`
*   **Authentication:** Required.
*   **Platform:** Windows Only.
*   **Arguments:**
    *   `server_name` (*str*, required): The server context for the task.
    *   `command` (*str*, required): The Bedrock Server Manager command to execute (e.g., `"backup-all"`, `"update-server"`). Must be one of the allowed commands.
    *   `triggers` (*List[Dict[str, Any]]*, required): A non-empty list of trigger definition objects. See server API documentation for the structure of trigger objects (e.g., `{"type": "Daily", "start": "YYYY-MM-DDTHH:MM:SS", "interval": 1}`).
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary confirming the task creation and including the generated task name.
        ```json
        {
            "status": "success",
            "message": "Windows task '<generated_task_name>' created successfully.",
            "created_task_name": "bedrock_MyWinServer_backup-all_..."
        }
        ```
*   **Raises:**
    *   `ValueError`: If `command` is not an allowed Windows task command (client-side).
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `InvalidInputError`: If `command` or `triggers` are invalid/missing, or `server_name` is invalid.
    *   `OperationFailedError` (HTTP 403/500 from API): If manager is not on Windows.
    *   `APIServerSideError`: If task XML creation/import fails (`schtasks` errors, config errors).
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    daily_trigger = [{"type": "Daily", "start": "2024-07-04T03:00:00", "interval": 1}]
    try:
        response = await client.async_add_server_windows_task("MyWinServer", "backup-all", daily_trigger)
        print(f"Task '{response['created_task_name']}' created: {response['message']}")
    except ValueError as e:
        print(f"Input error: {e}")
    ```

---
##### `async_get_server_windows_task_details(server_name, task_name)`

Retrieves details about a specific Windows scheduled task by parsing its XML configuration file.

*   **Corresponds to:** `POST /api/server/{server_name}/task_scheduler/details`
*   **Authentication:** Required.
*   **Platform:** Windows Only.
*   **Arguments:**
    *   `server_name` (*str*, required): The server context.
    *   `task_name` (*str*, required): The full name of the task whose details are to be retrieved.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary containing the parsed task details.
        ```json
        {
            "status": "success",
            "task_details": {
                "command_path": "C:\\path\\to\\manager.exe",
                "command_args": "backup-all --server MyWinServer",
                "base_command": "backup-all",
                "triggers": [ /* ...parsed trigger objects... */ ]
            }
        }
        ```
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `InvalidInputError`: If `task_name` is missing or invalid.
    *   `NotFoundError`: If the task's XML configuration file is not found by the API.
    *   `OperationFailedError` (HTTP 403/500 from API): If manager is not on Windows.
    *   `APIServerSideError`: If task XML parsing fails on the manager.
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    task_name_to_get = "bedrock_MyWinServer_backup-all_..."
    response = await client.async_get_server_windows_task_details("MyWinServer", task_name_to_get)
    print("Task Details:", response.get("task_details"))
    ```

---
##### `async_modify_server_windows_task(server_name, task_name, command, triggers)`

Modifies an existing Windows scheduled task by deleting the old one and creating a new one with the provided details. The new task will have a new, timestamped name.

*   **Corresponds to:** `PUT /api/server/{server_name}/task_scheduler/task/{task_name}`
*   **Authentication:** Required.
*   **Platform:** Windows Only.
*   **Arguments:**
    *   `server_name` (*str*, required): The server context.
    *   `task_name` (*str*, required): The current, full name of the task to be replaced. This will be URL-encoded for the path.
    *   `command` (*str*, required): The new Bedrock Server Manager command for the task.
    *   `triggers` (*List[Dict[str, Any]]*, required): A list of new trigger definitions for the task.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary confirming the modification and providing the name of the newly created task.
        ```json
        {
            "status": "success",
            "message": "Windows task modified successfully.",
            "new_task_name": "bedrock_MyWinServer_restart-server_..." // New task name
        }
        ```
*   **Raises:**
    *   `ValueError`: If `command` is not an allowed Windows task command (client-side).
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `InvalidInputError`: If new `command` or `triggers` are invalid.
    *   `OperationFailedError` (HTTP 403/500 from API): If manager is not on Windows.
    *   `APIServerSideError`: If deleting the old task or creating/importing the new task fails.
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    old_task = "bedrock_MyWinServer_backup-all_..."
    new_triggers = [{"type": "Weekly", "start": "2024-07-06T05:00:00", "days": ["Saturday"]}]
    try:
        response = await client.async_modify_server_windows_task("MyWinServer", old_task, "restart-server", new_triggers)
        print(f"Task modified, new task: {response['new_task_name']}")
    except ValueError as e:
        print(f"Input error: {e}")
    ```

---
##### `async_delete_server_windows_task(server_name, task_name)`

Deletes an existing Windows scheduled task and its associated XML configuration file.

*   **Corresponds to:** `DELETE /api/server/{server_name}/task_scheduler/task/{task_name}`
*   **Authentication:** Required.
*   **Platform:** Windows Only.
*   **Arguments:**
    *   `server_name` (*str*, required): The server context.
    *   `task_name` (*str*, required): The full name of the task to delete. This will be URL-encoded for the path.
*   **Returns:**
    *   *Type:* `Dict[str, Any]`
    *   *Description:* A dictionary confirming the deletion.
        ```json
        {
            "status": "success",
            "message": "Task '<task_name>' and its definition file deleted successfully."
        }
        ```
*   **Raises:**
    *   `CannotConnectError`: If connection to the API fails.
    *   `AuthError`: If authentication fails.
    *   `OperationFailedError` (HTTP 403/500 from API): If manager is not on Windows.
    *   `APIServerSideError`: If deleting the task from Task Scheduler or its XML file fails.
    *   `APIError`: For other API response issues.
*   **Example:**
    ```python
    task_to_delete = "bedrock_MyWinServer_restart-server_..."
    response = await client.async_delete_server_windows_task("MyWinServer", task_to_delete)
    print(response['message'])
    ```

---