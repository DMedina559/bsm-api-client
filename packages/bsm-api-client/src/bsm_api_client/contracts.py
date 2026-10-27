# Generated from bundled OpenAPI by scripts/generate_models.py.
from __future__ import annotations

from typing import Annotated, Literal
from uuid import UUID

from pydantic import AwareDatetime, ConfigDict, Field, JsonValue, SecretStr

from bsm_api_client.contract_base import ContractModel


class ActionResponse(ContractModel):
    """Validate and serialize the ActionResponse contract."""

    model_config = ConfigDict(extra="forbid")
    message: str = Field(..., title="Message")
    status: Literal["success", "skipped", "partial"] | None = Field(
        "success", title="Status"
    )


Player = Annotated[str, Field(min_length=1, pattern=".*\\S.*")]


class AddPlayersPayload(ContractModel):
    """Request model for manually adding players to the database.

    Each string in the 'players' list should be in the format "gamertag:xuid"."""

    model_config = ConfigDict(extra="forbid")
    players: list[Player] = Field(
        ...,
        description='List of player strings, e.g., ["PlayerOne:123xuid", "PlayerTwo:456xuid"]',
        min_length=1,
        title="Players",
    )


ParsedCount = Annotated[int, Field(ge=0, title="Parsed Count")]
SubmittedCount = Annotated[int, Field(ge=0, title="Submitted Count")]
UniqueCount = Annotated[int, Field(ge=0, title="Unique Count")]


class AddServerBanResponse(ContractModel):
    """Validate and serialize the AddServerBanResponse contract."""

    model_config = ConfigDict(extra="forbid")
    message: str = Field(..., title="Message")
    server_name: str = Field(
        ...,
        examples=["example"],
        min_length=1,
        pattern="^[a-zA-Z0-9_-]+$",
        title="Server Name",
    )
    status: Literal["success", "skipped", "partial"] | None = Field(
        "success", title="Status"
    )


class AddToAllowlistResponse(ContractModel):
    """Validate and serialize the AddToAllowlistResponse contract."""

    model_config = ConfigDict(extra="forbid")
    added_count: int = Field(..., ge=0, title="Added Count")
    message: str | None = Field(None, title="Message")
    status: Literal["success"] = Field("success", title="Status")


class AddonActionPayload(ContractModel):
    """Request model for modifying a specific addon (e.g. enable, disable, uninstall)."""

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
    """Request model for reordering active addons."""

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
    """Request model for changing the active subpack of an addon."""

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
    """Request model for adding players to the allowlist."""

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
    """Validate and serialize the AllowlistPlayer contract."""

    model_config = ConfigDict(extra="forbid")
    ignoresPlayerLimit: bool | None = Field(False, title="Ignoresplayerlimit")
    name: str = Field(..., min_length=1, pattern=".*\\S.*", title="Name")
    xuid: str | None = Field(None, title="Xuid")


class AllowlistRemovalDetails(ContractModel):
    """Validate and serialize the AllowlistRemovalDetails contract."""

    model_config = ConfigDict(extra="forbid")
    not_found: list[str] = Field(..., title="Not Found")
    removed: list[str] = Field(..., title="Removed")


class AllowlistRemovePayload(ContractModel):
    """Request model for removing players from the allowlist."""

    model_config = ConfigDict(extra="forbid")
    players: list[str] = Field(
        ..., description="List of player gamertags to remove.", title="Players"
    )


class BackupActionPayload(ContractModel):
    """Request model for triggering a backup action."""

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


class BackupCopy(ContractModel):
    """Validate and serialize the BackupCopy contract."""

    model_config = ConfigDict(extra="forbid")
    attempts: int | None = Field(0, title="Attempts")
    completed_at: str | None = Field(None, title="Completed At")
    error: str | None = Field(None, title="Error")
    next_retry_at: str | None = Field(None, title="Next Retry At")
    status: Literal["pending", "completed", "failed", "pruned"] = Field(
        ..., title="Status"
    )


class BackupFile(ContractModel):
    """Validate and serialize the BackupFile contract."""

    model_config = ConfigDict(extra="forbid")
    component: Literal[
        "server_directory",
        "world",
        "server.properties",
        "allowlist.json",
        "permissions.json",
        "script_config",
        "bsm_settings",
        "behavior_packs",
        "resource_packs",
        "development_behavior_packs",
        "development_resource_packs",
    ] = Field(..., title="Component")
    executable: bool | None = Field(False, title="Executable")
    path: str = Field(..., title="Path")
    sha256: str = Field(..., pattern="^[a-f0-9]{64}$", title="Sha256")
    size: int = Field(..., ge=0, title="Size")


class BackupFilesResponse(ContractModel):
    """Validate and serialize the BackupFilesResponse contract."""

    model_config = ConfigDict(extra="forbid")
    backups: list[str] | dict[str, list[str]] = Field(..., title="Backups")
    message: str | None = Field(None, title="Message")
    status: Literal["success"] = Field("success", title="Status")


class BackupManifest(ContractModel):
    """Validate and serialize the BackupManifest contract."""

    model_config = ConfigDict(extra="forbid")
    backup_id: UUID = Field(..., title="Backup Id")
    bedrock_version: str = Field(..., title="Bedrock Version")
    bsm_version: str = Field(..., title="Bsm Version")
    capture_finished_at: AwareDatetime = Field(..., title="Capture Finished At")
    capture_method: Literal["offline", "live"] = Field(..., title="Capture Method")
    capture_started_at: AwareDatetime = Field(..., title="Capture Started At")
    components: dict[
        Literal[
            "server_directory",
            "world",
            "server.properties",
            "allowlist.json",
            "permissions.json",
            "script_config",
            "bsm_settings",
            "behavior_packs",
            "resource_packs",
            "development_behavior_packs",
            "development_resource_packs",
        ],
        Literal["included", "absent"],
    ] = Field(..., title="Components")
    created_at: AwareDatetime = Field(..., title="Created At")
    directories: list[str] | None = Field(None, title="Directories")
    files: list[BackupFile] = Field(..., title="Files")
    format: Literal["bsmbackup"] = Field("bsmbackup", title="Format")
    format_version: Literal[1] = Field(1, title="Format Version")
    mode: Literal["world", "selected", "full"] | None = Field(None, title="Mode")
    reason: (
        Literal["manual", "pre_start", "pre_update", "pre_restore", "scheduled"] | None
    ) = Field("manual", title="Reason")
    selected_components: (
        list[
            Literal[
                "server_directory",
                "world",
                "server.properties",
                "allowlist.json",
                "permissions.json",
                "script_config",
                "bsm_settings",
                "behavior_packs",
                "resource_packs",
                "development_behavior_packs",
                "development_resource_packs",
            ]
        ]
        | None
    ) = Field(None, title="Selected Components")
    source_architecture: str | None = Field(None, title="Source Architecture")
    source_platform: str | None = Field(None, title="Source Platform")
    source_server: str = Field(..., title="Source Server")
    source_world: str = Field(..., title="Source World")
    warnings: list[str] | None = Field(None, title="Warnings")


class BackupVerification(ContractModel):
    """Validate and serialize the BackupVerification contract."""

    model_config = ConfigDict(extra="forbid")
    error: str | None = Field(None, title="Error")
    status: Literal["unverified", "verified", "failed"] | None = Field(
        "unverified", title="Status"
    )
    verified_at: str | None = Field(None, title="Verified At")


class BackupsDiagnostics(ContractModel):
    """Validate and serialize the BackupsDiagnostics contract."""

    model_config = ConfigDict(extra="forbid")
    archives: int = Field(..., title="Archives")
    destination_failures: int = Field(..., title="Destination Failures")
    failed: int = Field(..., title="Failed")
    kind: Literal["backups"] = Field("backups", title="Kind")
    missing_keys: int = Field(..., title="Missing Keys")
    servers: int = Field(..., title="Servers")
    total_bytes: int = Field(..., title="Total Bytes")
    without_backup: int = Field(..., title="Without Backup")


class BanAddRequest(ContractModel):
    """Validate and serialize the BanAddRequest contract."""

    model_config = ConfigDict(extra="forbid")
    player_name: str = Field(..., title="Player Name")
    reason: str | None = Field(None, title="Reason")
    xuid: str = Field(..., title="Xuid")


class BanInfo(ContractModel):
    """Validate and serialize the BanInfo contract."""

    model_config = ConfigDict(extra="forbid")
    banned_at: str | None = Field(None, title="Banned At")
    player_name: str = Field(..., title="Player Name")
    reason: str | None = Field(None, title="Reason")
    xuid: str = Field(..., title="Xuid")


class BanRemoveRequest(ContractModel):
    """Validate and serialize the BanRemoveRequest contract."""

    model_config = ConfigDict(extra="forbid")
    xuid: str = Field(..., title="Xuid")


class BaseApiResponse(ContractModel):
    """Validate and serialize the BaseApiResponse contract."""

    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    status: Literal["success", "skipped", "partial"] = Field(..., title="Status")


class BodyImportServerSnapshot(ContractModel):
    file: bytes = Field(
        ...,
        json_schema_extra={"contentMediaType": "application/octet-stream"},
        title="File",
    )
    recovery_key: str | None = Field(None, title="Recovery Key")


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
    """Request payload for changing the user's password.

    :ivar current_password: The current password for verification.

    :ivar new_password: The new password."""

    model_config = ConfigDict(extra="forbid")
    current_password: SecretStr = Field(..., min_length=1, title="Current Password")
    new_password: SecretStr = Field(..., min_length=1, title="New Password")


class CollectionDiagnostics(ContractModel):
    """Validate and serialize the CollectionDiagnostics contract."""

    model_config = ConfigDict(extra="forbid")
    active: bool | None = Field(False, title="Active")
    cache_age_seconds: float | None = Field(None, title="Cache Age Seconds")
    cache_hits: int | None = Field(0, title="Cache Hits")
    collections: int | None = Field(0, title="Collections")
    failures: int | None = Field(0, title="Failures")
    last_duration_ms: float | None = Field(None, title="Last Duration Ms")
    last_error_type: str | None = Field(None, title="Last Error Type")
    last_periodic_error_type: str | None = Field(None, title="Last Periodic Error Type")
    last_periodic_success_at: float | None = Field(
        None, title="Last Periodic Success At"
    )
    last_success_at: float | None = Field(None, title="Last Success At")
    periodic_cycles: int | None = Field(0, title="Periodic Cycles")
    periodic_enabled: bool | None = Field(False, title="Periodic Enabled")
    periodic_failures: int | None = Field(0, title="Periodic Failures")
    periodic_status: (
        Literal["disabled", "not_started", "running", "stopped", "failed"] | None
    ) = Field("disabled", title="Periodic Status")
    requests: int | None = Field(0, title="Requests")
    status: Literal["ok", "degraded", "unavailable"] | None = Field(
        "ok", title="Status"
    )


