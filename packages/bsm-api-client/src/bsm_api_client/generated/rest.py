"""Typed REST interface generated from the bundled OpenAPI contract."""

from .models.access_policy_info import AccessPolicyInfo
from .models.access_preview import AccessPreview
from .models.access_server_info import AccessServerInfo
from .models.account_server_access_info import AccountServerAccessInfo
from .models.add_players_manually_response import AddPlayersManuallyResponse
from .models.add_players_payload import AddPlayersPayload
from .models.add_server_ban_response import AddServerBanResponse
from .models.add_to_allowlist_response import AddToAllowlistResponse
from .models.addon_action_payload import AddonActionPayload
from .models.addon_reorder_payload import AddonReorderPayload
from .models.addon_subpack_payload import AddonSubpackPayload
from .models.allowlist_add_payload import AllowlistAddPayload
from .models.allowlist_remove_payload import AllowlistRemovePayload
from .models.audit_log_response import AuditLogResponse
from .models.backup_health_response import BackupHealthResponse
from .models.backup_key_info import BackupKeyInfo
from .models.backup_keys_info import BackupKeysInfo
from .models.ban_add_request import BanAddRequest
from .models.ban_remove_request import BanRemoveRequest
from .models.base_api_response import BaseApiResponse
from .models.body_import_server_snapshot import BodyImportServerSnapshot
from .models.body_login import BodyLogin
from .models.body_upload_content_file import BodyUploadContentFile
from .models.change_password_payload import ChangePasswordPayload
from .models.command_payload import CommandPayload
from .models.compare_diagnostic_snapshots_request import CompareDiagnosticSnapshotsRequest
from .models.compare_diagnostic_snapshots_response import CompareDiagnosticSnapshotsResponse
from .models.complete_passkey_registration import CompletePasskeyRegistration
from .models.content_upload_response import ContentUploadResponse
from .models.control_schedule_payload import ControlSchedulePayload
from .models.create_integration_token import CreateIntegrationToken
from .models.created_integration_token import CreatedIntegrationToken
from .models.current_account_response import CurrentAccountResponse
from .models.custom_zips_response import CustomZipsResponse
from .models.delete_content_file_category import DeleteContentFileCategory
from .models.destination_cleanup_payload import DestinationCleanupPayload
from .models.download_content_file_category import DownloadContentFileCategory
from .models.error_envelope import ErrorEnvelope
from .models.event_catalog import EventCatalog
from .models.event_diagnostics import EventDiagnostics
from .models.factor_code import FactorCode
from .models.factor_enrollment import FactorEnrollment
from .models.file_name_payload import FileNamePayload
from .models.generate_token_payload import GenerateTokenPayload
from .models.get_all_global_settings_response import GetAllGlobalSettingsResponse
from .models.get_all_known_players_response import GetAllKnownPlayersResponse
from .models.get_all_server_settings_response import GetAllServerSettingsResponse
from .models.get_all_servers_data_response import GetAllServersDataResponse
from .models.get_allowlist_response import GetAllowlistResponse
from .models.get_application_diagnostics_response import GetApplicationDiagnosticsResponse
from .models.get_application_health_response import GetApplicationHealthResponse
from .models.get_application_metrics_response import GetApplicationMetricsResponse
from .models.get_bedrock_process_info_response import GetBedrockProcessInfoResponse
from .models.get_diagnostic_activity_phase_type_0 import GetDiagnosticActivityPhaseType0
from .models.get_diagnostic_activity_response import GetDiagnosticActivityResponse
from .models.get_diagnostic_activity_status_type_0 import GetDiagnosticActivityStatusType0
from .models.get_diagnostic_history_outcome_type_0 import GetDiagnosticHistoryOutcomeType0
from .models.get_diagnostic_history_response import GetDiagnosticHistoryResponse
from .models.get_diagnostic_report_response import GetDiagnosticReportResponse
from .models.get_diagnostic_runs_response import GetDiagnosticRunsResponse
from .models.get_diagnostic_trace_response import GetDiagnosticTraceResponse
from .models.get_event_activity_phase_type_0 import GetEventActivityPhaseType0
from .models.get_event_activity_status_type_0 import GetEventActivityStatusType0
from .models.get_permissions_response import GetPermissionsResponse
from .models.get_plugin_settings_response import GetPluginSettingsResponse
from .models.get_plugin_settings_scope import GetPluginSettingsScope
from .models.get_plugin_statuses_response import GetPluginStatusesResponse
from .models.get_properties_response import GetPropertiesResponse
from .models.get_raw_properties_response import GetRawPropertiesResponse
from .models.get_server_bans_response import GetServerBansResponse
from .models.get_server_process_response import GetServerProcessResponse
from .models.get_server_running_status_response import GetServerRunningStatusResponse
from .models.get_system_and_app_info_response import GetSystemAndAppInfoResponse
from .models.install_confirmation_response import InstallConfirmationResponse
from .models.install_server_payload import InstallServerPayload
from .models.installation_accepted_response import InstallationAcceptedResponse
from .models.integration_token_info import IntegrationTokenInfo
from .models.list_account_integration_tokens_status import ListAccountIntegrationTokensStatus
from .models.list_available_addons_response import ListAvailableAddonsResponse
from .models.list_available_worlds_response import ListAvailableWorldsResponse
from .models.list_backup_files_response import ListBackupFilesResponse
from .models.list_installed_addons_response import ListInstalledAddonsResponse
from .models.list_integration_tokens_status import ListIntegrationTokensStatus
from .models.list_schedules_response import ListSchedulesResponse
from .models.list_snapshots_response import ListSnapshotsResponse
from .models.log_history_page import LogHistoryPage
from .models.login_session_info import LoginSessionInfo
from .models.manage_snapshot_response import ManageSnapshotResponse
from .models.passkey_info import PasskeyInfo
from .models.passkey_login_options_request import PasskeyLoginOptionsRequest
from .models.passkey_login_verify_request import PasskeyLoginVerifyRequest
from .models.passkey_options_response import PasskeyOptionsResponse
from .models.permissions_set_payload import PermissionsSetPayload
from .models.permissions_update_response import PermissionsUpdateResponse
from .models.plugin_pages_response import PluginPagesResponse
from .models.plugin_settings_payload import PluginSettingsPayload
from .models.plugin_status_set_payload import PluginStatusSetPayload
from .models.profile_update_payload import ProfileUpdatePayload
from .models.properties_payload import PropertiesPayload
from .models.prune_download_cache_response import PruneDownloadCacheResponse
from .models.prune_downloads_payload import PruneDownloadsPayload
from .models.recovery_codes import RecoveryCodes
from .models.recovery_report_response import RecoveryReportResponse
from .models.registration_response import RegistrationResponse
from .models.reload_global_settings_response import ReloadGlobalSettingsResponse
from .models.reload_plugins_response import ReloadPluginsResponse
from .models.reload_single_plugin_response import ReloadSinglePluginResponse
from .models.remove_from_allowlist_response import RemoveFromAllowlistResponse
from .models.remove_server_ban_response import RemoveServerBanResponse
from .models.rename_passkey import RenamePasskey
from .models.rename_session import RenameSession
from .models.restart_server_response import RestartServerResponse
from .models.restore_action_payload import RestoreActionPayload
from .models.restore_recovery_response import RestoreRecoveryResponse
from .models.revoke_sessions import RevokeSessions
from .models.revoke_trusted_devices import RevokeTrustedDevices
from .models.runtime_status import RuntimeStatus
from .models.scan_and_update_player_db_response import ScanAndUpdatePlayerDbResponse
from .models.scheduled_task import ScheduledTask
from .models.security_event_info import SecurityEventInfo
from .models.security_status import SecurityStatus
from .models.send_command_response import SendCommandResponse
from .models.server_setting_item_payload import ServerSettingItemPayload
from .models.server_summary import ServerSummary
from .models.set_global_setting_response import SetGlobalSettingResponse
from .models.set_plugin_setting_response import SetPluginSettingResponse
from .models.set_plugin_status_response import SetPluginStatusResponse
from .models.set_properties_response import SetPropertiesResponse
from .models.set_server_access import SetServerAccess
from .models.set_server_setting_response import SetServerSettingResponse
from .models.setting_item_payload import SettingItemPayload
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
from .models.trigger_external_app_event_response import TriggerExternalAppEventResponse
from .models.trusted_device_info import TrustedDeviceInfo
from .models.update_user_role_payload import UpdateUserRolePayload
from .models.user_login_payload import UserLoginPayload
from .models.user_response import UserResponse
from .models.verified_security import VerifiedSecurity
from .models.verify_passkey_assertion import VerifyPasskeyAssertion
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

    async def add_players(self, *, body: AddPlayersPayload) -> AddPlayersManuallyResponse | ErrorEnvelope | None:
        """Generated add_players operation."""
        return cast(AddPlayersManuallyResponse | ErrorEnvelope | None, await self._owner.async_call_generated('add_players', parameters={}, body=body, authenticated=True, typed=True))

    async def add_players_detailed(self, *, body: AddPlayersPayload) -> Response[AddPlayersManuallyResponse | ErrorEnvelope]:
        """Generated add_players operation."""
        return cast(Response[AddPlayersManuallyResponse | ErrorEnvelope], await self._owner.async_call_generated('add_players', parameters={}, body=body, authenticated=True, detailed=True))

    async def add_server_ban(self, server_name: str, *, body: BanAddRequest) -> AddServerBanResponse | ErrorEnvelope | None:
        """Generated add_server_ban operation."""
        return cast(AddServerBanResponse | ErrorEnvelope | None, await self._owner.async_call_generated('add_server_ban', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def add_server_ban_detailed(self, server_name: str, *, body: BanAddRequest) -> Response[AddServerBanResponse | ErrorEnvelope]:
        """Generated add_server_ban operation."""
        return cast(Response[AddServerBanResponse | ErrorEnvelope], await self._owner.async_call_generated('add_server_ban', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

    async def begin_passkey_login(self, *, body: None | PasskeyLoginOptionsRequest | Unset=UNSET) -> ErrorEnvelope | PasskeyOptionsResponse | None:
        """Generated begin_passkey_login operation."""
        return cast(ErrorEnvelope | PasskeyOptionsResponse | None, await self._owner.async_call_generated('begin_passkey_login', parameters={}, body=body, authenticated=False, typed=True))

    async def begin_passkey_login_detailed(self, *, body: None | PasskeyLoginOptionsRequest | Unset=UNSET) -> Response[ErrorEnvelope | PasskeyOptionsResponse]:
        """Generated begin_passkey_login operation."""
        return cast(Response[ErrorEnvelope | PasskeyOptionsResponse], await self._owner.async_call_generated('begin_passkey_login', parameters={}, body=body, authenticated=False, detailed=True))

    async def begin_passkey_registration(self) -> ErrorEnvelope | PasskeyOptionsResponse | None:
        """Generated begin_passkey_registration operation."""
        return cast(ErrorEnvelope | PasskeyOptionsResponse | None, await self._owner.async_call_generated('begin_passkey_registration', parameters={}, body=None, authenticated=True, typed=True))

    async def begin_passkey_registration_detailed(self) -> Response[ErrorEnvelope | PasskeyOptionsResponse]:
        """Generated begin_passkey_registration operation."""
        return cast(Response[ErrorEnvelope | PasskeyOptionsResponse], await self._owner.async_call_generated('begin_passkey_registration', parameters={}, body=None, authenticated=True, detailed=True))

    async def begin_passkey_step_up(self) -> ErrorEnvelope | PasskeyOptionsResponse | None:
        """Generated begin_passkey_step_up operation."""
        return cast(ErrorEnvelope | PasskeyOptionsResponse | None, await self._owner.async_call_generated('begin_passkey_step_up', parameters={}, body=None, authenticated=True, typed=True))

    async def begin_passkey_step_up_detailed(self) -> Response[ErrorEnvelope | PasskeyOptionsResponse]:
        """Generated begin_passkey_step_up operation."""
        return cast(Response[ErrorEnvelope | PasskeyOptionsResponse], await self._owner.async_call_generated('begin_passkey_step_up', parameters={}, body=None, authenticated=True, detailed=True))

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

    async def compare_diagnostic_snapshots(self, *, body: CompareDiagnosticSnapshotsRequest) -> CompareDiagnosticSnapshotsResponse | ErrorEnvelope | None:
        """Generated compare_diagnostic_snapshots operation."""
        return cast(CompareDiagnosticSnapshotsResponse | ErrorEnvelope | None, await self._owner.async_call_generated('compare_diagnostic_snapshots', parameters={}, body=body, authenticated=True, typed=True))

    async def compare_diagnostic_snapshots_detailed(self, *, body: CompareDiagnosticSnapshotsRequest) -> Response[CompareDiagnosticSnapshotsResponse | ErrorEnvelope]:
        """Generated compare_diagnostic_snapshots operation."""
        return cast(Response[CompareDiagnosticSnapshotsResponse | ErrorEnvelope], await self._owner.async_call_generated('compare_diagnostic_snapshots', parameters={}, body=body, authenticated=True, detailed=True))

    async def complete_passkey_login(self, *, body: PasskeyLoginVerifyRequest) -> ErrorEnvelope | TokenResponse | None:
        """Generated complete_passkey_login operation."""
        return cast(ErrorEnvelope | TokenResponse | None, await self._owner.async_call_generated('complete_passkey_login', parameters={}, body=body, authenticated=False, typed=True))

    async def complete_passkey_login_detailed(self, *, body: PasskeyLoginVerifyRequest) -> Response[ErrorEnvelope | TokenResponse]:
        """Generated complete_passkey_login operation."""
        return cast(Response[ErrorEnvelope | TokenResponse], await self._owner.async_call_generated('complete_passkey_login', parameters={}, body=body, authenticated=False, detailed=True))

    async def complete_passkey_registration(self, *, body: CompletePasskeyRegistration) -> ErrorEnvelope | PasskeyInfo | None:
        """Generated complete_passkey_registration operation."""
        return cast(ErrorEnvelope | PasskeyInfo | None, await self._owner.async_call_generated('complete_passkey_registration', parameters={}, body=body, authenticated=True, typed=True))

    async def complete_passkey_registration_detailed(self, *, body: CompletePasskeyRegistration) -> Response[ErrorEnvelope | PasskeyInfo]:
        """Generated complete_passkey_registration operation."""
        return cast(Response[ErrorEnvelope | PasskeyInfo], await self._owner.async_call_generated('complete_passkey_registration', parameters={}, body=body, authenticated=True, detailed=True))

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

    async def create_first_user(self, *, body: UserLoginPayload) -> ErrorEnvelope | TokenResponse | None:
        """Generated create_first_user operation."""
        return cast(ErrorEnvelope | TokenResponse | None, await self._owner.async_call_generated('create_first_user', parameters={}, body=body, authenticated=False, typed=True))

    async def create_first_user_detailed(self, *, body: UserLoginPayload) -> Response[ErrorEnvelope | TokenResponse]:
        """Generated create_first_user operation."""
        return cast(Response[ErrorEnvelope | TokenResponse], await self._owner.async_call_generated('create_first_user', parameters={}, body=body, authenticated=False, detailed=True))

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

    async def delete_content_file(self, category: DeleteContentFileCategory, filename: str) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated delete_content_file operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('delete_content_file', parameters={'category': category, 'filename': filename}, body=None, authenticated=True, typed=True))

    async def delete_content_file_detailed(self, category: DeleteContentFileCategory, filename: str) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated delete_content_file operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('delete_content_file', parameters={'category': category, 'filename': filename}, body=None, authenticated=True, detailed=True))

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

    async def delete_server_snapshot(self, server_name: str, backup_id: str) -> ErrorEnvelope | ManageSnapshotResponse | None:
        """Generated delete_server_snapshot operation."""
        return cast(ErrorEnvelope | ManageSnapshotResponse | None, await self._owner.async_call_generated('delete_server_snapshot', parameters={'server_name': server_name, 'backup_id': backup_id}, body=None, authenticated=True, typed=True))

    async def delete_server_snapshot_detailed(self, server_name: str, backup_id: str) -> Response[ErrorEnvelope | ManageSnapshotResponse]:
        """Generated delete_server_snapshot operation."""
        return cast(Response[ErrorEnvelope | ManageSnapshotResponse], await self._owner.async_call_generated('delete_server_snapshot', parameters={'server_name': server_name, 'backup_id': backup_id}, body=None, authenticated=True, detailed=True))

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

    async def download_content_file(self, category: DownloadContentFileCategory, filename: str) -> ErrorEnvelope | File | None:
        """Generated download_content_file operation."""
        return cast(ErrorEnvelope | File | None, await self._owner.async_call_generated('download_content_file', parameters={'category': category, 'filename': filename}, body=None, authenticated=True, typed=True))

    async def download_content_file_detailed(self, category: DownloadContentFileCategory, filename: str) -> Response[ErrorEnvelope | File]:
        """Generated download_content_file operation."""
        return cast(Response[ErrorEnvelope | File], await self._owner.async_call_generated('download_content_file', parameters={'category': category, 'filename': filename}, body=None, authenticated=True, detailed=True))

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

    async def get_application_diagnostics(self) -> ErrorEnvelope | GetApplicationDiagnosticsResponse | None:
        """Generated get_application_diagnostics operation."""
        return cast(ErrorEnvelope | GetApplicationDiagnosticsResponse | None, await self._owner.async_call_generated('get_application_diagnostics', parameters={}, body=None, authenticated=True, typed=True))

    async def get_application_diagnostics_detailed(self) -> Response[ErrorEnvelope | GetApplicationDiagnosticsResponse]:
        """Generated get_application_diagnostics operation."""
        return cast(Response[ErrorEnvelope | GetApplicationDiagnosticsResponse], await self._owner.async_call_generated('get_application_diagnostics', parameters={}, body=None, authenticated=True, detailed=True))

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

    async def get_diagnostic_activity(self, *, operation_id: None | str | Unset=UNSET, sequence_id: None | str | Unset=UNSET, operation_name: None | str | Unset=UNSET, server_name: None | str | Unset=UNSET, source: None | str | Unset=UNSET, phase: GetDiagnosticActivityPhaseType0 | None | Unset=UNSET, name: None | str | Unset=UNSET, owner: None | str | Unset=UNSET, correlation_id: None | str | Unset=UNSET, status: GetDiagnosticActivityStatusType0 | None | Unset=UNSET, limit: int | Unset=100) -> ErrorEnvelope | GetDiagnosticActivityResponse | None:
        """Generated get_diagnostic_activity operation."""
        return cast(ErrorEnvelope | GetDiagnosticActivityResponse | None, await self._owner.async_call_generated('get_diagnostic_activity', parameters={'operation_id': operation_id, 'sequence_id': sequence_id, 'operation_name': operation_name, 'server_name': server_name, 'source': source, 'phase': phase, 'name': name, 'owner': owner, 'correlation_id': correlation_id, 'status': status, 'limit': limit}, body=None, authenticated=True, typed=True))

    async def get_diagnostic_activity_detailed(self, *, operation_id: None | str | Unset=UNSET, sequence_id: None | str | Unset=UNSET, operation_name: None | str | Unset=UNSET, server_name: None | str | Unset=UNSET, source: None | str | Unset=UNSET, phase: GetDiagnosticActivityPhaseType0 | None | Unset=UNSET, name: None | str | Unset=UNSET, owner: None | str | Unset=UNSET, correlation_id: None | str | Unset=UNSET, status: GetDiagnosticActivityStatusType0 | None | Unset=UNSET, limit: int | Unset=100) -> Response[ErrorEnvelope | GetDiagnosticActivityResponse]:
        """Generated get_diagnostic_activity operation."""
        return cast(Response[ErrorEnvelope | GetDiagnosticActivityResponse], await self._owner.async_call_generated('get_diagnostic_activity', parameters={'operation_id': operation_id, 'sequence_id': sequence_id, 'operation_name': operation_name, 'server_name': server_name, 'source': source, 'phase': phase, 'name': name, 'owner': owner, 'correlation_id': correlation_id, 'status': status, 'limit': limit}, body=None, authenticated=True, detailed=True))

    async def get_diagnostic_history(self, *, limit: int | Unset=100, subsystem: None | str | Unset=UNSET, instance_id: None | str | Unset=UNSET, correlation_id: None | str | Unset=UNSET, cursor: None | str | Unset=UNSET, owner: None | str | Unset=UNSET, code: None | str | Unset=UNSET, outcome: GetDiagnosticHistoryOutcomeType0 | None | Unset=UNSET, operation_id: None | str | Unset=UNSET) -> ErrorEnvelope | GetDiagnosticHistoryResponse | None:
        """Generated get_diagnostic_history operation."""
        return cast(ErrorEnvelope | GetDiagnosticHistoryResponse | None, await self._owner.async_call_generated('get_diagnostic_history', parameters={'limit': limit, 'subsystem': subsystem, 'instance_id': instance_id, 'correlation_id': correlation_id, 'cursor': cursor, 'owner': owner, 'code': code, 'outcome': outcome, 'operation_id': operation_id}, body=None, authenticated=True, typed=True))

    async def get_diagnostic_history_detailed(self, *, limit: int | Unset=100, subsystem: None | str | Unset=UNSET, instance_id: None | str | Unset=UNSET, correlation_id: None | str | Unset=UNSET, cursor: None | str | Unset=UNSET, owner: None | str | Unset=UNSET, code: None | str | Unset=UNSET, outcome: GetDiagnosticHistoryOutcomeType0 | None | Unset=UNSET, operation_id: None | str | Unset=UNSET) -> Response[ErrorEnvelope | GetDiagnosticHistoryResponse]:
        """Generated get_diagnostic_history operation."""
        return cast(Response[ErrorEnvelope | GetDiagnosticHistoryResponse], await self._owner.async_call_generated('get_diagnostic_history', parameters={'limit': limit, 'subsystem': subsystem, 'instance_id': instance_id, 'correlation_id': correlation_id, 'cursor': cursor, 'owner': owner, 'code': code, 'outcome': outcome, 'operation_id': operation_id}, body=None, authenticated=True, detailed=True))

    async def get_diagnostic_report(self) -> ErrorEnvelope | GetDiagnosticReportResponse | None:
        """Generated get_diagnostic_report operation."""
        return cast(ErrorEnvelope | GetDiagnosticReportResponse | None, await self._owner.async_call_generated('get_diagnostic_report', parameters={}, body=None, authenticated=True, typed=True))

    async def get_diagnostic_report_detailed(self) -> Response[ErrorEnvelope | GetDiagnosticReportResponse]:
        """Generated get_diagnostic_report operation."""
        return cast(Response[ErrorEnvelope | GetDiagnosticReportResponse], await self._owner.async_call_generated('get_diagnostic_report', parameters={}, body=None, authenticated=True, detailed=True))

    async def get_diagnostic_runs(self, *, limit: int | Unset=20) -> ErrorEnvelope | GetDiagnosticRunsResponse | None:
        """Generated get_diagnostic_runs operation."""
        return cast(ErrorEnvelope | GetDiagnosticRunsResponse | None, await self._owner.async_call_generated('get_diagnostic_runs', parameters={'limit': limit}, body=None, authenticated=True, typed=True))

    async def get_diagnostic_runs_detailed(self, *, limit: int | Unset=20) -> Response[ErrorEnvelope | GetDiagnosticRunsResponse]:
        """Generated get_diagnostic_runs operation."""
        return cast(Response[ErrorEnvelope | GetDiagnosticRunsResponse], await self._owner.async_call_generated('get_diagnostic_runs', parameters={'limit': limit}, body=None, authenticated=True, detailed=True))

    async def get_diagnostic_trace(self, correlation_id: str, *, limit: int | Unset=100, cursor: None | str | Unset=UNSET) -> ErrorEnvelope | GetDiagnosticTraceResponse | None:
        """Generated get_diagnostic_trace operation."""
        return cast(ErrorEnvelope | GetDiagnosticTraceResponse | None, await self._owner.async_call_generated('get_diagnostic_trace', parameters={'correlation_id': correlation_id, 'limit': limit, 'cursor': cursor}, body=None, authenticated=True, typed=True))

    async def get_diagnostic_trace_detailed(self, correlation_id: str, *, limit: int | Unset=100, cursor: None | str | Unset=UNSET) -> Response[ErrorEnvelope | GetDiagnosticTraceResponse]:
        """Generated get_diagnostic_trace operation."""
        return cast(Response[ErrorEnvelope | GetDiagnosticTraceResponse], await self._owner.async_call_generated('get_diagnostic_trace', parameters={'correlation_id': correlation_id, 'limit': limit, 'cursor': cursor}, body=None, authenticated=True, detailed=True))

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

    async def get_panorama(self) -> ErrorEnvelope | File | None:
        """Generated get_panorama operation."""
        return cast(ErrorEnvelope | File | None, await self._owner.async_call_generated('get_panorama', parameters={}, body=None, authenticated=False, typed=True))

    async def get_panorama_detailed(self) -> Response[ErrorEnvelope | File]:
        """Generated get_panorama operation."""
        return cast(Response[ErrorEnvelope | File], await self._owner.async_call_generated('get_panorama', parameters={}, body=None, authenticated=False, detailed=True))

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

    async def get_server_addon_icon(self, server_name: str, *, pack_type: str, uuid: str) -> ErrorEnvelope | File | None:
        """Generated get_server_addon_icon operation."""
        return cast(ErrorEnvelope | File | None, await self._owner.async_call_generated('get_server_addon_icon', parameters={'server_name': server_name, 'pack_type': pack_type, 'uuid': uuid}, body=None, authenticated=True, typed=True))

    async def get_server_addon_icon_detailed(self, server_name: str, *, pack_type: str, uuid: str) -> Response[ErrorEnvelope | File]:
        """Generated get_server_addon_icon operation."""
        return cast(Response[ErrorEnvelope | File], await self._owner.async_call_generated('get_server_addon_icon', parameters={'server_name': server_name, 'pack_type': pack_type, 'uuid': uuid}, body=None, authenticated=True, detailed=True))

    async def get_server_bans(self, server_name: str) -> ErrorEnvelope | GetServerBansResponse | None:
        """Generated get_server_bans operation."""
        return cast(ErrorEnvelope | GetServerBansResponse | None, await self._owner.async_call_generated('get_server_bans', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def get_server_bans_detailed(self, server_name: str) -> Response[ErrorEnvelope | GetServerBansResponse]:
        """Generated get_server_bans operation."""
        return cast(Response[ErrorEnvelope | GetServerBansResponse], await self._owner.async_call_generated('get_server_bans', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def get_server_process(self, server_name: str) -> ErrorEnvelope | GetServerProcessResponse | None:
        """Generated get_server_process operation."""
        return cast(ErrorEnvelope | GetServerProcessResponse | None, await self._owner.async_call_generated('get_server_process', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def get_server_process_detailed(self, server_name: str) -> Response[ErrorEnvelope | GetServerProcessResponse]:
        """Generated get_server_process operation."""
        return cast(Response[ErrorEnvelope | GetServerProcessResponse], await self._owner.async_call_generated('get_server_process', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def get_server_process_info(self, server_name: str) -> ErrorEnvelope | GetBedrockProcessInfoResponse | None:
        """Generated get_server_process_info operation."""
        return cast(ErrorEnvelope | GetBedrockProcessInfoResponse | None, await self._owner.async_call_generated('get_server_process_info', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def get_server_process_info_detailed(self, server_name: str) -> Response[ErrorEnvelope | GetBedrockProcessInfoResponse]:
        """Generated get_server_process_info operation."""
        return cast(Response[ErrorEnvelope | GetBedrockProcessInfoResponse], await self._owner.async_call_generated('get_server_process_info', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def get_server_settings(self, server_name: str) -> ErrorEnvelope | GetAllServerSettingsResponse | None:
        """Generated get_server_settings operation."""
        return cast(ErrorEnvelope | GetAllServerSettingsResponse | None, await self._owner.async_call_generated('get_server_settings', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def get_server_settings_detailed(self, server_name: str) -> Response[ErrorEnvelope | GetAllServerSettingsResponse]:
        """Generated get_server_settings operation."""
        return cast(Response[ErrorEnvelope | GetAllServerSettingsResponse], await self._owner.async_call_generated('get_server_settings', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def get_server_status(self, server_name: str) -> ErrorEnvelope | GetServerRunningStatusResponse | None:
        """Generated get_server_status operation."""
        return cast(ErrorEnvelope | GetServerRunningStatusResponse | None, await self._owner.async_call_generated('get_server_status', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def get_server_status_detailed(self, server_name: str) -> Response[ErrorEnvelope | GetServerRunningStatusResponse]:
        """Generated get_server_status operation."""
        return cast(Response[ErrorEnvelope | GetServerRunningStatusResponse], await self._owner.async_call_generated('get_server_status', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def get_server_summary(self, server_name: str) -> ErrorEnvelope | ServerSummary | None:
        """Generated get_server_summary operation."""
        return cast(ErrorEnvelope | ServerSummary | None, await self._owner.async_call_generated('get_server_summary', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def get_server_summary_detailed(self, server_name: str) -> Response[ErrorEnvelope | ServerSummary]:
        """Generated get_server_summary operation."""
        return cast(Response[ErrorEnvelope | ServerSummary], await self._owner.async_call_generated('get_server_summary', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def get_settings(self) -> ErrorEnvelope | GetAllGlobalSettingsResponse | None:
        """Generated get_settings operation."""
        return cast(ErrorEnvelope | GetAllGlobalSettingsResponse | None, await self._owner.async_call_generated('get_settings', parameters={}, body=None, authenticated=True, typed=True))

    async def get_settings_detailed(self) -> Response[ErrorEnvelope | GetAllGlobalSettingsResponse]:
        """Generated get_settings operation."""
        return cast(Response[ErrorEnvelope | GetAllGlobalSettingsResponse], await self._owner.async_call_generated('get_settings', parameters={}, body=None, authenticated=True, detailed=True))

    async def get_setup_status(self) -> ErrorEnvelope | SetupStatusResponse | None:
        """Generated get_setup_status operation."""
        return cast(ErrorEnvelope | SetupStatusResponse | None, await self._owner.async_call_generated('get_setup_status', parameters={}, body=None, authenticated=False, typed=True))

    async def get_setup_status_detailed(self) -> Response[ErrorEnvelope | SetupStatusResponse]:
        """Generated get_setup_status operation."""
        return cast(Response[ErrorEnvelope | SetupStatusResponse], await self._owner.async_call_generated('get_setup_status', parameters={}, body=None, authenticated=False, detailed=True))

    async def get_subsystem_diagnostics(self, subsystem: str) -> ErrorEnvelope | GetApplicationDiagnosticsResponse | None:
        """Generated get_subsystem_diagnostics operation."""
        return cast(ErrorEnvelope | GetApplicationDiagnosticsResponse | None, await self._owner.async_call_generated('get_subsystem_diagnostics', parameters={'subsystem': subsystem}, body=None, authenticated=True, typed=True))

    async def get_subsystem_diagnostics_detailed(self, subsystem: str) -> Response[ErrorEnvelope | GetApplicationDiagnosticsResponse]:
        """Generated get_subsystem_diagnostics operation."""
        return cast(Response[ErrorEnvelope | GetApplicationDiagnosticsResponse], await self._owner.async_call_generated('get_subsystem_diagnostics', parameters={'subsystem': subsystem}, body=None, authenticated=True, detailed=True))

    async def get_system_info(self) -> ErrorEnvelope | GetSystemAndAppInfoResponse | None:
        """Generated get_system_info operation."""
        return cast(ErrorEnvelope | GetSystemAndAppInfoResponse | None, await self._owner.async_call_generated('get_system_info', parameters={}, body=None, authenticated=False, typed=True))

    async def get_system_info_detailed(self) -> Response[ErrorEnvelope | GetSystemAndAppInfoResponse]:
        """Generated get_system_info operation."""
        return cast(Response[ErrorEnvelope | GetSystemAndAppInfoResponse], await self._owner.async_call_generated('get_system_info', parameters={}, body=None, authenticated=False, detailed=True))

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

    async def get_world_icon(self, server_name: str) -> ErrorEnvelope | File | None:
        """Generated get_world_icon operation."""
        return cast(ErrorEnvelope | File | None, await self._owner.async_call_generated('get_world_icon', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def get_world_icon_detailed(self, server_name: str) -> Response[ErrorEnvelope | File]:
        """Generated get_world_icon operation."""
        return cast(Response[ErrorEnvelope | File], await self._owner.async_call_generated('get_world_icon', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

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

    async def list_account_integration_tokens(self, user_id: int, *, limit: int | Unset=100, offset: int | Unset=0, status: ListAccountIntegrationTokensStatus | Unset=ListAccountIntegrationTokensStatus.ALL) -> ErrorEnvelope | list[IntegrationTokenInfo] | None:
        """Generated list_account_integration_tokens operation."""
        return cast(ErrorEnvelope | list[IntegrationTokenInfo] | None, await self._owner.async_call_generated('list_account_integration_tokens', parameters={'user_id': user_id, 'limit': limit, 'offset': offset, 'status': status}, body=None, authenticated=True, typed=True))

    async def list_account_integration_tokens_detailed(self, user_id: int, *, limit: int | Unset=100, offset: int | Unset=0, status: ListAccountIntegrationTokensStatus | Unset=ListAccountIntegrationTokensStatus.ALL) -> Response[ErrorEnvelope | list[IntegrationTokenInfo]]:
        """Generated list_account_integration_tokens operation."""
        return cast(Response[ErrorEnvelope | list[IntegrationTokenInfo]], await self._owner.async_call_generated('list_account_integration_tokens', parameters={'user_id': user_id, 'limit': limit, 'offset': offset, 'status': status}, body=None, authenticated=True, detailed=True))

    async def list_account_login_sessions(self, user_id: int) -> ErrorEnvelope | list[LoginSessionInfo] | None:
        """Generated list_account_login_sessions operation."""
        return cast(ErrorEnvelope | list[LoginSessionInfo] | None, await self._owner.async_call_generated('list_account_login_sessions', parameters={'user_id': user_id}, body=None, authenticated=True, typed=True))

    async def list_account_login_sessions_detailed(self, user_id: int) -> Response[ErrorEnvelope | list[LoginSessionInfo]]:
        """Generated list_account_login_sessions operation."""
        return cast(Response[ErrorEnvelope | list[LoginSessionInfo]], await self._owner.async_call_generated('list_account_login_sessions', parameters={'user_id': user_id}, body=None, authenticated=True, detailed=True))

    async def list_account_passkeys(self, user_id: int) -> ErrorEnvelope | list[PasskeyInfo] | None:
        """Generated list_account_passkeys operation."""
        return cast(ErrorEnvelope | list[PasskeyInfo] | None, await self._owner.async_call_generated('list_account_passkeys', parameters={'user_id': user_id}, body=None, authenticated=True, typed=True))

    async def list_account_passkeys_detailed(self, user_id: int) -> Response[ErrorEnvelope | list[PasskeyInfo]]:
        """Generated list_account_passkeys operation."""
        return cast(Response[ErrorEnvelope | list[PasskeyInfo]], await self._owner.async_call_generated('list_account_passkeys', parameters={'user_id': user_id}, body=None, authenticated=True, detailed=True))

    async def list_application_events(self) -> ErrorEnvelope | EventCatalog | None:
        """Generated list_application_events operation."""
        return cast(ErrorEnvelope | EventCatalog | None, await self._owner.async_call_generated('list_application_events', parameters={}, body=None, authenticated=True, typed=True))

    async def list_application_events_detailed(self) -> Response[ErrorEnvelope | EventCatalog]:
        """Generated list_application_events operation."""
        return cast(Response[ErrorEnvelope | EventCatalog], await self._owner.async_call_generated('list_application_events', parameters={}, body=None, authenticated=True, detailed=True))

    async def list_audit_logs(self, *, limit: int | Unset=100, offset: int | Unset=0) -> ErrorEnvelope | list[AuditLogResponse] | None:
        """Generated list_audit_logs operation."""
        return cast(ErrorEnvelope | list[AuditLogResponse] | None, await self._owner.async_call_generated('list_audit_logs', parameters={'limit': limit, 'offset': offset}, body=None, authenticated=True, typed=True))

    async def list_audit_logs_detailed(self, *, limit: int | Unset=100, offset: int | Unset=0) -> Response[ErrorEnvelope | list[AuditLogResponse]]:
        """Generated list_audit_logs operation."""
        return cast(Response[ErrorEnvelope | list[AuditLogResponse]], await self._owner.async_call_generated('list_audit_logs', parameters={'limit': limit, 'offset': offset}, body=None, authenticated=True, detailed=True))

    async def list_available_addons(self) -> ErrorEnvelope | ListAvailableAddonsResponse | None:
        """Generated list_available_addons operation."""
        return cast(ErrorEnvelope | ListAvailableAddonsResponse | None, await self._owner.async_call_generated('list_available_addons', parameters={}, body=None, authenticated=True, typed=True))

    async def list_available_addons_detailed(self) -> Response[ErrorEnvelope | ListAvailableAddonsResponse]:
        """Generated list_available_addons operation."""
        return cast(Response[ErrorEnvelope | ListAvailableAddonsResponse], await self._owner.async_call_generated('list_available_addons', parameters={}, body=None, authenticated=True, detailed=True))

    async def list_available_worlds(self) -> ErrorEnvelope | ListAvailableWorldsResponse | None:
        """Generated list_available_worlds operation."""
        return cast(ErrorEnvelope | ListAvailableWorldsResponse | None, await self._owner.async_call_generated('list_available_worlds', parameters={}, body=None, authenticated=True, typed=True))

    async def list_available_worlds_detailed(self) -> Response[ErrorEnvelope | ListAvailableWorldsResponse]:
        """Generated list_available_worlds operation."""
        return cast(Response[ErrorEnvelope | ListAvailableWorldsResponse], await self._owner.async_call_generated('list_available_worlds', parameters={}, body=None, authenticated=True, detailed=True))

    async def list_backup_keys(self) -> BackupKeysInfo | ErrorEnvelope | None:
        """Generated list_backup_keys operation."""
        return cast(BackupKeysInfo | ErrorEnvelope | None, await self._owner.async_call_generated('list_backup_keys', parameters={}, body=None, authenticated=True, typed=True))

    async def list_backup_keys_detailed(self) -> Response[BackupKeysInfo | ErrorEnvelope]:
        """Generated list_backup_keys operation."""
        return cast(Response[BackupKeysInfo | ErrorEnvelope], await self._owner.async_call_generated('list_backup_keys', parameters={}, body=None, authenticated=True, detailed=True))

    async def list_downloads(self) -> CustomZipsResponse | ErrorEnvelope | None:
        """Generated list_downloads operation."""
        return cast(CustomZipsResponse | ErrorEnvelope | None, await self._owner.async_call_generated('list_downloads', parameters={}, body=None, authenticated=True, typed=True))

    async def list_downloads_detailed(self) -> Response[CustomZipsResponse | ErrorEnvelope]:
        """Generated list_downloads operation."""
        return cast(Response[CustomZipsResponse | ErrorEnvelope], await self._owner.async_call_generated('list_downloads', parameters={}, body=None, authenticated=True, detailed=True))

    async def list_integration_tokens(self, *, limit: int | Unset=100, offset: int | Unset=0, status: ListIntegrationTokensStatus | Unset=ListIntegrationTokensStatus.ALL) -> ErrorEnvelope | list[IntegrationTokenInfo] | None:
        """Generated list_integration_tokens operation."""
        return cast(ErrorEnvelope | list[IntegrationTokenInfo] | None, await self._owner.async_call_generated('list_integration_tokens', parameters={'limit': limit, 'offset': offset, 'status': status}, body=None, authenticated=True, typed=True))

    async def list_integration_tokens_detailed(self, *, limit: int | Unset=100, offset: int | Unset=0, status: ListIntegrationTokensStatus | Unset=ListIntegrationTokensStatus.ALL) -> Response[ErrorEnvelope | list[IntegrationTokenInfo]]:
        """Generated list_integration_tokens operation."""
        return cast(Response[ErrorEnvelope | list[IntegrationTokenInfo]], await self._owner.async_call_generated('list_integration_tokens', parameters={'limit': limit, 'offset': offset, 'status': status}, body=None, authenticated=True, detailed=True))

    async def list_login_sessions(self) -> ErrorEnvelope | list[LoginSessionInfo] | None:
        """Generated list_login_sessions operation."""
        return cast(ErrorEnvelope | list[LoginSessionInfo] | None, await self._owner.async_call_generated('list_login_sessions', parameters={}, body=None, authenticated=True, typed=True))

    async def list_login_sessions_detailed(self) -> Response[ErrorEnvelope | list[LoginSessionInfo]]:
        """Generated list_login_sessions operation."""
        return cast(Response[ErrorEnvelope | list[LoginSessionInfo]], await self._owner.async_call_generated('list_login_sessions', parameters={}, body=None, authenticated=True, detailed=True))

    async def list_passkeys(self) -> ErrorEnvelope | list[PasskeyInfo] | None:
        """Generated list_passkeys operation."""
        return cast(ErrorEnvelope | list[PasskeyInfo] | None, await self._owner.async_call_generated('list_passkeys', parameters={}, body=None, authenticated=True, typed=True))

    async def list_passkeys_detailed(self) -> Response[ErrorEnvelope | list[PasskeyInfo]]:
        """Generated list_passkeys operation."""
        return cast(Response[ErrorEnvelope | list[PasskeyInfo]], await self._owner.async_call_generated('list_passkeys', parameters={}, body=None, authenticated=True, detailed=True))

    async def list_players(self) -> ErrorEnvelope | GetAllKnownPlayersResponse | None:
        """Generated list_players operation."""
        return cast(ErrorEnvelope | GetAllKnownPlayersResponse | None, await self._owner.async_call_generated('list_players', parameters={}, body=None, authenticated=True, typed=True))

    async def list_players_detailed(self) -> Response[ErrorEnvelope | GetAllKnownPlayersResponse]:
        """Generated list_players operation."""
        return cast(Response[ErrorEnvelope | GetAllKnownPlayersResponse], await self._owner.async_call_generated('list_players', parameters={}, body=None, authenticated=True, detailed=True))

    async def list_plugins(self) -> ErrorEnvelope | GetPluginStatusesResponse | None:
        """Generated list_plugins operation."""
        return cast(ErrorEnvelope | GetPluginStatusesResponse | None, await self._owner.async_call_generated('list_plugins', parameters={}, body=None, authenticated=True, typed=True))

    async def list_plugins_detailed(self) -> Response[ErrorEnvelope | GetPluginStatusesResponse]:
        """Generated list_plugins operation."""
        return cast(Response[ErrorEnvelope | GetPluginStatusesResponse], await self._owner.async_call_generated('list_plugins', parameters={}, body=None, authenticated=True, detailed=True))

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

    async def list_server_addons(self, server_name: str) -> ErrorEnvelope | ListInstalledAddonsResponse | None:
        """Generated list_server_addons operation."""
        return cast(ErrorEnvelope | ListInstalledAddonsResponse | None, await self._owner.async_call_generated('list_server_addons', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def list_server_addons_detailed(self, server_name: str) -> Response[ErrorEnvelope | ListInstalledAddonsResponse]:
        """Generated list_server_addons operation."""
        return cast(Response[ErrorEnvelope | ListInstalledAddonsResponse], await self._owner.async_call_generated('list_server_addons', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def list_server_backups(self, server_name: str, backup_type: str) -> ErrorEnvelope | ListBackupFilesResponse | None:
        """Generated list_server_backups operation."""
        return cast(ErrorEnvelope | ListBackupFilesResponse | None, await self._owner.async_call_generated('list_server_backups', parameters={'server_name': server_name, 'backup_type': backup_type}, body=None, authenticated=True, typed=True))

    async def list_server_backups_detailed(self, server_name: str, backup_type: str) -> Response[ErrorEnvelope | ListBackupFilesResponse]:
        """Generated list_server_backups operation."""
        return cast(Response[ErrorEnvelope | ListBackupFilesResponse], await self._owner.async_call_generated('list_server_backups', parameters={'server_name': server_name, 'backup_type': backup_type}, body=None, authenticated=True, detailed=True))

    async def list_server_snapshots(self, server_name: str) -> ErrorEnvelope | ListSnapshotsResponse | None:
        """Generated list_server_snapshots operation."""
        return cast(ErrorEnvelope | ListSnapshotsResponse | None, await self._owner.async_call_generated('list_server_snapshots', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def list_server_snapshots_detailed(self, server_name: str) -> Response[ErrorEnvelope | ListSnapshotsResponse]:
        """Generated list_server_snapshots operation."""
        return cast(Response[ErrorEnvelope | ListSnapshotsResponse], await self._owner.async_call_generated('list_server_snapshots', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def list_servers(self) -> ErrorEnvelope | GetAllServersDataResponse | None:
        """Generated list_servers operation."""
        return cast(ErrorEnvelope | GetAllServersDataResponse | None, await self._owner.async_call_generated('list_servers', parameters={}, body=None, authenticated=True, typed=True))

    async def list_servers_detailed(self) -> Response[ErrorEnvelope | GetAllServersDataResponse]:
        """Generated list_servers operation."""
        return cast(Response[ErrorEnvelope | GetAllServersDataResponse], await self._owner.async_call_generated('list_servers', parameters={}, body=None, authenticated=True, detailed=True))

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

    async def list_trusted_devices(self) -> ErrorEnvelope | list[TrustedDeviceInfo] | None:
        """Generated list_trusted_devices operation."""
        return cast(ErrorEnvelope | list[TrustedDeviceInfo] | None, await self._owner.async_call_generated('list_trusted_devices', parameters={}, body=None, authenticated=True, typed=True))

    async def list_trusted_devices_detailed(self) -> Response[ErrorEnvelope | list[TrustedDeviceInfo]]:
        """Generated list_trusted_devices operation."""
        return cast(Response[ErrorEnvelope | list[TrustedDeviceInfo]], await self._owner.async_call_generated('list_trusted_devices', parameters={}, body=None, authenticated=True, detailed=True))

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

    async def logout(self) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated logout operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('logout', parameters={}, body=None, authenticated=True, typed=True))

    async def logout_detailed(self) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated logout operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('logout', parameters={}, body=None, authenticated=True, detailed=True))

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

    async def preview_account_server_access(self, user_id: int, *, body: SetServerAccess) -> AccessPreview | ErrorEnvelope | None:
        """Generated preview_account_server_access operation."""
        return cast(AccessPreview | ErrorEnvelope | None, await self._owner.async_call_generated('preview_account_server_access', parameters={'user_id': user_id}, body=body, authenticated=True, typed=True))

    async def preview_account_server_access_detailed(self, user_id: int, *, body: SetServerAccess) -> Response[AccessPreview | ErrorEnvelope]:
        """Generated preview_account_server_access operation."""
        return cast(Response[AccessPreview | ErrorEnvelope], await self._owner.async_call_generated('preview_account_server_access', parameters={'user_id': user_id}, body=body, authenticated=True, detailed=True))

    async def preview_integration_token(self, *, body: CreateIntegrationToken) -> AccessPreview | ErrorEnvelope | None:
        """Generated preview_integration_token operation."""
        return cast(AccessPreview | ErrorEnvelope | None, await self._owner.async_call_generated('preview_integration_token', parameters={}, body=body, authenticated=True, typed=True))

    async def preview_integration_token_detailed(self, *, body: CreateIntegrationToken) -> Response[AccessPreview | ErrorEnvelope]:
        """Generated preview_integration_token operation."""
        return cast(Response[AccessPreview | ErrorEnvelope], await self._owner.async_call_generated('preview_integration_token', parameters={}, body=body, authenticated=True, detailed=True))

    async def prune_backups(self, server_name: str) -> ErrorEnvelope | TaskAcceptedResponse | None:
        """Generated prune_backups operation."""
        return cast(ErrorEnvelope | TaskAcceptedResponse | None, await self._owner.async_call_generated('prune_backups', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def prune_backups_detailed(self, server_name: str) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
        """Generated prune_backups operation."""
        return cast(Response[ErrorEnvelope | TaskAcceptedResponse], await self._owner.async_call_generated('prune_backups', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

    async def prune_downloads(self, *, body: PruneDownloadsPayload) -> ErrorEnvelope | PruneDownloadCacheResponse | None:
        """Generated prune_downloads operation."""
        return cast(ErrorEnvelope | PruneDownloadCacheResponse | None, await self._owner.async_call_generated('prune_downloads', parameters={}, body=body, authenticated=True, typed=True))

    async def prune_downloads_detailed(self, *, body: PruneDownloadsPayload) -> Response[ErrorEnvelope | PruneDownloadCacheResponse]:
        """Generated prune_downloads operation."""
        return cast(Response[ErrorEnvelope | PruneDownloadCacheResponse], await self._owner.async_call_generated('prune_downloads', parameters={}, body=body, authenticated=True, detailed=True))

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

    async def register_user(self, token: str, *, body: UserLoginPayload) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated register_user operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('register_user', parameters={'token': token}, body=body, authenticated=False, typed=True))

    async def register_user_detailed(self, token: str, *, body: UserLoginPayload) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated register_user operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('register_user', parameters={'token': token}, body=body, authenticated=False, detailed=True))

    async def reload_plugin(self, plugin_name: str) -> ErrorEnvelope | ReloadSinglePluginResponse | None:
        """Generated reload_plugin operation."""
        return cast(ErrorEnvelope | ReloadSinglePluginResponse | None, await self._owner.async_call_generated('reload_plugin', parameters={'plugin_name': plugin_name}, body=None, authenticated=True, typed=True))

    async def reload_plugin_detailed(self, plugin_name: str) -> Response[ErrorEnvelope | ReloadSinglePluginResponse]:
        """Generated reload_plugin operation."""
        return cast(Response[ErrorEnvelope | ReloadSinglePluginResponse], await self._owner.async_call_generated('reload_plugin', parameters={'plugin_name': plugin_name}, body=None, authenticated=True, detailed=True))

    async def reload_plugins(self) -> ErrorEnvelope | ReloadPluginsResponse | None:
        """Generated reload_plugins operation."""
        return cast(ErrorEnvelope | ReloadPluginsResponse | None, await self._owner.async_call_generated('reload_plugins', parameters={}, body=None, authenticated=True, typed=True))

    async def reload_plugins_detailed(self) -> Response[ErrorEnvelope | ReloadPluginsResponse]:
        """Generated reload_plugins operation."""
        return cast(Response[ErrorEnvelope | ReloadPluginsResponse], await self._owner.async_call_generated('reload_plugins', parameters={}, body=None, authenticated=True, detailed=True))

    async def reload_settings(self) -> ErrorEnvelope | ReloadGlobalSettingsResponse | None:
        """Generated reload_settings operation."""
        return cast(ErrorEnvelope | ReloadGlobalSettingsResponse | None, await self._owner.async_call_generated('reload_settings', parameters={}, body=None, authenticated=True, typed=True))

    async def reload_settings_detailed(self) -> Response[ErrorEnvelope | ReloadGlobalSettingsResponse]:
        """Generated reload_settings operation."""
        return cast(Response[ErrorEnvelope | ReloadGlobalSettingsResponse], await self._owner.async_call_generated('reload_settings', parameters={}, body=None, authenticated=True, detailed=True))

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

    async def rename_passkey(self, passkey_id: str, *, body: RenamePasskey) -> ErrorEnvelope | PasskeyInfo | None:
        """Generated rename_passkey operation."""
        return cast(ErrorEnvelope | PasskeyInfo | None, await self._owner.async_call_generated('rename_passkey', parameters={'passkey_id': passkey_id}, body=body, authenticated=True, typed=True))

    async def rename_passkey_detailed(self, passkey_id: str, *, body: RenamePasskey) -> Response[ErrorEnvelope | PasskeyInfo]:
        """Generated rename_passkey operation."""
        return cast(Response[ErrorEnvelope | PasskeyInfo], await self._owner.async_call_generated('rename_passkey', parameters={'passkey_id': passkey_id}, body=body, authenticated=True, detailed=True))

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

    async def revoke_passkey(self, passkey_id: str) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated revoke_passkey operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('revoke_passkey', parameters={'passkey_id': passkey_id}, body=None, authenticated=True, typed=True))

    async def revoke_passkey_detailed(self, passkey_id: str) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated revoke_passkey operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('revoke_passkey', parameters={'passkey_id': passkey_id}, body=None, authenticated=True, detailed=True))

    async def revoke_trusted_device(self, device_id: str) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated revoke_trusted_device operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('revoke_trusted_device', parameters={'device_id': device_id}, body=None, authenticated=True, typed=True))

    async def revoke_trusted_device_detailed(self, device_id: str) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated revoke_trusted_device operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('revoke_trusted_device', parameters={'device_id': device_id}, body=None, authenticated=True, detailed=True))

    async def revoke_trusted_devices(self, *, body: RevokeTrustedDevices) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated revoke_trusted_devices operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('revoke_trusted_devices', parameters={}, body=body, authenticated=True, typed=True))

    async def revoke_trusted_devices_detailed(self, *, body: RevokeTrustedDevices) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated revoke_trusted_devices operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('revoke_trusted_devices', parameters={}, body=body, authenticated=True, detailed=True))

    async def rotate_account_recovery_codes(self) -> ErrorEnvelope | RecoveryCodes | None:
        """Generated rotate_account_recovery_codes operation."""
        return cast(ErrorEnvelope | RecoveryCodes | None, await self._owner.async_call_generated('rotate_account_recovery_codes', parameters={}, body=None, authenticated=True, typed=True))

    async def rotate_account_recovery_codes_detailed(self) -> Response[ErrorEnvelope | RecoveryCodes]:
        """Generated rotate_account_recovery_codes operation."""
        return cast(Response[ErrorEnvelope | RecoveryCodes], await self._owner.async_call_generated('rotate_account_recovery_codes', parameters={}, body=None, authenticated=True, detailed=True))

    async def rotate_backup_key(self) -> BackupKeyInfo | ErrorEnvelope | None:
        """Generated rotate_backup_key operation."""
        return cast(BackupKeyInfo | ErrorEnvelope | None, await self._owner.async_call_generated('rotate_backup_key', parameters={}, body=None, authenticated=True, typed=True))

    async def rotate_backup_key_detailed(self) -> Response[BackupKeyInfo | ErrorEnvelope]:
        """Generated rotate_backup_key operation."""
        return cast(Response[BackupKeyInfo | ErrorEnvelope], await self._owner.async_call_generated('rotate_backup_key', parameters={}, body=None, authenticated=True, detailed=True))

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

    async def scan_players(self) -> ErrorEnvelope | ScanAndUpdatePlayerDbResponse | None:
        """Generated scan_players operation."""
        return cast(ErrorEnvelope | ScanAndUpdatePlayerDbResponse | None, await self._owner.async_call_generated('scan_players', parameters={}, body=None, authenticated=True, typed=True))

    async def scan_players_detailed(self) -> Response[ErrorEnvelope | ScanAndUpdatePlayerDbResponse]:
        """Generated scan_players operation."""
        return cast(Response[ErrorEnvelope | ScanAndUpdatePlayerDbResponse], await self._owner.async_call_generated('scan_players', parameters={}, body=None, authenticated=True, detailed=True))

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

    async def set_plugin_status(self, plugin_name: str, *, body: PluginStatusSetPayload) -> ErrorEnvelope | SetPluginStatusResponse | None:
        """Generated set_plugin_status operation."""
        return cast(ErrorEnvelope | SetPluginStatusResponse | None, await self._owner.async_call_generated('set_plugin_status', parameters={'plugin_name': plugin_name}, body=body, authenticated=True, typed=True))

    async def set_plugin_status_detailed(self, plugin_name: str, *, body: PluginStatusSetPayload) -> Response[ErrorEnvelope | SetPluginStatusResponse]:
        """Generated set_plugin_status operation."""
        return cast(Response[ErrorEnvelope | SetPluginStatusResponse], await self._owner.async_call_generated('set_plugin_status', parameters={'plugin_name': plugin_name}, body=body, authenticated=True, detailed=True))

    async def set_properties(self, server_name: str, *, body: PropertiesPayload) -> ErrorEnvelope | SetPropertiesResponse | None:
        """Generated set_properties operation."""
        return cast(ErrorEnvelope | SetPropertiesResponse | None, await self._owner.async_call_generated('set_properties', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def set_properties_detailed(self, server_name: str, *, body: PropertiesPayload) -> Response[ErrorEnvelope | SetPropertiesResponse]:
        """Generated set_properties operation."""
        return cast(Response[ErrorEnvelope | SetPropertiesResponse], await self._owner.async_call_generated('set_properties', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

    async def set_server_setting(self, server_name: str, *, body: ServerSettingItemPayload) -> ErrorEnvelope | SetServerSettingResponse | None:
        """Generated set_server_setting operation."""
        return cast(ErrorEnvelope | SetServerSettingResponse | None, await self._owner.async_call_generated('set_server_setting', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def set_server_setting_detailed(self, server_name: str, *, body: ServerSettingItemPayload) -> Response[ErrorEnvelope | SetServerSettingResponse]:
        """Generated set_server_setting operation."""
        return cast(Response[ErrorEnvelope | SetServerSettingResponse], await self._owner.async_call_generated('set_server_setting', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

    async def set_setting(self, *, body: SettingItemPayload) -> ErrorEnvelope | SetGlobalSettingResponse | None:
        """Generated set_setting operation."""
        return cast(ErrorEnvelope | SetGlobalSettingResponse | None, await self._owner.async_call_generated('set_setting', parameters={}, body=body, authenticated=True, typed=True))

    async def set_setting_detailed(self, *, body: SettingItemPayload) -> Response[ErrorEnvelope | SetGlobalSettingResponse]:
        """Generated set_setting operation."""
        return cast(Response[ErrorEnvelope | SetGlobalSettingResponse], await self._owner.async_call_generated('set_setting', parameters={}, body=body, authenticated=True, detailed=True))

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

    async def trigger_plugin_event(self, *, body: TriggerEventPayload) -> ErrorEnvelope | TriggerExternalAppEventResponse | None:
        """Generated trigger_plugin_event operation."""
        return cast(ErrorEnvelope | TriggerExternalAppEventResponse | None, await self._owner.async_call_generated('trigger_plugin_event', parameters={}, body=body, authenticated=True, typed=True))

    async def trigger_plugin_event_detailed(self, *, body: TriggerEventPayload) -> Response[ErrorEnvelope | TriggerExternalAppEventResponse]:
        """Generated trigger_plugin_event operation."""
        return cast(Response[ErrorEnvelope | TriggerExternalAppEventResponse], await self._owner.async_call_generated('trigger_plugin_event', parameters={}, body=body, authenticated=True, detailed=True))

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

    async def upload_content_file(self, *, body: BodyUploadContentFile) -> ContentUploadResponse | ErrorEnvelope | None:
        """Generated upload_content_file operation."""
        return cast(ContentUploadResponse | ErrorEnvelope | None, await self._owner.async_call_generated('upload_content_file', parameters={}, body=body, authenticated=True, typed=True))

    async def upload_content_file_detailed(self, *, body: BodyUploadContentFile) -> Response[ContentUploadResponse | ErrorEnvelope]:
        """Generated upload_content_file operation."""
        return cast(Response[ContentUploadResponse | ErrorEnvelope], await self._owner.async_call_generated('upload_content_file', parameters={}, body=body, authenticated=True, detailed=True))

    async def validate_registration_token(self, token: str) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated validate_registration_token operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('validate_registration_token', parameters={'token': token}, body=None, authenticated=False, typed=True))

    async def validate_registration_token_detailed(self, token: str) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated validate_registration_token operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('validate_registration_token', parameters={'token': token}, body=None, authenticated=False, detailed=True))

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

    async def verify_account_security_passkey(self, *, body: VerifyPasskeyAssertion) -> ErrorEnvelope | VerifiedSecurity | None:
        """Generated verify_account_security_passkey operation."""
        return cast(ErrorEnvelope | VerifiedSecurity | None, await self._owner.async_call_generated('verify_account_security_passkey', parameters={}, body=body, authenticated=True, typed=True))

    async def verify_account_security_passkey_detailed(self, *, body: VerifyPasskeyAssertion) -> Response[ErrorEnvelope | VerifiedSecurity]:
        """Generated verify_account_security_passkey operation."""
        return cast(Response[ErrorEnvelope | VerifiedSecurity], await self._owner.async_call_generated('verify_account_security_passkey', parameters={}, body=body, authenticated=True, detailed=True))
