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

## Pydantic Models

The client now uses Pydantic models for request payloads and response objects. This provides better data validation and an improved developer experience. The models are defined in `bsm_api_client.models`.

## Authentication Methods

Methods related to client authentication. These are part of `ClientBase` but exposed via the main client.

### `async client.authenticate() -> Token`

*   **Description**: Authenticates with the API using the provided username and password. Stores the JWT token internally for subsequent requests. Typically, this method is called automatically by the client when an authenticated endpoint is accessed and no valid token is present.
*   **API Endpoint**: `POST /auth/token`
*   **Request Body**: `application/x-www-form-urlencoded` with `username` and `password`.
*   **Returns**: `Token` - A Pydantic model containing the access token.
*   **Raises**: `AuthError` on failure.
*   **Note**: This method was updated to use form data and target the `/auth/token` endpoint.

### `async client.async_logout() -> Dict[str, Any]`

*   **Description**: Logs the current user out by calling the API's logout endpoint. Clears the internally stored JWT token.
*   **API Endpoint**: `GET /auth/logout`
*   **Returns**: `Dict[str, Any]` - API response, typically a success message.
*   **Raises**: `APIError` or subclasses on failure.

## Manager Methods

Global management and information methods.

### `async client.async_get_info() -> GeneralApiResponse`

*   **Description**: Gets system and application information from the manager.
*   **API Endpoint**: `GET /api/info`
*   **Returns**: `GeneralApiResponse` - A Pydantic model containing system and application info.

### `async client.async_scan_players() -> GeneralApiResponse`

*   **Description**: Triggers scanning of player logs across all servers.
*   **API Endpoint**: `POST /api/players/scan`
*   **Returns**: `GeneralApiResponse` - A Pydantic model containing the API response.

### `async client.async_get_players() -> GeneralApiResponse`

*   **Description**: Gets the global list of known players (name and XUID).
*   **API Endpoint**: `GET /api/players/get`
*   **Returns**: `GeneralApiResponse` - A Pydantic model containing the list of players.

### `async client.async_add_players(payload: AddPlayersPayload) -> GeneralApiResponse`

*   **Description**: Adds or updates players in the global list.
*   **API Endpoint**: `POST /api/players/add`
*   **Arguments**:
    *   `payload: AddPlayersPayload` - Pydantic model containing a list of player strings.
*   **Returns**: `GeneralApiResponse` - A Pydantic model containing the API response.

### `async client.async_prune_downloads(payload: PruneDownloadsPayload) -> GeneralApiResponse`

*   **Description**: Triggers pruning of downloaded server archives in a specified directory.
*   **API Endpoint**: `POST /api/downloads/prune`
*   **Arguments**:
    *   `payload: PruneDownloadsPayload` - Pydantic model containing the directory and keep count.
*   **Returns**: `GeneralApiResponse` - A Pydantic model containing the API response.

### `async client.async_install_new_server(payload: InstallServerPayload) -> InstallServerResponse`

*   **Description**: Requests installation of a new Bedrock server instance.
*   **API Endpoint**: `POST /api/server/install`
*   **Arguments**:
    *   `payload: InstallServerPayload` - Pydantic model containing server name, version, and overwrite flag.
*   **Returns**: `InstallServerResponse` - A Pydantic model containing the API response. May indicate success or `confirm_needed`.

### `async client.async_get_all_settings() -> SettingsResponse`

*   **Description**: Retrieves all global application settings.
*   **API Endpoint**: `GET /api/settings`
*   **Returns**: `SettingsResponse` - A Pydantic model containing the settings.

### `async client.async_set_setting(payload: SettingItem) -> SettingsResponse`

*   **Description**: Sets a specific global application setting.
*   **API Endpoint**: `POST /api/settings`
*   **Arguments**:
    *   `payload: SettingItem` - Pydantic model containing the key and value of the setting.