class CommandPayload(ContractModel):
    """Request model for sending a command to a server."""

    model_config = ConfigDict(extra="forbid")
    command: str = Field(
        ...,
        description="The command to send to the server.",
        min_length=1,
        title="Command",
    )


class CompletedItem(ContractModel):
    """Validate and serialize the CompletedItem contract."""

    model_config = ConfigDict(extra="forbid")
    error: None = Field(None, title="Error")
    outcome: Literal["completed"] = Field("completed", title="Outcome")
    path: str | None = Field(None, title="Path")
    reason: None = Field(None, title="Reason")


class ContentListResponse(ContractModel):
    """Response model for content listing endpoints.

    :ivar files: A list of filenames found."""

    model_config = ConfigDict(extra="forbid")
    files: list[str] | None = Field(None, title="Files")
    message: str | None = Field(None, title="Message")
    status: Literal["success", "skipped", "partial"] = Field(..., title="Status")


class CustomZipsResponse(ContractModel):
    """Response model for custom zips list."""

    model_config = ConfigDict(extra="forbid")
    custom_zips: list[str] = Field(..., title="Custom Zips")
    message: str | None = Field(None, title="Message")
    status: Literal["success", "skipped", "partial"] = Field(..., title="Status")


class DestinationCleanupPayload(ContractModel):
    """Validate and serialize the DestinationCleanupPayload contract."""

    model_config = ConfigDict(extra="forbid")
    token: str | None = Field(None, title="Token")


class DiagnosticChange(ContractModel):
    """Validate and serialize the DiagnosticChange contract."""

    model_config = ConfigDict(extra="forbid")
    after: float | int | bool | str | None = Field(..., title="After")
    before: float | int | bool | str | None = Field(..., title="Before")
    counter_reset: bool | None = Field(False, title="Counter Reset")
    delta: float | None = Field(None, title="Delta")
    field: str = Field(..., title="Field")
    subsystem: str = Field(..., title="Subsystem")


class DiagnosticComparison(ContractModel):
    """Validate and serialize the DiagnosticComparison contract."""

    model_config = ConfigDict(extra="forbid")
    after_snapshot_id: str = Field(..., title="After Snapshot Id")
    before_snapshot_id: str = Field(..., title="Before Snapshot Id")
    changes: list[DiagnosticChange] | None = Field(
        None, max_length=200, title="Changes"
    )
    elapsed_seconds: float | None = Field(..., title="Elapsed Seconds")
    same_instance: bool = Field(..., title="Same Instance")
    truncated: bool | None = Field(False, title="Truncated")


class DiagnosticEnvironment(ContractModel):
    """Validate and serialize the DiagnosticEnvironment contract."""

    model_config = ConfigDict(extra="forbid")
    backend_version: str = Field(..., title="Backend Version")
    database_dialect: str | None = Field(None, title="Database Dialect")
    database_schema_revision: str | None = Field(None, title="Database Schema Revision")
    frontend_version: str | None = Field(None, title="Frontend Version")
    operating_system: str = Field(..., title="Operating System")
    python_version: str = Field(..., title="Python Version")


class DiagnosticHealthSample(ContractModel):
    """Validate and serialize the DiagnosticHealthSample contract."""

    model_config = ConfigDict(extra="forbid")
    ready: bool | None = Field(..., title="Ready")
    sections: dict[str, Literal["ok", "degraded", "unavailable", "unknown"]] = Field(
        ..., max_length=1000, title="Sections"
    )
    status: Literal["ok", "degraded", "unavailable", "unknown"] = Field(
        ..., title="Status"
    )


class DiagnosticIssue(ContractModel):
    """Validate and serialize the DiagnosticIssue contract."""

    model_config = ConfigDict(extra="forbid")
    action: (
        Literal[
            "inspect_logs",
            "inspect_events",
            "inspect_storage",
            "inspect_plugins",
            "wait_for_drain",
            "check_configuration",
        ]
        | None
    ) = Field(None, title="Action")
    code: str = Field(..., title="Code")
    message: str = Field(..., title="Message")
    severity: Literal["warning", "error"] | None = Field("warning", title="Severity")


CorrelationId = Annotated[str, Field(max_length=160, title="Correlation Id")]
DurationMs = Annotated[float, Field(ge=0.0, title="Duration Ms")]
ErrorType = Annotated[str, Field(max_length=80, title="Error Type")]
OperationId = Annotated[str, Field(max_length=160, title="Operation Id")]
Owner = Annotated[str, Field(max_length=160, title="Owner")]


class DiagnosticRecord(ContractModel):
    """Validate and serialize the DiagnosticRecord contract."""

    model_config = ConfigDict(extra="forbid")
    backend_version: str | None = Field(None, title="Backend Version")
    code: str = Field(..., max_length=80, title="Code")
    correlation_id: CorrelationId | None = Field(None, title="Correlation Id")
    duration_ms: DurationMs | None = Field(None, title="Duration Ms")
    error_type: ErrorType | None = Field(None, title="Error Type")
    health: DiagnosticHealthSample | None = None
    id: str = Field(..., title="Id")
    instance_id: str = Field(..., title="Instance Id")
    operation: str = Field(..., max_length=160, title="Operation")
    operation_id: OperationId | None = Field(None, title="Operation Id")
    outcome: Literal["completed", "failed", "cancelled"] = Field(..., title="Outcome")
    owner: Owner | None = Field(None, title="Owner")
    phase: str | None = Field(None, title="Phase")
    subsystem: str = Field(..., max_length=80, pattern="^[\\w.:-]+$", title="Subsystem")
    timestamp: float = Field(..., title="Timestamp")


class DiagnosticRun(ContractModel):
    """Validate and serialize the DiagnosticRun contract."""

    model_config = ConfigDict(extra="forbid")
    backend_version: str | None = Field(None, title="Backend Version")
    cancelled_records: int = Field(..., title="Cancelled Records")
    current_instance: bool = Field(..., title="Current Instance")
    failed_records: int = Field(..., title="Failed Records")
    first_record_at: float = Field(..., title="First Record At")
    instance_id: str = Field(..., title="Instance Id")
    last_observed_phase: str | None = Field(None, title="Last Observed Phase")
    last_record_at: float = Field(..., title="Last Record At")
    recording_closed: bool | None = Field(None, title="Recording Closed")
    retained_records: int = Field(..., title="Retained Records")


class DiagnosticRuns(ContractModel):
    """Validate and serialize the DiagnosticRuns contract."""

    model_config = ConfigDict(extra="forbid")
    available: bool = Field(..., title="Available")
    runs: list[DiagnosticRun] = Field(..., title="Runs")
    truncated: bool = Field(..., title="Truncated")


class EventDelivery(ContractModel):
    """Validate and serialize the EventDelivery contract."""

    model_config = ConfigDict(extra="forbid")
    failed: int | None = Field(0, ge=0, title="Failed")
    owner: str = Field(..., title="Owner")
    sent: int | None = Field(0, ge=0, title="Sent")
    targeted: int | None = Field(0, ge=0, title="Targeted")
    unavailable: int | None = Field(0, ge=0, title="Unavailable")


class EventFilter(ContractModel):
    """Validate and serialize the EventFilter contract."""

    model_config = ConfigDict(extra="forbid")
    correlation_id: str | None = Field(None, title="Correlation Id")
    operation_name: str | None = Field(None, title="Operation Name")
    plugin_name: str | None = Field(None, title="Plugin Name")
    sequence_id: str | None = Field(None, title="Sequence Id")
    server_name: str | None = Field(None, title="Server Name")
    source: str | None = Field(None, title="Source")


MaxWorkers = Annotated[int, Field(ge=1, le=10000, title="Max Workers")]
MaxWorkersPerOwner = Annotated[
    int, Field(ge=1, le=10000, title="Max Workers Per Owner")
]


class EventOptions(ContractModel):
    """Validate and serialize the EventOptions contract."""

    model_config = ConfigDict(extra="forbid")
    history_limit: int | None = Field(200, ge=0, le=10000, title="History Limit")
    hook_timeout_seconds: float | None = Field(
        120, gt=0.0, le=3600.0, title="Hook Timeout Seconds"
    )
    listener_timeout_seconds: float | None = Field(
        30, gt=0.0, le=3600.0, title="Listener Timeout Seconds"
    )
    max_active: int | None = Field(256, ge=1, le=10000, title="Max Active")
    max_depth: int | None = Field(32, ge=1, le=128, title="Max Depth")
    max_workers: MaxWorkers | None = Field(None, title="Max Workers")
    max_workers_per_owner: MaxWorkersPerOwner | None = Field(
        None, title="Max Workers Per Owner"
    )


class EventSubscriptionInfo(ContractModel):
    """Validate and serialize the EventSubscriptionInfo contract."""

    model_config = ConfigDict(extra="forbid")
    active: bool = Field(..., title="Active")
    after: list[str] | None = Field([], title="After")
    before: list[str] | None = Field([], title="Before")
    calls: int | None = Field(0, title="Calls")
    failures: int | None = Field(0, title="Failures")
    filters: EventFilter | None = None
    kind: Literal["legacy", "hook", "observer"] = Field(..., title="Kind")
    last_duration_ms: float | None = Field(0, title="Last Duration Ms")
    last_status: str | None = Field(None, title="Last Status")
    listener_id: str = Field(..., title="Listener Id")
    name: str = Field(..., title="Name")
    once: bool = Field(..., title="Once")
    owner: str = Field(..., title="Owner")
    priority: int = Field(..., title="Priority")
    subscription_id: str = Field(..., title="Subscription Id")
    timeouts: int | None = Field(0, title="Timeouts")
    unresolved_after: list[str] | None = Field([], title="Unresolved After")
    unresolved_before: list[str] | None = Field([], title="Unresolved Before")


class EventSubscriptions(ContractModel):
    """Validate and serialize the EventSubscriptions contract."""

    model_config = ConfigDict(extra="forbid")
    items: list[EventSubscriptionInfo] | None = Field(None, title="Items")
    total: int | None = Field(0, title="Total")
    truncated: bool | None = Field(False, title="Truncated")


class FileNamePayload(ContractModel):
    """Payload for file-based operations.

    :ivar filename: The name of the file to operate on."""

    model_config = ConfigDict(extra="forbid")
    filename: str = Field(..., min_length=1, pattern=".*\\S.*", title="Filename")


class GenerateTokenPayload(ContractModel):
    """Request payload for generating a registration token.

    :ivar role: The role to assign to the user registering with this token."""

    model_config = ConfigDict(extra="forbid")
    role: Literal["admin", "moderator", "user"] = Field(..., title="Role")


class GetAllowlistResponse(ContractModel):
    """Validate and serialize the GetAllowlistResponse contract."""

    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    players: list[AllowlistPlayer] = Field(..., title="Players")
    status: Literal["success"] = Field("success", title="Status")


Revision = Annotated[int, Field(ge=1, le=9007199254740991, title="Revision")]


