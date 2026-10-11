"""Typed REST interface generated from the bundled OpenAPI contract."""

from .models.action_response import ActionResponse
from .models.add_players_payload import AddPlayersPayload
from .models.add_players_response import AddPlayersResponse
from .models.add_server_ban_response import AddServerBanResponse
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
from .models.ban_add_request import BanAddRequest
from .models.ban_remove_request import BanRemoveRequest
from .models.base_api_response import BaseApiResponse
from .models.body_login import BodyLogin
from .models.change_password_payload import ChangePasswordPayload
from .models.command_payload import CommandPayload
from .models.content_list_response import ContentListResponse
from .models.custom_zips_response import CustomZipsResponse
from .models.error_envelope import ErrorEnvelope
from .models.file_name_payload import FileNamePayload
from .models.generate_token_payload import GenerateTokenPayload
from .models.get_allowlist_response import GetAllowlistResponse
from .models.get_application_health_response import GetApplicationHealthResponse
from .models.get_application_metrics_response import GetApplicationMetricsResponse
from .models.get_permissions_response import GetPermissionsResponse
from .models.get_plugin_settings_response import GetPluginSettingsResponse
from .models.get_properties_response import GetPropertiesResponse
from .models.get_server_bans_response import GetServerBansResponse
from .models.install_confirmation_response import InstallConfirmationResponse
from .models.install_server_payload import InstallServerPayload
from .models.installation_accepted_response import InstallationAcceptedResponse
from .models.list_available_addons_response import ListAvailableAddonsResponse
from .models.log_history_page import LogHistoryPage
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
from .models.registration_response import RegistrationResponse
from .models.remove_server_ban_response import RemoveServerBanResponse
from .models.restart_server_response import RestartServerResponse
from .models.restore_action_payload import RestoreActionPayload
from .models.server_process_info_response import ServerProcessInfoResponse
from .models.server_running_status_response import ServerRunningStatusResponse
from .models.server_setting_item_payload import ServerSettingItemPayload
from .models.server_settings_response import ServerSettingsResponse
from .models.server_summary import ServerSummary
from .models.servers_list_response import ServersListResponse
from .models.set_plugin_setting_response import SetPluginSettingResponse
from .models.setting_item_response import SettingItemResponse
from .models.settings_response import SettingsResponse
from .models.setup_account_response import SetupAccountResponse
from .models.setup_status_response import SetupStatusResponse
from .models.start_server_response import StartServerResponse
from .models.stop_server_response import StopServerResponse
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
from .types import Response, UNSET, Unset
from http import HTTPStatus
from typing import Any, cast
from typing import cast