*   **Returns**: `SettingsResponse` - A Pydantic model containing the API response.

### `async client.async_reload_settings() -> SettingsResponse`

*   **Description**: Forces a reload of global application settings and logging configuration.
*   **API Endpoint**: `POST /api/settings/reload`
*   **Returns**: `SettingsResponse` - A Pydantic model containing the API response.

### `async client.async_get_panorama_image() -> bytes`

*   **Description**: Fetches the custom `panorama.jpeg` background image.
*   **API Endpoint**: `GET /api/panorama`
*   **Returns**: `bytes` - Raw image data.
*   **Note**: This method makes a direct session call to handle binary data.

### `async client.async_get_custom_zips() -> GeneralApiResponse`

*   **Description**: Retrieves a list of available custom server ZIP files.
*   **API Endpoint**: `GET /api/downloads/list`
*   **Returns**: `GeneralApiResponse` - A Pydantic model containing the list of custom zips.

### `async client.async_get_themes() -> Dict[str, Any]`

*   **Description**: Retrieves a list of available themes.
*   **API Endpoint**: `GET /api/themes`
*   **Returns**: `Dict[str, Any]` - A dictionary of themes.

## Server Information Methods

Methods for retrieving information about specific server instances.

### `async client.async_get_servers_details() -> GeneralApiResponse`

*   **Description**: Fetches a list of all detected server instances with details (name, status, version).
*   **API Endpoint**: `GET /api/servers`
*   **Returns**: `GeneralApiResponse` - A Pydantic model containing the list of servers.

### `async client.async_get_server_names() -> List[str]`

*   **Description**: Convenience wrapper around `async_get_servers_details` to get a list of just server names.
*   **Returns**: `List[str]` - Sorted list of server names.

### `async client.async_get_server_validate(server_name: str) -> bool`

*   **Description**: Validates if the server directory and executable exist.
*   **API Endpoint**: `GET /api/server/{server_name}/validate`
*   **Returns**: `bool` - True if valid, otherwise raises `ServerNotFoundError` or `APIError`.

### `async client.async_get_server_process_info(server_name: str) -> GeneralApiResponse`

*   **Description**: Gets runtime status information (PID, CPU, Memory, Uptime) for a server.
*   **API Endpoint**: `GET /api/server/{server_name}/process_info`
*   **Returns**: `GeneralApiResponse` - A Pydantic model containing the process info.

### `async client.async_get_server_running_status(server_name: str) -> GeneralApiResponse`

*   **Description**: Checks if the Bedrock server process is currently running.
*   **API Endpoint**: `GET /api/server/{server_name}/status`
*   **Returns**: `GeneralApiResponse` - A Pydantic model containing the running status.
*   **Note**: Path changed from `.../running_status` to `.../status`. Response structure also changed.

### `async client.async_get_server_config_status(server_name: str) -> GeneralApiResponse`

*   **Description**: Gets the status string stored in the server's configuration file.
*   **API Endpoint**: `GET /api/server/{server_name}/config_status`
*   **Returns**: `GeneralApiResponse` - A Pydantic model containing the config status.

### `async client.async_get_server_version(server_name: str) -> GeneralApiResponse`

*   **Description**: Gets the installed Bedrock server version from the server's config file.
*   **API Endpoint**: `GET /api/server/{server_name}/version`
*   **Returns**: `GeneralApiResponse` - A Pydantic model containing the version.

### `async client.async_get_server_properties(server_name: str) -> GeneralApiResponse`

*   **Description**: Retrieves the parsed content of the server's `server.properties` file.
*   **API Endpoint**: `GET /api/server/{server_name}/properties/get`
*   **Returns**: `GeneralApiResponse` - A Pydantic model containing the properties.

### `async client.async_get_server_permissions_data(server_name: str) -> GeneralApiResponse`

