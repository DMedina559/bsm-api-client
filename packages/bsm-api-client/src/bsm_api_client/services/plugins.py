import logging
from typing import Literal, cast

from ..generated.models.get_plugin_settings_scope import GetPluginSettingsScope
from ..models import (
    ActionResponse,
    GetPluginSettingsResponse,
    PluginSettingsPayload,
    PluginStatusesResponse,
    PluginStatusSetPayload,
    SetPluginSettingResponse,
    TriggerEventPayload,
    TriggerEventResponse,
)
from ..validation import parse_response
from .base import Service

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.plugins")


class PluginsService(Service):
    """Service containing methods for interacting with Plugin Management API endpoints."""

    async def async_get_plugin_statuses(self) -> PluginStatusesResponse:
        """Retrieves the status of all discovered plugins.

        :returns: `PluginStatusesResponse`.

        .. code-block:: python

            response = await client.plugins.async_get_plugin_statuses()
        """
        _LOGGER.info("Requesting status of all plugins.")
        response = await self.async_call_generated(
            "list_plugins", authenticated=True, typed=True
        )
        return cast(
            PluginStatusesResponse, parse_response(PluginStatusesResponse, response)
        )

    async def async_set_plugin_status(
        self, plugin_name: str, payload: PluginStatusSetPayload
    ) -> ActionResponse:
        """Enables or disables a specific plugin.

        :param plugin_name: The name of the plugin to modify.

        :param payload: A `PluginStatusSetPayload` object with the new status.

        :returns: `ActionResponse`.
        :raises ValueError: If plugin_name is empty.

        .. code-block:: python

            response = await client.plugins.async_set_plugin_status("my_plugin", payload)
        """
        if not plugin_name:
            _LOGGER.error("Plugin name cannot be empty for set_plugin_enabled.")
            raise ValueError("Plugin name cannot be empty.")
        _LOGGER.info(
            "Setting plugin '%s' to enabled state: %s.", plugin_name, payload.enabled
        )
        response = await self.async_call_generated(
            "set_plugin_status",
            parameters={"plugin_name": plugin_name},
            body=payload.model_dump(),
            authenticated=True,
            typed=True,
        )
        return cast(ActionResponse, parse_response(ActionResponse, response))

    async def async_reload_plugins(self) -> ActionResponse:
        """Triggers a full reload of all plugins.

        :returns: `ActionResponse`.

        .. code-block:: python

            response = await client.plugins.async_reload_plugins()
        """
        _LOGGER.info("Requesting reload of all plugins.")
        response = await self.async_call_generated(
            "reload_plugins", authenticated=True, typed=True
        )
        return cast(ActionResponse, parse_response(ActionResponse, response))

    async def async_trigger_plugin_event(
        self, payload: TriggerEventPayload
    ) -> TriggerEventResponse:
        """Triggers a custom plugin event.

        :param payload: A `TriggerEventPayload` object with the event details.

        :returns: `TriggerEventResponse`.

        .. code-block:: python

            response = await client.plugins.async_trigger_plugin_event(payload)
        """
        _LOGGER.debug("Triggering custom plugin event '%s'", payload.event_name)
        response = await self.async_call_generated(
            "trigger_plugin_event",
            body=payload.model_dump(),
            authenticated=True,
            typed=True,
        )
        return cast(
            TriggerEventResponse, parse_response(TriggerEventResponse, response)
        )

    async def async_get_plugin_settings(
        self,
        plugin_name: str,
        *,
        scope: Literal["plugin", "global", "server"] = "plugin",
        server_name: str | None = None,
    ) -> GetPluginSettingsResponse:
        """Read settings and the plugin's current validation schema.

        :param plugin_name: The plugin identifier.

        :param scope: Plugin-local, global, or per-server settings.
        :param server_name: Required for server scope.
        :returns: `GetPluginSettingsResponse`.
        """
        if (scope == "server") != (server_name is not None):
            raise ValueError(
                "Server scope requires server_name; other scopes must omit it"
            )
        query: dict[str, str] = {}
        if scope != "plugin":
            query["scope"] = GetPluginSettingsScope(scope)
        if server_name is not None:
            query["server_name"] = server_name
        response = await self.async_call_generated(
            "get_plugin_settings",
            parameters={"plugin_name": plugin_name, **query},
            authenticated=True,
            typed=True,
        )
        return parse_response(GetPluginSettingsResponse, response)

    async def async_update_plugin_settings(
        self, plugin_name: str, payload: PluginSettingsPayload
    ) -> SetPluginSettingResponse:
        """Validate and persist a plugin's settings.

        :param plugin_name: The plugin identifier.

        :param payload: The PluginSettingsPayload request model.

        :returns: `SetPluginSettingResponse`.
        """
        response = await self.async_call_generated(
            "update_plugin_settings",
            parameters={"plugin_name": plugin_name},
            body=payload.model_dump(mode="json", exclude_unset=True),
            authenticated=True,
            typed=True,
        )
        return parse_response(SetPluginSettingResponse, response)
