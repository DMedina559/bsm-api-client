# src/bsm_api_client/models.py
"""Pydantic models for the Bedrock Server Manager API.

This module defines the Pydantic models used for data validation and serialization
in the Bedrock Server Manager API client. These models correspond to the request
and response bodies of the various API endpoints.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    """Response model for successful authentication.

    Attributes:
        access_token: The JWT access token for authenticating subsequent requests.
        token_type: The type of token, typically "bearer".
        message: An optional message, e.g., "Login successful".
    """

    access_token: str
    token_type: str
    message: Optional[str] = None


class ActionResponse(BaseModel):
    """Generic response model for actions.

    Attributes:
        status: The status of the action, e.g., "success".
        message: A descriptive message about the outcome of the action.
        details: Optional additional details about the action's result.
        task_id: The ID of the background task if one was created.
        redirect_url: An optional URL for redirection after the operation.
        backups: A list of available backups.
    """

    status: str = "success"
    message: str
    details: Optional[Any] = None
    task_id: Optional[str] = None
    redirect_url: Optional[str] = None
    backups: Optional[Any] = None


class BaseApiResponse(BaseModel):
    """Base model for simple API responses.

    Attributes:
        status: The status of the response, e.g., "success".
        message: An optional descriptive message.
    """

    status: str
    message: Optional[str] = None


class UserResponse(BaseModel):
    """Pydantic model representing a user.

    Attributes:
        id: The user's ID.
        username: The user's username.
        identity_type: The type of identity (e.g., "local").
        role: The user's role.
        is_active: Whether the user is active.
        theme: The user's preferred theme. Defaults to "default".
    """

    id: int
    username: str
    identity_type: Optional[str] = None
    role: str
    is_active: bool
    theme: str = "default"


class ThemeUpdatePayload(BaseModel):
    """Request payload for updating the user's theme.

    Attributes:
        theme: The new theme name.
    """

    theme: str


class ProfileUpdatePayload(BaseModel):
    """Request payload for updating user profile details.

    Attributes:
        full_name: The user's full name.
        email: The user's email address.
    """

    full_name: str
    email: str


class ChangePasswordPayload(BaseModel):
    """Request payload for changing the user's password.

    Attributes:
        current_password: The current password for verification.
        new_password: The new password.
    """

    current_password: str
    new_password: str


class InstallServerPayload(BaseModel):
    """Request model for installing a new server.

    Attributes:
        server_name: Name for the new server.
        server_version: Version to install (e.g., 'LATEST', '1.20.10.01', 'CUSTOM'). Defaults to "LATEST".
        server_zip_path: Path to a custom ZIP file, if 'CUSTOM' version is selected.
        overwrite: If True, confirm overwriting an existing installation.
    """

    server_name: str = Field(..., min_length=1, max_length=50)
    server_version: str = "LATEST"
    server_zip_path: Optional[str] = None
    overwrite: Optional[bool] = False


class InstallServerResponse(BaseModel):
    """Response model for server installation requests.

    Attributes:
        status: Status of the installation ('success', 'confirm_needed', 'pending').
        message: Descriptive message about the operation.
        server_name: Name of the server, especially if confirmation is needed.
        task_id: Task ID for background installation.
    """

    status: str
    message: str
    server_name: Optional[str] = None
    task_id: Optional[str] = None


class PropertiesPayload(BaseModel):
    """Request model for updating server.properties.

    Attributes:
        properties: Dictionary of properties to set.
    """

    properties: Dict[str, Any]


class PropertiesGetResponse(BaseModel):
    """Response model for server properties.

    Attributes:
        status: The status of the response.
        message: An optional descriptive message.
        properties: Dictionary of properties to set.
    """

    status: str
    message: Optional[str] = None
    properties: Dict[str, Any]


class AllowlistAddPayload(BaseModel):
    """Request model for adding players to the allowlist.

    Attributes:
        players: List of player gamertags to add.
        ignoresPlayerLimit: Set 'ignoresPlayerLimit' for these players.
    """

    players: List[str]
    ignoresPlayerLimit: bool = False


class AllowlistGetResponse(BaseModel):
    """Response model for server allowlist.

    Attributes:
        status: The status of the response.
        message: An optional descriptive message.
        players: The list of players on the allowlist.
    """

    status: str
    message: Optional[str] = None
    players: List[Dict[str, Any]]


class AllowlistRemovePayload(BaseModel):
    """Request model for removing players from the allowlist.

    Attributes:
        players: List of player gamertags to remove.
    """

    players: List[str]


class PlayerPermissionPayload(BaseModel):
    """Represents a single player's permission data sent from the client.

    Attributes:
        xuid: The player's XUID.
        name: The player's Name.
        permission_level: The permission level.
    """

    xuid: str
    name: str
    permission_level: str


class PermissionsSetPayload(BaseModel):
    """Request model for setting multiple player permissions.

    Attributes:
        permissions: List of player permission entries.
    """

    permissions: List[PlayerPermissionPayload]


class PermissionsGetResponse(BaseModel):
    """Response model for server permissions.

    Attributes:
        status: The status of the response.
        message: An optional descriptive message.
        permissions: The list of permissions on the server.
    """

    status: str
    message: Optional[str] = None
    permissions: List[Dict[str, Any]]


class PermissionsUpdateResponse(BaseModel):
    """Response model for permissions update.

    Attributes:
        status: The status of the response.
        message: An optional descriptive message.
        errors: A dictionary of errors, if any occurred.
    """

    status: str
    message: Optional[str] = None
    errors: Optional[Dict[str, str]] = None


class ServiceUpdatePayload(BaseModel):
    """Request model for updating server-specific service settings.

    Attributes:
        autoupdate: Enable/disable automatic updates for the server.
        autostart: Enable/disable service autostart for the server.
    """

    autoupdate: Optional[bool] = None
    autostart: Optional[bool] = None


class ContentListResponse(BaseModel):
    """Response model for content listing endpoints.

    Attributes:
        status: The status of the request.
        message: An optional descriptive message.
        files: A list of filenames found.
    """

    status: str
    message: Optional[str] = None
    files: Optional[List[str]] = None


class SettingItemResponse(BaseModel):
    """Request model for a single setting key-value pair.

    Attributes:
        key: The dot-notation key of the setting (e.g., 'web.port').
        value: The new value for the setting.
    """

    key: str
    value: Any


class SettingsResponse(BaseModel):
    """Response model for settings operations.

    Attributes:
        status: The status of the request.
        message: An optional descriptive message.
        settings: A dictionary of all settings.
        setting: The specific setting that was modified.
    """

    status: str
    message: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None
    setting: Optional[SettingItemResponse] = None


class CommandPayload(BaseModel):
    """Request model for sending a command to a server.

    Attributes:
        command: The command to send to the server.
    """

    command: str = Field(..., min_length=1)


class PruneDownloadsPayload(BaseModel):
    """Request model for pruning the download cache.

    Attributes:
        directory: The subdirectory within the main download cache to prune (e.g., 'stable' or 'preview').
        keep: Number of most recent files to keep. Defaults to config if omitted.
    """

    directory: str = Field(..., min_length=1)
    keep: Optional[int] = Field(None, ge=0)


class PruneDownloadsResponse(BaseModel):
    """Response model for pruning downloads.

    Attributes:
        status: The status of the response.
        message: An optional descriptive message.
        files_deleted: The number of files deleted.
        files_kept: The number of files kept.
    """

    status: str
    message: Optional[str] = None
    files_deleted: Optional[int] = None
    files_kept: Optional[int] = None


class AddPlayersPayload(BaseModel):
    """Request model for manually adding players to the database.

    Attributes:
        players: List of player strings, e.g., ["PlayerOne:123xuid", "PlayerTwo:456xuid"]
    """

    players: List[str]


class AddPlayersResponse(BaseModel):
    """Response model for adding players, typically returns just inherited fields or single item data.

    Attributes:
        status: The status of the response.
        message: An optional descriptive message.
        details: Optional data payload.
        count: Optional count of added players.
    """

    status: str
    message: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    count: Optional[int] = None


class TriggerEventPayload(BaseModel):
    """Request model for triggering a custom plugin event.

    Attributes:
        event_name: The namespaced name of the event to trigger (e.g., 'myplugin:myevent').
        payload: Optional dictionary payload for the event.
    """

    event_name: str = Field(..., min_length=1)
    payload: Optional[Dict[str, Any]] = None


class TriggerEventResponse(BaseModel):
    """Response model for triggering a custom plugin event."""

    status: str
    message: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class PluginStatusesResponse(BaseModel):
    """Response model for plugin statuses."""

    status: str
    message: Optional[str] = None
    plugins: Optional[Dict[str, Dict[str, Any]]] = None


class PluginStatusSetPayload(BaseModel):
    """Request model for setting a plugin's enabled status.

    Attributes:
        enabled: Set to true to enable the plugin, false to disable.
    """

    enabled: bool


class RestoreTypePayload(BaseModel):
    """Request model for specifying the type of restore operation.

    Attributes:
        restore_type: The type of restore to perform (e.g., 'world', 'properties').
    """

    restore_type: str


class RestoreActionPayload(BaseModel):
    """Request model for triggering a restore action.

    Attributes:
        restore_type: Type of restore: 'world', 'properties', 'allowlist', 'permissions', or 'all'.
        backup_file: Name of the backup file (basename) to restore from (required if not 'all').
    """

    restore_type: str
    backup_file: Optional[str] = None


class BackupActionPayload(BaseModel):
    """Request model for triggering a backup action.

    Attributes:
        backup_type: Type of backup: 'world', 'config', or 'all'.
        file_to_backup: Name of config file if backup_type is 'config' (e.g., 'server.properties').
    """

    backup_type: str
    file_to_backup: Optional[str] = None


class FileNamePayload(BaseModel):
    """Payload for file-based operations.

    Attributes:
        filename: The name of the file to operate on.
    """

    filename: str


class SetupStatusResponse(BaseModel):
    """Response model for setup status.

    Attributes:
        needs_setup: Whether the setup is needed.
    """

    needs_setup: bool


class AuditLogResponse(BaseModel):
    """Response model for audit logs."""

    id: int
    user_id: int
    action: str
    details: Optional[Dict[str, Any]] = None
    timestamp: str


class CustomZipsResponse(BaseModel):
    """Response model for custom zips list."""

    status: str
    message: Optional[str] = None
    custom_zips: List[str]


class AppInfoResponse(BaseModel):
    """Response model for app/system info."""

    status: str
    message: Optional[str] = None
    info: Optional[Dict[str, Any]] = None


class ThemeListResponse(BaseModel):
    """Response model for theme lists."""

    status: str
    message: Optional[str] = None
    themes: Optional[List[str]] = None


class PlayerListResponse(BaseModel):
    """Response model for player lists."""

    status: str
    message: Optional[str] = None
    players: Optional[List[Dict[str, Any]]] = None


class ServerSchemaResponse(BaseModel):
    """Schema representing server information in lists."""

    name: str
    status: str
    version: str
    player_count: int


class ServersListResponse(BaseModel):
    """Response model for lists of server data."""

    status: str
    message: Optional[str] = None
    servers: Optional[List[ServerSchemaResponse]] = None


class ServerRunningStatusResponse(BaseModel):
    """Response model for server running status."""

    status: str
    message: Optional[str] = None
    running: Optional[bool] = None


class ServerConfigStatusResponse(BaseModel):
    """Response model for server config status."""

    status: str
    message: Optional[str] = None
    config_status: Optional[str] = None


class ServerVersionResponse(BaseModel):
    """Response model for server installed version."""

    status: str
    message: Optional[str] = None
    version: Optional[str] = None


class ServerProcessInfoResponse(BaseModel):
    """Response model for server process info."""

    status: str
    message: Optional[str] = None
    process_info: Optional[Dict[str, Any]] = None


class ServerSettingItemPayload(BaseModel):
    """Request model for a single server setting key-value pair."""

    key: str
    value: Any


class ServerSettingsResponse(BaseModel):
    """Response model for server settings operations."""

    status: str
    message: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None
    setting: Optional[ServerSettingItemPayload] = None


class UpdateUserRolePayload(BaseModel):
    """Request payload for updating a user's role."""

    role: str


