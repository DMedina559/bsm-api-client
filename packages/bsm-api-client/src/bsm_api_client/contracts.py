# Generated from bundled OpenAPI by tools/generate_models.py.
from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import AwareDatetime, ConfigDict, Field, JsonValue, SecretStr

from bsm_api_client.contract_base import ContractModel


class ActionResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    message: str = Field(..., title="Message")
    status: Literal["success", "skipped"] | None = Field("success", title="Status")


class AddPlayersPayload(ContractModel):
    model_config = ConfigDict(extra="forbid")
    players: list[str] = Field(
        ...,
        description='List of player strings, e.g., ["PlayerOne:123xuid", "PlayerTwo:456xuid"]',
        title="Players",
    )


class AddServerBanResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    message: str = Field(..., title="Message")
    status: Literal["success", "skipped"] | None = Field("success", title="Status")


class AddonActionPayload(ContractModel):
    model_config = ConfigDict(extra="forbid")
    pack_type: Literal["behavior", "resource"] = Field(
        ...,
        description="The type of the pack: 'behavior' or 'resource'.",
        title="Pack Type",
    )
    pack_uuid: str = Field(
        ...,
        description="The UUID of the pack.",
        min_length=1,
        pattern=".*\\S.*",
        title="Pack Uuid",
    )


Uuid = Annotated[str, Field(min_length=1, pattern=".*\\S.*")]


class AddonReorderPayload(ContractModel):
    model_config = ConfigDict(extra="forbid")
    pack_type: Literal["behavior", "resource"] = Field(
        ...,
        description="The type of the pack: 'behavior' or 'resource'.",
        title="Pack Type",
    )
    uuids: list[Uuid] = Field(
        ...,
        description="The exact list of currently active UUIDs in the new desired order.",
        title="Uuids",
    )


class AddonSubpackPayload(ContractModel):
    model_config = ConfigDict(extra="forbid")
    pack_type: Literal["behavior", "resource"] = Field(
        ...,
        description="The type of the pack: 'behavior' or 'resource'.",
        title="Pack Type",
    )
    pack_uuid: str = Field(
        ...,
        description="The UUID of the pack.",
        min_length=1,
        pattern=".*\\S.*",
        title="Pack Uuid",
    )
    subpack_name: str = Field(
        ...,
        description="The folder name of the subpack to activate.",
        min_length=1,
        pattern=".*\\S.*",
        title="Subpack Name",
    )


class AllowlistAddPayload(ContractModel):
    model_config = ConfigDict(extra="forbid")
    ignoresPlayerLimit: bool | None = Field(
        False,
        description="Set 'ignoresPlayerLimit' for these players.",
        title="Ignoresplayerlimit",
    )
    players: list[str] = Field(
        ..., description="List of player gamertags to add.", title="Players"
    )


class AllowlistPlayer(ContractModel):
    model_config = ConfigDict(extra="forbid")
    ignoresPlayerLimit: bool | None = Field(False, title="Ignoresplayerlimit")
    name: str = Field(..., min_length=1, pattern=".*\\S.*", title="Name")
    xuid: str | None = Field(None, title="Xuid")


class AllowlistRemovePayload(ContractModel):
    model_config = ConfigDict(extra="forbid")
    players: list[str] = Field(
        ..., description="List of player gamertags to remove.", title="Players"
    )


class AppInfoResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    info: dict[str, Any] | None = Field(None, title="Info")
    message: str | None = Field(None, title="Message")
    status: Literal["success", "skipped"] = Field(..., title="Status")


class AuditLogResponse(ContractModel):
    action: str = Field(..., title="Action")
    details: dict[str, Any] | None = Field(None, title="Details")
    id: int = Field(..., title="Id")
    timestamp: AwareDatetime = Field(..., title="Timestamp")
    user_id: int = Field(..., title="User Id")


