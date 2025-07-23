# src/bsm_api_client/models.py
"""Pydantic models for the Bedrock Server Manager API.

This module defines the Pydantic models used for data validation and serialization
in the Bedrock Server Manager API client. These models correspond to the request
and response bodies of the various API endpoints.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class Token(BaseModel):
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
    """

    status: str = "success"
    message: str
    details: Optional[Any] = None


class InstallServerPayload(BaseModel):
    """Request model for installing a new server.

    Attributes:
        server_name: The name for the new server.
        server_version: The version of the server to install (e.g., "1.20.10").
                        Defaults to "LATEST".
        server_zip_path: Optional path to a custom server ZIP file.
        overwrite: Whether to overwrite an existing server with the same name.
    """

    server_name: str = Field(..., min_length=1, max_length=50)
    server_version: str = "LATEST"
    server_zip_path: Optional[str] = None
    overwrite: bool = False


class InstallServerResponse(BaseModel):
    """Response model for server installation requests.

    Attributes:
        status: The status of the installation request.
        message: A message describing the result.
        task_id: The ID of the background task if installation started.
        server_name: The name of the server being installed.
    """

    status: str
    message: str
    task_id: Optional[str] = None
    server_name: Optional[str] = None


class PropertiesPayload(BaseModel):
    """Request model for updating server.properties.

    Attributes:
        properties: A dictionary of server properties to update.
    """

    properties: Dict[str, Any]


class AllowlistAddPayload(BaseModel):
    """Request model for adding players to the allowlist.

    Attributes:
        players: A list of player names or XUIDs to add.
        ignoresPlayerLimit: Whether adding these players ignores the player limit.
    """

    players: List[str]
    ignoresPlayerLimit: bool = False


class AllowlistRemovePayload(BaseModel):
    """Request model for removing players from the allowlist.

    Attributes:
        players: A list of player names or XUIDs to remove.
    """

    players: List[str]


class PlayerPermission(BaseModel):
    """Represents a single player's permission data.

    Attributes:
        name: The player's name.
        xuid: The player's Xbox User ID.
        permission_level: The permission level to assign (e.g., "operator").
    """

    name: str
    xuid: str
    permission_level: str


class PermissionsSetPayload(BaseModel):
    """Request model for setting multiple player permissions.

    Attributes:
        permissions: A list of PlayerPermission objects.
    """

    permissions: List[PlayerPermission]


class ServiceUpdatePayload(BaseModel):
    """Request model for updating server-specific service settings.

    Attributes:
        autoupdate: Enable or disable automatic updates for the server.
        autostart: Enable or disable automatic startup for the server.
    """

    autoupdate: Optional[bool] = None
    autostart: Optional[bool] = None


class BackupRestoreResponse(BaseModel):
    """Generic API response model for backup and restore operations.

    Attributes:
        status: The status of the operation.
        message: A descriptive message.
        details: Optional additional details.
        redirect_url: An optional URL for redirection after the operation.
        backups: A list of available backups.
    """

    status: str
    message: Optional[str] = None
    details: Optional[Any] = None
    redirect_url: Optional[str] = None
    backups: Optional[List[Any]] = None


class ContentListResponse(BaseModel):
    """Response for listing content like worlds and addons.

    Attributes:
        status: The status of the request.
        message: A descriptive message.
        files: A list of file names.
    """

    status: str
    message: Optional[str] = None
    files: Optional[List[str]] = None


class SettingItem(BaseModel):
    """Request model for a single setting key-value pair.

    Attributes:
        key: The key of the setting.
        value: The value of the setting.
    """



    key: str
    value: Any


class SettingsResponse(BaseModel):
    """Response model for settings operations.

    Attributes:
        status: The status of the request.
        message: A descriptive message.
        settings: A dictionary of all settings.
        setting: The specific setting that was modified.
    """

    status: str
    message: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None
    setting: Optional[SettingItem] = None


class GeneralApiResponse(BaseModel):
    """A general-purpose API response model for various endpoints.

    Attributes:
        status: The response status.
        message: An optional descriptive message.
        data: A generic dictionary for any other data.
        servers: A list of servers.
        info: System or application information.
        players: A list of players.
        files_deleted: The number of files deleted.
        files_kept: The number of files kept.
        properties: A dictionary of server properties.
    """

    status: str
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    servers: Optional[List[Dict[str, Any]]] = None
    info: Optional[Dict[str, Any]] = None
    players: Optional[List[Dict[str, Any]]] = None
    files_deleted: Optional[int] = None
    files_kept: Optional[int] = None
    properties: Optional[Dict[str, Any]] = None


class PluginApiResponse(BaseModel):
    """Generic API response model for plugin operations.

    Attributes:
        status: The response status.
        message: An optional descriptive message.
        data: A generic field for any other data related to the plugin.
    """

    status: str
    message: Optional[str] = None
    data: Optional[Any] = None


class CommandPayload(BaseModel):
    """Request model for sending a command to a server.

    Attributes:
        command: The command string to execute on the server.
    """

    command: str = Field(..., min_length=1)


class PruneDownloadsPayload(BaseModel):
    """Request model for pruning the download cache.

    Attributes:
        directory: The directory to prune.
        keep: The number of files to keep.
    """

    directory: str = Field(..., min_length=1)
    keep: Optional[int] = Field(None, ge=0)


class AddPlayersPayload(BaseModel):
    """Request model for manually adding players to the database.

    Attributes:
        players: A list of player strings, typically "name:xuid".
    """

    players: List[str]


class TriggerEventPayload(BaseModel):
    """Request model for triggering a custom plugin event.

    Attributes:
        event_name: The name of the event to trigger.
        payload: An optional dictionary of data to pass with the event.
    """

    event_name: str = Field(..., min_length=1)
    payload: Optional[Dict[str, Any]] = None


class PluginStatusSetPayload(BaseModel):
    """Request model for setting a plugin's enabled status.

    Attributes:
        enabled: The desired enabled state of the plugin.
    """

    enabled: bool


class RestoreTypePayload(BaseModel):
    """Request model for specifying the type of restore operation.

    Attributes:
        restore_type: The type of restore to perform (e.g., "world", "server").
    """

    restore_type: str


class RestoreActionPayload(BaseModel):
    """Request model for triggering a restore action.

    Attributes:
        restore_type: The type of restore to perform.
        backup_file: The specific backup file to use for the restore.
    """

    restore_type: str
    backup_file: Optional[str] = None


class BackupActionPayload(BaseModel):
    """Request model for triggering a backup action.

    Attributes:
        backup_type: The type of backup to perform (e.g., "world", "server").
        file_to_backup: The specific file or world to backup.
    """

    backup_type: str
    file_to_backup: Optional[str] = None


class FileNamePayload(BaseModel):
    """A simple model for payloads that only contain a filename.

    Attributes:
        filename: The name of the file.
    """

    filename: str