*   **Description**: Retrieves player permissions from the server's `permissions.json` file.
*   **API Endpoint**: `GET /api/server/{server_name}/permissions/get`
*   **Returns**: `GeneralApiResponse` - A Pydantic model containing the permissions.

### `async client.async_get_server_allowlist(server_name: str) -> GeneralApiResponse`

*   **Description**: Retrieves the list of players from the server's `allowlist.json` file.
*   **API Endpoint**: `GET /api/server/{server_name}/allowlist/get`
*   **Returns**: `GeneralApiResponse` - A Pydantic model containing the allowlist.

### `async client.async_get_world_icon_image(server_name: str) -> bytes`

*   **Description**: Fetches the `world_icon.jpeg` for a server.
*   **API Endpoint**: `GET /api/server/{server_name}/world/icon`
*   **Arguments**:
    *   `server_name: str`
*   **Returns**: `bytes` - Raw image data.
*   **Note**: This method makes a direct session call to handle binary data and includes authentication retry logic.

## Server Action Methods

Methods for performing actions on server instances.

### `async client.async_start_server(server_name: str) -> ActionResponse`

*   **Description**: Starts the specified server.
*   **API Endpoint**: `POST /api/server/{server_name}/start`
*   **Returns**: `ActionResponse` - A Pydantic model containing the API response.

### `async client.async_stop_server(server_name: str) -> ActionResponse`

*   **Description**: Stops the specified server.
*   **API Endpoint**: `POST /api/server/{server_name}/stop`
*   **Returns**: `ActionResponse` - A Pydantic model containing the API response.

### `async client.async_restart_server(server_name: str) -> ActionResponse`

*   **Description**: Restarts the specified server.
*   **API Endpoint**: `POST /api/server/{server_name}/restart`
*   **Returns**: `ActionResponse` - A Pydantic model containing the API response.

### `async client.async_send_server_command(server_name: str, payload: CommandPayload) -> ActionResponse`

*   **Description**: Sends a command to the server's console.
*   **API Endpoint**: `POST /api/server/{server_name}/send_command`
*   **Arguments**:
    *   `server_name: str`
    *   `payload: CommandPayload` - Pydantic model containing the command.
*   **Returns**: `ActionResponse` - A Pydantic model containing the API response.

### `async client.async_update_server(server_name: str) -> ActionResponse`

*   **Description**: Checks for and applies updates to the server.
*   **API Endpoint**: `POST /api/server/{server_name}/update`
*   **Returns**: `ActionResponse` - A Pydantic model containing the API response.

### `async client.async_add_server_allowlist(server_name: str, payload: AllowlistAddPayload) -> ActionResponse`

*   **Description**: Adds players to the server's allowlist.
*   **API Endpoint**: `POST /api/server/{server_name}/allowlist/add`
*   **Arguments**:
    *   `server_name: str`
    *   `payload: AllowlistAddPayload` - Pydantic model containing the players to add.
*   **Returns**: `ActionResponse` - A Pydantic model containing the API response.

### `async client.async_remove_server_allowlist_players(server_name: str, payload: AllowlistRemovePayload) -> ActionResponse`

*   **Description**: Removes players from the server's allowlist.
*   **API Endpoint**: `DELETE /api/server/{server_name}/allowlist/remove`
*   **Arguments**:
    *   `server_name: str`
    *   `payload: AllowlistRemovePayload` - Pydantic model containing the players to remove.
*   **Returns**: `ActionResponse` - A Pydantic model containing the API response.

### `async client.async_set_server_permissions(server_name: str, payload: PermissionsSetPayload) -> ActionResponse`

*   **Description**: Updates permission levels for players.
*   **API Endpoint**: `PUT /api/server/{server_name}/permissions/set`
*   **Arguments**:
    *   `server_name: str`
    *   `payload: PermissionsSetPayload` - Pydantic model containing the permissions to set.
*   **Returns**: `ActionResponse` - A Pydantic model containing the API response.

