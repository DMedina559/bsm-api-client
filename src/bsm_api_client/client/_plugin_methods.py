# src/bsm_api_client/client/_plugin_methods.py
"""Mixin class for Bedrock Server Manager API Client, handling Plugin Management endpoints."""

import logging
from typing import Any, Dict, Optional, List
from ..models import PluginStatusSetPayload, TriggerEventPayload, PluginApiResponse

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.plugins")


class PluginMethodsMixin:
    """Mixin containing methods for interacting with Plugin Management API endpoints."""

    async def async_get_plugin_statuses(self) -> PluginApiResponse:
        """
        Retrieves the status, version, and description of all discovered plugins.

        Corresponds to: GET /api/plugins
        Authentication: Required.

        Returns:
            Dict[str, Any]: API response, typically including a "plugins" dictionary.
                Example:
                {
                    "status": "success",
                    "plugins": {
                        "MyPlugin": {
                            "enabled": True,
                            "version": "1.0.0",
                            "description": "This is my awesome plugin."
                        },
                        "AnotherPlugin": {
                            "enabled": False,
                            "version": "0.5.2",
                            "description": "Does something else cool."
                        }
                    }
                }

        Raises:
            CannotConnectError: If connection to the API fails.
            AuthError: If authentication fails.
            APIServerSideError: If there's an issue reading plugin configurations on the server.
            APIError: For other API response issues.
        """
        _LOGGER.info("Requesting status of all plugins.")
        response = await self._request(
            method="GET", path="/plugins", authenticated=True
        )
        return PluginApiResponse.model_validate(response)

    async def async_set_plugin_status(
        self, plugin_name: str, payload: PluginStatusSetPayload
    ) -> PluginApiResponse:
        """
        Enables or disables a specific plugin.

        Corresponds to: POST /api/plugins/{plugin_name}
        Authentication: Required.

        Args:
            plugin_name (str): The name of the plugin (filename without .py).
            payload: A PluginStatusSetPayload object.

        Returns:
            Dict[str, Any]: API response, typically confirming the action.
                Example:
                {
                    "status": "success",
                    "message": "Plugin 'MyPlugin' has been enabled. Reload plugins for changes to take full effect."
                }

        Raises:
            ValueError: If plugin_name is empty.
            CannotConnectError: If connection to the API fails.
            AuthError: If authentication fails.
            InvalidInputError: If JSON body is invalid or 'enabled' field is missing.
            NotFoundError: If plugin_name does not exist.
            APIServerSideError: If saving the configuration fails on the server.
            APIError: For other API response issues.
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
        """
        Triggers a full reload of all plugins.

        Corresponds to: PUT /api/plugins/reload
        Authentication: Required.

        Returns:
            Dict[str, Any]: API response, typically confirming the reload.
                Example:
                {
                    "status": "success",
                    "message": "Plugins have been reloaded successfully."
                }

        Raises:
            CannotConnectError: If connection to the API fails.
            AuthError: If authentication fails.
            APIServerSideError: If the reload process encounters an error on the server.
            APIError: For other API response issues.
        """
        _LOGGER.info("Requesting reload of all plugins.")
        response = await self._request(
            method="PUT", path="/plugins/reload", authenticated=True
        )
        return PluginApiResponse.model_validate(response)

    async def async_trigger_plugin_event(
        self, payload: TriggerEventPayload
    ) -> PluginApiResponse:
        """
        Triggers a custom plugin event.

        Corresponds to: POST /api/plugins/trigger_event
        Authentication: Required.

        Args:
            payload: A TriggerEventPayload object.

        Returns:
            Dict[str, Any]: API response, typically confirming the event was triggered.
                Example:
                {
                    "status": "success",
                    "message": "Event 'my_custom_plugin:some_action' triggered."
                }

        Raises:
            ValueError: If event_name is empty.
            CannotConnectError: If connection to the API fails.
            AuthError: If authentication fails.
            InvalidInputError: If event_name is missing or payload is not an object.
            APIServerSideError: If an error occurs while triggering the event on the server.
            APIError: For other API response issues.
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
