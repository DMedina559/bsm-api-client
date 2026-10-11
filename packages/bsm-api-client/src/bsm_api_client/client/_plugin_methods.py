"""Mixin class for plugin management methods.

This module provides the `PluginMethodsMixin` class, which includes methods
for managing plugins through the Bedrock Server Manager API.
"""

import logging
from typing import cast

from ..generated_adapter import GeneratedOperationMethods
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

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.plugins")


class PluginMethodsMixin(GeneratedOperationMethods):
    """Mixin containing methods for interacting with Plugin Management API endpoints."""

    async def async_get_plugin_statuses(self) -> PluginStatusesResponse:
        """Retrieves the status of all discovered plugins.

        :returns: A `PluginStatusesResponse` object containing the statuses of all plugins.

        :raises APIError: For API-related errors.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_get_plugin_statuses()
        """
        _LOGGER.info("Requesting status of all plugins.")
        response = await self.async_call_generated("list_plugins", authenticated=True)
        return cast(
            PluginStatusesResponse, parse_response(PluginStatusesResponse, response)
        )

    async def async_set_plugin_status(
        self, plugin_name: str, payload: PluginStatusSetPayload
    ) -> ActionResponse:
        """Enables or disables a specific plugin.

        :param plugin_name: The name of the plugin to modify.
        :param payload: A `PluginStatusSetPayload` object with the new status.

        :returns: A `ActionResponse` object confirming the status change.

        :raises ValueError: If `plugin_name` is empty.
        :raises APIError: For API-related errors.


        .. rubric:: Example:
        .. code-block:: python

            payload = ...
            response = await client.async_set_plugin_status(payload)
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
        )
        return cast(ActionResponse, parse_response(ActionResponse, response))

    async def async_reload_plugins(self) -> ActionResponse:
        """Triggers a full reload of all plugins.

        :returns: A `ActionResponse` object confirming the reload.

        :raises APIError: For API-related errors.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_reload_plugins()
        """
        _LOGGER.info("Requesting reload of all plugins.")
        response = await self.async_call_generated("reload_plugins", authenticated=True)
        return cast(ActionResponse, parse_response(ActionResponse, response))

    async def async_trigger_plugin_event(
        self, payload: TriggerEventPayload
    ) -> TriggerEventResponse:
        """Triggers a custom plugin event.

        :param payload: A `TriggerEventPayload` object with the event details.

        :returns: A `TriggerEventResponse` object confirming the event was triggered.

        :raises APIError: For API-related errors.


        .. rubric:: Example:
        .. code-block:: python

            payload = ...
            response = await client.async_trigger_plugin_event(payload)
        """
        _LOGGER.debug("Triggering custom plugin event '%s'", payload.event_name)
        response = await self.async_call_generated(
            "trigger_plugin_event", body=payload.model_dump(), authenticated=True
        )
        return cast(
            TriggerEventResponse, parse_response(TriggerEventResponse, response)
        )

    async def async_get_plugin_settings(
        self, plugin_name: str
    ) -> GetPluginSettingsResponse:
        """Read settings and the plugin's current validation schema."""
        response = await self.async_call_generated(
            "get_plugin_settings",
            parameters={"plugin_name": plugin_name},
            authenticated=True,
        )
        return parse_response(GetPluginSettingsResponse, response)

    async def async_update_plugin_settings(
        self, plugin_name: str, payload: PluginSettingsPayload
    ) -> SetPluginSettingResponse:
        """Validate and persist a plugin's settings."""
        response = await self.async_call_generated(
            "update_plugin_settings",
            parameters={"plugin_name": plugin_name},
            body=payload.model_dump(mode="json"),
            authenticated=True,
        )
        return parse_response(SetPluginSettingResponse, response)
