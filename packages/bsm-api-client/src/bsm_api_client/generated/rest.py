"""Typed REST interface generated from the bundled OpenAPI contract."""

from .models.access_policy_info import AccessPolicyInfo
from .models.access_server_info import AccessServerInfo
from .models.account_server_access_info import AccountServerAccessInfo
from .models.action_response import ActionResponse
from .models.add_players_payload import AddPlayersPayload
from .models.add_players_response import AddPlayersResponse
from .models.add_server_ban_response import AddServerBanResponse
from .models.add_to_allowlist_response import AddToAllowlistResponse
from .models.addon_action_payload import AddonActionPayload
from .models.addon_list_response import AddonListResponse
from .models.addon_reorder_payload import AddonReorderPayload
from .models.addon_subpack_payload import AddonSubpackPayload
from .models.allowlist_add_payload import AllowlistAddPayload
from .models.allowlist_remove_payload import AllowlistRemovePayload
from .models.app_info_response import AppInfoResponse
from .models.audit_log_response import AuditLogResponse
from .models.backup_action_payload import BackupActionPayload
from .models.backup_files_response import BackupFilesResponse
from .models.backup_health_response import BackupHealthResponse
from .models.ban_add_request import BanAddRequest
from .models.ban_remove_request import BanRemoveRequest
from .models.base_api_response import BaseApiResponse
from .models.body_import_server_snapshot import BodyImportServerSnapshot
from .models.body_login import BodyLogin
from .models.change_password_payload import ChangePasswordPayload
from .models.command_payload import CommandPayload
from .models.compare_diagnostic_snapshots_request import CompareDiagnosticSnapshotsRequest
from .models.content_list_response import ContentListResponse
from .models.control_schedule_payload import ControlSchedulePayload
from .models.create_integration_token import CreateIntegrationToken
from .models.created_integration_token import CreatedIntegrationToken
from .models.current_account_response import CurrentAccountResponse
from .models.custom_zips_response import CustomZipsResponse
from .models.destination_cleanup_payload import DestinationCleanupPayload
from .models.diagnostic_activity import DiagnosticActivity
from .models.diagnostic_comparison import DiagnosticComparison
from .models.diagnostic_history import DiagnosticHistory
from .models.diagnostic_report import DiagnosticReport
from .models.diagnostic_runs import DiagnosticRuns
from .models.diagnostic_snapshot import DiagnosticSnapshot
from .models.diagnostic_trace import DiagnosticTrace
from .models.error_envelope import ErrorEnvelope
from .models.event_catalog import EventCatalog
from .models.event_diagnostics import EventDiagnostics
from .models.factor_code import FactorCode
from .models.factor_enrollment import FactorEnrollment
from .models.file_name_payload import FileNamePayload
from .models.generate_token_payload import GenerateTokenPayload
from .models.get_allowlist_response import GetAllowlistResponse
from .models.get_application_health_response import GetApplicationHealthResponse
from .models.get_application_metrics_response import GetApplicationMetricsResponse
from .models.get_diagnostic_activity_phase_type_0 import GetDiagnosticActivityPhaseType0
from .models.get_diagnostic_activity_status_type_0 import GetDiagnosticActivityStatusType0
from .models.get_diagnostic_history_outcome_type_0 import GetDiagnosticHistoryOutcomeType0
from .models.get_event_activity_phase_type_0 import GetEventActivityPhaseType0
from .models.get_event_activity_status_type_0 import GetEventActivityStatusType0
from .models.get_permissions_response import GetPermissionsResponse
from .models.get_plugin_settings_response import GetPluginSettingsResponse
from .models.get_plugin_settings_scope import GetPluginSettingsScope
from .models.get_properties_response import GetPropertiesResponse
from .models.get_raw_properties_response import GetRawPropertiesResponse
from .models.get_server_bans_response import GetServerBansResponse
from .models.install_confirmation_response import InstallConfirmationResponse
from .models.install_server_payload import InstallServerPayload
from .models.installation_accepted_response import InstallationAcceptedResponse
from .models.integration_token_info import IntegrationTokenInfo
from .models.list_available_addons_response import ListAvailableAddonsResponse
from .models.list_backup_keys_response_list_backup_keys import ListBackupKeysResponseListBackupKeys
from .models.list_schedules_response import ListSchedulesResponse
from .models.list_snapshots_response import ListSnapshotsResponse
from .models.log_history_page import LogHistoryPage
from .models.login_session_info import LoginSessionInfo
from .models.permissions_set_payload import PermissionsSetPayload
from .models.permissions_update_response import PermissionsUpdateResponse
from .models.player_list_response import PlayerListResponse
from .models.plugin_pages_response import PluginPagesResponse
from .models.plugin_settings_payload import PluginSettingsPayload
from .models.plugin_status_set_payload import PluginStatusSetPayload
from .models.plugin_statuses_response import PluginStatusesResponse
from .models.profile_update_payload import ProfileUpdatePayload
from .models.properties_payload import PropertiesPayload
from .models.prune_downloads_payload import PruneDownloadsPayload
from .models.prune_downloads_response import PruneDownloadsResponse
from .models.recovery_codes import RecoveryCodes
from .models.recovery_report_response import RecoveryReportResponse
from .models.registration_response import RegistrationResponse
from .models.remove_from_allowlist_response import RemoveFromAllowlistResponse
from .models.remove_server_ban_response import RemoveServerBanResponse
from .models.rename_session import RenameSession
from .models.restart_server_response import RestartServerResponse
from .models.restore_action_payload import RestoreActionPayload
from .models.restore_recovery_response import RestoreRecoveryResponse
from .models.revoke_sessions import RevokeSessions
from .models.rotate_backup_key_response_rotate_backup_key import RotateBackupKeyResponseRotateBackupKey
from .models.runtime_status import RuntimeStatus
from .models.scheduled_task import ScheduledTask
from .models.security_event_info import SecurityEventInfo
from .models.security_status import SecurityStatus
from .models.send_command_response import SendCommandResponse
from .models.server_process_info_response import ServerProcessInfoResponse
from .models.server_running_status_response import ServerRunningStatusResponse
from .models.server_setting_item_payload import ServerSettingItemPayload
from .models.server_settings_response import ServerSettingsResponse
from .models.server_summary import ServerSummary
from .models.servers_list_response import ServersListResponse
from .models.set_plugin_setting_response import SetPluginSettingResponse
from .models.set_properties_response import SetPropertiesResponse
from .models.set_server_access import SetServerAccess
from .models.setting_item_payload import SettingItemPayload
from .models.settings_response import SettingsResponse
from .models.setup_account_response import SetupAccountResponse
from .models.setup_status_response import SetupStatusResponse
from .models.shutdown_request import ShutdownRequest
from .models.shutdown_response import ShutdownResponse
from .models.snapshot_copy_payload import SnapshotCopyPayload
from .models.snapshot_create_payload import SnapshotCreatePayload
from .models.snapshot_inspect_payload import SnapshotInspectPayload
from .models.snapshot_manage_payload import SnapshotManagePayload
from .models.snapshot_plan_payload import SnapshotPlanPayload
from .models.snapshot_restore_payload import SnapshotRestorePayload
from .models.start_server_response import StartServerResponse
from .models.stop_server_response import StopServerResponse
from .models.success_response import SuccessResponse
from .models.task_accepted_response import TaskAcceptedResponse
from .models.task_snapshot import TaskSnapshot
from .models.theme_list_response import ThemeListResponse
from .models.theme_update_payload import ThemeUpdatePayload
from .models.token_response import TokenResponse
from .models.trigger_event_payload import TriggerEventPayload
from .models.trigger_event_response import TriggerEventResponse
from .models.update_user_role_payload import UpdateUserRolePayload
from .models.user_login_payload import UserLoginPayload
from .models.user_response import UserResponse
from .models.verified_security import VerifiedSecurity
from .models.verify_security import VerifySecurity
from .types import File, Response, UNSET, Unset
from http import HTTPStatus
from typing import Any, cast
from typing import cast