class BackupActionPayload(ContractModel):
    model_config = ConfigDict(extra="forbid")
    backup_type: str = Field(
        ...,
        description="Type of backup: 'world', 'config', or 'all'.",
        title="Backup Type",
    )
    file_to_backup: str | None = Field(
        None,
        description="Name of config file if backup_type is 'config' (e.g., 'server.properties').",
        title="File To Backup",
    )


class BackupFilesResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    backups: list[str] | dict[str, list[str]] = Field(..., title="Backups")
    message: str | None = Field(None, title="Message")
    status: Literal["success"] = Field("success", title="Status")


class BanAddRequest(ContractModel):
    model_config = ConfigDict(extra="forbid")
    player_name: str = Field(..., title="Player Name")
    reason: str | None = Field(None, title="Reason")
    xuid: str = Field(..., title="Xuid")


class BanInfo(ContractModel):
    model_config = ConfigDict(extra="forbid")
    banned_at: str | None = Field(None, title="Banned At")
    player_name: str = Field(..., title="Player Name")
    reason: str | None = Field(None, title="Reason")
    xuid: str = Field(..., title="Xuid")


class BanRemoveRequest(ContractModel):
    model_config = ConfigDict(extra="forbid")
    xuid: str = Field(..., title="Xuid")


class BaseApiResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    status: Literal["success", "skipped"] = Field(..., title="Status")


GrantType = Annotated[str, Field(pattern="^password$", title="Grant Type")]


class BodyLogin(ContractModel):
    client_id: str | None = Field(None, title="Client Id")
    client_secret: SecretStr | None = Field(None, title="Client Secret")
    grant_type: GrantType | None = Field(None, title="Grant Type")
    password: SecretStr = Field(..., title="Password")
    remember_me: bool | None = Field(False, title="Remember Me")
    scope: str | None = Field("", title="Scope")
    username: str = Field(..., title="Username")


class ChangePasswordPayload(ContractModel):
    model_config = ConfigDict(extra="forbid")
    current_password: str = Field(..., title="Current Password")
    new_password: str = Field(..., title="New Password")


class CommandPayload(ContractModel):
    model_config = ConfigDict(extra="forbid")
    command: str = Field(
        ...,
        description="The command to send to the server.",
        min_length=1,
        title="Command",
    )


class ContentListResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    files: list[str] | None = Field(None, title="Files")
    message: str | None = Field(None, title="Message")
    status: Literal["success", "skipped"] = Field(..., title="Status")


class CustomZipsResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    custom_zips: list[str] = Field(..., title="Custom Zips")
    message: str | None = Field(None, title="Message")
    status: Literal["success", "skipped"] = Field(..., title="Status")


class FileNamePayload(ContractModel):
    model_config = ConfigDict(extra="forbid")
    filename: str = Field(..., title="Filename")


class GenerateTokenPayload(ContractModel):
    model_config = ConfigDict(extra="forbid")
    role: Literal["admin", "moderator", "user"] = Field(..., title="Role")


class GetAllowlistResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    players: list[AllowlistPlayer] = Field(..., title="Players")
    status: Literal["success"] = Field("success", title="Status")


Revision = Annotated[int, Field(ge=1, le=9007199254740991, title="Revision")]


class GetPropertiesResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    properties: dict[str, str] = Field(..., title="Properties")
    raw_content: str = Field(..., title="Raw Content")
    status: Literal["success"] = Field("success", title="Status")


class GetServerBansResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    bans: list[BanInfo] = Field(..., title="Bans")
    message: str | None = Field(None, title="Message")
    status: Literal["success"] = Field("success", title="Status")


class HealthCheck(ContractModel):
    model_config = ConfigDict(extra="forbid")
    healthy: bool = Field(..., title="Healthy")
    message: str = Field(..., title="Message")
    status: Literal["success"] = Field("success", title="Status")


class InstallConfirmationResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    message: str = Field(..., title="Message")
    server_name: str = Field(..., title="Server Name")
    status: Literal["confirm_needed"] = Field("confirm_needed", title="Status")


