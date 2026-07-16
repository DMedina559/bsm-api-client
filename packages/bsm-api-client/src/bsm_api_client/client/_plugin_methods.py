# src/bsm_api_client/client/_plugin_methods.py
"""Mixin class for plugin management methods.

This module provides the `PluginMethodsMixin` class, which includes methods
for managing plugins through the Bedrock Server Manager API.
"""

import logging
from typing import Any, Callable, cast

from ..models import (
    ActionResponse,
    PluginStatusesResponse,
    PluginStatusSetPayload,
    TriggerEventPayload,
    TriggerEventResponse,
)

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.plugins")


class PluginMethodsMixin:
    """Mixin containing methods for interacting with Plugin Management API endpoints."""

    _request: Callable[..., Any]

    async def async_get_plugin_statuses(self) -> PluginStatusesResponse:
        """Retrieves the status of all discovered plugins.

        :returns: A `PluginStatusesResponse` object containing the statuses of all plugins.

        :raises APIError: For API-related errors.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_get_plugin_statuses()
        """
        _LOGGER.info("Requesting status of all plugins.")
        response = await self._request(
            method="GET", path="/plugins", authenticated=True
        )
        return cast(
            PluginStatusesResponse, PluginStatusesResponse.model_validate(response)
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
        response = await self._request(
            method="POST",
            path=f"/plugins/{plugin_name}",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return cast(ActionResponse, ActionResponse.model_validate(response))

    async def async_reload_plugins(self) -> ActionResponse:
        """Triggers a full reload of all plugins.

        :returns: A `ActionResponse` object confirming the reload.

        :raises APIError: For API-related errors.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_reload_plugins()
        """
        _LOGGER.info("Requesting reload of all plugins.")
        response = await self._request(
            method="PUT", path="/plugins/reload", authenticated=True
        )
        return cast(ActionResponse, ActionResponse.model_validate(response))

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
        return cast(TriggerEventResponse, TriggerEventResponse.model_validate(response))