### `async client.async_update_server_properties(server_name: str, payload: PropertiesPayload) -> ActionResponse`

*   **Description**: Updates `server.properties` file.
*   **API Endpoint**: `POST /api/server/{server_name}/properties/set`
*   **Arguments**:
    *   `server_name: str`
    *   `payload: PropertiesPayload` - Pydantic model containing the properties to update.
*   **Returns**: `ActionResponse` - A Pydantic model containing the API response.

### `async client.async_configure_server_os_service(server_name: str, payload: ServiceUpdatePayload) -> ActionResponse`

*   **Description**: Configures OS-specific service settings (autostart, autoupdate).
*   **API Endpoint**: `POST /api/server/{server_name}/service/update`
*   **Arguments**:
    *   `server_name: str`
    *   `payload: ServiceUpdatePayload` - Pydantic model containing the service configuration.
*   **Returns**: `ActionResponse` - A Pydantic model containing the API response.

### `async client.async_delete_server(server_name: str) -> ActionResponse`

*   **Description**: Permanently deletes a server instance. **Use with caution.**
*   **API Endpoint**: `DELETE /api/server/{server_name}/delete`
*   **Returns**: `ActionResponse` - A Pydantic model containing the API response.

## Content Management Methods

Methods for managing server content like backups, worlds, and addons.

### `async client.async_list_server_backups(server_name: str, backup_type: str) -> BackupRestoreResponse`

*   **Description**: Lists backup filenames for a server and type.
*   **API Endpoint**: `GET /api/server/{server_name}/backup/list/{backup_type}`
*   **Arguments**:
    *   `server_name: str`
    *   `backup_type: str` (e.g., "world", "properties", "all")
*   **Returns**: `BackupRestoreResponse` - A Pydantic model containing the API response.

### `async client.async_get_content_worlds() -> ContentListResponse`

*   **Description**: Lists available world template files (`.mcworld`).
*   **API Endpoint**: `GET /api/content/worlds`
*   **Returns**: `ContentListResponse` - A Pydantic model containing the list of worlds.

### `async client.async_get_content_addons() -> ContentListResponse`

*   **Description**: Lists available addon files (`.mcpack`, `.mcaddon`).
*   **API Endpoint**: `GET /api/content/addons`
*   **Returns**: `ContentListResponse` - A Pydantic model containing the list of addons.

### `async client.async_trigger_server_backup(server_name: str, payload: BackupActionPayload) -> BackupRestoreResponse`

*   **Description**: Triggers a backup operation.
*   **API Endpoint**: `POST /api/server/{server_name}/backup/action`
*   **Arguments**:
    *   `server_name: str`
    *   `payload: BackupActionPayload` - Pydantic model containing the backup type and file to backup.
*   **Returns**: `BackupRestoreResponse` - A Pydantic model containing the API response.

### `async client.async_export_server_world(server_name: str) -> ActionResponse`

*   **Description**: Exports the server's current world to a `.mcworld` file.
*   **API Endpoint**: `POST /api/server/{server_name}/world/export`
*   **Returns**: `ActionResponse` - A Pydantic model containing the API response.

### `async client.async_reset_server_world(server_name: str) -> ActionResponse`

*   **Description**: Resets the server's current world. **Use with caution.**
*   **API Endpoint**: `DELETE /api/server/{server_name}/world/reset`
*   **Returns**: `ActionResponse` - A Pydantic model containing the API response.

### `async client.async_prune_server_backups(server_name: str) -> BackupRestoreResponse`

*   **Description**: Prunes older backups for a server based on server-defined retention.
*   **API Endpoint**: `POST /api/server/{server_name}/backups/prune`
*   **Returns**: `BackupRestoreResponse` - A Pydantic model containing the API response.
*   **Note**: `keep` parameter removed; retention is server-managed for this endpoint.

### `async client.async_restore_server_backup(server_name: str, payload: RestoreActionPayload) -> BackupRestoreResponse`