class RestClient:

    def __init__(self, owner: Any):
        self._owner = owner

    async def add_allowlist_players(self, server_name: str, *, body: AllowlistAddPayload) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated add_allowlist_players operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('add_allowlist_players', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def add_allowlist_players_detailed(self, server_name: str, *, body: AllowlistAddPayload) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated add_allowlist_players operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('add_allowlist_players', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

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

    async def get_account(self) -> ErrorEnvelope | UserResponse | None:
        """Generated get_account operation."""
        return cast(ErrorEnvelope | UserResponse | None, await self._owner.async_call_generated('get_account', parameters={}, body=None, authenticated=True, typed=True))

    async def get_account_detailed(self) -> Response[ErrorEnvelope | UserResponse]:
        """Generated get_account operation."""
        return cast(Response[ErrorEnvelope | UserResponse], await self._owner.async_call_generated('get_account', parameters={}, body=None, authenticated=True, detailed=True))

    async def get_allowlist(self, server_name: str) -> ErrorEnvelope | GetAllowlistResponse | None:
        """Generated get_allowlist operation."""
        return cast(ErrorEnvelope | GetAllowlistResponse | None, await self._owner.async_call_generated('get_allowlist', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def get_allowlist_detailed(self, server_name: str) -> Response[ErrorEnvelope | GetAllowlistResponse]:
        """Generated get_allowlist operation."""
        return cast(Response[ErrorEnvelope | GetAllowlistResponse], await self._owner.async_call_generated('get_allowlist', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

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

    async def get_plugin_settings(self, plugin_name: str) -> ErrorEnvelope | GetPluginSettingsResponse | None:
        """Generated get_plugin_settings operation."""
        return cast(ErrorEnvelope | GetPluginSettingsResponse | None, await self._owner.async_call_generated('get_plugin_settings', parameters={'plugin_name': plugin_name}, body=None, authenticated=True, typed=True))

    async def get_plugin_settings_detailed(self, plugin_name: str) -> Response[ErrorEnvelope | GetPluginSettingsResponse]:
        """Generated get_plugin_settings operation."""
        return cast(Response[ErrorEnvelope | GetPluginSettingsResponse], await self._owner.async_call_generated('get_plugin_settings', parameters={'plugin_name': plugin_name}, body=None, authenticated=True, detailed=True))

    async def get_properties(self, server_name: str) -> ErrorEnvelope | GetPropertiesResponse | None:
        """Generated get_properties operation."""
        return cast(ErrorEnvelope | GetPropertiesResponse | None, await self._owner.async_call_generated('get_properties', parameters={'server_name': server_name}, body=None, authenticated=True, typed=True))

    async def get_properties_detailed(self, server_name: str) -> Response[ErrorEnvelope | GetPropertiesResponse]:
        """Generated get_properties operation."""
        return cast(Response[ErrorEnvelope | GetPropertiesResponse], await self._owner.async_call_generated('get_properties', parameters={'server_name': server_name}, body=None, authenticated=True, detailed=True))

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

    async def get_world_icon(self, server_name: str) -> Any | ErrorEnvelope | None:
        """Generated get_world_icon operation."""
        return cast(Any | ErrorEnvelope | None, await self._owner.async_call_generated('get_world_icon', parameters={'server_name': server_name}, body=None, authenticated=False, typed=True))

    async def get_world_icon_detailed(self, server_name: str) -> Response[Any | ErrorEnvelope]:
        """Generated get_world_icon operation."""
        return cast(Response[Any | ErrorEnvelope], await self._owner.async_call_generated('get_world_icon', parameters={'server_name': server_name}, body=None, authenticated=False, detailed=True))

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

    async def list_downloads(self) -> CustomZipsResponse | ErrorEnvelope | None:
        """Generated list_downloads operation."""
        return cast(CustomZipsResponse | ErrorEnvelope | None, await self._owner.async_call_generated('list_downloads', parameters={}, body=None, authenticated=True, typed=True))

    async def list_downloads_detailed(self) -> Response[CustomZipsResponse | ErrorEnvelope]:
        """Generated list_downloads operation."""
        return cast(Response[CustomZipsResponse | ErrorEnvelope], await self._owner.async_call_generated('list_downloads', parameters={}, body=None, authenticated=True, detailed=True))

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

    async def remove_allowlist_players(self, server_name: str, *, body: AllowlistRemovePayload) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated remove_allowlist_players operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('remove_allowlist_players', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def remove_allowlist_players_detailed(self, server_name: str, *, body: AllowlistRemovePayload) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated remove_allowlist_players operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('remove_allowlist_players', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

    async def remove_server_ban(self, server_name: str, *, body: BanRemoveRequest) -> ErrorEnvelope | RemoveServerBanResponse | None:
        """Generated remove_server_ban operation."""
        return cast(ErrorEnvelope | RemoveServerBanResponse | None, await self._owner.async_call_generated('remove_server_ban', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def remove_server_ban_detailed(self, server_name: str, *, body: BanRemoveRequest) -> Response[ErrorEnvelope | RemoveServerBanResponse]:
        """Generated remove_server_ban operation."""
        return cast(Response[ErrorEnvelope | RemoveServerBanResponse], await self._owner.async_call_generated('remove_server_ban', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

    async def reorder_addons(self, server_name: str, *, body: AddonReorderPayload) -> ErrorEnvelope | TaskAcceptedResponse | None:
        """Generated reorder_addons operation."""
        return cast(ErrorEnvelope | TaskAcceptedResponse | None, await self._owner.async_call_generated('reorder_addons', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def reorder_addons_detailed(self, server_name: str, *, body: AddonReorderPayload) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
        """Generated reorder_addons operation."""
        return cast(Response[ErrorEnvelope | TaskAcceptedResponse], await self._owner.async_call_generated('reorder_addons', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

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

    async def scan_players(self) -> AddPlayersResponse | ErrorEnvelope | None:
        """Generated scan_players operation."""
        return cast(AddPlayersResponse | ErrorEnvelope | None, await self._owner.async_call_generated('scan_players', parameters={}, body=None, authenticated=True, typed=True))

    async def scan_players_detailed(self) -> Response[AddPlayersResponse | ErrorEnvelope]:
        """Generated scan_players operation."""
        return cast(Response[AddPlayersResponse | ErrorEnvelope], await self._owner.async_call_generated('scan_players', parameters={}, body=None, authenticated=True, detailed=True))

    async def send_command(self, server_name: str, *, body: CommandPayload) -> ActionResponse | ErrorEnvelope | None:
        """Generated send_command operation."""
        return cast(ActionResponse | ErrorEnvelope | None, await self._owner.async_call_generated('send_command', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def send_command_detailed(self, server_name: str, *, body: CommandPayload) -> Response[ActionResponse | ErrorEnvelope]:
        """Generated send_command operation."""
        return cast(Response[ActionResponse | ErrorEnvelope], await self._owner.async_call_generated('send_command', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

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

    async def set_properties(self, server_name: str, *, body: PropertiesPayload) -> BaseApiResponse | ErrorEnvelope | None:
        """Generated set_properties operation."""
        return cast(BaseApiResponse | ErrorEnvelope | None, await self._owner.async_call_generated('set_properties', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def set_properties_detailed(self, server_name: str, *, body: PropertiesPayload) -> Response[BaseApiResponse | ErrorEnvelope]:
        """Generated set_properties operation."""
        return cast(Response[BaseApiResponse | ErrorEnvelope], await self._owner.async_call_generated('set_properties', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

    async def set_server_setting(self, server_name: str, *, body: ServerSettingItemPayload) -> ErrorEnvelope | ServerSettingsResponse | None:
        """Generated set_server_setting operation."""
        return cast(ErrorEnvelope | ServerSettingsResponse | None, await self._owner.async_call_generated('set_server_setting', parameters={'server_name': server_name}, body=body, authenticated=True, typed=True))

    async def set_server_setting_detailed(self, server_name: str, *, body: ServerSettingItemPayload) -> Response[ErrorEnvelope | ServerSettingsResponse]:
        """Generated set_server_setting operation."""
        return cast(Response[ErrorEnvelope | ServerSettingsResponse], await self._owner.async_call_generated('set_server_setting', parameters={'server_name': server_name}, body=body, authenticated=True, detailed=True))

    async def set_setting(self, *, body: SettingItemResponse) -> ErrorEnvelope | SettingsResponse | None:
        """Generated set_setting operation."""
        return cast(ErrorEnvelope | SettingsResponse | None, await self._owner.async_call_generated('set_setting', parameters={}, body=body, authenticated=True, typed=True))

    async def set_setting_detailed(self, *, body: SettingItemResponse) -> Response[ErrorEnvelope | SettingsResponse]:
        """Generated set_setting operation."""
        return cast(Response[ErrorEnvelope | SettingsResponse], await self._owner.async_call_generated('set_setting', parameters={}, body=body, authenticated=True, detailed=True))

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