class GetPropertiesResponse(ContractModel):
    """Validate and serialize the GetPropertiesResponse contract."""

    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    properties: dict[str, str] = Field(..., title="Properties")
    raw_content: str = Field(..., title="Raw Content")
    status: Literal["success"] = Field("success", title="Status")


class GetRawPropertiesResponse(ContractModel):
    """Validate and serialize the GetRawPropertiesResponse contract."""

    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    raw_content: str = Field(..., title="Raw Content")
    status: Literal["success"] = Field("success", title="Status")


class GetServerBansResponse(ContractModel):
    """Validate and serialize the GetServerBansResponse contract."""

    model_config = ConfigDict(extra="forbid")
    bans: list[BanInfo] = Field(..., title="Bans")
    message: str | None = Field(None, title="Message")
    status: Literal["success"] = Field("success", title="Status")


class HealthCheck(ContractModel):
    """Validate and serialize the HealthCheck contract."""

    model_config = ConfigDict(extra="forbid")
    healthy: bool = Field(..., title="Healthy")
    message: str = Field(..., title="Message")
    status: Literal["success"] = Field("success", title="Status")


class InstallConfirmationResponse(ContractModel):
    """Validate and serialize the InstallConfirmationResponse contract."""

    model_config = ConfigDict(extra="forbid")
    message: str = Field(..., title="Message")
    server_name: str = Field(..., title="Server Name")
    status: Literal["confirm_needed"] = Field("confirm_needed", title="Status")


class InstallServerPayload(ContractModel):
    """Request model for installing a new server."""

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
    """Validate and serialize the InstallationAcceptedResponse contract."""

    model_config = ConfigDict(extra="forbid")
    message: str = Field(..., title="Message")
    server_name: str = Field(..., title="Server Name")
    status: Literal["accepted"] = Field("accepted", title="Status")
    task_id: str = Field(..., title="Task Id")


class ListAvailableAddonsResponse(ContractModel):
    """Validate and serialize the ListAvailableAddonsResponse contract."""

    model_config = ConfigDict(extra="forbid")
    files: list[str] = Field(..., title="Files")
    message: str | None = Field(None, title="Message")
    status: Literal["success"] = Field("success", title="Status")


class ListenerFailure(ContractModel):
    """Validate and serialize the ListenerFailure contract."""

    model_config = ConfigDict(extra="forbid")
    code: Literal[
        "event_listener_failed",
        "event_listener_timeout",
        "event_depth_limit",
        "event_capacity",
    ] = Field(..., title="Code")
    error_type: str = Field(..., title="Error Type")
    owner: str = Field(..., title="Owner")


class ListenerRecord(ContractModel):
    """Validate and serialize the ListenerRecord contract."""

    model_config = ConfigDict(extra="forbid")
    duration_ms: float | None = Field(0, ge=0.0, title="Duration Ms")
    failure: ListenerFailure | None = None
    listener_name: str = Field(..., title="Listener Name")
    observer: bool = Field(..., title="Observer")
    owner: str = Field(..., title="Owner")
    status: (
        Literal["running", "completed", "failed", "timed_out", "cancelled"] | None
    ) = Field("running", title="Status")
    subscription_id: str = Field(..., title="Subscription Id")


class LogHistoryPage(ContractModel):
    """Validate and serialize the LogHistoryPage contract."""

    data: str = Field(..., title="Data")
    end: int = Field(..., title="End")
    file_id: str = Field(..., title="File Id")
    has_more: bool = Field(..., title="Has More")
    start: int = Field(..., title="Start")


class MetricsDiagnostics(ContractModel):
    """Validate and serialize the MetricsDiagnostics contract."""

    model_config = ConfigDict(extra="forbid")
    attempts: int | None = Field(0, title="Attempts")
    event_loop_lag_breaches: int | None = Field(0, title="Event Loop Lag Breaches")
    event_loop_lag_ms: float | None = Field(0, title="Event Loop Lag Ms")
    event_loop_lag_threshold_ms: float | None = Field(
        100, title="Event Loop Lag Threshold Ms"
    )
    failures: int | None = Field(0, title="Failures")
    interval_seconds: float | None = Field(None, title="Interval Seconds")
    kind: Literal["metrics"] = Field("metrics", title="Kind")
    last_duration_ms: float | None = Field(None, title="Last Duration Ms")
    last_error_type: str | None = Field(None, title="Last Error Type")
    last_sample_at: float | None = Field(None, title="Last Sample At")
    missed_intervals: int | None = Field(0, title="Missed Intervals")
    recent_max_event_loop_lag_ms: float | None = Field(
        0, title="Recent Max Event Loop Lag Ms"
    )
    sample_age_seconds: float | None = Field(None, title="Sample Age Seconds")
    successes: int | None = Field(0, title="Successes")
    unavailable_measurements: list[str] | None = Field(
        None, title="Unavailable Measurements"
    )
    warming_up: bool | None = Field(True, title="Warming Up")


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


class OperationSnapshot(ContractModel):
    """Immutable coordination metadata; response bodies and secrets are excluded."""

    model_config = ConfigDict(extra="forbid")
    correlation_id: str = Field(..., title="Correlation Id")
    finished_at: float | None = Field(None, title="Finished At")
    name: str = Field(..., title="Name")
    operation_id: str = Field(..., title="Operation Id")
    outcome: str | None = Field(None, title="Outcome")
    owner: str | None = Field("application", title="Owner")
    parent_operation_id: str | None = Field(None, title="Parent Operation Id")
    purpose: str | None = Field(None, title="Purpose")
    root_operation_id: str = Field(..., title="Root Operation Id")
    scope: list[str] | None = Field([], title="Scope")
    sequence_id: str = Field(..., title="Sequence Id")
    server_name: str | None = Field(None, title="Server Name")
    source: str | None = Field("application", title="Source")
    started_at: float = Field(..., title="Started At")
    status: Literal["running", "finished", "failed", "cancelled"] | None = Field(
        "running", title="Status"
    )


class PersistenceDiagnostics(ContractModel):
    """Validate and serialize the PersistenceDiagnostics contract."""

    model_config = ConfigDict(extra="forbid")
    accepting: bool = Field(..., title="Accepting")
    dropped: int = Field(..., title="Dropped")
    history_limit: int = Field(..., title="History Limit")
    last_error_type: str | None = Field(None, title="Last Error Type")
    last_read_error_type: str | None = Field(None, title="Last Read Error Type")
    last_read_success_at: float | None = Field(None, title="Last Read Success At")
    last_success_at: float | None = Field(None, title="Last Success At")
    queue_limit: int = Field(..., title="Queue Limit")
    queued: int = Field(..., title="Queued")
    read_failures: int | None = Field(0, title="Read Failures")
    retention_days: int = Field(..., title="Retention Days")
    write_failures: int = Field(..., title="Write Failures")
    writer_status: Literal["not_started", "running", "failed", "closed"] | None = Field(
        "not_started", title="Writer Status"
    )


class PlayerInfo(ContractModel):
    """Validate and serialize the PlayerInfo contract."""

    model_config = ConfigDict(extra="forbid")
    name: str = Field(..., title="Name")
    xuid: str = Field(..., title="Xuid")


class PlayerListResponse(ContractModel):
    """Response model for player lists."""

    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    players: list[PlayerInfo] | None = Field(None, title="Players")
    status: Literal["success", "skipped", "partial"] = Field(..., title="Status")


class PlayerPermission(ContractModel):
    """Validate and serialize the PlayerPermission contract."""

    model_config = ConfigDict(extra="forbid")
    name: str = Field(..., title="Name")
    permission_level: str = Field(..., title="Permission Level")
    xuid: str = Field(..., title="Xuid")


class PlayerPermissionPayload(ContractModel):
    """Represent a single player's permission data sent from the client."""

    model_config = ConfigDict(extra="forbid")
    name: str = Field(..., title="Name")
    permission_level: Literal["visitor", "member", "operator"] = Field(
        ..., title="Permission Level"
    )
    xuid: str = Field(..., title="Xuid")


class PluginDiagnostic(ContractModel):
    """Validate and serialize the PluginDiagnostic contract."""

    model_config = ConfigDict(extra="forbid")
    active_tasks: int = Field(..., title="Active Tasks")
    diagnostic_providers: int | None = Field(0, title="Diagnostic Providers")
    drain_failures: int | None = Field(0, title="Drain Failures")
    draining: bool = Field(..., title="Draining")
    generation: int = Field(..., title="Generation")
    last_drain_duration_ms: float | None = Field(None, title="Last Drain Duration Ms")
    last_transition_at: float | None = Field(None, title="Last Transition At")
    listeners: int | None = Field(0, title="Listeners")
    load_failures: int | None = Field(0, title="Load Failures")
    managed_tasks: int | None = Field(0, title="Managed Tasks")
    name: str = Field(..., title="Name")
    status: str = Field(..., title="Status")
    version: str | None = Field(None, title="Version")
    workers: int | None = Field(0, title="Workers")


class PluginInfo(ContractModel):
    """Validate and serialize the PluginInfo contract."""

    model_config = ConfigDict(extra="forbid")
    author: str | None = Field("", title="Author")
    description: str | None = Field("", title="Description")
    enabled: bool = Field(..., title="Enabled")
    has_global_settings: bool | None = Field(False, title="Has Global Settings")
    has_server_settings: bool | None = Field(False, title="Has Server Settings")
    has_settings: bool | None = Field(False, title="Has Settings")
    status: str | None = Field("UNKNOWN", title="Status")
    version: str | None = Field("N/A", title="Version")


class PluginPagesResponse(ContractModel):
    """Response model for plugin native UI pages."""

    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    pages: list[dict[str, JsonValue]] | None = Field(None, title="Pages")
    status: Literal["success", "skipped", "partial"] = Field(..., title="Status")


ServerName = Annotated[
    str,
    Field(
        examples=["example"],
        min_length=1,
        pattern="^[a-zA-Z0-9_-]+$",
        title="Server Name",
    ),
]


class PluginSettingsPayload(ContractModel):
    """Validate and serialize the PluginSettingsPayload contract."""

    model_config = ConfigDict(extra="forbid")
    scope: Literal["plugin", "global", "server"] | None = Field("plugin", title="Scope")
    server_name: ServerName | None = Field(None, title="Server Name")
    settings: dict[str, JsonValue] = Field(..., title="Settings")


class PluginStatusSetPayload(ContractModel):
    """Request model for setting a plugin's enabled status."""

    model_config = ConfigDict(extra="forbid")
    enabled: bool = Field(
        ...,
        description="Set to true to enable the plugin, false to disable.",
        title="Enabled",
    )


class PluginStatusesResponse(ContractModel):
    """Response model for plugin statuses."""

    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    plugins: dict[str, PluginInfo] | None = Field(None, title="Plugins")
    status: Literal["success", "skipped", "partial"] = Field(..., title="Status")