class InstallServerPayload(ContractModel):
    model_config = ConfigDict(extra="forbid")
    overwrite: bool | None = Field(
        False,
        description="If True, confirm overwriting an existing installation.",
        title="Overwrite",
    )
    server_name: str = Field(
        ...,
        description="Name for the new server.",
        examples=["example"],
        max_length=50,
        min_length=1,
        pattern="^[a-zA-Z0-9_-]+$",
        title="Server Name",
    )
    server_version: str | None = Field(
        "LATEST",
        description="Version to install (e.g., 'LATEST', '1.20.10.01', 'CUSTOM').",
        title="Server Version",
    )
    server_zip_path: str | None = Field(
        None,
        description="Path to a custom ZIP file, if 'CUSTOM' version is selected.",
        title="Server Zip Path",
    )


class InstallationAcceptedResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    message: str = Field(..., title="Message")
    server_name: str = Field(..., title="Server Name")
    status: Literal["accepted"] = Field("accepted", title="Status")
    task_id: str = Field(..., title="Task Id")


class ListAvailableAddonsResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    files: list[str] = Field(..., title="Files")
    message: str | None = Field(None, title="Message")
    status: Literal["success"] = Field("success", title="Status")


class LogHistoryPage(ContractModel):
    data: str = Field(..., title="Data")
    end: int = Field(..., title="End")
    file_id: str = Field(..., title="File Id")
    has_more: bool = Field(..., title="Has More")
    start: int = Field(..., title="Start")


AppCpuPercent = Annotated[float, Field(ge=0.0, title="App Cpu Percent")]
AppRamMb = Annotated[float, Field(ge=0.0, title="App Ram Mb")]
DiskReadKibS = Annotated[float, Field(ge=0.0, title="Disk Read Kib S")]
DiskWriteKibS = Annotated[float, Field(ge=0.0, title="Disk Write Kib S")]
NetRxKibS = Annotated[float, Field(ge=0.0, title="Net Rx Kib S")]
NetTxKibS = Annotated[float, Field(ge=0.0, title="Net Tx Kib S")]
SysCpuPercent = Annotated[float, Field(ge=0.0, title="Sys Cpu Percent")]
SysRamMb = Annotated[float, Field(ge=0.0, title="Sys Ram Mb")]
SysRamPercent = Annotated[float, Field(ge=0.0, title="Sys Ram Percent")]
SysRamTotalMb = Annotated[float, Field(ge=0.0, title="Sys Ram Total Mb")]
ThreadCount = Annotated[int, Field(ge=0, title="Thread Count")]
UptimeSeconds = Annotated[float, Field(ge=0.0, title="Uptime Seconds")]


class PermissionsUpdateResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    errors: dict[str, str] | None = Field(None, title="Errors")
    message: str | None = Field(None, title="Message")
    status: Literal["success", "skipped"] = Field(..., title="Status")