class RestClient:

    def __init__(self, owner: Any):
        self._owner = owner

    async def add_allowlist_players(self, server_name: str, *, body: AllowlistAddPayload) -> AddToAllowlistResponse | ErrorEnvelope | None:
        """Generated add_allowlist_players operation."""
        return cast(AddToAllowlistResponse | ErrorEnvelope | None, await self._owner.async_call_generated('add_allowlist_players', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def add_allowlist_players_detailed(self, server_name: str, *, body: AllowlistAddPayload) -> Response[AddToAllowlistResponse | ErrorEnvelope]:
        """Generated add_allowlist_players operation."""
        return cast(Response[AddToAllowlistResponse | ErrorEnvelope], await self._owner.async_call_generated('add_allowlist_players', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

    async def add_players(self, *, body: AddPlayersPayload) -> AddPlayersResponse | ErrorEnvelope | None:
        """Generated add_players operation."""
        return cast(AddPlayersResponse | ErrorEnvelope | None, await self._owner.async_call_generated('add_players', parameters={}, body=body, authenticated=True, typed=True))

    async def add_players_detailed(self, *, body: AddPlayersPayload) -> Response[AddPlayersResponse | ErrorEnvelope]:
        """Generated add_players operation."""
        return cast(Response[AddPlayersResponse | ErrorEnvelope], await self._owner.async_call_generated('add_players', parameters={}, body=body, authenticated=True, detailed=True))

    async def add_server_ban(self, server_name: str, *, body: BanAddRequest) -> AddServerBanResponse | ErrorEnvelope | None:
        """Generated add_server_ban operation."""
        return cast(AddServerBanResponse | ErrorEnvelope | None, await self._owner.async_call_generated('add_server_ban', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def add_server_ban_detailed(self, server_name: str, *, body: BanAddRequest) -> Response[AddServerBanResponse | ErrorEnvelope]:
        """Generated add_server_ban operation."""
        return cast(Response[AddServerBanResponse | ErrorEnvelope], await self._owner.async_call_generated('add_server_ban', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

    async def change_password(self, *, body: ChangePasswordPayload) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated change_password operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('change_password', parameters={}, body=body, authenticated=True, typed=True))

    async def change_password_detailed(self, *, body: ChangePasswordPayload) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated change_password operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('change_password', parameters={}, body=body, authenticated=True, detailed=True))

    async def cleanup_backup_destination(self, server_name: str, destination: str, *, body: DestinationCleanupPayload) -> ErrorEnvelope | TaskAcceptedResponse | None:
        """Generated cleanup_backup_destination operation."""
        return cast(ErrorEnvelope | TaskAcceptedResponse | None, await self._owner.async_call_generated('cleanup_backup_destination', parameters={'server_name': server_name, 'destination': destination}, body=body, authenticated=True, typed=True))

    async def cleanup_backup_destination_detailed(self, server_name: str, destination: str, *, body: DestinationCleanupPayload) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
        """Generated cleanup_backup_destination operation."""
        return cast(Response[ErrorEnvelope | TaskAcceptedResponse], await self._owner.async_call_generated('cleanup_backup_destination', parameters={'server_name': server_name, 'destination': destination}, body=body, authenticated=True, detailed=True))

    async def compare_diagnostic_snapshots(self, *, body: CompareDiagnosticSnapshotsRequest) -> DiagnosticComparison | ErrorEnvelope | None:
        """Generated compare_diagnostic_snapshots operation."""
        return cast(DiagnosticComparison | ErrorEnvelope | None, await self._owner.async_call_generated('compare_diagnostic_snapshots', parameters={}, body=body, authenticated=True, typed=True))

    async def compare_diagnostic_snapshots_detailed(self, *, body: CompareDiagnosticSnapshotsRequest) -> Response[DiagnosticComparison | ErrorEnvelope]:
        """Generated compare_diagnostic_snapshots operation."""
        return cast(Response[DiagnosticComparison | ErrorEnvelope], await self._owner.async_call_generated('compare_diagnostic_snapshots', parameters={}, body=body, authenticated=True, detailed=True))

    async def confirm_account_mfa(self, *, body: FactorCode) -> ErrorEnvelope | RecoveryCodes | None:
        """Generated confirm_account_mfa operation."""
        return cast(ErrorEnvelope | RecoveryCodes | None, await self._owner.async_call_generated('confirm_account_mfa', parameters={}, body=body, authenticated=True, typed=True))

    async def confirm_account_mfa_detailed(self, *, body: FactorCode) -> Response[ErrorEnvelope | RecoveryCodes]:
        """Generated confirm_account_mfa operation."""
        return cast(Response[ErrorEnvelope | RecoveryCodes], await self._owner.async_call_generated('confirm_account_mfa', parameters={}, body=body, authenticated=True, detailed=True))

    async def control_schedule(self, schedule_id: str, *, body: ControlSchedulePayload) -> ErrorEnvelope | SuccessResponse | None:
        """Generated control_schedule operation."""
        return cast(ErrorEnvelope | SuccessResponse | None, await self._owner.async_call_generated('control_schedule', parameters={'schedule_id': schedule_id}, body=body, authenticated=True, typed=True))

    async def control_schedule_detailed(self, schedule_id: str, *, body: ControlSchedulePayload) -> Response[ErrorEnvelope | SuccessResponse]:
        """Generated control_schedule operation."""
        return cast(Response[ErrorEnvelope | SuccessResponse], await self._owner.async_call_generated('control_schedule', parameters={'schedule_id': schedule_id}, body=body, authenticated=True, detailed=True))

    async def create_backup(self, server_name: str, *, body: BackupActionPayload) -> ErrorEnvelope | TaskAcceptedResponse | None:
        """Generated create_backup operation."""
        return cast(ErrorEnvelope | TaskAcceptedResponse | None, await self._owner.async_call_generated('create_backup', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def create_backup_detailed(self, server_name: str, *, body: BackupActionPayload) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
        """Generated create_backup operation."""
        return cast(Response[ErrorEnvelope | TaskAcceptedResponse], await self._owner.async_call_generated('create_backup', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

    async def create_first_user(self, *, body: UserLoginPayload) -> ErrorEnvelope | SetupAccountResponse | None:
        """Generated create_first_user operation."""
        return cast(ErrorEnvelope | SetupAccountResponse | None, await self._owner.async_call_generated('create_first_user', parameters={}, body=body, authenticated=False, typed=True))

    async def create_first_user_detailed(self, *, body: UserLoginPayload) -> Response[ErrorEnvelope | SetupAccountResponse]:
        """Generated create_first_user operation."""
        return cast(Response[ErrorEnvelope | SetupAccountResponse], await self._owner.async_call_generated('create_first_user', parameters={}, body=body, authenticated=False, detailed=True))

    async def create_integration_token(self, *, body: CreateIntegrationToken) -> CreatedIntegrationToken | ErrorEnvelope | None:
        """Generated create_integration_token operation."""
        return cast(CreatedIntegrationToken | ErrorEnvelope | None, await self._owner.async_call_generated('create_integration_token', parameters={}, body=body, authenticated=True, typed=True))

    async def create_integration_token_detailed(self, *, body: CreateIntegrationToken) -> Response[CreatedIntegrationToken | ErrorEnvelope]:
        """Generated create_integration_token operation."""
        return cast(Response[CreatedIntegrationToken | ErrorEnvelope], await self._owner.async_call_generated('create_integration_token', parameters={}, body=body, authenticated=True, detailed=True))

    async def create_server_snapshot(self, server_name: str, *, body: SnapshotCreatePayload) -> ErrorEnvelope | TaskAcceptedResponse | None:
        """Generated create_server_snapshot operation."""
        return cast(ErrorEnvelope | TaskAcceptedResponse | None, await self._owner.async_call_generated('create_server_snapshot', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def create_server_snapshot_detailed(self, server_name: str, *, body: SnapshotCreatePayload) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
        """Generated create_server_snapshot operation."""
        return cast(Response[ErrorEnvelope | TaskAcceptedResponse], await self._owner.async_call_generated('create_server_snapshot', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

    async def delete_schedule(self, schedule_id: str) -> ErrorEnvelope | SuccessResponse | None:
        """Generated delete_schedule operation."""
        return cast(ErrorEnvelope | SuccessResponse | None, await self._owner.async_call_generated('delete_schedule', parameters={'schedule_id': schedule_id}, body=None, authenticated=True, typed=True))

    async def delete_schedule_detailed(self, schedule_id: str) -> Response[ErrorEnvelope | SuccessResponse]:
        """Generated delete_schedule operation."""
        return cast(Response[ErrorEnvelope | SuccessResponse], await self._owner.async_call_generated('delete_schedule', parameters={'schedule_id': schedule_id}, body=None, authenticated=True, detailed=True))

    async def delete_server(self, server_name: str) -> ErrorEnvelope | TaskAcceptedResponse | None:
        """Generated delete_server operation."""
        return cast(ErrorEnvelope | TaskAcceptedResponse | None, await self._owner.async_call_generated('delete_server', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def delete_server_detailed(self, server_name: str) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
        """Generated delete_server operation."""
        return cast(Response[ErrorEnvelope | TaskAcceptedResponse], await self._owner.async_call_generated('delete_server', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def delete_user(self, user_id: int) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated delete_user operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('delete_user', parameters={'user_id': user_id}, body=None, authenticated=True, typed=True))

    async def delete_user_detailed(self, user_id: int) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated delete_user operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('delete_user', parameters={'user_id': user_id}, body=None, authenticated=True, detailed=True))

    async def disable_account_mfa(self) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated disable_account_mfa operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('disable_account_mfa', parameters={}, body=None, authenticated=True, typed=True))

    async def disable_account_mfa_detailed(self) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated disable_account_mfa operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('disable_account_mfa', parameters={}, body=None, authenticated=True, detailed=True))

    async def disable_addon(self, server_name: str, *, body: AddonActionPayload) -> ErrorEnvelope | TaskAcceptedResponse | None:
        """Generated disable_addon operation."""
        return cast(ErrorEnvelope | TaskAcceptedResponse | None, await self._owner.async_call_generated('disable_addon', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def disable_addon_detailed(self, server_name: str, *, body: AddonActionPayload) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
        """Generated disable_addon operation."""
        return cast(Response[ErrorEnvelope | TaskAcceptedResponse], await self._owner.async_call_generated('disable_addon', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

    async def disable_user(self, user_id: int) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated disable_user operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('disable_user', parameters={'user_id': user_id}, body=None, authenticated=True, typed=True))

    async def disable_user_detailed(self, user_id: int) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated disable_user operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('disable_user', parameters={'user_id': user_id}, body=None, authenticated=True, detailed=True))

    async def download_backup_emergency_kit(self, key_id: str) -> ErrorEnvelope | str | None:
        """Generated download_backup_emergency_kit operation."""
        return cast(ErrorEnvelope | str | None, await self._owner.async_call_generated('download_backup_emergency_kit', parameters={'key_id': key_id}, body=None, authenticated=True, typed=True))

    async def download_backup_emergency_kit_detailed(self, key_id: str) -> Response[ErrorEnvelope | str]:
        """Generated download_backup_emergency_kit operation."""
        return cast(Response[ErrorEnvelope | str], await self._owner.async_call_generated('download_backup_emergency_kit', parameters={'key_id': key_id}, body=None, authenticated=True, detailed=True))

    async def download_backup_recovery_report(self, server_name: str) -> ErrorEnvelope | RecoveryReportResponse | None:
        """Generated download_backup_recovery_report operation."""
        return cast(ErrorEnvelope | RecoveryReportResponse | None, await self._owner.async_call_generated('download_backup_recovery_report', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def download_backup_recovery_report_detailed(self, server_name: str) -> Response[ErrorEnvelope | RecoveryReportResponse]:
        """Generated download_backup_recovery_report operation."""
        return cast(Response[ErrorEnvelope | RecoveryReportResponse], await self._owner.async_call_generated('download_backup_recovery_report', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def download_server_snapshot(self, server_name: str, backup_id: str) -> ErrorEnvelope | File | None:
        """Generated download_server_snapshot operation."""
        return cast(ErrorEnvelope | File | None, await self._owner.async_call_generated('download_server_snapshot', parameters={'server_name': server_name, 'backup_id': backup_id}, body=None, authenticated=True, typed=True))

    async def download_server_snapshot_detailed(self, server_name: str, backup_id: str) -> Response[ErrorEnvelope | File]:
        """Generated download_server_snapshot operation."""
        return cast(Response[ErrorEnvelope | File], await self._owner.async_call_generated('download_server_snapshot', parameters={'server_name': server_name, 'backup_id': backup_id}, body=None, authenticated=True, detailed=True))

    async def dry_run_server_restore(self, server_name: str, backup_id: str, *, body: SnapshotPlanPayload) -> ErrorEnvelope | TaskAcceptedResponse | None:
        """Generated dry_run_server_restore operation."""
        return cast(ErrorEnvelope | TaskAcceptedResponse | None, await self._owner.async_call_generated('dry_run_server_restore', parameters={'server_name': server_name, 'backup_id': backup_id}, body=body, authenticated=True, typed=True))

    async def dry_run_server_restore_detailed(self, server_name: str, backup_id: str, *, body: SnapshotPlanPayload) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
        """Generated dry_run_server_restore operation."""
        return cast(Response[ErrorEnvelope | TaskAcceptedResponse], await self._owner.async_call_generated('dry_run_server_restore', parameters={'server_name': server_name, 'backup_id': backup_id}, body=body, authenticated=True, detailed=True))

    async def enable_addon(self, server_name: str, *, body: AddonActionPayload) -> ErrorEnvelope | TaskAcceptedResponse | None:
        """Generated enable_addon operation."""
        return cast(ErrorEnvelope | TaskAcceptedResponse | None, await self._owner.async_call_generated('enable_addon', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def enable_addon_detailed(self, server_name: str, *, body: AddonActionPayload) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
        """Generated enable_addon operation."""
        return cast(Response[ErrorEnvelope | TaskAcceptedResponse], await self._owner.async_call_generated('enable_addon', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

    async def enable_user(self, user_id: int) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated enable_user operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('enable_user', parameters={'user_id': user_id}, body=None, authenticated=True, typed=True))

    async def enable_user_detailed(self, user_id: int) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated enable_user operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('enable_user', parameters={'user_id': user_id}, body=None, authenticated=True, detailed=True))

    async def enroll_account_mfa(self) -> ErrorEnvelope | FactorEnrollment | None:
        """Generated enroll_account_mfa operation."""
        return cast(ErrorEnvelope | FactorEnrollment | None, await self._owner.async_call_generated('enroll_account_mfa', parameters={}, body=None, authenticated=True, typed=True))

    async def enroll_account_mfa_detailed(self) -> Response[ErrorEnvelope | FactorEnrollment]:
        """Generated enroll_account_mfa operation."""
        return cast(Response[ErrorEnvelope | FactorEnrollment], await self._owner.async_call_generated('enroll_account_mfa', parameters={}, body=None, authenticated=True, detailed=True))

    async def export_decrypted_snapshot(self, server_name: str, backup_id: str, *, body: SnapshotInspectPayload) -> ErrorEnvelope | File | None:
        """Generated export_decrypted_snapshot operation."""
        return cast(ErrorEnvelope | File | None, await self._owner.async_call_generated('export_decrypted_snapshot', parameters={'server_name': server_name, 'backup_id': backup_id}, body=body, authenticated=True, typed=True))

    async def export_decrypted_snapshot_detailed(self, server_name: str, backup_id: str, *, body: SnapshotInspectPayload) -> Response[ErrorEnvelope | File]:
        """Generated export_decrypted_snapshot operation."""
        return cast(Response[ErrorEnvelope | File], await self._owner.async_call_generated('export_decrypted_snapshot', parameters={'server_name': server_name, 'backup_id': backup_id}, body=body, authenticated=True, detailed=True))

    async def export_world(self, server_name: str) -> ErrorEnvelope | TaskAcceptedResponse | None:
        """Generated export_world operation."""
        return cast(ErrorEnvelope | TaskAcceptedResponse | None, await self._owner.async_call_generated('export_world', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def export_world_detailed(self, server_name: str) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
        """Generated export_world operation."""
        return cast(Response[ErrorEnvelope | TaskAcceptedResponse], await self._owner.async_call_generated('export_world', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def generate_registration_token(self, *, body: GenerateTokenPayload) -> ErrorEnvelope | RegistrationResponse | None:
        """Generated generate_registration_token operation."""
        return cast(ErrorEnvelope | RegistrationResponse | None, await self._owner.async_call_generated('generate_registration_token', parameters={}, body=body, authenticated=True, typed=True))

    async def generate_registration_token_detailed(self, *, body: GenerateTokenPayload) -> Response[ErrorEnvelope | RegistrationResponse]:
        """Generated generate_registration_token operation."""
        return cast(Response[ErrorEnvelope | RegistrationResponse], await self._owner.async_call_generated('generate_registration_token', parameters={}, body=body, authenticated=True, detailed=True))

    async def get_access_policy(self) -> AccessPolicyInfo | ErrorEnvelope | None:
        """Generated get_access_policy operation."""
        return cast(AccessPolicyInfo | ErrorEnvelope | None, await self._owner.async_call_generated('get_access_policy', parameters={}, body=None, authenticated=True, typed=True))

    async def get_access_policy_detailed(self) -> Response[AccessPolicyInfo | ErrorEnvelope]:
        """Generated get_access_policy operation."""
        return cast(Response[AccessPolicyInfo | ErrorEnvelope], await self._owner.async_call_generated('get_access_policy', parameters={}, body=None, authenticated=True, detailed=True))

    async def get_account(self) -> CurrentAccountResponse | ErrorEnvelope | None:
        """Generated get_account operation."""
        return cast(CurrentAccountResponse | ErrorEnvelope | None, await self._owner.async_call_generated('get_account', parameters={}, body=None, authenticated=True, typed=True))

    async def get_account_detailed(self) -> Response[CurrentAccountResponse | ErrorEnvelope]:
        """Generated get_account operation."""
        return cast(Response[CurrentAccountResponse | ErrorEnvelope], await self._owner.async_call_generated('get_account', parameters={}, body=None, authenticated=True, detailed=True))

    async def get_account_permissions(self) -> ErrorEnvelope | list[str] | None:
        """Generated get_account_permissions operation."""
        return cast(ErrorEnvelope | list[str] | None, await self._owner.async_call_generated('get_account_permissions', parameters={}, body=None, authenticated=True, typed=True))

    async def get_account_permissions_detailed(self) -> Response[ErrorEnvelope | list[str]]:
        """Generated get_account_permissions operation."""
        return cast(Response[ErrorEnvelope | list[str]], await self._owner.async_call_generated('get_account_permissions', parameters={}, body=None, authenticated=True, detailed=True))

    async def get_account_security(self) -> ErrorEnvelope | SecurityStatus | None:
        """Generated get_account_security operation."""
        return cast(ErrorEnvelope | SecurityStatus | None, await self._owner.async_call_generated('get_account_security', parameters={}, body=None, authenticated=True, typed=True))

    async def get_account_security_detailed(self) -> Response[ErrorEnvelope | SecurityStatus]:
        """Generated get_account_security operation."""
        return cast(Response[ErrorEnvelope | SecurityStatus], await self._owner.async_call_generated('get_account_security', parameters={}, body=None, authenticated=True, detailed=True))

    async def get_account_server_access(self, user_id: int) -> AccountServerAccessInfo | ErrorEnvelope | None:
        """Generated get_account_server_access operation."""
        return cast(AccountServerAccessInfo | ErrorEnvelope | None, await self._owner.async_call_generated('get_account_server_access', parameters={'user_id': user_id}, body=None, authenticated=True, typed=True))

    async def get_account_server_access_detailed(self, user_id: int) -> Response[AccountServerAccessInfo | ErrorEnvelope]:
        """Generated get_account_server_access operation."""
        return cast(Response[AccountServerAccessInfo | ErrorEnvelope], await self._owner.async_call_generated('get_account_server_access', parameters={'user_id': user_id}, body=None, authenticated=True, detailed=True))

    async def get_allowlist(self, server_name: str) -> ErrorEnvelope | GetAllowlistResponse | None:
        """Generated get_allowlist operation."""
        return cast(ErrorEnvelope | GetAllowlistResponse | None, await self._owner.async_call_generated('get_allowlist', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def get_allowlist_detailed(self, server_name: str) -> Response[ErrorEnvelope | GetAllowlistResponse]:
        """Generated get_allowlist operation."""
        return cast(Response[ErrorEnvelope | GetAllowlistResponse], await self._owner.async_call_generated('get_allowlist', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def get_application_diagnostics(self) -> DiagnosticSnapshot | ErrorEnvelope | None:
        """Generated get_application_diagnostics operation."""
        return cast(DiagnosticSnapshot | ErrorEnvelope | None, await self._owner.async_call_generated('get_application_diagnostics', parameters={}, body=None, authenticated=True, typed=True))

    async def get_application_diagnostics_detailed(self) -> Response[DiagnosticSnapshot | ErrorEnvelope]:
        """Generated get_application_diagnostics operation."""
        return cast(Response[DiagnosticSnapshot | ErrorEnvelope], await self._owner.async_call_generated('get_application_diagnostics', parameters={}, body=None, authenticated=True, detailed=True))

    async def get_application_health(self) -> ErrorEnvelope | GetApplicationHealthResponse | None:
        """Generated get_application_health operation."""
        return cast(ErrorEnvelope | GetApplicationHealthResponse | None, await self._owner.async_call_generated('get_application_health', parameters={}, body=None, authenticated=True, typed=True))

    async def get_application_health_detailed(self) -> Response[ErrorEnvelope | GetApplicationHealthResponse]:
        """Generated get_application_health operation."""
        return cast(Response[ErrorEnvelope | GetApplicationHealthResponse], await self._owner.async_call_generated('get_application_health', parameters={}, body=None, authenticated=True, detailed=True))

    async def get_application_metrics(self) -> ErrorEnvelope | GetApplicationMetricsResponse | None:
        """Generated get_application_metrics operation."""
        return cast(ErrorEnvelope | GetApplicationMetricsResponse | None, await self._owner.async_call_generated('get_application_metrics', parameters={}, body=None, authenticated=True, typed=True))

    async def get_application_metrics_detailed(self) -> Response[ErrorEnvelope | GetApplicationMetricsResponse]:
        """Generated get_application_metrics operation."""
        return cast(Response[ErrorEnvelope | GetApplicationMetricsResponse], await self._owner.async_call_generated('get_application_metrics', parameters={}, body=None, authenticated=True, detailed=True))

    async def get_backup_health(self, server_name: str) -> BackupHealthResponse | ErrorEnvelope | None:
        """Generated get_backup_health operation."""
        return cast(BackupHealthResponse | ErrorEnvelope | None, await self._owner.async_call_generated('get_backup_health', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def get_backup_health_detailed(self, server_name: str) -> Response[BackupHealthResponse | ErrorEnvelope]:
        """Generated get_backup_health operation."""
        return cast(Response[BackupHealthResponse | ErrorEnvelope], await self._owner.async_call_generated('get_backup_health', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def get_diagnostic_activity(self, *, operation_id: None | str | Unset=UNSET, sequence_id: None | str | Unset=UNSET, operation_name: None | str | Unset=UNSET, server_name: None | str | Unset=UNSET, source: None | str | Unset=UNSET, phase: GetDiagnosticActivityPhaseType0 | None | Unset=UNSET, name: None | str | Unset=UNSET, owner: None | str | Unset=UNSET, correlation_id: None | str | Unset=UNSET, status: GetDiagnosticActivityStatusType0 | None | Unset=UNSET, limit: int | Unset=100) -> DiagnosticActivity | ErrorEnvelope | None:
        """Generated get_diagnostic_activity operation."""
        return cast(DiagnosticActivity | ErrorEnvelope | None, await self._owner.async_call_generated('get_diagnostic_activity', parameters={'operation_id': operation_id, 'sequence_id': sequence_id, 'operation_name': operation_name, 'server_name': server_name, 'source': source, 'phase': phase, 'name': name, 'owner': owner, 'correlation_id': correlation_id, 'status': status, 'limit': limit}, body=None, authenticated=True, typed=True))

    async def get_diagnostic_activity_detailed(self, *, operation_id: None | str | Unset=UNSET, sequence_id: None | str | Unset=UNSET, operation_name: None | str | Unset=UNSET, server_name: None | str | Unset=UNSET, source: None | str | Unset=UNSET, phase: GetDiagnosticActivityPhaseType0 | None | Unset=UNSET, name: None | str | Unset=UNSET, owner: None | str | Unset=UNSET, correlation_id: None | str | Unset=UNSET, status: GetDiagnosticActivityStatusType0 | None | Unset=UNSET, limit: int | Unset=100) -> Response[DiagnosticActivity | ErrorEnvelope]:
        """Generated get_diagnostic_activity operation."""
        return cast(Response[DiagnosticActivity | ErrorEnvelope], await self._owner.async_call_generated('get_diagnostic_activity', parameters={'operation_id': operation_id, 'sequence_id': sequence_id, 'operation_name': operation_name, 'server_name': server_name, 'source': source, 'phase': phase, 'name': name, 'owner': owner, 'correlation_id': correlation_id, 'status': status, 'limit': limit}, body=None, authenticated=True, detailed=True))

    async def get_diagnostic_history(self, *, limit: int | Unset=100, subsystem: None | str | Unset=UNSET, instance_id: None | str | Unset=UNSET, correlation_id: None | str | Unset=UNSET, cursor: None | str | Unset=UNSET, owner: None | str | Unset=UNSET, code: None | str | Unset=UNSET, outcome: GetDiagnosticHistoryOutcomeType0 | None | Unset=UNSET, operation_id: None | str | Unset=UNSET) -> DiagnosticHistory | ErrorEnvelope | None:
        """Generated get_diagnostic_history operation."""
        return cast(DiagnosticHistory | ErrorEnvelope | None, await self._owner.async_call_generated('get_diagnostic_history', parameters={'limit': limit, 'subsystem': subsystem, 'instance_id': instance_id, 'correlation_id': correlation_id, 'cursor': cursor, 'owner': owner, 'code': code, 'outcome': outcome, 'operation_id': operation_id}, body=None, authenticated=True, typed=True))

    async def get_diagnostic_history_detailed(self, *, limit: int | Unset=100, subsystem: None | str | Unset=UNSET, instance_id: None | str | Unset=UNSET, correlation_id: None | str | Unset=UNSET, cursor: None | str | Unset=UNSET, owner: None | str | Unset=UNSET, code: None | str | Unset=UNSET, outcome: GetDiagnosticHistoryOutcomeType0 | None | Unset=UNSET, operation_id: None | str | Unset=UNSET) -> Response[DiagnosticHistory | ErrorEnvelope]:
        """Generated get_diagnostic_history operation."""
        return cast(Response[DiagnosticHistory | ErrorEnvelope], await self._owner.async_call_generated('get_diagnostic_history', parameters={'limit': limit, 'subsystem': subsystem, 'instance_id': instance_id, 'correlation_id': correlation_id, 'cursor': cursor, 'owner': owner, 'code': code, 'outcome': outcome, 'operation_id': operation_id}, body=None, authenticated=True, detailed=True))

    async def get_diagnostic_report(self) -> DiagnosticReport | ErrorEnvelope | None:
        """Generated get_diagnostic_report operation."""
        return cast(DiagnosticReport | ErrorEnvelope | None, await self._owner.async_call_generated('get_diagnostic_report', parameters={}, body=None, authenticated=True, typed=True))

    async def get_diagnostic_report_detailed(self) -> Response[DiagnosticReport | ErrorEnvelope]:
        """Generated get_diagnostic_report operation."""
        return cast(Response[DiagnosticReport | ErrorEnvelope], await self._owner.async_call_generated('get_diagnostic_report', parameters={}, body=None, authenticated=True, detailed=True))

    async def get_diagnostic_runs(self, *, limit: int | Unset=20) -> DiagnosticRuns | ErrorEnvelope | None:
        """Generated get_diagnostic_runs operation."""
        return cast(DiagnosticRuns | ErrorEnvelope | None, await self._owner.async_call_generated('get_diagnostic_runs', parameters={'limit': limit}, body=None, authenticated=True, typed=True))

    async def get_diagnostic_runs_detailed(self, *, limit: int | Unset=20) -> Response[DiagnosticRuns | ErrorEnvelope]:
        """Generated get_diagnostic_runs operation."""
        return cast(Response[DiagnosticRuns | ErrorEnvelope], await self._owner.async_call_generated('get_diagnostic_runs', parameters={'limit': limit}, body=None, authenticated=True, detailed=True))

    async def get_diagnostic_trace(self, correlation_id: str, *, limit: int | Unset=100, cursor: None | str | Unset=UNSET) -> DiagnosticTrace | ErrorEnvelope | None:
        """Generated get_diagnostic_trace operation."""
        return cast(DiagnosticTrace | ErrorEnvelope | None, await self._owner.async_call_generated('get_diagnostic_trace', parameters={'correlation_id': correlation_id, 'limit': limit, 'cursor': cursor}, body=None, authenticated=True, typed=True))

    async def get_diagnostic_trace_detailed(self, correlation_id: str, *, limit: int | Unset=100, cursor: None | str | Unset=UNSET) -> Response[DiagnosticTrace | ErrorEnvelope]:
        """Generated get_diagnostic_trace operation."""
        return cast(Response[DiagnosticTrace | ErrorEnvelope], await self._owner.async_call_generated('get_diagnostic_trace', parameters={'correlation_id': correlation_id, 'limit': limit, 'cursor': cursor}, body=None, authenticated=True, detailed=True))

    async def get_event_activity(self, *, operation_id: None | str | Unset=UNSET, sequence_id: None | str | Unset=UNSET, operation_name: None | str | Unset=UNSET, server_name: None | str | Unset=UNSET, source: None | str | Unset=UNSET, phase: GetEventActivityPhaseType0 | None | Unset=UNSET, name: None | str | Unset=UNSET, owner: None | str | Unset=UNSET, correlation_id: None | str | Unset=UNSET, status: GetEventActivityStatusType0 | None | Unset=UNSET, limit: int | Unset=200) -> ErrorEnvelope | EventDiagnostics | None:
        """Generated get_event_activity operation."""
        return cast(ErrorEnvelope | EventDiagnostics | None, await self._owner.async_call_generated('get_event_activity', parameters={'operation_id': operation_id, 'sequence_id': sequence_id, 'operation_name': operation_name, 'server_name': server_name, 'source': source, 'phase': phase, 'name': name, 'owner': owner, 'correlation_id': correlation_id, 'status': status, 'limit': limit}, body=None, authenticated=True, typed=True))

    async def get_event_activity_detailed(self, *, operation_id: None | str | Unset=UNSET, sequence_id: None | str | Unset=UNSET, operation_name: None | str | Unset=UNSET, server_name: None | str | Unset=UNSET, source: None | str | Unset=UNSET, phase: GetEventActivityPhaseType0 | None | Unset=UNSET, name: None | str | Unset=UNSET, owner: None | str | Unset=UNSET, correlation_id: None | str | Unset=UNSET, status: GetEventActivityStatusType0 | None | Unset=UNSET, limit: int | Unset=200) -> Response[ErrorEnvelope | EventDiagnostics]:
        """Generated get_event_activity operation."""
        return cast(Response[ErrorEnvelope | EventDiagnostics], await self._owner.async_call_generated('get_event_activity', parameters={'operation_id': operation_id, 'sequence_id': sequence_id, 'operation_name': operation_name, 'server_name': server_name, 'source': source, 'phase': phase, 'name': name, 'owner': owner, 'correlation_id': correlation_id, 'status': status, 'limit': limit}, body=None, authenticated=True, detailed=True))

    async def get_log_history(self, *, topic: str, before: int | None | Unset=UNSET, file_id: None | str | Unset=UNSET) -> ErrorEnvelope | LogHistoryPage | None:
        """Generated get_log_history operation."""
        return cast(ErrorEnvelope | LogHistoryPage | None, await self._owner.async_call_generated('get_log_history', parameters={'topic': topic, 'before': before, 'file_id': file_id}, body=None, authenticated=True, typed=True))

    async def get_log_history_detailed(self, *, topic: str, before: int | None | Unset=UNSET, file_id: None | str | Unset=UNSET) -> Response[ErrorEnvelope | LogHistoryPage]:
        """Generated get_log_history operation."""
        return cast(Response[ErrorEnvelope | LogHistoryPage], await self._owner.async_call_generated('get_log_history', parameters={'topic': topic, 'before': before, 'file_id': file_id}, body=None, authenticated=True, detailed=True))

    async def get_panorama(self) -> Any | ErrorEnvelope | None:
        """Generated get_panorama operation."""
        return cast(Any | ErrorEnvelope | None, await self._owner.async_call_generated('get_panorama', parameters={}, body=None, authenticated=False, typed=True))

    async def get_panorama_detailed(self) -> Response[Any | ErrorEnvelope]:
        """Generated get_panorama operation."""
        return cast(Response[Any | ErrorEnvelope], await self._owner.async_call_generated('get_panorama', parameters={}, body=None, authenticated=False, detailed=True))

    async def get_permissions(self, server_name: str) -> ErrorEnvelope | GetPermissionsResponse | None:
        """Generated get_permissions operation."""
        return cast(ErrorEnvelope | GetPermissionsResponse | None, await self._owner.async_call_generated('get_permissions', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def get_permissions_detailed(self, server_name: str) -> Response[ErrorEnvelope | GetPermissionsResponse]:
        """Generated get_permissions operation."""
        return cast(Response[ErrorEnvelope | GetPermissionsResponse], await self._owner.async_call_generated('get_permissions', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def get_plugin_pages(self) -> ErrorEnvelope | PluginPagesResponse | None:
        """Generated get_plugin_pages operation."""
        return cast(ErrorEnvelope | PluginPagesResponse | None, await self._owner.async_call_generated('get_plugin_pages', parameters={}, body=None, authenticated=True, typed=True))

    async def get_plugin_pages_detailed(self) -> Response[ErrorEnvelope | PluginPagesResponse]:
        """Generated get_plugin_pages operation."""
        return cast(Response[ErrorEnvelope | PluginPagesResponse], await self._owner.async_call_generated('get_plugin_pages', parameters={}, body=None, authenticated=True, detailed=True))

    async def get_plugin_settings(self, plugin_name: str, *, scope: GetPluginSettingsScope | Unset=GetPluginSettingsScope.PLUGIN, server_name: None | str | Unset=UNSET) -> ErrorEnvelope | GetPluginSettingsResponse | None:
        """Generated get_plugin_settings operation."""
        return cast(ErrorEnvelope | GetPluginSettingsResponse | None, await self._owner.async_call_generated('get_plugin_settings', parameters={'plugin_name': plugin_name, 'scope': scope, 'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def get_plugin_settings_detailed(self, plugin_name: str, *, scope: GetPluginSettingsScope | Unset=GetPluginSettingsScope.PLUGIN, server_name: None | str | Unset=UNSET) -> Response[ErrorEnvelope | GetPluginSettingsResponse]:
        """Generated get_plugin_settings operation."""
        return cast(Response[ErrorEnvelope | GetPluginSettingsResponse], await self._owner.async_call_generated('get_plugin_settings', parameters={'plugin_name': plugin_name, 'scope': scope, 'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def get_properties(self, server_name: str) -> ErrorEnvelope | GetPropertiesResponse | None:
        """Generated get_properties operation."""
        return cast(ErrorEnvelope | GetPropertiesResponse | None, await self._owner.async_call_generated('get_properties', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def get_properties_detailed(self, server_name: str) -> Response[ErrorEnvelope | GetPropertiesResponse]:
        """Generated get_properties operation."""
        return cast(Response[ErrorEnvelope | GetPropertiesResponse], await self._owner.async_call_generated('get_properties', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def get_raw_properties(self, server_name: str) -> ErrorEnvelope | GetRawPropertiesResponse | None:
        """Generated get_raw_properties operation."""
        return cast(ErrorEnvelope | GetRawPropertiesResponse | None, await self._owner.async_call_generated('get_raw_properties', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def get_raw_properties_detailed(self, server_name: str) -> Response[ErrorEnvelope | GetRawPropertiesResponse]:
        """Generated get_raw_properties operation."""
        return cast(Response[ErrorEnvelope | GetRawPropertiesResponse], await self._owner.async_call_generated('get_raw_properties', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def get_restore_recovery(self, server_name: str) -> ErrorEnvelope | RestoreRecoveryResponse | None:
        """Generated get_restore_recovery operation."""
        return cast(ErrorEnvelope | RestoreRecoveryResponse | None, await self._owner.async_call_generated('get_restore_recovery', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def get_restore_recovery_detailed(self, server_name: str) -> Response[ErrorEnvelope | RestoreRecoveryResponse]:
        """Generated get_restore_recovery operation."""
        return cast(Response[ErrorEnvelope | RestoreRecoveryResponse], await self._owner.async_call_generated('get_restore_recovery', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def get_server_addon_icon(self, server_name: str, *, pack_type: str, uuid: str) -> Any | ErrorEnvelope | None:
        """Generated get_server_addon_icon operation."""
        return cast(Any | ErrorEnvelope | None, await self._owner.async_call_generated('get_server_addon_icon', parameters={'server_name': server_name, 'pack_type': pack_type, 'uuid': uuid}, body=None, authenticated=False, typed=True))

    async def get_server_addon_icon_detailed(self, server_name: str, *, pack_type: str, uuid: str) -> Response[Any | ErrorEnvelope]:
        """Generated get_server_addon_icon operation."""
        return cast(Response[Any | ErrorEnvelope], await self._owner.async_call_generated('get_server_addon_icon', parameters={'server_name': server_name, 'pack_type': pack_type, 'uuid': uuid}, body=None, authenticated=False, detailed=True))

    async def get_server_bans(self, server_name: str) -> ErrorEnvelope | GetServerBansResponse | None:
        """Generated get_server_bans operation."""
        return cast(ErrorEnvelope | GetServerBansResponse | None, await self._owner.async_call_generated('get_server_bans', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def get_server_bans_detailed(self, server_name: str) -> Response[ErrorEnvelope | GetServerBansResponse]:
        """Generated get_server_bans operation."""
        return cast(Response[ErrorEnvelope | GetServerBansResponse], await self._owner.async_call_generated('get_server_bans', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def get_server_process_info(self, server_name: str) -> ErrorEnvelope | ServerProcessInfoResponse | None:
        """Generated get_server_process_info operation."""
        return cast(ErrorEnvelope | ServerProcessInfoResponse | None, await self._owner.async_call_generated('get_server_process_info', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def get_server_process_info_detailed(self, server_name: str) -> Response[ErrorEnvelope | ServerProcessInfoResponse]:
        """Generated get_server_process_info operation."""
        return cast(Response[ErrorEnvelope | ServerProcessInfoResponse], await self._owner.async_call_generated('get_server_process_info', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def get_server_settings(self, server_name: str) -> ErrorEnvelope | ServerSettingsResponse | None:
        """Generated get_server_settings operation."""
        return cast(ErrorEnvelope | ServerSettingsResponse | None, await self._owner.async_call_generated('get_server_settings', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def get_server_settings_detailed(self, server_name: str) -> Response[ErrorEnvelope | ServerSettingsResponse]:
        """Generated get_server_settings operation."""
        return cast(Response[ErrorEnvelope | ServerSettingsResponse], await self._owner.async_call_generated('get_server_settings', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def get_server_status(self, server_name: str) -> ErrorEnvelope | ServerRunningStatusResponse | None:
        """Generated get_server_status operation."""
        return cast(ErrorEnvelope | ServerRunningStatusResponse | None, await self._owner.async_call_generated('get_server_status', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def get_server_status_detailed(self, server_name: str) -> Response[ErrorEnvelope | ServerRunningStatusResponse]:
        """Generated get_server_status operation."""
        return cast(Response[ErrorEnvelope | ServerRunningStatusResponse], await self._owner.async_call_generated('get_server_status', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def get_server_summary(self, server_name: str) -> ErrorEnvelope | ServerSummary | None:
        """Generated get_server_summary operation."""
        return cast(ErrorEnvelope | ServerSummary | None, await self._owner.async_call_generated('get_server_summary', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def get_server_summary_detailed(self, server_name: str) -> Response[ErrorEnvelope | ServerSummary]:
        """Generated get_server_summary operation."""
        return cast(Response[ErrorEnvelope | ServerSummary], await self._owner.async_call_generated('get_server_summary', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def get_settings(self) -> ErrorEnvelope | SettingsResponse | None:
        """Generated get_settings operation."""
        return cast(ErrorEnvelope | SettingsResponse | None, await self._owner.async_call_generated('get_settings', parameters={}, body=None, authenticated=True, typed=True))

    async def get_settings_detailed(self) -> Response[ErrorEnvelope | SettingsResponse]:
        """Generated get_settings operation."""
        return cast(Response[ErrorEnvelope | SettingsResponse], await self._owner.async_call_generated('get_settings', parameters={}, body=None, authenticated=True, detailed=True))

    async def get_setup_status(self) -> ErrorEnvelope | SetupStatusResponse | None:
        """Generated get_setup_status operation."""
        return cast(ErrorEnvelope | SetupStatusResponse | None, await self._owner.async_call_generated('get_setup_status', parameters={}, body=None, authenticated=False, typed=True))

    async def get_setup_status_detailed(self) -> Response[ErrorEnvelope | SetupStatusResponse]:
        """Generated get_setup_status operation."""
        return cast(Response[ErrorEnvelope | SetupStatusResponse], await self._owner.async_call_generated('get_setup_status', parameters={}, body=None, authenticated=False, detailed=True))

    async def get_subsystem_diagnostics(self, subsystem: str) -> DiagnosticSnapshot | ErrorEnvelope | None:
        """Generated get_subsystem_diagnostics operation."""
        return cast(DiagnosticSnapshot | ErrorEnvelope | None, await self._owner.async_call_generated('get_subsystem_diagnostics', parameters={'subsystem': subsystem}, body=None, authenticated=True, typed=True))

    async def get_subsystem_diagnostics_detailed(self, subsystem: str) -> Response[DiagnosticSnapshot | ErrorEnvelope]:
        """Generated get_subsystem_diagnostics operation."""
        return cast(Response[DiagnosticSnapshot | ErrorEnvelope], await self._owner.async_call_generated('get_subsystem_diagnostics', parameters={'subsystem': subsystem}, body=None, authenticated=True, detailed=True))

    async def get_system_info(self) -> AppInfoResponse | ErrorEnvelope | None:
        """Generated get_system_info operation."""
        return cast(AppInfoResponse | ErrorEnvelope | None, await self._owner.async_call_generated('get_system_info', parameters={}, body=None, authenticated=False, typed=True))

    async def get_system_info_detailed(self) -> Response[AppInfoResponse | ErrorEnvelope]:
        """Generated get_system_info operation."""
        return cast(Response[AppInfoResponse | ErrorEnvelope], await self._owner.async_call_generated('get_system_info', parameters={}, body=None, authenticated=False, detailed=True))

    async def get_task_status(self, task_id: str) -> ErrorEnvelope | TaskSnapshot | None:
        """Generated get_task_status operation."""
        return cast(ErrorEnvelope | TaskSnapshot | None, await self._owner.async_call_generated('get_task_status', parameters={'task_id': task_id}, body=None, authenticated=True, typed=True))

    async def get_task_status_detailed(self, task_id: str) -> Response[ErrorEnvelope | TaskSnapshot]:
        """Generated get_task_status operation."""
        return cast(Response[ErrorEnvelope | TaskSnapshot], await self._owner.async_call_generated('get_task_status', parameters={'task_id': task_id}, body=None, authenticated=True, detailed=True))

    async def get_web_runtime(self) -> ErrorEnvelope | RuntimeStatus | None:
        """Generated get_web_runtime operation."""
        return cast(ErrorEnvelope | RuntimeStatus | None, await self._owner.async_call_generated('get_web_runtime', parameters={}, body=None, authenticated=True, typed=True))

    async def get_web_runtime_detailed(self) -> Response[ErrorEnvelope | RuntimeStatus]:
        """Generated get_web_runtime operation."""
        return cast(Response[ErrorEnvelope | RuntimeStatus], await self._owner.async_call_generated('get_web_runtime', parameters={}, body=None, authenticated=True, detailed=True))

    async def get_world_icon(self, server_name: str) -> Any | ErrorEnvelope | None:
        """Generated get_world_icon operation."""
        return cast(Any | ErrorEnvelope | None, await self._owner.async_call_generated('get_world_icon', parameters={'server_name': server_name}, body=None, authenticated=False, typed=True))

    async def get_world_icon_detailed(self, server_name: str) -> Response[Any | ErrorEnvelope]:
        """Generated get_world_icon operation."""
        return cast(Response[Any | ErrorEnvelope], await self._owner.async_call_generated('get_world_icon', parameters={'server_name': server_name}, body=None, authenticated=False, detailed=True))

    async def import_server_snapshot(self, server_name: str, *, body: BodyImportServerSnapshot) -> ErrorEnvelope | ListSnapshotsResponse | None:
        """Generated import_server_snapshot operation."""
        return cast(ErrorEnvelope | ListSnapshotsResponse | None, await self._owner.async_call_generated('import_server_snapshot', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def import_server_snapshot_detailed(self, server_name: str, *, body: BodyImportServerSnapshot) -> Response[ErrorEnvelope | ListSnapshotsResponse]:
        """Generated import_server_snapshot operation."""
        return cast(Response[ErrorEnvelope | ListSnapshotsResponse], await self._owner.async_call_generated('import_server_snapshot', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

    async def inspect_server_snapshot(self, server_name: str, backup_id: str, *, body: SnapshotInspectPayload) -> ErrorEnvelope | TaskAcceptedResponse | None:
        """Generated inspect_server_snapshot operation."""
        return cast(ErrorEnvelope | TaskAcceptedResponse | None, await self._owner.async_call_generated('inspect_server_snapshot', parameters={'server_name': server_name, 'backup_id': backup_id}, body=body, authenticated=True, typed=True))

    async def inspect_server_snapshot_detailed(self, server_name: str, backup_id: str, *, body: SnapshotInspectPayload) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
        """Generated inspect_server_snapshot operation."""
        return cast(Response[ErrorEnvelope | TaskAcceptedResponse], await self._owner.async_call_generated('inspect_server_snapshot', parameters={'server_name': server_name, 'backup_id': backup_id}, body=body, authenticated=True, detailed=True))

    async def install_addon(self, server_name: str, *, body: FileNamePayload) -> ErrorEnvelope | TaskAcceptedResponse | None:
        """Generated install_addon operation."""
        return cast(ErrorEnvelope | TaskAcceptedResponse | None, await self._owner.async_call_generated('install_addon', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def install_addon_detailed(self, server_name: str, *, body: FileNamePayload) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
        """Generated install_addon operation."""
        return cast(Response[ErrorEnvelope | TaskAcceptedResponse], await self._owner.async_call_generated('install_addon', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

    async def install_server(self, *, body: InstallServerPayload) -> ErrorEnvelope | InstallationAcceptedResponse | InstallConfirmationResponse | None:
        """Generated install_server operation."""
        return cast(ErrorEnvelope | InstallationAcceptedResponse | InstallConfirmationResponse | None, await self._owner.async_call_generated('install_server', parameters={}, body=body, authenticated=True, typed=True))

    async def install_server_detailed(self, *, body: InstallServerPayload) -> Response[ErrorEnvelope | InstallationAcceptedResponse | InstallConfirmationResponse]:
        """Generated install_server operation."""
        return cast(Response[ErrorEnvelope | InstallationAcceptedResponse | InstallConfirmationResponse], await self._owner.async_call_generated('install_server', parameters={}, body=body, authenticated=True, detailed=True))

    async def install_world(self, server_name: str, *, body: FileNamePayload) -> ErrorEnvelope | TaskAcceptedResponse | None:
        """Generated install_world operation."""
        return cast(ErrorEnvelope | TaskAcceptedResponse | None, await self._owner.async_call_generated('install_world', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def install_world_detailed(self, server_name: str, *, body: FileNamePayload) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
        """Generated install_world operation."""
        return cast(Response[ErrorEnvelope | TaskAcceptedResponse], await self._owner.async_call_generated('install_world', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

    async def list_access_servers(self) -> ErrorEnvelope | list[AccessServerInfo] | None:
        """Generated list_access_servers operation."""
        return cast(ErrorEnvelope | list[AccessServerInfo] | None, await self._owner.async_call_generated('list_access_servers', parameters={}, body=None, authenticated=True, typed=True))

    async def list_access_servers_detailed(self) -> Response[ErrorEnvelope | list[AccessServerInfo]]:
        """Generated list_access_servers operation."""
        return cast(Response[ErrorEnvelope | list[AccessServerInfo]], await self._owner.async_call_generated('list_access_servers', parameters={}, body=None, authenticated=True, detailed=True))

    async def list_account_integration_tokens(self, user_id: int) -> ErrorEnvelope | list[IntegrationTokenInfo] | None:
        """Generated list_account_integration_tokens operation."""
        return cast(ErrorEnvelope | list[IntegrationTokenInfo] | None, await self._owner.async_call_generated('list_account_integration_tokens', parameters={'user_id': user_id}, body=None, authenticated=True, typed=True))

    async def list_account_integration_tokens_detailed(self, user_id: int) -> Response[ErrorEnvelope | list[IntegrationTokenInfo]]:
        """Generated list_account_integration_tokens operation."""
        return cast(Response[ErrorEnvelope | list[IntegrationTokenInfo]], await self._owner.async_call_generated('list_account_integration_tokens', parameters={'user_id': user_id}, body=None, authenticated=True, detailed=True))

    async def list_account_login_sessions(self, user_id: int) -> ErrorEnvelope | list[LoginSessionInfo] | None:
        """Generated list_account_login_sessions operation."""
        return cast(ErrorEnvelope | list[LoginSessionInfo] | None, await self._owner.async_call_generated('list_account_login_sessions', parameters={'user_id': user_id}, body=None, authenticated=True, typed=True))

    async def list_account_login_sessions_detailed(self, user_id: int) -> Response[ErrorEnvelope | list[LoginSessionInfo]]:
        """Generated list_account_login_sessions operation."""
        return cast(Response[ErrorEnvelope | list[LoginSessionInfo]], await self._owner.async_call_generated('list_account_login_sessions', parameters={'user_id': user_id}, body=None, authenticated=True, detailed=True))

    async def list_application_events(self) -> ErrorEnvelope | EventCatalog | None:
        """Generated list_application_events operation."""
        return cast(ErrorEnvelope | EventCatalog | None, await self._owner.async_call_generated('list_application_events', parameters={}, body=None, authenticated=True, typed=True))

    async def list_application_events_detailed(self) -> Response[ErrorEnvelope | EventCatalog]:
        """Generated list_application_events operation."""
        return cast(Response[ErrorEnvelope | EventCatalog], await self._owner.async_call_generated('list_application_events', parameters={}, body=None, authenticated=True, detailed=True))

    async def list_audit_logs(self) -> ErrorEnvelope | list[AuditLogResponse] | None:
        """Generated list_audit_logs operation."""
        return cast(ErrorEnvelope | list[AuditLogResponse] | None, await self._owner.async_call_generated('list_audit_logs', parameters={}, body=None, authenticated=True, typed=True))

    async def list_audit_logs_detailed(self) -> Response[ErrorEnvelope | list[AuditLogResponse]]:
        """Generated list_audit_logs operation."""
        return cast(Response[ErrorEnvelope | list[AuditLogResponse]], await self._owner.async_call_generated('list_audit_logs', parameters={}, body=None, authenticated=True, detailed=True))

    async def list_available_addons(self) -> ErrorEnvelope | ListAvailableAddonsResponse | None:
        """Generated list_available_addons operation."""
        return cast(ErrorEnvelope | ListAvailableAddonsResponse | None, await self._owner.async_call_generated('list_available_addons', parameters={}, body=None, authenticated=True, typed=True))

    async def list_available_addons_detailed(self) -> Response[ErrorEnvelope | ListAvailableAddonsResponse]:
        """Generated list_available_addons operation."""
        return cast(Response[ErrorEnvelope | ListAvailableAddonsResponse], await self._owner.async_call_generated('list_available_addons', parameters={}, body=None, authenticated=True, detailed=True))

    async def list_available_worlds(self) -> ContentListResponse | ErrorEnvelope | None:
        """Generated list_available_worlds operation."""
        return cast(ContentListResponse | ErrorEnvelope | None, await self._owner.async_call_generated('list_available_worlds', parameters={}, body=None, authenticated=True, typed=True))

    async def list_available_worlds_detailed(self) -> Response[ContentListResponse | ErrorEnvelope]:
        """Generated list_available_worlds operation."""
        return cast(Response[ContentListResponse | ErrorEnvelope], await self._owner.async_call_generated('list_available_worlds', parameters={}, body=None, authenticated=True, detailed=True))

    async def list_backup_keys(self) -> ErrorEnvelope | ListBackupKeysResponseListBackupKeys | None:
        """Generated list_backup_keys operation."""
        return cast(ErrorEnvelope | ListBackupKeysResponseListBackupKeys | None, await self._owner.async_call_generated('list_backup_keys', parameters={}, body=None, authenticated=True, typed=True))

    async def list_backup_keys_detailed(self) -> Response[ErrorEnvelope | ListBackupKeysResponseListBackupKeys]:
        """Generated list_backup_keys operation."""
        return cast(Response[ErrorEnvelope | ListBackupKeysResponseListBackupKeys], await self._owner.async_call_generated('list_backup_keys', parameters={}, body=None, authenticated=True, detailed=True))

    async def list_downloads(self) -> CustomZipsResponse | ErrorEnvelope | None:
        """Generated list_downloads operation."""
        return cast(CustomZipsResponse | ErrorEnvelope | None, await self._owner.async_call_generated('list_downloads', parameters={}, body=None, authenticated=True, typed=True))

    async def list_downloads_detailed(self) -> Response[CustomZipsResponse | ErrorEnvelope]:
        """Generated list_downloads operation."""
        return cast(Response[CustomZipsResponse | ErrorEnvelope], await self._owner.async_call_generated('list_downloads', parameters={}, body=None, authenticated=True, detailed=True))

    async def list_integration_tokens(self) -> ErrorEnvelope | list[IntegrationTokenInfo] | None:
        """Generated list_integration_tokens operation."""
        return cast(ErrorEnvelope | list[IntegrationTokenInfo] | None, await self._owner.async_call_generated('list_integration_tokens', parameters={}, body=None, authenticated=True, typed=True))

    async def list_integration_tokens_detailed(self) -> Response[ErrorEnvelope | list[IntegrationTokenInfo]]:
        """Generated list_integration_tokens operation."""
        return cast(Response[ErrorEnvelope | list[IntegrationTokenInfo]], await self._owner.async_call_generated('list_integration_tokens', parameters={}, body=None, authenticated=True, detailed=True))

    async def list_login_sessions(self) -> ErrorEnvelope | list[LoginSessionInfo] | None:
        """Generated list_login_sessions operation."""
        return cast(ErrorEnvelope | list[LoginSessionInfo] | None, await self._owner.async_call_generated('list_login_sessions', parameters={}, body=None, authenticated=True, typed=True))

    async def list_login_sessions_detailed(self) -> Response[ErrorEnvelope | list[LoginSessionInfo]]:
        """Generated list_login_sessions operation."""
        return cast(Response[ErrorEnvelope | list[LoginSessionInfo]], await self._owner.async_call_generated('list_login_sessions', parameters={}, body=None, authenticated=True, detailed=True))

    async def list_players(self) -> ErrorEnvelope | PlayerListResponse | None:
        """Generated list_players operation."""
        return cast(ErrorEnvelope | PlayerListResponse | None, await self._owner.async_call_generated('list_players', parameters={}, body=None, authenticated=True, typed=True))

    async def list_players_detailed(self) -> Response[ErrorEnvelope | PlayerListResponse]:
        """Generated list_players operation."""
        return cast(Response[ErrorEnvelope | PlayerListResponse], await self._owner.async_call_generated('list_players', parameters={}, body=None, authenticated=True, detailed=True))

    async def list_plugins(self) -> ErrorEnvelope | PluginStatusesResponse | None:
        """Generated list_plugins operation."""
        return cast(ErrorEnvelope | PluginStatusesResponse | None, await self._owner.async_call_generated('list_plugins', parameters={}, body=None, authenticated=True, typed=True))

    async def list_plugins_detailed(self) -> Response[ErrorEnvelope | PluginStatusesResponse]:
        """Generated list_plugins operation."""
        return cast(Response[ErrorEnvelope | PluginStatusesResponse], await self._owner.async_call_generated('list_plugins', parameters={}, body=None, authenticated=True, detailed=True))

    async def list_schedules(self, *, server_name: None | str | Unset=UNSET) -> ErrorEnvelope | ListSchedulesResponse | None:
        """Generated list_schedules operation."""
        return cast(ErrorEnvelope | ListSchedulesResponse | None, await self._owner.async_call_generated('list_schedules', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def list_schedules_detailed(self, *, server_name: None | str | Unset=UNSET) -> Response[ErrorEnvelope | ListSchedulesResponse]:
        """Generated list_schedules operation."""
        return cast(Response[ErrorEnvelope | ListSchedulesResponse], await self._owner.async_call_generated('list_schedules', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def list_security_activity(self) -> ErrorEnvelope | list[SecurityEventInfo] | None:
        """Generated list_security_activity operation."""
        return cast(ErrorEnvelope | list[SecurityEventInfo] | None, await self._owner.async_call_generated('list_security_activity', parameters={}, body=None, authenticated=True, typed=True))

    async def list_security_activity_detailed(self) -> Response[ErrorEnvelope | list[SecurityEventInfo]]:
        """Generated list_security_activity operation."""
        return cast(Response[ErrorEnvelope | list[SecurityEventInfo]], await self._owner.async_call_generated('list_security_activity', parameters={}, body=None, authenticated=True, detailed=True))

    async def list_server_addons(self, server_name: str) -> AddonListResponse | ErrorEnvelope | None:
        """Generated list_server_addons operation."""
        return cast(AddonListResponse | ErrorEnvelope | None, await self._owner.async_call_generated('list_server_addons', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def list_server_addons_detailed(self, server_name: str) -> Response[AddonListResponse | ErrorEnvelope]:
        """Generated list_server_addons operation."""
        return cast(Response[AddonListResponse | ErrorEnvelope], await self._owner.async_call_generated('list_server_addons', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def list_server_backups(self, server_name: str, backup_type: str) -> BackupFilesResponse | ErrorEnvelope | None:
        """Generated list_server_backups operation."""
        return cast(BackupFilesResponse | ErrorEnvelope | None, await self._owner.async_call_generated('list_server_backups', parameters={'server_name': server_name, 'backup_type': backup_type}, body=None, authenticated=True, typed=True))

    async def list_server_backups_detailed(self, server_name: str, backup_type: str) -> Response[BackupFilesResponse | ErrorEnvelope]:
        """Generated list_server_backups operation."""
        return cast(Response[BackupFilesResponse | ErrorEnvelope], await self._owner.async_call_generated('list_server_backups', parameters={'server_name': server_name, 'backup_type': backup_type}, body=None, authenticated=True, detailed=True))

    async def list_server_snapshots(self, server_name: str) -> ErrorEnvelope | ListSnapshotsResponse | None:
        """Generated list_server_snapshots operation."""
        return cast(ErrorEnvelope | ListSnapshotsResponse | None, await self._owner.async_call_generated('list_server_snapshots', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def list_server_snapshots_detailed(self, server_name: str) -> Response[ErrorEnvelope | ListSnapshotsResponse]:
        """Generated list_server_snapshots operation."""
        return cast(Response[ErrorEnvelope | ListSnapshotsResponse], await self._owner.async_call_generated('list_server_snapshots', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def list_servers(self) -> ErrorEnvelope | ServersListResponse | None:
        """Generated list_servers operation."""
        return cast(ErrorEnvelope | ServersListResponse | None, await self._owner.async_call_generated('list_servers', parameters={}, body=None, authenticated=True, typed=True))

    async def list_servers_detailed(self) -> Response[ErrorEnvelope | ServersListResponse]:
        """Generated list_servers operation."""
        return cast(Response[ErrorEnvelope | ServersListResponse], await self._owner.async_call_generated('list_servers', parameters={}, body=None, authenticated=True, detailed=True))

    async def list_tasks(self) -> ErrorEnvelope | list[TaskSnapshot] | None:
        """Generated list_tasks operation."""
        return cast(ErrorEnvelope | list[TaskSnapshot] | None, await self._owner.async_call_generated('list_tasks', parameters={}, body=None, authenticated=True, typed=True))

    async def list_tasks_detailed(self) -> Response[ErrorEnvelope | list[TaskSnapshot]]:
        """Generated list_tasks operation."""
        return cast(Response[ErrorEnvelope | list[TaskSnapshot]], await self._owner.async_call_generated('list_tasks', parameters={}, body=None, authenticated=True, detailed=True))

    async def list_themes(self) -> ErrorEnvelope | ThemeListResponse | None:
        """Generated list_themes operation."""
        return cast(ErrorEnvelope | ThemeListResponse | None, await self._owner.async_call_generated('list_themes', parameters={}, body=None, authenticated=False, typed=True))

    async def list_themes_detailed(self) -> Response[ErrorEnvelope | ThemeListResponse]:
        """Generated list_themes operation."""
        return cast(Response[ErrorEnvelope | ThemeListResponse], await self._owner.async_call_generated('list_themes', parameters={}, body=None, authenticated=False, detailed=True))

    async def list_users(self) -> ErrorEnvelope | list[UserResponse] | None:
        """Generated list_users operation."""
        return cast(ErrorEnvelope | list[UserResponse] | None, await self._owner.async_call_generated('list_users', parameters={}, body=None, authenticated=True, typed=True))

    async def list_users_detailed(self) -> Response[ErrorEnvelope | list[UserResponse]]:
        """Generated list_users operation."""
        return cast(Response[ErrorEnvelope | list[UserResponse]], await self._owner.async_call_generated('list_users', parameters={}, body=None, authenticated=True, detailed=True))

    async def login(self, *, body: BodyLogin) -> ErrorEnvelope | TokenResponse | None:
        """Generated login operation."""
        return cast(ErrorEnvelope | TokenResponse | None, await self._owner.async_call_generated('login', parameters={}, body=body, authenticated=False, typed=True))

    async def login_detailed(self, *, body: BodyLogin) -> Response[ErrorEnvelope | TokenResponse]:
        """Generated login operation."""
        return cast(Response[ErrorEnvelope | TokenResponse], await self._owner.async_call_generated('login', parameters={}, body=body, authenticated=False, detailed=True))

    async def logout(self) -> Any | ErrorEnvelope | None:
        """Generated logout operation."""
        return cast(Any | ErrorEnvelope | None, await self._owner.async_call_generated('logout', parameters={}, body=None, authenticated=True, typed=True))

    async def logout_detailed(self) -> Response[Any | ErrorEnvelope]:
        """Generated logout operation."""
        return cast(Response[Any | ErrorEnvelope], await self._owner.async_call_generated('logout', parameters={}, body=None, authenticated=True, detailed=True))

    async def manage_server_snapshot(self, server_name: str, backup_id: str, *, body: SnapshotManagePayload) -> ErrorEnvelope | TaskAcceptedResponse | None:
        """Generated manage_server_snapshot operation."""
        return cast(ErrorEnvelope | TaskAcceptedResponse | None, await self._owner.async_call_generated('manage_server_snapshot', parameters={'server_name': server_name, 'backup_id': backup_id}, body=body, authenticated=True, typed=True))

    async def manage_server_snapshot_detailed(self, server_name: str, backup_id: str, *, body: SnapshotManagePayload) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
        """Generated manage_server_snapshot operation."""
        return cast(Response[ErrorEnvelope | TaskAcceptedResponse], await self._owner.async_call_generated('manage_server_snapshot', parameters={'server_name': server_name, 'backup_id': backup_id}, body=body, authenticated=True, detailed=True))

    async def plan_snapshot_restore(self, server_name: str, backup_id: str, *, body: SnapshotPlanPayload) -> ErrorEnvelope | TaskAcceptedResponse | None:
        """Generated plan_snapshot_restore operation."""
        return cast(ErrorEnvelope | TaskAcceptedResponse | None, await self._owner.async_call_generated('plan_snapshot_restore', parameters={'server_name': server_name, 'backup_id': backup_id}, body=body, authenticated=True, typed=True))

    async def plan_snapshot_restore_detailed(self, server_name: str, backup_id: str, *, body: SnapshotPlanPayload) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
        """Generated plan_snapshot_restore operation."""
        return cast(Response[ErrorEnvelope | TaskAcceptedResponse], await self._owner.async_call_generated('plan_snapshot_restore', parameters={'server_name': server_name, 'backup_id': backup_id}, body=body, authenticated=True, detailed=True))

    async def prepare_backup_copy(self, server_name: str, backup_id: str, *, body: SnapshotCopyPayload) -> ErrorEnvelope | TaskAcceptedResponse | None:
        """Generated prepare_backup_copy operation."""
        return cast(ErrorEnvelope | TaskAcceptedResponse | None, await self._owner.async_call_generated('prepare_backup_copy', parameters={'server_name': server_name, 'backup_id': backup_id}, body=body, authenticated=True, typed=True))

    async def prepare_backup_copy_detailed(self, server_name: str, backup_id: str, *, body: SnapshotCopyPayload) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
        """Generated prepare_backup_copy operation."""
        return cast(Response[ErrorEnvelope | TaskAcceptedResponse], await self._owner.async_call_generated('prepare_backup_copy', parameters={'server_name': server_name, 'backup_id': backup_id}, body=body, authenticated=True, detailed=True))

    async def prune_backups(self, server_name: str) -> ErrorEnvelope | TaskAcceptedResponse | None:
        """Generated prune_backups operation."""
        return cast(ErrorEnvelope | TaskAcceptedResponse | None, await self._owner.async_call_generated('prune_backups', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def prune_backups_detailed(self, server_name: str) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
        """Generated prune_backups operation."""
        return cast(Response[ErrorEnvelope | TaskAcceptedResponse], await self._owner.async_call_generated('prune_backups', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def prune_downloads(self, *, body: PruneDownloadsPayload) -> ErrorEnvelope | PruneDownloadsResponse | None:
        """Generated prune_downloads operation."""
        return cast(ErrorEnvelope | PruneDownloadsResponse | None, await self._owner.async_call_generated('prune_downloads', parameters={}, body=body, authenticated=True, typed=True))

    async def prune_downloads_detailed(self, *, body: PruneDownloadsPayload) -> Response[ErrorEnvelope | PruneDownloadsResponse]:
        """Generated prune_downloads operation."""
        return cast(Response[ErrorEnvelope | PruneDownloadsResponse], await self._owner.async_call_generated('prune_downloads', parameters={}, body=body, authenticated=True, detailed=True))

    async def reauthenticate(self, *, remember_me: bool | None | Unset=UNSET) -> ErrorEnvelope | TokenResponse | None:
        """Generated reauthenticate operation."""
        return cast(ErrorEnvelope | TokenResponse | None, await self._owner.async_call_generated('reauthenticate', parameters={'remember_me': remember_me}, body=None, authenticated=True, typed=True))

    async def reauthenticate_detailed(self, *, remember_me: bool | None | Unset=UNSET) -> Response[ErrorEnvelope | TokenResponse]:
        """Generated reauthenticate operation."""
        return cast(Response[ErrorEnvelope | TokenResponse], await self._owner.async_call_generated('reauthenticate', parameters={'remember_me': remember_me}, body=None, authenticated=True, detailed=True))

    async def recover_server_backup(self, server_name: str) -> ErrorEnvelope | TaskAcceptedResponse | None:
        """Generated recover_server_backup operation."""
        return cast(ErrorEnvelope | TaskAcceptedResponse | None, await self._owner.async_call_generated('recover_server_backup', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def recover_server_backup_detailed(self, server_name: str) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
        """Generated recover_server_backup operation."""
        return cast(Response[ErrorEnvelope | TaskAcceptedResponse], await self._owner.async_call_generated('recover_server_backup', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def register_user(self, token: str, *, body: UserLoginPayload) -> Any | ErrorEnvelope | None:
        """Generated register_user operation."""
        return cast(Any | ErrorEnvelope | None, await self._owner.async_call_generated('register_user', parameters={'token': token}, body=body, authenticated=False, typed=True))

    async def register_user_detailed(self, token: str, *, body: UserLoginPayload) -> Response[Any | ErrorEnvelope]:
        """Generated register_user operation."""
        return cast(Response[Any | ErrorEnvelope], await self._owner.async_call_generated('register_user', parameters={'token': token}, body=body, authenticated=False, detailed=True))

    async def reload_plugin(self, plugin_name: str) -> ActionResponse | ErrorEnvelope | None:
        """Generated reload_plugin operation."""
        return cast(ActionResponse | ErrorEnvelope | None, await self._owner.async_call_generated('reload_plugin', parameters={'plugin_name': plugin_name}, body=None, authenticated=True, typed=True))

    async def reload_plugin_detailed(self, plugin_name: str) -> Response[ActionResponse | ErrorEnvelope]:
        """Generated reload_plugin operation."""
        return cast(Response[ActionResponse | ErrorEnvelope], await self._owner.async_call_generated('reload_plugin', parameters={'plugin_name': plugin_name}, body=None, authenticated=True, detailed=True))

    async def reload_plugins(self) -> ActionResponse | ErrorEnvelope | None:
        """Generated reload_plugins operation."""
        return cast(ActionResponse | ErrorEnvelope | None, await self._owner.async_call_generated('reload_plugins', parameters={}, body=None, authenticated=True, typed=True))

    async def reload_plugins_detailed(self) -> Response[ActionResponse | ErrorEnvelope]:
        """Generated reload_plugins operation."""
        return cast(Response[ActionResponse | ErrorEnvelope], await self._owner.async_call_generated('reload_plugins', parameters={}, body=None, authenticated=True, detailed=True))

    async def reload_settings(self) -> ErrorEnvelope | SettingsResponse | None:
        """Generated reload_settings operation."""
        return cast(ErrorEnvelope | SettingsResponse | None, await self._owner.async_call_generated('reload_settings', parameters={}, body=None, authenticated=True, typed=True))

    async def reload_settings_detailed(self) -> Response[ErrorEnvelope | SettingsResponse]:
        """Generated reload_settings operation."""
        return cast(Response[ErrorEnvelope | SettingsResponse], await self._owner.async_call_generated('reload_settings', parameters={}, body=None, authenticated=True, detailed=True))

    async def remove_allowlist_players(self, server_name: str, *, body: AllowlistRemovePayload) -> ErrorEnvelope | RemoveFromAllowlistResponse | None:
        """Generated remove_allowlist_players operation."""
        return cast(ErrorEnvelope | RemoveFromAllowlistResponse | None, await self._owner.async_call_generated('remove_allowlist_players', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def remove_allowlist_players_detailed(self, server_name: str, *, body: AllowlistRemovePayload) -> Response[ErrorEnvelope | RemoveFromAllowlistResponse]:
        """Generated remove_allowlist_players operation."""
        return cast(Response[ErrorEnvelope | RemoveFromAllowlistResponse], await self._owner.async_call_generated('remove_allowlist_players', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

    async def remove_server_ban(self, server_name: str, *, body: BanRemoveRequest) -> ErrorEnvelope | RemoveServerBanResponse | None:
        """Generated remove_server_ban operation."""
        return cast(ErrorEnvelope | RemoveServerBanResponse | None, await self._owner.async_call_generated('remove_server_ban', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def remove_server_ban_detailed(self, server_name: str, *, body: BanRemoveRequest) -> Response[ErrorEnvelope | RemoveServerBanResponse]:
        """Generated remove_server_ban operation."""
        return cast(Response[ErrorEnvelope | RemoveServerBanResponse], await self._owner.async_call_generated('remove_server_ban', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

    async def rename_login_session(self, session_id: str, *, body: RenameSession) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated rename_login_session operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('rename_login_session', parameters={'session_id': session_id}, body=body, authenticated=True, typed=True))

    async def rename_login_session_detailed(self, session_id: str, *, body: RenameSession) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated rename_login_session operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('rename_login_session', parameters={'session_id': session_id}, body=body, authenticated=True, detailed=True))

    async def reorder_addons(self, server_name: str, *, body: AddonReorderPayload) -> ErrorEnvelope | TaskAcceptedResponse | None:
        """Generated reorder_addons operation."""
        return cast(ErrorEnvelope | TaskAcceptedResponse | None, await self._owner.async_call_generated('reorder_addons', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def reorder_addons_detailed(self, server_name: str, *, body: AddonReorderPayload) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
        """Generated reorder_addons operation."""
        return cast(Response[ErrorEnvelope | TaskAcceptedResponse], await self._owner.async_call_generated('reorder_addons', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

    async def reset_account_mfa(self, user_id: int) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated reset_account_mfa operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('reset_account_mfa', parameters={'user_id': user_id}, body=None, authenticated=True, typed=True))

    async def reset_account_mfa_detailed(self, user_id: int) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated reset_account_mfa operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('reset_account_mfa', parameters={'user_id': user_id}, body=None, authenticated=True, detailed=True))

    async def reset_world(self, server_name: str) -> ErrorEnvelope | TaskAcceptedResponse | None:
        """Generated reset_world operation."""
        return cast(ErrorEnvelope | TaskAcceptedResponse | None, await self._owner.async_call_generated('reset_world', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def reset_world_detailed(self, server_name: str) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
        """Generated reset_world operation."""
        return cast(Response[ErrorEnvelope | TaskAcceptedResponse], await self._owner.async_call_generated('reset_world', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def restart_server(self, server_name: str) -> ErrorEnvelope | RestartServerResponse | None:
        """Generated restart_server operation."""
        return cast(ErrorEnvelope | RestartServerResponse | None, await self._owner.async_call_generated('restart_server', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def restart_server_detailed(self, server_name: str) -> Response[ErrorEnvelope | RestartServerResponse]:
        """Generated restart_server operation."""
        return cast(Response[ErrorEnvelope | RestartServerResponse], await self._owner.async_call_generated('restart_server', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def restore_backup(self, server_name: str, *, body: RestoreActionPayload) -> ErrorEnvelope | TaskAcceptedResponse | None:
        """Generated restore_backup operation."""
        return cast(ErrorEnvelope | TaskAcceptedResponse | None, await self._owner.async_call_generated('restore_backup', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def restore_backup_detailed(self, server_name: str, *, body: RestoreActionPayload) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
        """Generated restore_backup operation."""
        return cast(Response[ErrorEnvelope | TaskAcceptedResponse], await self._owner.async_call_generated('restore_backup', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

    async def restore_server_snapshot(self, server_name: str, backup_id: str, *, body: SnapshotRestorePayload) -> ErrorEnvelope | TaskAcceptedResponse | None:
        """Generated restore_server_snapshot operation."""
        return cast(ErrorEnvelope | TaskAcceptedResponse | None, await self._owner.async_call_generated('restore_server_snapshot', parameters={'server_name': server_name, 'backup_id': backup_id}, body=body, authenticated=True, typed=True))

    async def restore_server_snapshot_detailed(self, server_name: str, backup_id: str, *, body: SnapshotRestorePayload) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
        """Generated restore_server_snapshot operation."""
        return cast(Response[ErrorEnvelope | TaskAcceptedResponse], await self._owner.async_call_generated('restore_server_snapshot', parameters={'server_name': server_name, 'backup_id': backup_id}, body=body, authenticated=True, detailed=True))

    async def revoke_account_integration_token(self, user_id: int, token_id: str) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated revoke_account_integration_token operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('revoke_account_integration_token', parameters={'user_id': user_id, 'token_id': token_id}, body=None, authenticated=True, typed=True))

    async def revoke_account_integration_token_detailed(self, user_id: int, token_id: str) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated revoke_account_integration_token operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('revoke_account_integration_token', parameters={'user_id': user_id, 'token_id': token_id}, body=None, authenticated=True, detailed=True))

    async def revoke_account_login_session(self, user_id: int, session_id: str) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated revoke_account_login_session operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('revoke_account_login_session', parameters={'user_id': user_id, 'session_id': session_id}, body=None, authenticated=True, typed=True))

    async def revoke_account_login_session_detailed(self, user_id: int, session_id: str) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated revoke_account_login_session operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('revoke_account_login_session', parameters={'user_id': user_id, 'session_id': session_id}, body=None, authenticated=True, detailed=True))

    async def revoke_account_login_sessions(self, user_id: int) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated revoke_account_login_sessions operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('revoke_account_login_sessions', parameters={'user_id': user_id}, body=None, authenticated=True, typed=True))

    async def revoke_account_login_sessions_detailed(self, user_id: int) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated revoke_account_login_sessions operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('revoke_account_login_sessions', parameters={'user_id': user_id}, body=None, authenticated=True, detailed=True))

    async def revoke_all_integration_tokens(self) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated revoke_all_integration_tokens operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('revoke_all_integration_tokens', parameters={}, body=None, authenticated=True, typed=True))

    async def revoke_all_integration_tokens_detailed(self) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated revoke_all_integration_tokens operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('revoke_all_integration_tokens', parameters={}, body=None, authenticated=True, detailed=True))

    async def revoke_integration_token(self, token_id: str) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated revoke_integration_token operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('revoke_integration_token', parameters={'token_id': token_id}, body=None, authenticated=True, typed=True))

    async def revoke_integration_token_detailed(self, token_id: str) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated revoke_integration_token operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('revoke_integration_token', parameters={'token_id': token_id}, body=None, authenticated=True, detailed=True))

    async def revoke_login_session(self, session_id: str) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated revoke_login_session operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('revoke_login_session', parameters={'session_id': session_id}, body=None, authenticated=True, typed=True))

    async def revoke_login_session_detailed(self, session_id: str) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated revoke_login_session operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('revoke_login_session', parameters={'session_id': session_id}, body=None, authenticated=True, detailed=True))

    async def revoke_login_sessions(self, *, body: RevokeSessions) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated revoke_login_sessions operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('revoke_login_sessions', parameters={}, body=body, authenticated=True, typed=True))

    async def revoke_login_sessions_detailed(self, *, body: RevokeSessions) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated revoke_login_sessions operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('revoke_login_sessions', parameters={}, body=body, authenticated=True, detailed=True))

    async def rotate_account_recovery_codes(self) -> ErrorEnvelope | RecoveryCodes | None:
        """Generated rotate_account_recovery_codes operation."""
        return cast(ErrorEnvelope | RecoveryCodes | None, await self._owner.async_call_generated('rotate_account_recovery_codes', parameters={}, body=None, authenticated=True, typed=True))

    async def rotate_account_recovery_codes_detailed(self) -> Response[ErrorEnvelope | RecoveryCodes]:
        """Generated rotate_account_recovery_codes operation."""
        return cast(Response[ErrorEnvelope | RecoveryCodes], await self._owner.async_call_generated('rotate_account_recovery_codes', parameters={}, body=None, authenticated=True, detailed=True))

    async def rotate_backup_key(self) -> ErrorEnvelope | RotateBackupKeyResponseRotateBackupKey | None:
        """Generated rotate_backup_key operation."""
        return cast(ErrorEnvelope | RotateBackupKeyResponseRotateBackupKey | None, await self._owner.async_call_generated('rotate_backup_key', parameters={}, body=None, authenticated=True, typed=True))

    async def rotate_backup_key_detailed(self) -> Response[ErrorEnvelope | RotateBackupKeyResponseRotateBackupKey]:
        """Generated rotate_backup_key operation."""
        return cast(Response[ErrorEnvelope | RotateBackupKeyResponseRotateBackupKey], await self._owner.async_call_generated('rotate_backup_key', parameters={}, body=None, authenticated=True, detailed=True))

    async def rotate_integration_token(self, token_id: str) -> CreatedIntegrationToken | ErrorEnvelope | None:
        """Generated rotate_integration_token operation."""
        return cast(CreatedIntegrationToken | ErrorEnvelope | None, await self._owner.async_call_generated('rotate_integration_token', parameters={'token_id': token_id}, body=None, authenticated=True, typed=True))

    async def rotate_integration_token_detailed(self, token_id: str) -> Response[CreatedIntegrationToken | ErrorEnvelope]:
        """Generated rotate_integration_token operation."""
        return cast(Response[CreatedIntegrationToken | ErrorEnvelope], await self._owner.async_call_generated('rotate_integration_token', parameters={'token_id': token_id}, body=None, authenticated=True, detailed=True))

    async def save_schedule(self, schedule_id: str, *, body: ScheduledTask) -> ErrorEnvelope | SuccessResponse | None:
        """Generated save_schedule operation."""
        return cast(ErrorEnvelope | SuccessResponse | None, await self._owner.async_call_generated('save_schedule', parameters={'schedule_id': schedule_id}, body=body, authenticated=True, typed=True))

    async def save_schedule_detailed(self, schedule_id: str, *, body: ScheduledTask) -> Response[ErrorEnvelope | SuccessResponse]:
        """Generated save_schedule operation."""
        return cast(Response[ErrorEnvelope | SuccessResponse], await self._owner.async_call_generated('save_schedule', parameters={'schedule_id': schedule_id}, body=body, authenticated=True, detailed=True))

    async def scan_players(self) -> AddPlayersResponse | ErrorEnvelope | None:
        """Generated scan_players operation."""
        return cast(AddPlayersResponse | ErrorEnvelope | None, await self._owner.async_call_generated('scan_players', parameters={}, body=None, authenticated=True, typed=True))

    async def scan_players_detailed(self) -> Response[AddPlayersResponse | ErrorEnvelope]:
        """Generated scan_players operation."""
        return cast(Response[AddPlayersResponse | ErrorEnvelope], await self._owner.async_call_generated('scan_players', parameters={}, body=None, authenticated=True, detailed=True))

    async def send_command(self, server_name: str, *, body: CommandPayload) -> ErrorEnvelope | SendCommandResponse | None:
        """Generated send_command operation."""
        return cast(ErrorEnvelope | SendCommandResponse | None, await self._owner.async_call_generated('send_command', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def send_command_detailed(self, server_name: str, *, body: CommandPayload) -> Response[ErrorEnvelope | SendCommandResponse]:
        """Generated send_command operation."""
        return cast(Response[ErrorEnvelope | SendCommandResponse], await self._owner.async_call_generated('send_command', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

    async def set_account_server_access(self, user_id: int, *, body: SetServerAccess) -> AccountServerAccessInfo | ErrorEnvelope | None:
        """Generated set_account_server_access operation."""
        return cast(AccountServerAccessInfo | ErrorEnvelope | None, await self._owner.async_call_generated('set_account_server_access', parameters={'user_id': user_id}, body=body, authenticated=True, typed=True))

    async def set_account_server_access_detailed(self, user_id: int, *, body: SetServerAccess) -> Response[AccountServerAccessInfo | ErrorEnvelope]:
        """Generated set_account_server_access operation."""
        return cast(Response[AccountServerAccessInfo | ErrorEnvelope], await self._owner.async_call_generated('set_account_server_access', parameters={'user_id': user_id}, body=body, authenticated=True, detailed=True))

    async def set_permissions(self, server_name: str, *, body: PermissionsSetPayload) -> ErrorEnvelope | PermissionsUpdateResponse | None:
        """Generated set_permissions operation."""
        return cast(ErrorEnvelope | PermissionsUpdateResponse | None, await self._owner.async_call_generated('set_permissions', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def set_permissions_detailed(self, server_name: str, *, body: PermissionsSetPayload) -> Response[ErrorEnvelope | PermissionsUpdateResponse]:
        """Generated set_permissions operation."""
        return cast(Response[ErrorEnvelope | PermissionsUpdateResponse], await self._owner.async_call_generated('set_permissions', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

    async def set_plugin_status(self, plugin_name: str, *, body: PluginStatusSetPayload) -> ActionResponse | ErrorEnvelope | None:
        """Generated set_plugin_status operation."""
        return cast(ActionResponse | ErrorEnvelope | None, await self._owner.async_call_generated('set_plugin_status', parameters={'plugin_name': plugin_name}, body=body, authenticated=True, typed=True))

    async def set_plugin_status_detailed(self, plugin_name: str, *, body: PluginStatusSetPayload) -> Response[ActionResponse | ErrorEnvelope]:
        """Generated set_plugin_status operation."""
        return cast(Response[ActionResponse | ErrorEnvelope], await self._owner.async_call_generated('set_plugin_status', parameters={'plugin_name': plugin_name}, body=body, authenticated=True, detailed=True))

    async def set_properties(self, server_name: str, *, body: PropertiesPayload) -> ErrorEnvelope | SetPropertiesResponse | None:
        """Generated set_properties operation."""
        return cast(ErrorEnvelope | SetPropertiesResponse | None, await self._owner.async_call_generated('set_properties', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def set_properties_detailed(self, server_name: str, *, body: PropertiesPayload) -> Response[ErrorEnvelope | SetPropertiesResponse]:
        """Generated set_properties operation."""
        return cast(Response[ErrorEnvelope | SetPropertiesResponse], await self._owner.async_call_generated('set_properties', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

    async def set_server_setting(self, server_name: str, *, body: ServerSettingItemPayload) -> ErrorEnvelope | ServerSettingsResponse | None:
        """Generated set_server_setting operation."""
        return cast(ErrorEnvelope | ServerSettingsResponse | None, await self._owner.async_call_generated('set_server_setting', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def set_server_setting_detailed(self, server_name: str, *, body: ServerSettingItemPayload) -> Response[ErrorEnvelope | ServerSettingsResponse]:
        """Generated set_server_setting operation."""
        return cast(Response[ErrorEnvelope | ServerSettingsResponse], await self._owner.async_call_generated('set_server_setting', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

    async def set_setting(self, *, body: SettingItemPayload) -> ErrorEnvelope | SettingsResponse | None:
        """Generated set_setting operation."""
        return cast(ErrorEnvelope | SettingsResponse | None, await self._owner.async_call_generated('set_setting', parameters={}, body=body, authenticated=True, typed=True))

    async def set_setting_detailed(self, *, body: SettingItemPayload) -> Response[ErrorEnvelope | SettingsResponse]:
        """Generated set_setting operation."""
        return cast(Response[ErrorEnvelope | SettingsResponse], await self._owner.async_call_generated('set_setting', parameters={}, body=body, authenticated=True, detailed=True))

    async def shutdown_web_runtime(self, *, body: ShutdownRequest) -> ErrorEnvelope | ShutdownResponse | None:
        """Generated shutdown_web_runtime operation."""
        return cast(ErrorEnvelope | ShutdownResponse | None, await self._owner.async_call_generated('shutdown_web_runtime', parameters={}, body=body, authenticated=True, typed=True))

    async def shutdown_web_runtime_detailed(self, *, body: ShutdownRequest) -> Response[ErrorEnvelope | ShutdownResponse]:
        """Generated shutdown_web_runtime operation."""
        return cast(Response[ErrorEnvelope | ShutdownResponse], await self._owner.async_call_generated('shutdown_web_runtime', parameters={}, body=body, authenticated=True, detailed=True))

    async def start_server(self, server_name: str) -> ErrorEnvelope | StartServerResponse | None:
        """Generated start_server operation."""
        return cast(ErrorEnvelope | StartServerResponse | None, await self._owner.async_call_generated('start_server', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def start_server_detailed(self, server_name: str) -> Response[ErrorEnvelope | StartServerResponse]:
        """Generated start_server operation."""
        return cast(Response[ErrorEnvelope | StartServerResponse], await self._owner.async_call_generated('start_server', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def stop_server(self, server_name: str) -> ErrorEnvelope | StopServerResponse | None:
        """Generated stop_server operation."""
        return cast(ErrorEnvelope | StopServerResponse | None, await self._owner.async_call_generated('stop_server', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def stop_server_detailed(self, server_name: str) -> Response[ErrorEnvelope | StopServerResponse]:
        """Generated stop_server operation."""
        return cast(Response[ErrorEnvelope | StopServerResponse], await self._owner.async_call_generated('stop_server', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def trigger_plugin_event(self, *, body: TriggerEventPayload) -> ErrorEnvelope | TriggerEventResponse | None:
        """Generated trigger_plugin_event operation."""
        return cast(ErrorEnvelope | TriggerEventResponse | None, await self._owner.async_call_generated('trigger_plugin_event', parameters={}, body=body, authenticated=True, typed=True))

    async def trigger_plugin_event_detailed(self, *, body: TriggerEventPayload) -> Response[ErrorEnvelope | TriggerEventResponse]:
        """Generated trigger_plugin_event operation."""
        return cast(Response[ErrorEnvelope | TriggerEventResponse], await self._owner.async_call_generated('trigger_plugin_event', parameters={}, body=body, authenticated=True, detailed=True))

    async def uninstall_addon(self, server_name: str, *, body: AddonActionPayload) -> ErrorEnvelope | TaskAcceptedResponse | None:
        """Generated uninstall_addon operation."""
        return cast(ErrorEnvelope | TaskAcceptedResponse | None, await self._owner.async_call_generated('uninstall_addon', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def uninstall_addon_detailed(self, server_name: str, *, body: AddonActionPayload) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
        """Generated uninstall_addon operation."""
        return cast(Response[ErrorEnvelope | TaskAcceptedResponse], await self._owner.async_call_generated('uninstall_addon', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

    async def update_account_profile(self, *, body: ProfileUpdatePayload) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated update_account_profile operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('update_account_profile', parameters={}, body=body, authenticated=True, typed=True))

    async def update_account_profile_detailed(self, *, body: ProfileUpdatePayload) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated update_account_profile operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('update_account_profile', parameters={}, body=body, authenticated=True, detailed=True))

    async def update_account_theme(self, *, body: ThemeUpdatePayload) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated update_account_theme operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('update_account_theme', parameters={}, body=body, authenticated=True, typed=True))

    async def update_account_theme_detailed(self, *, body: ThemeUpdatePayload) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated update_account_theme operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('update_account_theme', parameters={}, body=body, authenticated=True, detailed=True))

    async def update_addon_subpack(self, server_name: str, *, body: AddonSubpackPayload) -> ErrorEnvelope | TaskAcceptedResponse | None:
        """Generated update_addon_subpack operation."""
        return cast(ErrorEnvelope | TaskAcceptedResponse | None, await self._owner.async_call_generated('update_addon_subpack', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def update_addon_subpack_detailed(self, server_name: str, *, body: AddonSubpackPayload) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
        """Generated update_addon_subpack operation."""
        return cast(Response[ErrorEnvelope | TaskAcceptedResponse], await self._owner.async_call_generated('update_addon_subpack', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

    async def update_plugin_settings(self, plugin_name: str, *, body: PluginSettingsPayload) -> ErrorEnvelope | SetPluginSettingResponse | None:
        """Generated update_plugin_settings operation."""
        return cast(ErrorEnvelope | SetPluginSettingResponse | None, await self._owner.async_call_generated('update_plugin_settings', parameters={'plugin_name': plugin_name}, body=body, authenticated=True, typed=True))

    async def update_plugin_settings_detailed(self, plugin_name: str, *, body: PluginSettingsPayload) -> Response[ErrorEnvelope | SetPluginSettingResponse]:
        """Generated update_plugin_settings operation."""
        return cast(Response[ErrorEnvelope | SetPluginSettingResponse], await self._owner.async_call_generated('update_plugin_settings', parameters={'plugin_name': plugin_name}, body=body, authenticated=True, detailed=True))

    async def update_server(self, server_name: str) -> ErrorEnvelope | TaskAcceptedResponse | None:
        """Generated update_server operation."""
        return cast(ErrorEnvelope | TaskAcceptedResponse | None, await self._owner.async_call_generated('update_server', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def update_server_detailed(self, server_name: str) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
        """Generated update_server operation."""
        return cast(Response[ErrorEnvelope | TaskAcceptedResponse], await self._owner.async_call_generated('update_server', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def update_user_role(self, user_id: int, *, body: UpdateUserRolePayload) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated update_user_role operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('update_user_role', parameters={'user_id': user_id}, body=body, authenticated=True, typed=True))

    async def update_user_role_detailed(self, user_id: int, *, body: UpdateUserRolePayload) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated update_user_role operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('update_user_role', parameters={'user_id': user_id}, body=body, authenticated=True, detailed=True))

    async def validate_registration_token(self, token: str) -> Any | ErrorEnvelope | None:
        """Generated validate_registration_token operation."""
        return cast(Any | ErrorEnvelope | None, await self._owner.async_call_generated('validate_registration_token', parameters={'token': token}, body=None, authenticated=False, typed=True))

    async def validate_registration_token_detailed(self, token: str) -> Response[Any | ErrorEnvelope]:
        """Generated validate_registration_token operation."""
        return cast(Response[Any | ErrorEnvelope], await self._owner.async_call_generated('validate_registration_token', parameters={'token': token}, body=None, authenticated=False, detailed=True))

    async def validate_server(self, server_name: str) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated validate_server operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('validate_server', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def validate_server_detailed(self, server_name: str) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated validate_server operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('validate_server', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def verify_account_security(self, *, body: VerifySecurity) -> ErrorEnvelope | VerifiedSecurity | None:
        """Generated verify_account_security operation."""
        return cast(ErrorEnvelope | VerifiedSecurity | None, await self._owner.async_call_generated('verify_account_security', parameters={}, body=body, authenticated=True, typed=True))

    async def verify_account_security_detailed(self, *, body: VerifySecurity) -> Response[ErrorEnvelope | VerifiedSecurity]:
        """Generated verify_account_security operation."""
        return cast(Response[ErrorEnvelope | VerifiedSecurity], await self._owner.async_call_generated('verify_account_security', parameters={}, body=body, authenticated=True, detailed=True))