class PluginValues(ContractModel):
    """Explicit observations; string dumps and secrets are excluded."""

    model_config = ConfigDict(extra="forbid")
    health: Literal["ok", "degraded", "unknown"] | None = Field(
        "unknown", title="Health"
    )
    kind: Literal["plugin_values"] = Field("plugin_values", title="Kind")
    units: (
        dict[str, Literal["count", "seconds", "milliseconds", "bytes", "percent"]]
        | None
    ) = Field(None, max_length=50, title="Units")
    values: dict[str, float | bool | None] = Field(..., max_length=50, title="Values")


class PluginsDiagnostics(ContractModel):
    """Validate and serialize the PluginsDiagnostics contract."""

    model_config = ConfigDict(extra="forbid")
    kind: Literal["plugins"] = Field("plugins", title="Kind")
    plugins: list[PluginDiagnostic] | None = Field(None, title="Plugins")
    total: int | None = Field(0, title="Total")
    truncated: bool | None = Field(False, title="Truncated")


class ProcessDiagnostic(ContractModel):
    """Validate and serialize the ProcessDiagnostic contract."""

    model_config = ConfigDict(extra="forbid")
    expected_status: str = Field(..., title="Expected Status")
    last_error_type: str | None = Field(None, title="Last Error Type")
    observed_at: float | None = Field(None, title="Observed At")
    observed_running: bool | None = Field(None, title="Observed Running")
    pid: int | None = Field(None, title="Pid")
    server_name: str = Field(..., title="Server Name")


class ProcessInfo(ContractModel):
    """Validate and serialize the ProcessInfo contract."""

    model_config = ConfigDict(extra="forbid")
    cpu_percent: float = Field(..., title="Cpu Percent")
    memory_mb: float = Field(..., title="Memory Mb")
    pid: int = Field(..., title="Pid")
    uptime: str = Field(..., title="Uptime")


class ProcessesDiagnostics(ContractModel):
    """Validate and serialize the ProcessesDiagnostics contract."""

    model_config = ConfigDict(extra="forbid")
    kind: Literal["processes"] = Field("processes", title="Kind")
    last_monitor_at: float | None = Field(None, title="Last Monitor At")
    monitor_failures: int | None = Field(None, title="Monitor Failures")
    observation_available: bool = Field(..., title="Observation Available")
    observed_running: int = Field(..., title="Observed Running")
    processes: list[ProcessDiagnostic] | None = Field(None, title="Processes")
    registered: int = Field(..., title="Registered")
    truncated: bool | None = Field(False, title="Truncated")


class ProfileUpdatePayload(ContractModel):
    """Request payload for updating user profile details.

    :ivar full_name: The user's full name.

    :ivar email: The user's email address."""

    model_config = ConfigDict(extra="forbid")
    email: str = Field(..., title="Email")
    full_name: str = Field(..., title="Full Name")


class PropertiesPayload(ContractModel):
    """Request model for updating server.properties."""

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
    """Request model for pruning the download cache."""

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


class RecentDiagnosticCounts(ContractModel):
    """Validate and serialize the RecentDiagnosticCounts contract."""

    model_config = ConfigDict(extra="forbid")
    cancelled: int | None = Field(0, title="Cancelled")
    failed: int | None = Field(0, title="Failed")
    timeouts: int | None = Field(0, title="Timeouts")


class RecentDiagnosticWindow(ContractModel):
    """Validate and serialize the RecentDiagnosticWindow contract."""

    model_config = ConfigDict(extra="forbid")
    bucket_seconds: Literal[10] = Field(10, title="Bucket Seconds")
    by_subsystem: dict[str, RecentDiagnosticCounts] | None = Field(
        None, title="By Subsystem"
    )
    cancelled: int | None = Field(0, title="Cancelled")
    failures: int | None = Field(0, title="Failures")
    observed_since: float = Field(..., title="Observed Since")
    timeouts: int | None = Field(0, title="Timeouts")
    window_seconds: Literal[300] = Field(300, title="Window Seconds")


class RecoveryReportArchive(ContractModel):
    """Validate and serialize the RecoveryReportArchive contract."""

    model_config = ConfigDict(extra="forbid")
    archive_reference: str = Field(..., title="Archive Reference")
    copies_completed: int = Field(..., title="Copies Completed")
    copies_failed: int = Field(..., title="Copies Failed")
    encrypted: bool = Field(..., title="Encrypted")
    key_available: bool = Field(..., title="Key Available")
    verification_status: Literal["unverified", "verified", "failed"] = Field(
        ..., title="Verification Status"
    )
    verified_at: str | None = Field(None, title="Verified At")


class RecoveryReportDrill(ContractModel):
    """Validate and serialize the RecoveryReportDrill contract."""

    model_config = ConfigDict(extra="forbid")
    archive_reference: str = Field(..., title="Archive Reference")
    checked_at: str | None = Field(None, title="Checked At")
    checked_files: int | None = Field(0, title="Checked Files")
    status: Literal["passed", "failed", "running"] = Field(..., title="Status")


class RecoveryReportOutcome(ContractModel):
    """Validate and serialize the RecoveryReportOutcome contract."""

    model_config = ConfigDict(extra="forbid")
    archive_reference: str = Field(..., title="Archive Reference")
    cleanup_needed: bool | None = Field(False, title="Cleanup Needed")
    committed: bool | None = Field(None, title="Committed")
    components: list[
        Literal[
            "server_directory",
            "world",
            "server.properties",
            "allowlist.json",
            "permissions.json",
            "script_config",
            "bsm_settings",
            "behavior_packs",
            "resource_packs",
            "development_behavior_packs",
            "development_resource_packs",
        ]
    ] = Field(..., title="Components")
    recorded_at: str = Field(..., title="Recorded At")
    restart_failed: bool | None = Field(False, title="Restart Failed")
    restarted: bool | None = Field(False, title="Restarted")
    status: Literal["completed", "failed", "cancelled"] = Field(..., title="Status")


class RegistrationResponse(ContractModel):
    """Validate and serialize the RegistrationResponse contract."""

    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    registration_url: str = Field(..., title="Registration Url")
    status: Literal["success"] = Field("success", title="Status")


class RegistryDiagnostics(ContractModel):
    """Validate and serialize the RegistryDiagnostics contract."""

    model_config = ConfigDict(extra="forbid")
    failures: int | None = Field(0, title="Failures")
    max_providers: int = Field(..., title="Max Providers")
    max_providers_per_owner: int = Field(..., title="Max Providers Per Owner")
    owner_limits_scope: Literal["plugins"] = Field(
        "plugins", title="Owner Limits Scope"
    )
    pending: int = Field(..., title="Pending")
    pending_by_owner: dict[str, int] | None = Field(None, title="Pending By Owner")
    registered: int = Field(..., title="Registered")
    registered_by_owner: dict[str, int] | None = Field(
        None, title="Registered By Owner"
    )
    rejected: int | None = Field(0, title="Rejected")
    timeouts: int | None = Field(0, title="Timeouts")


class RemoveFromAllowlistResponse(ContractModel):
    """Validate and serialize the RemoveFromAllowlistResponse contract."""

    model_config = ConfigDict(extra="forbid")
    details: AllowlistRemovalDetails
    message: str | None = Field(None, title="Message")
    status: Literal["success"] = Field("success", title="Status")


class RemoveServerBanResponse(ContractModel):
    """Validate and serialize the RemoveServerBanResponse contract."""

    model_config = ConfigDict(extra="forbid")
    message: str = Field(..., title="Message")
    server_name: str = Field(
        ...,
        examples=["example"],
        min_length=1,
        pattern="^[a-zA-Z0-9_-]+$",
        title="Server Name",
    )
    status: Literal["success", "skipped", "partial"] | None = Field(
        "success", title="Status"
    )


class RestartServerResponse(ContractModel):
    """Validate and serialize the RestartServerResponse contract."""

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
    """Request model for triggering a restore action."""

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


class RestoreRecoveryState(ContractModel):
    """Validate and serialize the RestoreRecoveryState contract."""

    model_config = ConfigDict(extra="forbid")
    active: bool = Field(..., title="Active")
    committed: bool | None = Field(None, title="Committed")
    error: str | None = Field(None, title="Error")


class RestoreVolume(ContractModel):
    """Validate and serialize the RestoreVolume contract."""

    model_config = ConfigDict(extra="forbid")
    available_bytes: int = Field(..., title="Available Bytes")
    required_bytes: int = Field(..., title="Required Bytes")
    roles: list[str] = Field(..., title="Roles")
    sufficient: bool = Field(..., title="Sufficient")


class RuntimeDiagnostics(ContractModel):
    """Validate and serialize the RuntimeDiagnostics contract."""

    model_config = ConfigDict(extra="forbid")
    draining_workers: int | None = Field(0, title="Draining Workers")
    kind: Literal["runtime"] = Field("runtime", title="Kind")
    oldest_draining_worker_seconds: float | None = Field(
        None, title="Oldest Draining Worker Seconds"
    )
    pending_lifecycle_stages: list[str] | None = Field(
        None, title="Pending Lifecycle Stages"
    )
    phase: str = Field(..., title="Phase")
    pid: int = Field(..., title="Pid")
    python_version: str = Field(..., title="Python Version")
    queued_workers: int | None = Field(0, title="Queued Workers")
    ready: bool | None = Field(False, title="Ready")
    running_workers: int | None = Field(0, title="Running Workers")
    shutdown_reason: str | None = Field(None, title="Shutdown Reason")
    shutdown_requested: bool | None = Field(None, title="Shutdown Requested")
    stage: str | None = Field(None, title="Stage")
    stage_elapsed_seconds: float | None = Field(None, title="Stage Elapsed Seconds")
    stage_started_at: float | None = Field(None, title="Stage Started At")
    stage_timeout_seconds: float | None = Field(None, title="Stage Timeout Seconds")
    uptime_seconds: float = Field(..., title="Uptime Seconds")
    version: str = Field(..., title="Version")


class RuntimeStatus(ContractModel):
    """Validate and serialize the RuntimeStatus contract."""

    model_config = ConfigDict(extra="forbid")
    instance_id: str = Field(..., title="Instance Id")
    phase: Literal["starting", "ready", "stopping", "stopped", "failed"] = Field(
        ..., title="LifecyclePhase"
    )
    pid: int = Field(..., title="Pid")
    shutdown_reason: (
        Literal["administrator", "local_cli", "service", "signal"] | None
    ) = Field(None, title="Shutdown Reason")
    shutdown_requested: bool = Field(..., title="Shutdown Requested")