class PlayerInfo(ContractModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(..., title="Name")
    xuid: str = Field(..., title="Xuid")


class PlayerListResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    players: list[PlayerInfo] | None = Field(None, title="Players")
    status: Literal["success", "skipped"] = Field(..., title="Status")


class PlayerPermission(ContractModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(..., title="Name")
    permission_level: str = Field(..., title="Permission Level")
    xuid: str = Field(..., title="Xuid")


class PlayerPermissionPayload(ContractModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(..., title="Name")
    permission_level: Literal["visitor", "member", "operator"] = Field(
        ..., title="Permission Level"
    )
    xuid: str = Field(..., title="Xuid")


class PlayerScanError(ContractModel):
    model_config = ConfigDict(extra="forbid")
    error: str = Field(..., title="Error")
    server: str = Field(..., title="Server")


class PluginInfo(ContractModel):
    model_config = ConfigDict(extra="forbid")
    author: str | None = Field("", title="Author")
    description: str | None = Field("", title="Description")
    enabled: bool = Field(..., title="Enabled")
    has_settings: bool | None = Field(False, title="Has Settings")
    status: str | None = Field("UNKNOWN", title="Status")
    version: str | None = Field("N/A", title="Version")


class PluginPagesResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    pages: list[dict[str, Any]] | None = Field(None, title="Pages")
    status: Literal["success", "skipped"] = Field(..., title="Status")


class PluginSettingsPayload(ContractModel):
    model_config = ConfigDict(extra="forbid")
    settings: dict[str, JsonValue] = Field(..., title="Settings")


class PluginStatusSetPayload(ContractModel):
    model_config = ConfigDict(extra="forbid")
    enabled: bool = Field(
        ...,
        description="Set to true to enable the plugin, false to disable.",
        title="Enabled",
    )


class PluginStatusesResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    plugins: dict[str, PluginInfo] | None = Field(None, title="Plugins")
    status: Literal["success", "skipped"] = Field(..., title="Status")


class ProcessInfo(ContractModel):
    model_config = ConfigDict(extra="forbid")
    cpu_percent: float = Field(..., title="Cpu Percent")
    memory_mb: float = Field(..., title="Memory Mb")
    pid: int = Field(..., title="Pid")
    uptime: str = Field(..., title="Uptime")


class ProfileUpdatePayload(ContractModel):
    model_config = ConfigDict(extra="forbid")
    email: str = Field(..., title="Email")
    full_name: str = Field(..., title="Full Name")


class PropertiesPayload(ContractModel):
    model_config = ConfigDict(extra="forbid")
    properties: dict[str, str] = Field(
        ..., description="Dictionary of properties to set.", title="Properties"
    )


Keep = Annotated[
    int,
    Field(
        description="Number of most recent files to keep. Defaults to config if omitted.",
        ge=0,
        title="Keep",
    ),
]


class PruneDownloadsPayload(ContractModel):
    model_config = ConfigDict(extra="forbid")
    directory: str = Field(
        ...,
        description="The subdirectory within the main download cache to prune (e.g., 'stable' or 'preview').",
        min_length=1,
        title="Directory",
    )
    keep: Keep | None = Field(
        None,
        description="Number of most recent files to keep. Defaults to config if omitted.",
        title="Keep",
    )


class PruneDownloadsResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    files_deleted: int | None = Field(None, title="Files Deleted")
    files_kept: int | None = Field(None, title="Files Kept")
    message: str | None = Field(None, title="Message")
    status: Literal["success", "skipped"] = Field(..., title="Status")


class RegistrationResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    registration_url: str = Field(..., title="Registration Url")
    status: Literal["success"] = Field("success", title="Status")


class RemoveServerBanResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    message: str = Field(..., title="Message")
    status: Literal["success", "skipped"] | None = Field("success", title="Status")


class RestartServerResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    message: str = Field(..., title="Message")
    outcome: Literal["restarted", "started"] = Field(..., title="Outcome")
    server_name: str = Field(
        ...,
        examples=["example"],
        min_length=1,
        pattern="^[a-zA-Z0-9_-]+$",
        title="Server Name",
    )
    status: Literal["success"] = Field("success", title="Status")


class RestoreActionPayload(ContractModel):
    model_config = ConfigDict(extra="forbid")
    backup_file: str | None = Field(
        None,
        description="Name of the backup file (basename) to restore from (required if not 'all').",
        title="Backup File",
    )
    restore_type: str = Field(
        ...,
        description="Type of restore: 'world', 'properties', 'allowlist', 'permissions', or 'all'.",
        title="Restore Type",
    )


CpuPercent = Annotated[float, Field(ge=0.0, title="Cpu Percent")]
MemoryMb = Annotated[float, Field(ge=0.0, title="Memory Mb")]
Pid = Annotated[int, Field(gt=0, title="Pid")]


class ServerMetrics(ContractModel):
    model_config = ConfigDict(extra="forbid")
    cpu_percent: CpuPercent | None = Field(None, title="Cpu Percent")
    memory_mb: MemoryMb | None = Field(None, title="Memory Mb")
    pid: Pid | None = Field(None, title="Pid")
    server_name: str = Field(..., title="Server Name")


class ServerProcessInfoResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    epoch: str | None = Field(None, title="Epoch")
    message: str | None = Field(None, title="Message")
    process_info: ProcessInfo | None = None
    revision: Revision | None = Field(None, title="Revision")
    status: Literal["success", "skipped"] = Field(..., title="Status")


class ServerRunningStatusResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    epoch: str | None = Field(None, title="Epoch")
    message: str | None = Field(None, title="Message")
    revision: Revision | None = Field(None, title="Revision")
    running: bool | None = Field(None, title="Running")
    status: Literal["success", "skipped"] = Field(..., title="Status")


class ServerSettingItemPayload(ContractModel):
    model_config = ConfigDict(extra="forbid")
    key: str = Field(
        ...,
        description="The dot-notation key of the setting (e.g., 'settings.autoupdate').",
        title="Key",
    )
    value: JsonValue = Field(..., description="The new value for the setting.")


class ServerSettingsResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    setting: ServerSettingItemPayload | None = None
    settings: dict[str, Any] | None = Field(None, title="Settings")
    status: Literal["success", "skipped"] = Field(..., title="Status")


class ServerSummary(ContractModel):
    model_config = ConfigDict(extra="forbid")
    epoch: str | None = Field(None, title="Epoch")
    name: str = Field(..., title="Name")
    player_count: int | None = Field(0, ge=0, title="Player Count")
    players: list[PlayerInfo] | None = Field(None, title="Players")
    revision: Revision | None = Field(None, title="Revision")
    status: str = Field(..., title="Status")
    version: str = Field(..., title="Version")


class ServersListResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    epoch: str | None = Field(None, title="Epoch")
    message: str | None = Field(None, title="Message")
    revision: Revision | None = Field(None, title="Revision")
    servers: list[ServerSummary] | None = Field(None, title="Servers")
    status: Literal["success", "skipped"] = Field(..., title="Status")


class SetPluginSettingResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    message: str = Field(..., title="Message")
    status: Literal["success", "skipped"] | None = Field("success", title="Status")


class SettingItemResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    key: str = Field(
        ...,
        description="The dot-notation key of the setting (e.g., 'web.port').",
        title="Key",
    )
    value: JsonValue = Field(..., description="The new value for the setting.")


class SettingsResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    setting: SettingItemResponse | None = None
    settings: dict[str, Any] | None = Field(None, title="Settings")
    status: Literal["success", "skipped"] = Field(..., title="Status")


class SetupAccountResponse(ContractModel):
    access_token: str = Field(..., title="Access Token")
    message: str = Field(..., title="Message")
    status: Literal["success"] = Field("success", title="Status")
    token_type: str = Field(..., title="Token Type")


class SetupStatusResponse(ContractModel):
    needs_setup: bool = Field(..., title="Needs Setup")


class StartServerResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    message: str = Field(..., title="Message")
    outcome: Literal["started", "already_running"] = Field(..., title="Outcome")
    server_name: str = Field(
        ...,
        examples=["example"],
        min_length=1,
        pattern="^[a-zA-Z0-9_-]+$",
        title="Server Name",
    )
    status: Literal["success"] = Field("success", title="Status")


class StopServerResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    message: str = Field(..., title="Message")
    outcome: Literal["stopped", "already_stopped"] = Field(..., title="Outcome")
    server_name: str = Field(
        ...,
        examples=["example"],
        min_length=1,
        pattern="^[a-zA-Z0-9_-]+$",
        title="Server Name",
    )
    status: Literal["success"] = Field("success", title="Status")


class Subpack(ContractModel):
    model_config = ConfigDict(extra="forbid")
    folder_name: str = Field(..., title="Folder Name")
    memory_tier: int | None = Field(None, title="Memory Tier")
    name: str | None = Field(None, title="Name")


class TaskAcceptedResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    message: str = Field(..., title="Message")
    status: Literal["accepted"] = Field("accepted", title="Status")
    task_id: str = Field(..., title="Task Id")


class ThemeListResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    status: Literal["success", "skipped"] = Field(..., title="Status")
    themes: list[str] | None = Field(None, title="Themes")


class ThemeUpdatePayload(ContractModel):
    model_config = ConfigDict(extra="forbid")
    theme: str = Field(..., title="Theme")


class TokenResponse(ContractModel):
    access_token: str = Field(..., title="Access Token")
    message: str | None = Field(None, title="Message")
    token_type: str = Field(..., title="Token Type")


class TriggerEventPayload(ContractModel):
    model_config = ConfigDict(extra="forbid")
    event_name: str = Field(
        ...,
        description="The namespaced name of the event to trigger (e.g., 'myplugin:myevent').",
        min_length=1,
        title="Event Name",
    )
    payload: dict[str, JsonValue] | None = Field(
        None, description="Optional dictionary payload for the event.", title="Payload"
    )


class TriggerEventResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    details: dict[str, Any] | None = Field(None, title="Details")
    message: str | None = Field(None, title="Message")
    status: Literal["success", "skipped"] = Field(..., title="Status")


class UpdateUserRolePayload(ContractModel):
    model_config = ConfigDict(extra="forbid")
    role: Literal["admin", "moderator", "user"] = Field(..., title="Role")


class UserLoginPayload(ContractModel):
    model_config = ConfigDict(extra="forbid")
    password: str = Field(..., min_length=1, title="Password")
    remember_me: bool | None = Field(False, title="Remember Me")
    username: str = Field(..., max_length=80, min_length=1, title="Username")


class UserResponse(ContractModel):
    id: int = Field(..., title="Id")
    identity_type: str | None = Field(None, title="Identity Type")
    is_active: bool = Field(..., title="Is Active")
    role: Literal["admin", "moderator", "user"] = Field(..., title="Role")
    theme: str | None = Field("default", title="Theme")
    username: str = Field(..., title="Username")


class APIErrorResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    code: Literal[
        "validation_error",
        "not_found",
        "conflict",
        "forbidden",
        "unauthorized",
        "http_error",
        "operation_canceled",
        "invalid_server_name",
        "server_start_failed",
        "server_stop_failed",
        "server_error",
        "application_error",
        "internal_error",
    ] = Field(..., title="Code")
    details: dict[str, JsonValue] | None = Field(None, title="Details")
    message: str = Field(..., title="Message")


class ErrorEnvelope(ContractModel):
    model_config = ConfigDict(extra="forbid")
    error: APIErrorResponse


class GetApplicationHealthResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    checked_at: float = Field(..., gt=0.0, title="Checked At")
    checks: dict[str, HealthCheck] = Field(..., title="Checks")
    health: Literal["healthy", "degraded"] = Field(..., title="Health")
    lifecycle: Literal["starting", "ready", "stopping", "stopped", "failed"] = Field(
        ..., title="LifecyclePhase"
    )
    message: str | None = Field(None, title="Message")
    status: Literal["success"] = Field("success", title="Status")


class GetPermissionsResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    permissions: list[PlayerPermission] = Field(..., title="Permissions")
    status: Literal["success"] = Field("success", title="Status")


class GetPluginSettingsResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    settings: dict[str, JsonValue] = Field(..., title="Settings")
    settings_schema: dict[str, JsonValue] | None = Field(None, title="Settings Schema")
    status: Literal["success"] = Field("success", title="Status")


class InstalledAddon(ContractModel):
    model_config = ConfigDict(extra="forbid")
    active_subpack: str | None = Field(None, title="Active Subpack")
    icon: str | None = Field(None, title="Icon")
    name: str = Field(..., title="Name")
    path: str | None = Field(None, title="Path")
    status: Literal["ACTIVE", "INACTIVE", "ORPHANED"] = Field(..., title="Status")
    subpacks: list[Subpack] | None = Field(None, title="Subpacks")
    uuid: str = Field(..., title="Uuid")
    version: list[int] = Field(..., title="Version")


class InstalledAddons(ContractModel):
    model_config = ConfigDict(extra="forbid")
    behavior_packs: list[InstalledAddon] | None = Field(None, title="Behavior Packs")
    resource_packs: list[InstalledAddon] | None = Field(None, title="Resource Packs")


class MetricsSample(ContractModel):
    model_config = ConfigDict(extra="forbid")
    app_cpu_percent: AppCpuPercent | None = Field(None, title="App Cpu Percent")
    app_ram_mb: AppRamMb | None = Field(None, title="App Ram Mb")
    asyncio_task_count: int = Field(..., ge=0, title="Asyncio Task Count")
    background_task_count: int = Field(..., ge=0, title="Background Task Count")
    disk_read_kib_s: DiskReadKibS | None = Field(None, title="Disk Read Kib S")
    disk_write_kib_s: DiskWriteKibS | None = Field(None, title="Disk Write Kib S")
    epoch: str | None = Field(None, title="Epoch")
    loop_lag_ms: float = Field(..., ge=0.0, title="Loop Lag Ms")
    net_rx_kib_s: NetRxKibS | None = Field(None, title="Net Rx Kib S")
    net_tx_kib_s: NetTxKibS | None = Field(None, title="Net Tx Kib S")
    revision: Revision | None = Field(None, title="Revision")
    servers: list[ServerMetrics] | None = Field(None, title="Servers")
    sys_cpu_percent: SysCpuPercent | None = Field(None, title="Sys Cpu Percent")
    sys_ram_mb: SysRamMb | None = Field(None, title="Sys Ram Mb")
    sys_ram_percent: SysRamPercent | None = Field(None, title="Sys Ram Percent")
    sys_ram_total_mb: SysRamTotalMb | None = Field(None, title="Sys Ram Total Mb")
    thread_count: ThreadCount | None = Field(None, title="Thread Count")
    timestamp: float = Field(..., gt=0.0, title="Timestamp")
    uptime_seconds: UptimeSeconds | None = Field(None, title="Uptime Seconds")


class PermissionsSetPayload(ContractModel):
    model_config = ConfigDict(extra="forbid")
    permissions: list[PlayerPermissionPayload] = Field(
        ..., description="List of player permission entries.", title="Permissions"
    )


class PlayerScanDetails(ContractModel):
    model_config = ConfigDict(extra="forbid")
    actually_saved_or_updated_in_db: int = Field(
        ..., ge=0, title="Actually Saved Or Updated In Db"
    )
    scan_errors: list[PlayerScanError] = Field(..., title="Scan Errors")
    total_entries_in_logs: int = Field(..., ge=0, title="Total Entries In Logs")
    unique_players_submitted_for_saving: int = Field(
        ..., ge=0, title="Unique Players Submitted For Saving"
    )


class TaskSnapshot(ContractModel):
    model_config = ConfigDict(extra="forbid")
    epoch: str | None = Field(None, title="Epoch")
    error: APIErrorResponse | None = None
    id: str = Field(..., title="Id")
    message: str = Field(..., title="Message")
    result: JsonValue | None = None
    revision: Revision | None = Field(None, title="Revision")
    status: Literal[
        "queued", "running", "completed", "failed", "cancelling", "cancelled"
    ] = Field(..., title="Status")


class AddPlayersResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    count: int | None = Field(None, title="Count")
    details: PlayerScanDetails | None = None
    message: str | None = Field(None, title="Message")
    status: Literal["success", "skipped"] = Field(..., title="Status")


class AddonListResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    addons: InstalledAddons | None = None
    message: str | None = Field(None, title="Message")
    status: Literal["success", "skipped"] = Field(..., title="Status")


class GetApplicationMetricsResponse(ContractModel):
    model_config = ConfigDict(extra="forbid")
    epoch: str | None = Field(None, title="Epoch")
    history: list[MetricsSample] = Field(..., title="History")
    history_limit: int = Field(..., gt=0, le=180, title="History Limit")
    interval_seconds: float = Field(..., gt=0.0, title="Interval Seconds")
    latest: MetricsSample
    message: str | None = Field(None, title="Message")
    revision: Revision | None = Field(None, title="Revision")
    status: Literal["success"] = Field("success", title="Status")