class AddonSchemaResponse(BaseModel):
    """Schema representing an individual addon."""

    name: str
    uuid: str
    version: List[int]
    status: str
    active_subpack: Optional[str] = None
    path: Optional[str] = None
    icon: Optional[str] = None
    subpacks: Optional[List[Dict[str, Any]]] = None


class AddonTypeGroupSchemaResponse(BaseModel):
    """Schema grouping behavior and resource packs."""

    behavior_packs: Optional[List[AddonSchemaResponse]] = None
    resource_packs: Optional[List[AddonSchemaResponse]] = None


class AddonListResponse(BaseModel):
    """Response model for retrieving all addons on a server."""

    status: str
    message: Optional[str] = None
    addons: Optional[AddonTypeGroupSchemaResponse] = None


class AddonActionPayload(BaseModel):
    """Request model for modifying a specific addon (e.g. enable, disable, uninstall)."""

    pack_uuid: str
    pack_type: str


class AddonSubpackPayload(BaseModel):
    """Request model for changing the active subpack of an addon."""

    pack_uuid: str
    pack_type: str
    subpack_name: Optional[str] = None
    model_config = {"extra": "allow"}


class AddonReorderPayload(BaseModel):
    """Request model for reordering active addons."""

    pack_type: str
    uuids: List[str]