class ScheduledTask(ContractModel):
    """Validate and serialize the ScheduledTask contract."""

    model_config = ConfigDict(extra="forbid")
    catch_up: bool | None = Field(True, title="Catch Up")
    enabled: bool | None = Field(True, title="Enabled")
    options: dict[str, JsonValue] | None = Field(None, title="Options")
    server_name: str = Field(..., max_length=160, min_length=1, title="Server Name")
    stagger_minutes: int | None = Field(15, ge=0, le=120, title="Stagger Minutes")
    task: str = Field(
        ...,
        max_length=160,
        pattern="^(backup|verify|[a-zA-Z0-9_.-]+:[a-zA-Z0-9_.-]+)$",
        title="Task",
    )
    time: str | None = Field(
        "03:00", pattern="^(?:[01][0-9]|2[0-3]):[0-5][0-9]$", title="Time"
    )
    timezone: str | None = Field("UTC", title="Timezone")
    weekdays: list[int] | None = Field(
        None, max_length=7, min_length=1, title="Weekdays"
    )


class SendCommandResponse(ContractModel):
    """Validate and serialize the SendCommandResponse contract."""

    model_config = ConfigDict(extra="forbid")
    message: str = Field(..., title="Message")
    server_name: str = Field(
        ...,
        examples=["example"],
        min_length=1,
        pattern="^[a-zA-Z0-9_-]+$",
        title="Server Name",
    )
    status: Literal["success", "skipped", "partial"] | None = Field(
        "success", title="Status"
    )


CpuPercent = Annotated[float, Field(ge=0.0, title="Cpu Percent")]
MemoryMb = Annotated[float, Field(ge=0.0, title="Memory Mb")]
Pid = Annotated[int, Field(gt=0, title="Pid")]


class ServerMetrics(ContractModel):
    """Validate and serialize the ServerMetrics contract."""

    model_config = ConfigDict(extra="forbid")
    cpu_percent: CpuPercent | None = Field(None, title="Cpu Percent")
    memory_mb: MemoryMb | None = Field(None, title="Memory Mb")
    pid: Pid | None = Field(None, title="Pid")
    server_name: str = Field(..., title="Server Name")


class ServerProcessInfoResponse(ContractModel):
    """Response model for server process info."""

    model_config = ConfigDict(extra="forbid")
    epoch: str | None = Field(None, title="Epoch")
    message: str | None = Field(None, title="Message")
    process_info: ProcessInfo | None = None
    revision: Revision | None = Field(None, title="Revision")
    status: Literal["success", "skipped", "partial"] = Field(..., title="Status")


class ServerRunningStatusResponse(ContractModel):
    """Response model for server running status."""

    model_config = ConfigDict(extra="forbid")
    epoch: str | None = Field(None, title="Epoch")
    message: str | None = Field(None, title="Message")
    revision: Revision | None = Field(None, title="Revision")
    running: bool | None = Field(None, title="Running")
    status: Literal["success", "skipped", "partial"] = Field(..., title="Status")


class ServerSettingItemPayload(ContractModel):
    """Request model for a single server setting key-value pair."""

    model_config = ConfigDict(extra="forbid")
    key: str = Field(
        ...,
        description="The dot-notation key of the setting (e.g., 'settings.autoupdate').",
        min_length=1,
        pattern=".*\\S.*",
        title="Key",
    )
    value: JsonValue = Field(..., description="The new value for the setting.")


class ServerSettingsResponse(ContractModel):
    """Response model for server settings operations."""

    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    setting: ServerSettingItemPayload | None = None
    settings: dict[str, JsonValue] | None = Field(None, title="Settings")
    status: Literal["success", "skipped", "partial"] = Field(..., title="Status")


class ServerSummary(ContractModel):
    """Validate and serialize the ServerSummary contract."""

    model_config = ConfigDict(extra="forbid")
    epoch: str | None = Field(None, title="Epoch")
    name: str = Field(..., title="Name")
    player_count: int | None = Field(0, ge=0, title="Player Count")
    players: list[PlayerInfo] | None = Field(None, title="Players")
    players_available: bool | None = Field(True, title="Players Available")
    revision: Revision | None = Field(None, title="Revision")
    status: str = Field(..., title="Status")
    version: str = Field(..., title="Version")


class SetPluginSettingResponse(ContractModel):
    """Validate and serialize the SetPluginSettingResponse contract."""

    model_config = ConfigDict(extra="forbid")
    message: str = Field(..., title="Message")
    status: Literal["success", "skipped", "partial"] | None = Field(
        "success", title="Status"
    )


class SetPropertiesResponse(ContractModel):
    """Validate and serialize the SetPropertiesResponse contract."""

    model_config = ConfigDict(extra="forbid")
    message: str = Field(..., title="Message")
    server_name: str = Field(
        ...,
        examples=["example"],
        min_length=1,
        pattern="^[a-zA-Z0-9_-]+$",
        title="Server Name",
    )
    status: Literal["success", "skipped", "partial"] | None = Field(
        "success", title="Status"
    )


class SettingItemResponse(ContractModel):
    """Request model for a single setting key-value pair."""

    model_config = ConfigDict(extra="forbid")
    key: str = Field(
        ...,
        description="The dot-notation key of the setting (e.g., 'web.port').",
        min_length=1,
        pattern=".*\\S.*",
        title="Key",
    )
    value: JsonValue = Field(..., description="The new value for the setting.")


class SettingsResponse(ContractModel):
    """Response model for settings operations."""

    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    setting: SettingItemResponse | None = None
    settings: dict[str, JsonValue] | None = Field(None, title="Settings")
    status: Literal["success", "skipped", "partial"] = Field(..., title="Status")


class SetupAccountResponse(ContractModel):
    """First account creation returns the same session credentials as login."""

    model_config = ConfigDict(extra="forbid")
    access_token: str = Field(..., title="Access Token")
    message: str = Field(..., title="Message")
    status: Literal["success"] = Field("success", title="Status")
    token_type: Literal["bearer"] = Field("bearer", title="Token Type")


class SetupStatusResponse(ContractModel):
    """Response model for setup status."""

    model_config = ConfigDict(extra="forbid")
    needs_setup: bool = Field(..., title="Needs Setup")


class ShutdownRequest(ContractModel):
    """Validate and serialize the ShutdownRequest contract."""

    model_config = ConfigDict(extra="forbid")


class ShutdownResponse(ContractModel):
    """Validate and serialize the ShutdownResponse contract."""

    model_config = ConfigDict(extra="forbid")
    instance_id: str = Field(..., title="Instance Id")
    phase: Literal["starting", "ready", "stopping", "stopped", "failed"] = Field(
        ..., title="LifecyclePhase"
    )
    pid: int = Field(..., title="Pid")
    shutdown_reason: (
        Literal["administrator", "local_cli", "service", "signal"] | None
    ) = Field(None, title="Shutdown Reason")
    shutdown_requested: bool = Field(..., title="Shutdown Requested")
    status: Literal["accepted"] = Field("accepted", title="Status")


class SkippedItem(ContractModel):
    """Validate and serialize the SkippedItem contract."""

    model_config = ConfigDict(extra="forbid")
    error: None = Field(None, title="Error")
    outcome: Literal["skipped"] = Field("skipped", title="Outcome")
    path: None = Field(None, title="Path")
    reason: str = Field(..., title="Reason")


class SnapshotCopyPayload(ContractModel):
    """Validate and serialize the SnapshotCopyPayload contract."""

    model_config = ConfigDict(extra="forbid")
    recovery_key: SecretStr | None = Field(None, title="Recovery Key")
    server_port: int = Field(..., ge=1, le=65535, title="Server Port")
    server_portv6: int = Field(..., ge=1, le=65535, title="Server Portv6")
    target_server: str = Field(..., title="Target Server")
    target_version: str | None = Field("LATEST", title="Target Version")


Components = Annotated[
    list[
        Literal[
            "world",
            "server.properties",
            "allowlist.json",
            "permissions.json",
            "script_config",
            "bsm_settings",
            "behavior_packs",
            "resource_packs",
            "development_behavior_packs",
            "development_resource_packs",
        ]
    ],
    Field(min_length=1, title="Components"),
]


class SnapshotCreatePayload(ContractModel):
    """Validate and serialize the SnapshotCreatePayload contract."""

    model_config = ConfigDict(extra="forbid")
    components: Components | None = Field(None, title="Components")
    encrypted: bool | None = Field(None, title="Encrypted")
    mode: Literal["world", "selected", "full"] | None = Field(None, title="Mode")


class SnapshotInspectPayload(ContractModel):
    """Validate and serialize the SnapshotInspectPayload contract."""

    model_config = ConfigDict(extra="forbid")
    recovery_key: SecretStr | None = Field(None, title="Recovery Key")


Label = Annotated[str, Field(max_length=120, title="Label")]
Notes = Annotated[str, Field(max_length=2000, title="Notes")]


class SnapshotManagePayload(ContractModel):
    """Validate and serialize the SnapshotManagePayload contract."""

    model_config = ConfigDict(extra="forbid")
    action: Literal[
        "verify", "pin", "unpin", "copy", "test_key", "annotate", "drill"
    ] = Field(..., title="Action")
    destination: str | None = Field(None, title="Destination")
    label: Label | None = Field(None, title="Label")
    notes: Notes | None = Field(None, title="Notes")
    recovery_key: SecretStr | None = Field(None, title="Recovery Key")


class SnapshotPlanPayload(ContractModel):
    """Validate and serialize the SnapshotPlanPayload contract."""

    model_config = ConfigDict(extra="forbid")
    components: list[
        Literal[
            "server_directory",
            "world",
            "server.properties",
            "allowlist.json",
            "permissions.json",
            "script_config",
            "bsm_settings",
            "behavior_packs",
            "resource_packs",
            "development_behavior_packs",
            "development_resource_packs",
        ]
    ] = Field(..., title="Components")
    recovery_key: SecretStr | None = Field(None, title="Recovery Key")


class SnapshotRestorePayload(ContractModel):
    """Validate and serialize the SnapshotRestorePayload contract."""

    model_config = ConfigDict(extra="forbid")
    components: list[
        Literal[
            "server_directory",
            "world",
            "server.properties",
            "allowlist.json",
            "permissions.json",
            "script_config",
            "bsm_settings",
            "behavior_packs",
            "resource_packs",
            "development_behavior_packs",
            "development_resource_packs",
        ]
    ] = Field(..., title="Components")
    recovery_key: SecretStr | None = Field(None, title="Recovery Key")
    restart: bool | None = Field(True, title="Restart")
    stop_running: bool | None = Field(True, title="Stop Running")
    token: str = Field(..., title="Token")


class StartServerResponse(ContractModel):
    """Validate and serialize the StartServerResponse contract."""

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


class StateDiagnostics(ContractModel):
    """Validate and serialize the StateDiagnostics contract."""

    model_config = ConfigDict(extra="forbid")
    counts: dict[str, int] = Field(..., title="Counts")
    epoch: str = Field(..., title="Epoch")
    kind: Literal["state"] = Field("state", title="Kind")
    observation_revision: int = Field(..., title="Observation Revision")
    oldest_pending_age_seconds: float | None = Field(
        None, title="Oldest Pending Age Seconds"
    )
    pending_changes: dict[str, int] = Field(..., title="Pending Changes")