*   **Description**: Restores a server's world or config file from a backup.
*   **API Endpoint**: `POST /api/server/{server_name}/restore/action`
*   **Arguments**:
    *   `server_name: str`
    *   `payload: RestoreActionPayload` - Pydantic model containing the restore type and backup file.
*   **Returns**: `BackupRestoreResponse` - A Pydantic model containing the API response.

### `async client.async_restore_server_latest_all(server_name: str) -> BackupRestoreResponse`

*   **Description**: Restores server world and config files from their latest backups.
*   **API Endpoint**: `POST /api/server/{server_name}/restore/action`
*   **Request Payload**: `{"restore_type": "all"}` (model: `RestoreActionPayload`)
*   **Returns**: `BackupRestoreResponse` - A Pydantic model containing the API response.
*   **Note**: Uses generic restore action endpoint; dedicated `/restore/all` removed.

### `async client.async_install_server_world(server_name: str, payload: FileNamePayload) -> ActionResponse`

*   **Description**: Installs a world from a `.mcworld` file.
*   **API Endpoint**: `POST /api/server/{server_name}/world/install`
*   **Arguments**:
    *   `server_name: str`
    *   `payload: FileNamePayload` - Pydantic model containing the filename.
*   **Returns**: `ActionResponse` - A Pydantic model containing the API response.

### `async client.async_install_server_addon(server_name: str, payload: FileNamePayload) -> ActionResponse`

*   **Description**: Installs an addon from a `.mcaddon` or `.mcpack` file.
*   **API Endpoint**: `POST /api/server/{server_name}/addon/install`
*   **Arguments**:
    *   `server_name: str`
    *   `payload: FileNamePayload` - Pydantic model containing the filename.
*   **Returns**: `ActionResponse` - A Pydantic model containing the API response.

### `async client.async_restore_select_backup_type(server_name: str, payload: RestoreTypePayload) -> BackupRestoreResponse`

*   **Description**: Selects a restore type, API returns redirect URL for file selection.
*   **API Endpoint**: `POST /api/server/{server_name}/restore/select_backup_type`
*   **Arguments**:
    *   `server_name: str`
    *   `payload: RestoreTypePayload` - Pydantic model containing the restore type.
*   **Returns**: `BackupRestoreResponse` - A Pydantic model containing the API response.

## Plugin Methods

Methods for managing plugins.

### `async client.async_get_plugin_statuses() -> PluginApiResponse`

*   **Description**: Retrieves status of all discovered plugins.
*   **API Endpoint**: `GET /api/plugins`
*   **Returns**: `PluginApiResponse` - A Pydantic model containing the plugin statuses.

### `async client.async_set_plugin_status(plugin_name: str, payload: PluginStatusSetPayload) -> PluginApiResponse`

*   **Description**: Enables or disables a specific plugin.
*   **API Endpoint**: `POST /api/plugins/{plugin_name}`
*   **Arguments**:
    * `plugin_name: str`
    * `payload: PluginStatusSetPayload` - Pydantic model containing the enabled status.
*   **Returns**: `PluginApiResponse` - A Pydantic model containing the API response.

### `async client.async_reload_plugins() -> PluginApiResponse`

*   **Description**: Triggers a full reload of all plugins.
*   **API Endpoint**: `PUT /api/plugins/reload`
*   **Returns**: `PluginApiResponse` - A Pydantic model containing the API response.
*   **Note**: HTTP method changed from POST to PUT.

### `async client.async_trigger_plugin_event(payload: TriggerEventPayload) -> PluginApiResponse`

*   **Description**: Triggers a custom plugin event.
*   **API Endpoint**: `POST /api/plugins/trigger_event`
*   **Arguments**:
    * `payload: TriggerEventPayload` - Pydantic model containing the event name and payload.
*   **Returns**: `PluginApiResponse` - A Pydantic model containing the API response.

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
