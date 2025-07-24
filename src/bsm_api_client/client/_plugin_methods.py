# src/bsm_api_client/client/_plugin_methods.py
"""Mixin class for plugin management methods.

This module provides the `PluginMethodsMixin` class, which includes methods
for managing plugins through the Bedrock Server Manager API.
"""

import logging
from typing import Any, Dict, Optional, List
from ..models import PluginStatusSetPayload, TriggerEventPayload, PluginApiResponse

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.plugins")


class PluginMethodsMixin:
    """Mixin containing methods for interacting with Plugin Management API endpoints."""

    async def async_get_plugin_statuses(self) -> PluginApiResponse:
        """Retrieves the status of all discovered plugins.

        Returns:
            A `PluginApiResponse` object containing the statuses of all plugins.

        Raises:
            APIError: For API-related errors.
        """
        _LOGGER.info("Requesting status of all plugins.")
        response = await self._request(
            method="GET", path="/plugins", authenticated=True
        )
        return PluginApiResponse.model_validate(response)

    async def async_set_plugin_status(
        self, plugin_name: str, payload: PluginStatusSetPayload
    ) -> PluginApiResponse:
        """Enables or disables a specific plugin.

        Args:
            plugin_name: The name of the plugin to modify.
            payload: A `PluginStatusSetPayload` object with the new status.

        Returns:
            A `PluginApiResponse` object confirming the status change.

        Raises:
            ValueError: If `plugin_name` is empty.
            APIError: For API-related errors.
        """
        if not plugin_name:
            _LOGGER.error("Plugin name cannot be empty for set_plugin_enabled.")
            raise ValueError("Plugin name cannot be empty.")

        _LOGGER.info(
            "Setting plugin '%s' to enabled state: %s.", plugin_name, payload.enabled
        )
        response = await self._request(
            method="POST",
            path=f"/plugins/{plugin_name}",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return PluginApiResponse.model_validate(response)

    async def async_reload_plugins(self) -> PluginApiResponse:
        """Triggers a full reload of all plugins.

        Returns:
            A `PluginApiResponse` object confirming the reload.

        Raises:
            APIError: For API-related errors.
        """
        _LOGGER.info("Requesting reload of all plugins.")
        response = await self._request(
            method="PUT", path="/plugins/reload", authenticated=True
        )
        return PluginApiResponse.model_validate(response)

    async def async_trigger_plugin_event(
        self, payload: TriggerEventPayload
    ) -> PluginApiResponse:
        """Triggers a custom plugin event.

        Args:
            payload: A `TriggerEventPayload` object with the event details.

        Returns:
            A `PluginApiResponse` object confirming the event was triggered.

        Raises:
            APIError: For API-related errors.
        """
        _LOGGER.info(
            "Triggering custom plugin event '%s' with payload: %s",
            payload.event_name,
            payload.payload,
        )
        response = await self._request(
            method="POST",
            path="/plugins/trigger_event",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return PluginApiResponse.model_validate(response)