class StopServerResponse(ContractModel):
    """Validate and serialize the StopServerResponse contract."""

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


class StorageDiagnostics(ContractModel):
    """Validate and serialize the StorageDiagnostics contract."""

    model_config = ConfigDict(extra="forbid")
    active: int | None = Field(0, title="Active")
    attempts: int | None = Field(0, title="Attempts")
    failures: int | None = Field(0, title="Failures")
    kind: Literal["storage"] = Field("storage", title="Kind")
    last_duration_ms: float | None = Field(None, title="Last Duration Ms")
    last_error_type: str | None = Field(None, title="Last Error Type")
    last_reload_at: float | None = Field(None, title="Last Reload At")
    last_reload_duration_ms: float | None = Field(None, title="Last Reload Duration Ms")
    last_reload_error_type: str | None = Field(None, title="Last Reload Error Type")
    last_success_at: float | None = Field(None, title="Last Success At")
    lock_wait_ms: float | None = Field(None, title="Lock Wait Ms")
    lock_waiters: int | None = Field(0, title="Lock Waiters")
    max_lock_wait_ms: float | None = Field(0, title="Max Lock Wait Ms")
    reload_active: bool | None = Field(False, title="Reload Active")
    reload_attempts: int | None = Field(0, title="Reload Attempts")
    reload_failures: int | None = Field(0, title="Reload Failures")
    reload_successes: int | None = Field(0, title="Reload Successes")
    successes: int | None = Field(0, title="Successes")
    total_lock_wait_ms: float | None = Field(0, title="Total Lock Wait Ms")


class Subpack(ContractModel):
    """Validate and serialize the Subpack contract."""

    model_config = ConfigDict(extra="forbid")
    folder_name: str = Field(..., title="Folder Name")
    memory_tier: int | None = Field(None, title="Memory Tier")
    name: str | None = Field(None, title="Name")


class SuccessResponse(ContractModel):
    """Validate and serialize the SuccessResponse contract."""

    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    status: Literal["success"] = Field("success", title="Status")


class TaskAcceptedResponse(ContractModel):
    """Validate and serialize the TaskAcceptedResponse contract."""

    model_config = ConfigDict(extra="forbid")
    message: str = Field(..., title="Message")
    status: Literal["accepted"] = Field("accepted", title="Status")
    task_id: str = Field(..., title="Task Id")


ProgressPercent = Annotated[float, Field(ge=0.0, le=100.0, title="Progress Percent")]


class TaskDiagnostic(ContractModel):
    """Validate and serialize the TaskDiagnostic contract."""

    model_config = ConfigDict(extra="forbid")
    cancellation_requested: bool | None = Field(False, title="Cancellation Requested")
    correlation_id: str | None = Field(None, title="Correlation Id")
    elapsed_seconds: float | None = Field(None, title="Elapsed Seconds")
    error_code: str | None = Field(None, title="Error Code")
    id: str = Field(..., title="Id")
    name: str | None = Field("background_task", title="Name")
    owner: str | None = Field(None, title="Owner")
    progress_percent: ProgressPercent | None = Field(None, title="Progress Percent")
    status: str = Field(..., title="Status")


class TasksDiagnostics(ContractModel):
    """Validate and serialize the TasksDiagnostics contract."""

    model_config = ConfigDict(extra="forbid")
    accepting: bool = Field(..., title="Accepting")
    active: int = Field(..., title="Active")
    capacity: int | None = Field(100, title="Capacity")
    concurrency_limit: int | None = Field(None, title="Concurrency Limit")
    counts_by_status: dict[str, int] = Field(..., title="Counts By Status")
    kind: Literal["tasks"] = Field("tasks", title="Kind")
    oldest_active_seconds: float | None = Field(None, title="Oldest Active Seconds")
    tasks: list[TaskDiagnostic] | None = Field(None, title="Tasks")


class ThemeListResponse(ContractModel):
    """Response model for theme lists."""

    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    status: Literal["success", "skipped", "partial"] = Field(..., title="Status")
    themes: list[str] | None = Field(None, title="Themes")


class ThemeUpdatePayload(ContractModel):
    """Request payload for updating the user's theme.

    :ivar theme: The new theme name."""

    model_config = ConfigDict(extra="forbid")
    theme: str = Field(..., title="Theme")


class TokenResponse(ContractModel):
    """Response model for successful authentication, providing an access token."""

    model_config = ConfigDict(extra="forbid")
    access_token: str = Field(..., title="Access Token")
    message: str | None = Field(None, title="Message")
    token_type: Literal["bearer"] = Field("bearer", title="Token Type")


class TransportDiagnostics(ContractModel):
    """Validate and serialize the TransportDiagnostics contract."""

    model_config = ConfigDict(extra="forbid")
    accepting: bool | None = Field(True, title="Accepting")
    active_sends: int | None = Field(0, title="Active Sends")
    connected_clients: int = Field(..., title="Connected Clients")
    delivery_mode: Literal["direct"] = Field("direct", title="Delivery Mode")
    disconnects_by_reason: dict[str, int] | None = Field(
        None, title="Disconnects By Reason"
    )
    dropped_messages: int | None = Field(0, title="Dropped Messages")
    failed_sends: int | None = Field(0, title="Failed Sends")
    high_water_mark: int | None = Field(0, title="High Water Mark")
    kind: Literal["transport"] = Field("transport", title="Kind")
    last_send_at: float | None = Field(None, title="Last Send At")
    last_send_duration_ms: float | None = Field(None, title="Last Send Duration Ms")
    max_pending_per_client: int | None = Field(0, title="Max Pending Per Client")
    pending_sends: int | None = Field(0, title="Pending Sends")
    queue_limit_per_client: int | None = Field(64, title="Queue Limit Per Client")
    send_timeouts: int | None = Field(0, title="Send Timeouts")
    subscriptions: int = Field(..., title="Subscriptions")
    successful_sends: int | None = Field(0, title="Successful Sends")
    topics: int = Field(..., title="Topics")


class TriggerEventPayload(ContractModel):
    """Request model for triggering a custom plugin event."""

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
    """Response model for triggering a custom plugin event."""

    model_config = ConfigDict(extra="forbid")
    details: dict[str, JsonValue] | None = Field(None, title="Details")
    message: str | None = Field(None, title="Message")
    status: Literal["success", "skipped", "partial"] = Field(..., title="Status")


class UpdateUserRolePayload(ContractModel):
    """Request payload for updating a user's role.

    :ivar role: The new role."""

    model_config = ConfigDict(extra="forbid")
    role: Literal["admin", "moderator", "user"] = Field(..., title="Role")


class UserLoginPayload(ContractModel):
    """Request model for user login credentials."""

    model_config = ConfigDict(extra="forbid")
    password: SecretStr = Field(..., min_length=1, title="Password")
    remember_me: bool | None = Field(False, title="Remember Me")
    username: str = Field(..., max_length=80, min_length=1, title="Username")


class UserResponse(ContractModel):
    """Pydantic model representing a user."""

    model_config = ConfigDict(extra="forbid")
    id: int = Field(..., title="Id")
    identity_type: str | None = Field(None, title="Identity Type")
    is_active: bool = Field(..., title="Is Active")
    role: Literal["admin", "moderator", "user"] = Field(..., title="Role")
    theme: str | None = Field("default", title="Theme")
    username: str = Field(..., title="Username")


class APIErrorResponse(ContractModel):
    """Safe serialized failure; Python callers receive exceptions."""

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
        "unavailable",
        "operation_incomplete",
        "file_error",
        "storage_error",
        "configuration_error",
        "network_error",
        "system_error",
    ] = Field(..., title="Code")
    details: dict[str, JsonValue] | None = Field(None, title="Details")
    message: str = Field(..., title="Message")


class AppInfoResponse(ContractModel):
    """Response model for app/system info."""

    model_config = ConfigDict(extra="forbid")
    info: dict[str, JsonValue] | None = Field(None, title="Info")
    message: str | None = Field(None, title="Message")
    status: Literal["success", "skipped", "partial"] = Field(..., title="Status")


class AuditLogResponse(ContractModel):
    """Validate and serialize the AuditLogResponse contract."""

    model_config = ConfigDict(extra="forbid")
    action: str = Field(..., title="Action")
    details: dict[str, JsonValue] | None = Field(None, title="Details")
    id: int = Field(..., title="Id")
    timestamp: AwareDatetime = Field(..., title="Timestamp")
    user_id: int = Field(..., title="User Id")


class BackupHealth(ContractModel):
    """Validate and serialize the BackupHealth contract."""

    model_config = ConfigDict(extra="forbid")
    alerts: list[dict[str, JsonValue]] | None = Field(None, title="Alerts")
    count: int = Field(..., title="Count")
    destination_failures: int | None = Field(0, title="Destination Failures")
    destinations: dict[str, JsonValue] | None = Field(None, title="Destinations")
    drill: dict[str, JsonValue] | None = Field(None, title="Drill")
    failed_count: int | None = Field(0, title="Failed Count")
    last_error: str | None = Field(None, title="Last Error")
    last_failure_at: str | None = Field(None, title="Last Failure At")
    last_success_at: str | None = Field(None, title="Last Success At")
    last_verified_at: str | None = Field(None, title="Last Verified At")
    missing_key_ids: list[str] | None = Field(None, title="Missing Key Ids")
    older_key_ids: list[str] | None = Field(None, title="Older Key Ids")
    readiness: Literal["ready", "attention", "unavailable"] | None = Field(
        "unavailable", title="Readiness"
    )
    readiness_reasons: list[str] | None = Field(None, title="Readiness Reasons")
    recovery_backup_id: str | None = Field(None, title="Recovery Backup Id")
    schedule: dict[str, JsonValue] | None = Field(None, title="Schedule")
    total_bytes: int = Field(..., title="Total Bytes")
    unverified_count: int | None = Field(0, title="Unverified Count")
    verification_interval_hours: int = Field(..., title="Verification Interval Hours")


class BackupHealthResponse(ContractModel):
    """Validate and serialize the BackupHealthResponse contract."""

    model_config = ConfigDict(extra="forbid")
    health: BackupHealth
    message: str | None = Field(None, title="Message")
    status: Literal["success"] = Field("success", title="Status")


class BackupSummary(ContractModel):
    """Validate and serialize the BackupSummary contract."""

    model_config = ConfigDict(extra="forbid")
    backup_id: str = Field(..., title="Backup Id")
    copies: dict[str, BackupCopy] | None = Field(None, title="Copies")
    created_at: str | None = Field(None, title="Created At")
    drill: dict[str, JsonValue] | None = Field(None, title="Drill")
    encrypted: bool = Field(..., title="Encrypted")
    error: str | None = Field(None, title="Error")
    filename: str = Field(..., title="Filename")
    key_id: str | None = Field(None, title="Key Id")
    label: str | None = Field("", title="Label")
    manifest: BackupManifest | None = None
    notes: str | None = Field("", title="Notes")
    origin: Literal["captured", "imported"] | None = Field("captured", title="Origin")
    pinned: bool | None = Field(False, title="Pinned")
    protected_until: str | None = Field(None, title="Protected Until")
    purpose: str | None = Field(None, title="Purpose")
    size: int = Field(..., title="Size")
    stage_durations_ms: dict[str, float] | None = Field(
        None, title="Stage Durations Ms"
    )
    verification: BackupVerification | None = None


