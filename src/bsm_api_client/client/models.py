# src/bsm_api_client/models.py
"""Pydantic models for the Bedrock Server Manager API."""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class Token(BaseModel):
    """Response model for successful authentication, providing an access token."""

    access_token: str
    token_type: str
    message: Optional[str] = None


class ActionResponse(BaseModel):
    """Generic response for actions."""

    status: str = "success"
    message: str
    details: Optional[Any] = None


class InstallServerPayload(BaseModel):
    """Request model for installing a new server."""

    server_name: str = Field(..., min_length=1, max_length=50)
    server_version: str = "LATEST"
    server_zip_path: Optional[str] = None
    overwrite: bool = False


class InstallServerResponse(BaseModel):
    """Response model for server installation requests."""

    status: str
    message: str
    task_id: Optional[str] = None
    server_name: Optional[str] = None


class PropertiesPayload(BaseModel):
    """Request model for updating server.properties."""

    properties: Dict[str, Any]


class Player(BaseModel):
    name: str
    ignoresPlayerLimit: bool = False

class AllowlistAddPayload(BaseModel):
    """Request model for adding players to the allowlist."""

    players: List[Player]


class AllowlistRemovePayload(BaseModel):
    """Request model for removing players from the allowlist."""

    players: List[Player]


class PlayerPermission(BaseModel):
    """Represents a single player's permission data sent from the client."""

    xuid: str
    permission: str


class PermissionsSetPayload(BaseModel):
    """Request model for setting multiple player permissions."""

    permissions: List[PlayerPermission]


class ServiceUpdatePayload(BaseModel):
    """Request model for updating server-specific service settings."""

    autoupdate: Optional[bool] = None
    autostart: Optional[bool] = None


class BackupRestoreResponse(BaseModel):
    """Generic API response model for backup and restore operations."""

    status: str
    message: Optional[str] = None
    details: Optional[Any] = None
    redirect_url: Optional[str] = None
    backups: Optional[List[Any]] = None


class ContentListResponse(BaseModel):
    """Response for listing content like worlds and addons."""

    status: str
    message: Optional[str] = None
    files: Optional[List[str]] = None


class SettingItem(BaseModel):
    """Request model for a single setting key-value pair."""

    key: str
    value: Any


class SettingsResponse(BaseModel):
    """Response model for settings operations."""

    status: str
    message: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None
    setting: Optional[SettingItem] = None


class GeneralApiResponse(BaseModel):
    """A general-purpose API response model."""

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
    """Generic API response model for plugin operations."""

    status: str
    message: Optional[str] = None
    data: Optional[Any] = None


class CommandPayload(BaseModel):
    """Request model for sending a command to a server."""

    command: str = Field(..., min_length=1)


class PruneDownloadsPayload(BaseModel):
    """Request model for pruning the download cache."""

    directory: str = Field(..., min_length=1)
    keep: Optional[int] = Field(None, ge=0)


class AddPlayersPayload(BaseModel):
    """Request model for manually adding players to the database."""

    players: List[str]


class TriggerEventPayload(BaseModel):
    """Request model for triggering a custom plugin event."""

    event_name: str = Field(..., min_length=1)
    payload: Optional[Dict[str, Any]] = None


class PluginStatusSetPayload(BaseModel):
    """Request model for setting a plugin's enabled status."""

    enabled: bool


class RestoreTypePayload(BaseModel):
    """Request model for specifying the type of restore operation."""

    restore_type: str


class RestoreActionPayload(BaseModel):
    """Request model for triggering a restore action."""

    restore_type: str
    backup_file: Optional[str] = None


class BackupActionPayload(BaseModel):
    """Request model for triggering a backup action."""

    backup_type: str
    file_to_backup: Optional[str] = None


class FileNamePayload(BaseModel):
    """A simple model for payloads that only contain a filename."""

    filename: str
