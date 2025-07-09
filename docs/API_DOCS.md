# Bedrock Server Manager API Client Documentation

This document provides documentation for the `bsm_api_client.BedrockServerManagerApi` Python client, used to interact with the Bedrock Server Manager API.

## Initialization

The client is initialized as follows:

```python
from bsm_api_client import BedrockServerManagerApi
import asyncio

async def main():
    client = BedrockServerManagerApi(
        host="your_server_host",
        username="your_username",
        password="your_password",
        port=11325, # Optional, defaults based on scheme or can be omitted
        # base_path="/api", # Optional, defaults to /api
        # request_timeout=10, # Optional, defaults to 10 seconds
        # use_ssl=False, # Optional, defaults to False
        # verify_ssl=True # Optional, defaults to True (if use_ssl is True)
    )

    try:
        # Authenticate (usually called automatically on first protected request,
        # but can be called explicitly)
        # await client.authenticate() # Not typically needed to call directly

        # Example: Get server list
        servers = await client.async_get_servers_details()
        print(servers)

        # Example: Get all settings (new method)
        settings = await client.async_get_all_settings()
        print(settings)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Authentication Methods

Methods related to client authentication. These are part of `ClientBase` but exposed via the main client.

### `async client.authenticate()`

*   **Description**: Authenticates with the API using the provided username and password. Stores the JWT token internally for subsequent requests. Typically, this method is called automatically by the client when an authenticated endpoint is accessed and no valid token is present.
*   **API Endpoint**: `POST /auth/token`
*   **Request Body**: `application/x-www-form-urlencoded` with `username` and `password`.
*   **Returns**: `bool` - `True` if authentication is successful.
*   **Raises**: `AuthError` on failure.
*   **Note**: This method was updated to use form data and target the `/auth/token` endpoint.

### `async client.async_logout()`

*   **Description**: Logs the current user out by calling the API's logout endpoint. Clears the internally stored JWT token.
*   **API Endpoint**: `GET /auth/logout`
*   **Returns**: `Dict[str, Any]` - API response, typically a success message.
*   **Raises**: `APIError` or subclasses on failure.

## Manager Methods

Global management and information methods.

### `async client.async_get_info()`

*   **Description**: Gets system and application information from the manager.
*   **API Endpoint**: `GET /api/info`
*   **Returns**: `Dict[str, Any]` - System and application info.

### `async client.async_scan_players()`

*   **Description**: Triggers scanning of player logs across all servers.
*   **API Endpoint**: `POST /api/players/scan`
*   **Returns**: `Dict[str, Any]` - API response.

### `async client.async_get_players()`

*   **Description**: Gets the global list of known players (name and XUID).
*   **API Endpoint**: `GET /api/players/get`
*   **Returns**: `Dict[str, Any]` - API response, players are usually in a "players" key.

### `async client.async_add_players(players_data: List[str])`

*   **Description**: Adds or updates players in the global list. Each string in `players_data` should be in "PlayerName:PlayerXUID" format.
*   **API Endpoint**: `POST /api/players/add`
*   **Arguments**:
    *   `players_data: List[str]` - List of player strings.
*   **Returns**: `Dict[str, Any]` - API response.

### `async client.async_prune_downloads(directory: str, keep: Optional[int] = None)`

*   **Description**: Triggers pruning of downloaded server archives in a specified directory.
*   **API Endpoint**: `POST /api/downloads/prune`
*   **Arguments**:
    *   `directory: str` - Subdirectory within the cache to prune (e.g., "stable").
    *   `keep: Optional[int]` - Number of recent archives to keep. (Payload: `{"directory": "...", "keep": ...}`)
*   **Returns**: `Dict[str, Any]` - API response.

### `async client.async_install_new_server(server_name: str, server_version: str, overwrite: bool = False)`

*   **Description**: Requests installation of a new Bedrock server instance.
*   **API Endpoint**: `POST /api/server/install`
*   **Arguments**:
    *   `server_name: str`
    *   `server_version: str` (e.g., "LATEST", "1.20.81.01")
    *   `overwrite: bool` (default: `False`)
*   **Returns**: `Dict[str, Any]` - API response (model: `InstallServerResponse`). May indicate success or `confirm_needed`.

### `async client.async_get_all_settings()` (New)

*   **Description**: Retrieves all global application settings.
*   **API Endpoint**: `GET /api/settings`
*   **Returns**: `Dict[str, Any]` - API response (model: `SettingsResponse`), settings are in a "settings" key.

### `async client.async_set_setting(key: str, value: Any)` (New)

*   **Description**: Sets a specific global application setting.
*   **API Endpoint**: `POST /api/settings`
*   **Arguments**:
    *   `key: str` - Dot-notation key of the setting (e.g., "web.port").
    *   `value: Any` - The new value for the setting.
*   **Request Payload**: `{"key": "...", "value": ...}` (model: `SettingItem`)
*   **Returns**: `Dict[str, Any]` - API response (model: `SettingsResponse`).

### `async client.async_reload_settings()` (New)

*   **Description**: Forces a reload of global application settings and logging configuration.
*   **API Endpoint**: `POST /api/settings/reload`
*   **Returns**: `Dict[str, Any]` - API response (model: `SettingsResponse`).

### `async client.async_get_panorama_image()` (New)

*   **Description**: Fetches the custom `panorama.jpeg` background image.
*   **API Endpoint**: `GET /api/panorama`
*   **Returns**: `bytes` - Raw image data.
*   **Note**: This method makes a direct session call to handle binary data.

## Server Information Methods

Methods for retrieving information about specific server instances.

### `async client.async_get_servers_details()`

*   **Description**: Fetches a list of all detected server instances with details (name, status, version).
*   **API Endpoint**: `GET /api/servers`
*   **Returns**: `List[Dict[str, Any]]` - List of server detail dictionaries from `response.get("servers")`.

### `async client.async_get_server_names()`

*   **Description**: Convenience wrapper around `async_get_servers_details` to get a list of just server names.
*   **Returns**: `List[str]` - Sorted list of server names.

### `async client.async_get_server_validate(server_name: str)`

*   **Description**: Validates if the server directory and executable exist.
*   **API Endpoint**: `GET /api/server/{server_name}/validate`
*   **Returns**: `bool` - True if valid, otherwise raises `ServerNotFoundError` or `APIError`.

### `async client.async_get_server_process_info(server_name: str)`

*   **Description**: Gets runtime status information (PID, CPU, Memory, Uptime) for a server.
*   **API Endpoint**: `GET /api/server/{server_name}/process_info`
*   **Returns**: `Dict[str, Any]` - Process info, `response.get("data", {}).get("process_info")` will be null if not running.

### `async client.async_get_server_running_status(server_name: str)`

*   **Description**: Checks if the Bedrock server process is currently running.
*   **API Endpoint**: `GET /api/server/{server_name}/status`
*   **Returns**: `Dict[str, Any]` - API Response. Running status is in `response.get("data", {}).get("running")`.
*   **Note**: Path changed from `.../running_status` to `.../status`. Response structure also changed.

### `async client.async_get_server_config_status(server_name: str)`

*   **Description**: Gets the status string stored in the server's configuration file.
*   **API Endpoint**: `GET /api/server/{server_name}/config_status`
*   **Returns**: `Dict[str, Any]` - Config status in `response.get("data", {}).get("config_status")`.

### `async client.async_get_server_version(server_name: str)`

*   **Description**: Gets the installed Bedrock server version from the server's config file.
*   **API Endpoint**: `GET /api/server/{server_name}/version`
*   **Returns**: `Optional[str]` - Version string from `response.get("data", {}).get("version")`, or None.

### `async client.async_get_server_properties(server_name: str)`

*   **Description**: Retrieves the parsed content of the server's `server.properties` file.
*   **API Endpoint**: `GET /api/server/{server_name}/properties/get`
*   **Returns**: `Dict[str, Any]` - Properties are in `response.get("properties")`.

### `async client.async_get_server_permissions_data(server_name: str)`

*   **Description**: Retrieves player permissions from the server's `permissions.json` file.
*   **API Endpoint**: `GET /api/server/{server_name}/permissions/get`
*   **Returns**: `Dict[str, Any]` - Permissions list in `response.get("data", {}).get("permissions")`.

### `async client.async_get_server_allowlist(server_name: str)`

*   **Description**: Retrieves the list of players from the server's `allowlist.json` file.
*   **API Endpoint**: `GET /api/server/{server_name}/allowlist/get`
*   **Returns**: `Dict[str, Any]` - Player list in `response.get("players")`.

### `async client.async_get_world_icon_image(server_name: str)` (New)

*   **Description**: Fetches the `world_icon.jpeg` for a server.
*   **API Endpoint**: `GET /api/server/{server_name}/world/icon`
*   **Arguments**:
    *   `server_name: str`
*   **Returns**: `bytes` - Raw image data.
*   **Note**: This method makes a direct session call to handle binary data and includes authentication retry logic.

## Server Action Methods

Methods for performing actions on server instances.

### `async client.async_start_server(server_name: str)`

*   **Description**: Starts the specified server.
*   **API Endpoint**: `POST /api/server/{server_name}/start`
*   **Returns**: `Dict[str, Any]` - API response (model: `ActionResponse`).

### `async client.async_stop_server(server_name: str)`

*   **Description**: Stops the specified server.
*   **API Endpoint**: `POST /api/server/{server_name}/stop`
*   **Returns**: `Dict[str, Any]` - API response (model: `ActionResponse`).

### `async client.async_restart_server(server_name: str)`

*   **Description**: Restarts the specified server.
*   **API Endpoint**: `POST /api/server/{server_name}/restart`
*   **Returns**: `Dict[str, Any]` - API response (model: `ActionResponse`).

### `async client.async_send_server_command(server_name: str, command: str)`

*   **Description**: Sends a command to the server's console.
*   **API Endpoint**: `POST /api/server/{server_name}/send_command`
*   **Arguments**:
    *   `server_name: str`
    *   `command: str`
*   **Request Payload**: `{"command": "..."}` (model: `CommandPayload`)
*   **Returns**: `Dict[str, Any]` - API response (model: `ActionResponse`).

### `async client.async_update_server(server_name: str)`

*   **Description**: Checks for and applies updates to the server.
*   **API Endpoint**: `POST /api/server/{server_name}/update`
*   **Returns**: `Dict[str, Any]` - API response (model: `ActionResponse`).

### `async client.async_add_server_allowlist(server_name: str, players: List[str], ignores_player_limit: bool = False)`

*   **Description**: Adds players to the server's allowlist.
*   **API Endpoint**: `POST /api/server/{server_name}/allowlist/add`
*   **Arguments**:
    *   `server_name: str`
    *   `players: List[str]`
    *   `ignores_player_limit: bool` (default: `False`)
*   **Request Payload**: `{"players": [...], "ignoresPlayerLimit": ...}` (model: `AllowlistAddPayload`)
*   **Returns**: `Dict[str, Any]` - API response.

### `async client.async_remove_server_allowlist_players(server_name: str, player_names: List[str])`

*   **Description**: Removes players from the server's allowlist.
*   **API Endpoint**: `DELETE /api/server/{server_name}/allowlist/remove`
*   **Arguments**:
    *   `server_name: str`
    *   `player_names: List[str]`
*   **Request Payload**: `{"players": [...]}` (model: `AllowlistRemovePayload`)
*   **Returns**: `Dict[str, Any]` - API response.

### `async client.async_set_server_permissions(server_name: str, permissions_input: Dict[str, str])`

*   **Description**: Updates permission levels for players.
*   **API Endpoint**: `PUT /api/server/{server_name}/permissions/set`
*   **Arguments**:
    *   `server_name: str`
    *   `permissions_input: Dict[str, str]` - Maps XUIDs to permission levels.
*   **Request Payload**: `{"permissions": [{"xuid": "...", "name": "Unknown", "permission_level": "..."}, ...]}` (model: `PermissionsSetPayload`)
*   **Returns**: `Dict[str, Any]` - API response.
*   **Note**: Payload structure changed. `name` is set to "Unknown".

### `async client.async_update_server_properties(server_name: str, properties_dict: Dict[str, Any])`

*   **Description**: Updates `server.properties` file.
*   **API Endpoint**: `POST /api/server/{server_name}/properties/set`
*   **Arguments**:
    *   `server_name: str`
    *   `properties_dict: Dict[str, Any]`
*   **Request Payload**: `{"properties": {...}}` (model: `PropertiesPayload`)
*   **Returns**: `Dict[str, Any]` - API response.
*   **Note**: Payload structure changed to wrap properties.

### `async client.async_configure_server_os_service(server_name: str, service_config: Dict[str, bool])`

*   **Description**: Configures OS-specific service settings (autostart, autoupdate).
*   **API Endpoint**: `POST /api/server/{server_name}/service/update`
*   **Arguments**:
    *   `server_name: str`
    *   `service_config: Dict[str, bool]` (e.g., `{"autoupdate": True, "autostart": False}`)
*   **Request Payload**: Direct `service_config` dictionary (model: `ServiceUpdatePayload`)
*   **Returns**: `Dict[str, Any]` - API response.

### `async client.async_delete_server(server_name: str)`

*   **Description**: Permanently deletes a server instance. **Use with caution.**
*   **API Endpoint**: `DELETE /api/server/{server_name}/delete`
*   **Returns**: `Dict[str, Any]` - API response (model: `ActionResponse`).

## Content Management Methods

Methods for managing server content like backups, worlds, and addons.

### `async client.async_list_server_backups(server_name: str, backup_type: str)`

*   **Description**: Lists backup filenames for a server and type.
*   **API Endpoint**: `GET /api/server/{server_name}/backup/list/{backup_type}`
*   **Arguments**:
    *   `server_name: str`
    *   `backup_type: str` (e.g., "world", "properties", "all")
*   **Returns**: `Dict[str, Any]` - API response (model: `BackupRestoreResponse`). Backup list in `response.get("backups")` or `response.get("details", {}).get("all_backups")`.

### `async client.async_get_content_worlds()`

*   **Description**: Lists available world template files (`.mcworld`).
*   **API Endpoint**: `GET /api/content/worlds`
*   **Returns**: `Dict[str, Any]` - API response (model: `ContentListResponse`). Files in `response.get("files")`.

### `async client.async_get_content_addons()`

*   **Description**: Lists available addon files (`.mcpack`, `.mcaddon`).
*   **API Endpoint**: `GET /api/content/addons`
*   **Returns**: `Dict[str, Any]` - API response (model: `ContentListResponse`). Files in `response.get("files")`.

### `async client.async_trigger_server_backup(server_name: str, backup_type: str = "all", file_to_backup: Optional[str] = None)`

*   **Description**: Triggers a backup operation.
*   **API Endpoint**: `POST /api/server/{server_name}/backup/action`
*   **Arguments**:
    *   `server_name: str`
    *   `backup_type: str` (default: "all"; "world", "config")
    *   `file_to_backup: Optional[str]` (required if `backup_type` is "config")
*   **Request Payload**: `{"backup_type": "...", "file_to_backup": "..."}` (model: `BackupActionPayload`)
*   **Returns**: `Dict[str, Any]` - API response (model: `BackupRestoreResponse`).

### `async client.async_export_server_world(server_name: str)`

*   **Description**: Exports the server's current world to a `.mcworld` file.
*   **API Endpoint**: `POST /api/server/{server_name}/world/export`
*   **Returns**: `Dict[str, Any]` - API response (model: `ActionResponse`).

### `async client.async_reset_server_world(server_name: str)`

*   **Description**: Resets the server's current world. **Use with caution.**
*   **API Endpoint**: `DELETE /api/server/{server_name}/world/reset`
*   **Returns**: `Dict[str, Any]` - API response (model: `ActionResponse`).

### `async client.async_prune_server_backups(server_name: str)`

*   **Description**: Prunes older backups for a server based on server-defined retention.
*   **API Endpoint**: `POST /api/server/{server_name}/backups/prune`
*   **Returns**: `Dict[str, Any]` - API response (model: `BackupRestoreResponse`).
*   **Note**: `keep` parameter removed; retention is server-managed for this endpoint.

### `async client.async_restore_server_backup(server_name: str, restore_type: str, backup_file: str)`

*   **Description**: Restores a server's world or config file from a backup.
*   **API Endpoint**: `POST /api/server/{server_name}/restore/action`
*   **Arguments**:
    *   `server_name: str`
    *   `restore_type: str` ("world", "properties", "allowlist", "permissions")
    *   `backup_file: str`
*   **Request Payload**: `{"restore_type": "...", "backup_file": "..."}` (model: `RestoreActionPayload`)
*   **Returns**: `Dict[str, Any]` - API response (model: `BackupRestoreResponse`).

### `async client.async_restore_server_latest_all(server_name: str)`

*   **Description**: Restores server world and config files from their latest backups.
*   **API Endpoint**: `POST /api/server/{server_name}/restore/action`
*   **Request Payload**: `{"restore_type": "all"}` (model: `RestoreActionPayload`)
*   **Returns**: `Dict[str, Any]` - API response (model: `BackupRestoreResponse`).
*   **Note**: Uses generic restore action endpoint; dedicated `/restore/all` removed.

### `async client.async_install_server_world(server_name: str, filename: str)`

*   **Description**: Installs a world from a `.mcworld` file.
*   **API Endpoint**: `POST /api/server/{server_name}/world/install`
*   **Arguments**:
    *   `server_name: str`
    *   `filename: str` (name of file in content/worlds)
*   **Request Payload**: `{"filename": "..."}` (model: `FileNamePayload`)
*   **Returns**: `Dict[str, Any]` - API response (model: `ActionResponse`).

### `async client.async_install_server_addon(server_name: str, filename: str)`

*   **Description**: Installs an addon from a `.mcaddon` or `.mcpack` file.
*   **API Endpoint**: `POST /api/server/{server_name}/addon/install`
*   **Arguments**:
    *   `server_name: str`
    *   `filename: str` (name of file in content/addons)
*   **Request Payload**: `{"filename": "..."}` (model: `FileNamePayload`)
*   **Returns**: `Dict[str, Any]` - API response (model: `ActionResponse`).

### `async client.async_restore_select_backup_type(server_name: str, restore_type: str)` (New)

*   **Description**: Selects a restore type, API returns redirect URL for file selection.
*   **API Endpoint**: `POST /api/server/{server_name}/restore/select_backup_type`
*   **Arguments**:
    *   `server_name: str`
    *   `restore_type: str` (e.g., "world", "properties")
*   **Request Payload**: `{"restore_type": "..."}` (model: `RestoreTypePayload`)
*   **Returns**: `Dict[str, Any]` - API response (model: `BackupRestoreResponse`), includes `redirect_url`.

## Scheduler Methods

Methods for managing scheduled tasks (OS-specific).

### `async client.async_add_server_cron_job(server_name: str, new_cron_job: str)` (Linux)

*   **Description**: Adds a new cron job.
*   **API Endpoint**: `POST /api/server/{server_name}/cron_scheduler/add`
*   **Request Payload**: `{"new_cron_job": "..."}` (model: `CronJobPayload`)
*   **Returns**: `Dict[str, Any]` - API response (model: `TaskApiResponse`).

### `async client.async_modify_server_cron_job(server_name: str, old_cron_job: str, new_cron_job: str)` (Linux)

*   **Description**: Modifies an existing cron job.
*   **API Endpoint**: `POST /api/server/{server_name}/cron_scheduler/modify`
*   **Request Payload**: `{"old_cron_job": "...", "new_cron_job": "..."}` (model: `CronJobPayload`)
*   **Returns**: `Dict[str, Any]` - API response (model: `TaskApiResponse`).

### `async client.async_delete_server_cron_job(server_name: str, cron_string: str)` (Linux)

*   **Description**: Deletes a cron job.
*   **API Endpoint**: `DELETE /api/server/{server_name}/cron_scheduler/delete`
*   **Arguments**:
    *   `server_name: str`
    *   `cron_string: str` (as query parameter)
*   **Returns**: `Dict[str, Any]` - API response (model: `TaskApiResponse`).

### `async client.async_add_server_windows_task(server_name: str, command: str, triggers: List[Dict[str, Any]])` (Windows)

*   **Description**: Adds a new Windows Scheduled Task.
*   **API Endpoint**: `POST /api/server/{server_name}/task_scheduler/add`
*   **Request Payload**: `{"command": "...", "triggers": [...]}` (model: `WindowsTaskPayload`)
*   **Returns**: `Dict[str, Any]` - API response (model: `TaskApiResponse`).

### `async client.async_modify_server_windows_task(server_name: str, task_name: str, command: str, triggers: List[Dict[str, Any]])` (Windows)

*   **Description**: Modifies an existing Windows Scheduled Task.
*   **API Endpoint**: `PUT /api/server/{server_name}/task_scheduler/task/{task_name}`
*   **Request Payload**: `{"command": "...", "triggers": [...]}` (model: `WindowsTaskPayload`)
*   **Returns**: `Dict[str, Any]` - API response (model: `TaskApiResponse`).

### `async client.async_delete_server_windows_task(server_name: str, task_name: str)` (Windows)

*   **Description**: Deletes a Windows Scheduled Task.
*   **API Endpoint**: `DELETE /api/server/{server_name}/task_scheduler/task/{task_name}`
*   **Returns**: `Dict[str, Any]` - API response (model: `TaskApiResponse`).

<!--
    TODO: The method `async_get_server_windows_task_details` was commented out
    in the client as its direct API endpoint equivalent
    (POST /api/server/{server_name}/task_scheduler/details)
    is not present in the new FastAPI specification.
-->

## Plugin Methods

Methods for managing plugins.

### `async client.async_get_plugin_statuses()`

*   **Description**: Retrieves status of all discovered plugins.
*   **API Endpoint**: `GET /api/plugins`
*   **Returns**: `Dict[str, Any]` - API response (model: `PluginApiResponse`). Plugin data in `response.get("data")`.

### `async client.async_set_plugin_status(plugin_name: str, enabled: bool)`

*   **Description**: Enables or disables a specific plugin.
*   **API Endpoint**: `POST /api/plugins/{plugin_name}`
*   **Request Payload**: `{"enabled": ...}` (model: `PluginStatusSetPayload`)
*   **Returns**: `Dict[str, Any]` - API response (model: `PluginApiResponse`).

### `async client.async_reload_plugins()`

*   **Description**: Triggers a full reload of all plugins.
*   **API Endpoint**: `PUT /api/plugins/reload`
*   **Returns**: `Dict[str, Any]` - API response (model: `PluginApiResponse`).
*   **Note**: HTTP method changed from POST to PUT.

### `async client.async_trigger_plugin_event(event_name: str, payload: Optional[Dict[str, Any]] = None)`

*   **Description**: Triggers a custom plugin event.
*   **API Endpoint**: `POST /api/plugins/trigger_event`
*   **Request Payload**: `{"event_name": "...", "payload": ...}` (model: `TriggerEventPayload`)
*   **Returns**: `Dict[str, Any]` - API response (model: `PluginApiResponse`).

## Error Handling

The client raises custom exceptions found in `bsm_api_client.exceptions`:
*   `APIError`: Base class for API related errors.
*   `CannotConnectError`: For connection issues.
*   `AuthError`: For authentication failures (401, 403).
*   `NotFoundError`: For 404 errors.
*   `ServerNotFoundError`: Specific 404 for server resources.
*   `ServerNotRunningError`: If an operation requires a running server.
*   `InvalidInputError`: For 400 Bad Request or 422 Unprocessable Entity (validation errors).
*   `OperationFailedError`: For general operation failures (e.g., 501).
*   `APIServerSideError`: For 500-level server errors.

Error responses from the API (often JSON with "message" or "detail" keys) are parsed and included in the exception.
For 422 Validation Errors, the message will typically be prefixed with "Validation Error: ".