class DiagnosticFinding(ContractModel):
    """Validate and serialize the DiagnosticFinding contract."""

    model_config = ConfigDict(extra="forbid")
    issue: DiagnosticIssue
    owner: str = Field(..., title="Owner")
    subsystem: str = Field(..., title="Subsystem")


class DiagnosticHistory(ContractModel):
    """Validate and serialize the DiagnosticHistory contract."""

    model_config = ConfigDict(extra="forbid")
    available: bool = Field(..., title="Available")
    next_cursor: str | None = Field(None, title="Next Cursor")
    records: list[DiagnosticRecord] = Field(..., title="Records")
    truncated: bool = Field(..., title="Truncated")


class DiagnosticSummary(ContractModel):
    """Validate and serialize the DiagnosticSummary contract."""

    model_config = ConfigDict(extra="forbid")
    counts_by_status: dict[str, int] = Field(..., title="Counts By Status")
    findings: list[DiagnosticFinding] | None = Field(
        None, max_length=100, title="Findings"
    )
    ready: bool | None = Field(..., title="Ready")
    status: Literal["ok", "degraded", "unavailable", "unknown"] = Field(
        ..., title="Status"
    )
    truncated: bool | None = Field(False, title="Truncated")


class ErrorEnvelope(ContractModel):
    """Validate and serialize the ErrorEnvelope contract."""

    model_config = ConfigDict(extra="forbid")
    error: APIErrorResponse


class EventDefinition(ContractModel):
    """Validate and serialize the EventDefinition contract."""

    model_config = ConfigDict(extra="forbid")
    description: str | None = Field("", title="Description")
    identity_keys: list[str] | None = Field([], title="Identity Keys")
    name: str = Field(
        ...,
        max_length=160,
        min_length=1,
        pattern="^[a-zA-Z0-9_][a-zA-Z0-9_.:-]*$",
        title="Name",
    )
    owner: str | None = Field("application", title="Owner")
    payload_schema: dict[str, JsonValue] | None = Field(None, title="Payload Schema")
    phase: Literal["before", "after", "custom", "lifecycle"] | None = Field(
        "custom", title="Phase"
    )
    public: bool | None = Field(True, title="Public")


class EventRecord(ContractModel):
    """Validate and serialize the EventRecord contract."""

    model_config = ConfigDict(extra="forbid")
    cancellation_reason: str | None = Field(None, title="Cancellation Reason")
    correlation_id: str = Field(..., title="Correlation Id")
    deliveries: list[EventDelivery] | None = Field(None, title="Deliveries")
    duration_ms: float | None = Field(0, title="Duration Ms")
    event_id: str = Field(..., title="Event Id")
    failures: list[ListenerFailure] | None = Field(None, title="Failures")
    listeners: list[ListenerRecord] | None = Field(None, title="Listeners")
    listeners_called: int | None = Field(0, title="Listeners Called")
    name: str = Field(..., title="Name")
    operation_id: str | None = Field(None, title="Operation Id")
    operation_name: str | None = Field(None, title="Operation Name")
    parent_event_id: str | None = Field(None, title="Parent Event Id")
    phase: Literal["before", "after", "custom", "lifecycle"] | None = Field(
        "custom", title="Phase"
    )
    rejection_reason: (
        Literal["recursion", "depth_limit", "capacity", "shutdown"] | None
    ) = Field(None, title="Rejection Reason")
    sequence_id: str | None = Field(None, title="Sequence Id")
    server_name: str | None = Field(None, title="Server Name")
    source: str = Field(..., title="Source")
    status: Literal[
        "dispatching", "completed", "partial", "cancelled", "suppressed"
    ] = Field(..., title="Status")
    timestamp: float = Field(..., title="Timestamp")


class FailureInfo(ContractModel):
    """Validate and serialize the FailureInfo contract."""

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
        "unavailable",
        "operation_incomplete",
        "file_error",
        "storage_error",
        "configuration_error",
        "network_error",
        "system_error",
    ] = Field(..., title="Code")
    details: dict[str, JsonValue] | None = Field(None, title="Details")
    message: str = Field(..., title="Message")


class GetApplicationHealthResponse(ContractModel):
    """Validate and serialize the GetApplicationHealthResponse contract."""

    model_config = ConfigDict(extra="forbid")
    checked_at: float = Field(..., gt=0.0, title="Checked At")
    checks: dict[str, HealthCheck] = Field(..., title="Checks")
    health: Literal["healthy", "degraded"] = Field(..., title="Health")
    instance_id: str | None = Field(None, title="Instance Id")
    lifecycle: Literal["starting", "ready", "stopping", "stopped", "failed"] = Field(
        ..., title="LifecyclePhase"
    )
    message: str | None = Field(None, title="Message")
    pid: int = Field(..., gt=0, title="Pid")
    ready: bool = Field(..., title="Ready")
    status: Literal["success"] = Field("success", title="Status")
    version: str = Field(..., title="Version")


class GetPermissionsResponse(ContractModel):
    """Validate and serialize the GetPermissionsResponse contract."""

    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    permissions: list[PlayerPermission] = Field(..., title="Permissions")
    status: Literal["success"] = Field("success", title="Status")


class GetPluginSettingsResponse(ContractModel):
    """Validate and serialize the GetPluginSettingsResponse contract."""

    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    settings: dict[str, JsonValue] = Field(..., title="Settings")
    settings_schema: dict[str, JsonValue] | None = Field(None, title="Settings Schema")
    status: Literal["success"] = Field("success", title="Status")


class InstalledAddon(ContractModel):
    """Validate and serialize the InstalledAddon contract."""

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
    """Validate and serialize the InstalledAddons contract."""

    model_config = ConfigDict(extra="forbid")
    behavior_packs: list[InstalledAddon] | None = Field(None, title="Behavior Packs")
    resource_packs: list[InstalledAddon] | None = Field(None, title="Resource Packs")


class ListSnapshotsResponse(ContractModel):
    """Validate and serialize the ListSnapshotsResponse contract."""

    model_config = ConfigDict(extra="forbid")
    backups: list[BackupSummary] = Field(..., title="Backups")
    message: str | None = Field(None, title="Message")
    status: Literal["success"] = Field("success", title="Status")


class MetricsSample(ContractModel):
    """Validate and serialize the MetricsSample contract."""

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


class OperationActivity(ContractModel):
    """Bounded, metadata-only global activity; recent results are not durable."""

    model_config = ConfigDict(extra="forbid")
    active: list[OperationSnapshot] | None = Field(None, title="Active")
    active_operations: int | None = Field(0, title="Active Operations")
    active_sequences: int | None = Field(0, title="Active Sequences")
    active_truncated: bool | None = Field(False, title="Active Truncated")
    completed: int | None = Field(0, title="Completed")
    history_limit: int | None = Field(0, title="History Limit")
    recent: list[OperationSnapshot] | None = Field(None, title="Recent")
    recent_truncated: bool | None = Field(False, title="Recent Truncated")


class PermissionsSetPayload(ContractModel):
    """Request model for setting multiple player permissions."""

    model_config = ConfigDict(extra="forbid")
    permissions: list[PlayerPermissionPayload] = Field(
        ..., description="List of player permission entries.", title="Permissions"
    )


class PlayerScanError(ContractModel):
    """Validate and serialize the PlayerScanError contract."""

    model_config = ConfigDict(extra="forbid")
    error: FailureInfo
    server: str = Field(..., title="Server")


class PruneDownloadsResponse(ContractModel):
    """Response model for pruning downloads."""

    model_config = ConfigDict(extra="forbid")
    failures: dict[str, FailureInfo] | None = Field(None, title="Failures")
    files_deleted: int | None = Field(None, title="Files Deleted")
    files_kept: int | None = Field(None, title="Files Kept")
    message: str | None = Field(None, title="Message")
    status: Literal["success", "skipped", "partial"] = Field(..., title="Status")


class RecoveryReportReview(ContractModel):
    """Validate and serialize the RecoveryReportReview contract."""

    model_config = ConfigDict(extra="forbid")
    archive_reference: str = Field(..., title="Archive Reference")
    change_counts: dict[str, int] = Field(..., title="Change Counts")
    checked_files: int = Field(..., title="Checked Files")
    components: list[
        Literal[
            "server_directory",
            "world",
            "server.properties",
            "allowlist.json",
            "permissions.json",
            "script_config",
            "bsm_settings",
            "behavior_packs",
            "resource_packs",
            "development_behavior_packs",
            "development_resource_packs",
        ]
    ] = Field(..., title="Components")
    dry_run: bool = Field(..., title="Dry Run")
    recorded_at: str = Field(..., title="Recorded At")
    sufficient_space: bool = Field(..., title="Sufficient Space")
    volumes: list[RestoreVolume] = Field(..., title="Volumes")


class ResourceFailure(ContractModel):
    """Validate and serialize the ResourceFailure contract."""

    model_config = ConfigDict(extra="forbid")
    error: FailureInfo
    resource: str = Field(..., title="Resource")


class RestoreRecoveryResponse(ContractModel):
    """Validate and serialize the RestoreRecoveryResponse contract."""

    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    recovery: RestoreRecoveryState
    status: Literal["success"] = Field("success", title="Status")


class ScheduleEntry(ContractModel):
    """Validate and serialize the ScheduleEntry contract."""

    model_config = ConfigDict(extra="forbid")
    attempts: int | None = Field(0, title="Attempts")
    available: bool = Field(..., title="Available")
    configuration: ScheduledTask
    last_error: str | None = Field(None, title="Last Error")
    last_status: str | None = Field(None, title="Last Status")
    last_success_at: str | None = Field(None, title="Last Success At")
    legacy: bool | None = Field(False, title="Legacy")
    next_run_at: str | None = Field(None, title="Next Run At")
    runs: list[dict[str, JsonValue]] | None = Field(None, title="Runs")
    schedule_id: str = Field(..., title="Schedule Id")


class ServersListResponse(ContractModel):
    """Validate and serialize the ServersListResponse contract."""

    model_config = ConfigDict(extra="forbid")
    epoch: str | None = Field(None, title="Epoch")
    errors: list[ResourceFailure] | None = Field(None, title="Errors")
    message: str | None = Field(None, title="Message")
    revision: Revision | None = Field(None, title="Revision")
    servers: list[ServerSummary] | None = Field(None, title="Servers")
    status: Literal["success", "skipped", "partial"] = Field(..., title="Status")


class TaskSnapshot(ContractModel):
    """Validate and serialize the TaskSnapshot contract."""

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


class AddonListResponse(ContractModel):
    """Response model for retrieving all addons on a server."""

    model_config = ConfigDict(extra="forbid")
    addons: InstalledAddons | None = None
    message: str | None = Field(None, title="Message")
    status: Literal["success", "skipped", "partial"] = Field(..., title="Status")


class EventCatalog(ContractModel):
    """Validate and serialize the EventCatalog contract."""

    model_config = ConfigDict(extra="forbid")
    events: list[EventDefinition] = Field(..., title="Events")


class EventDiagnostics(ContractModel):
    """Validate and serialize the EventDiagnostics contract."""

    model_config = ConfigDict(extra="forbid")
    accepting: bool = Field(..., title="Accepting")
    active: list[EventRecord] = Field(..., title="Active")
    active_dispatches: int | None = Field(0, title="Active Dispatches")
    active_listeners_by_owner: dict[str, int] | None = Field(
        None, title="Active Listeners By Owner"
    )
    active_truncated: bool | None = Field(False, title="Active Truncated")
    emitted: int = Field(..., title="Emitted")
    failed_listeners: int = Field(..., title="Failed Listeners")
    notification_delivery: Literal["inline"] = Field(
        "inline", title="Notification Delivery"
    )
    pending_waits: int | None = Field(0, title="Pending Waits")
    pending_workers: int | None = Field(0, title="Pending Workers")
    recent: list[EventRecord] = Field(..., title="Recent")
    recent_truncated: bool | None = Field(False, title="Recent Truncated")
    rejections_by_reason: dict[str, int] | None = Field(
        None, title="Rejections By Reason"
    )
    subscriptions: int = Field(..., title="Subscriptions")
    subscriptions_by_owner: dict[str, int] | None = Field(
        None, title="Subscriptions By Owner"
    )
    suppressed: int = Field(..., title="Suppressed")
    timeouts_by_owner: dict[str, int] | None = Field(None, title="Timeouts By Owner")
    workers_by_owner: dict[str, int] | None = Field(None, title="Workers By Owner")


class EventsDiagnostics(ContractModel):
    """Validate and serialize the EventsDiagnostics contract."""

    model_config = ConfigDict(extra="forbid")
    activity: EventDiagnostics
    capacity: EventOptions
    kind: Literal["events"] = Field("events", title="Kind")
    operations: OperationActivity | None = None
    subscriptions: EventSubscriptions | None = None
    truncated: bool | None = Field(False, title="Truncated")


class FailedItem(ContractModel):
    """Validate and serialize the FailedItem contract."""

    model_config = ConfigDict(extra="forbid")
    error: FailureInfo
    outcome: Literal["failed"] = Field("failed", title="Outcome")
    path: None = Field(None, title="Path")
    reason: str | None = Field(None, title="Reason")


class GetApplicationMetricsResponse(ContractModel):
    """Validate and serialize the GetApplicationMetricsResponse contract."""

    model_config = ConfigDict(extra="forbid")
    epoch: str | None = Field(None, title="Epoch")
    history: list[MetricsSample] = Field(..., title="History")
    history_limit: int = Field(..., gt=0, le=180, title="History Limit")
    interval_seconds: float = Field(..., gt=0.0, title="Interval Seconds")
    latest: MetricsSample
    message: str | None = Field(None, title="Message")
    revision: Revision | None = Field(None, title="Revision")
    status: Literal["success"] = Field("success", title="Status")


class ListSchedulesResponse(ContractModel):
    """Validate and serialize the ListSchedulesResponse contract."""

    model_config = ConfigDict(extra="forbid")
    host_timezone: str | None = Field(None, title="Host Timezone")
    schedules: list[ScheduleEntry] | None = Field(None, title="Schedules")
    server_time: str | None = Field(None, title="Server Time")
    task_types: list[str] | None = Field(None, title="Task Types")
    timezone_database_available: bool | None = Field(
        True, title="Timezone Database Available"
    )
    timezones: list[str] | None = Field(None, title="Timezones")


class PermissionsUpdateResponse(ContractModel):
    """Validate and serialize the PermissionsUpdateResponse contract."""

    model_config = ConfigDict(extra="forbid")
    errors: dict[str, str] | None = Field(None, title="Errors")
    message: str | None = Field(None, title="Message")
    outcomes: dict[str, CompletedItem | SkippedItem | FailedItem] | None = Field(
        None, title="Outcomes"
    )
    status: Literal["success", "skipped", "partial"] = Field(..., title="Status")
    updated: int | None = Field(0, ge=0, title="Updated")


class PlayerScanDetails(ContractModel):
    """Validate and serialize the PlayerScanDetails contract."""

    model_config = ConfigDict(extra="forbid")
    actually_saved_or_updated_in_db: int = Field(
        ..., ge=0, title="Actually Saved Or Updated In Db"
    )
    scan_errors: list[PlayerScanError] | None = Field(None, title="Scan Errors")
    total_entries_in_logs: int = Field(..., ge=0, title="Total Entries In Logs")
    unique_players_submitted_for_saving: int = Field(
        ..., ge=0, title="Unique Players Submitted For Saving"
    )


class RecoveryReport(ContractModel):
    """Validate and serialize the RecoveryReport contract."""

    model_config = ConfigDict(extra="forbid")
    archive_count: int = Field(..., title="Archive Count")
    archives: list[RecoveryReportArchive] = Field(..., title="Archives")
    archives_omitted: int = Field(..., title="Archives Omitted")
    destination_failures: int = Field(..., title="Destination Failures")
    generated_at: str = Field(..., title="Generated At")
    last_drill: RecoveryReportDrill | None = None
    last_restore: RecoveryReportOutcome | None = None
    last_review: RecoveryReportReview | None = None
    missing_key_count: int = Field(..., title="Missing Key Count")
    readiness: Literal["ready", "attention", "unavailable"] = Field(
        ..., title="Readiness"
    )
    recovery_pending: bool = Field(..., title="Recovery Pending")
    report_version: Literal[1] = Field(1, title="Report Version")


class RecoveryReportResponse(ContractModel):
    """Validate and serialize the RecoveryReportResponse contract."""

    model_config = ConfigDict(extra="forbid")
    message: str | None = Field(None, title="Message")
    report: RecoveryReport
    status: Literal["success"] = Field("success", title="Status")


class AddPlayersResponse(ContractModel):
    """Validate and serialize the AddPlayersResponse contract."""

    model_config = ConfigDict(extra="forbid")
    count: int | None = Field(None, title="Count")
    details: PlayerScanDetails | None = None
    message: str | None = Field(None, title="Message")
    parsed_count: ParsedCount | None = Field(None, title="Parsed Count")
    status: Literal["success", "skipped", "partial"] = Field(..., title="Status")
    submitted_count: SubmittedCount | None = Field(None, title="Submitted Count")
    unique_count: UniqueCount | None = Field(None, title="Unique Count")


class DiagnosticActivity(ContractModel):
    """Global current-instance metadata; no correlation filter is required."""

    model_config = ConfigDict(extra="forbid")
    events: EventDiagnostics | None = None
    issues: list[DiagnosticIssue] | None = Field(None, max_length=3, title="Issues")
    operations: OperationActivity | None = None
    scope: Literal["application"] = Field("application", title="Scope")
    subscriptions: EventSubscriptions | None = None
    truncated: bool | None = Field(False, title="Truncated")


class DiagnosticSection(ContractModel):
    """Validate and serialize the DiagnosticSection contract."""

    model_config = ConfigDict(extra="forbid")
    age_seconds: float | None = Field(None, title="Age Seconds")
    collected_at: float = Field(..., title="Collected At")
    data: (
        RuntimeDiagnostics
        | StateDiagnostics
        | StorageDiagnostics
        | EventsDiagnostics
        | TransportDiagnostics
        | PluginsDiagnostics
        | TasksDiagnostics
        | ProcessesDiagnostics
        | MetricsDiagnostics
        | PluginValues
        | BackupsDiagnostics
        | None
    ) = Field(None, title="Data")
    duration_ms: float | None = Field(0, title="Duration Ms")
    issues: list[DiagnosticIssue] | None = Field(None, max_length=20, title="Issues")
    last_success_at: float | None = Field(None, title="Last Success At")
    name: str = Field(..., title="Name")
    observed_at: float | None = Field(None, title="Observed At")
    owner: str | None = Field("application", title="Owner")
    stale: bool | None = Field(False, title="Stale")
    status: Literal["ok", "degraded", "unavailable", "unknown"] | None = Field(
        "unknown", title="Status"
    )


class DiagnosticSnapshot(ContractModel):
    """Validate and serialize the DiagnosticSnapshot contract."""

    model_config = ConfigDict(extra="forbid")
    collected_at: float = Field(..., title="Collected At")
    collection: CollectionDiagnostics | None = None
    counter_scope: Literal["current_instance"] = Field(
        "current_instance", title="Counter Scope"
    )
    environment: DiagnosticEnvironment
    instance_id: str = Field(..., title="Instance Id")
    persistence: PersistenceDiagnostics
    recent: RecentDiagnosticWindow | None = None
    registry: RegistryDiagnostics
    schema_version: Literal[1] = Field(1, title="Schema Version")
    sections: list[DiagnosticSection] = Field(..., max_length=1000, title="Sections")
    snapshot_id: str | None = Field(None, title="Snapshot Id")
    summary: DiagnosticSummary


class DiagnosticTrace(ContractModel):
    """Validate and serialize the DiagnosticTrace contract."""

    model_config = ConfigDict(extra="forbid")
    correlation_id: str = Field(..., title="Correlation Id")
    events: EventDiagnostics | None
    events_available: bool | None = Field(False, title="Events Available")
    history: DiagnosticHistory
    issues: list[DiagnosticIssue] | None = Field(None, max_length=4, title="Issues")
    operations: OperationActivity | None = None
    operations_available: bool | None = Field(False, title="Operations Available")
    tasks: list[TaskDiagnostic] = Field(..., title="Tasks")
    tasks_available: bool = Field(..., title="Tasks Available")
    truncated: bool | None = Field(False, title="Truncated")


class CompareDiagnosticSnapshotsRequest(ContractModel):
    """Validate and serialize the CompareDiagnosticSnapshotsRequest contract."""

    model_config = ConfigDict(extra="forbid")
    after: DiagnosticSnapshot
    before: DiagnosticSnapshot


class DiagnosticReport(ContractModel):
    """Validate and serialize the DiagnosticReport contract."""

    model_config = ConfigDict(extra="forbid")
    generated_at: float | None = Field(None, title="Generated At")
    history: DiagnosticHistory
    report_id: str | None = Field(None, title="Report Id")
    runs: DiagnosticRuns | None = None
    snapshot: DiagnosticSnapshot
