# src/bsm_api_client/client/_plugin_methods.py
"""Mixin class for Bedrock Server Manager API Client, handling Plugin Management endpoints."""

import logging
from typing import Any, Dict, Optional, List

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.plugins")


class PluginMethodsMixin:
    """Mixin containing methods for interacting with Plugin Management API endpoints."""

    async def async_get_plugin_statuses(self) -> Dict[str, Any]:
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
        return await self._request(method="GET", path="/plugins", authenticated=True)

    async def async_set_plugin_status(
        self, plugin_name: str, enabled: bool
    ) -> Dict[str, Any]:
        """
        Enables or disables a specific plugin.

        Corresponds to: POST /api/plugins/{plugin_name}
        Authentication: Required.

        Args:
            plugin_name (str): The name of the plugin (filename without .py).
            enabled (bool): Set to True to enable, False to disable.

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
            "Setting plugin '%s' to enabled state: %s.", plugin_name, enabled
        )
        return await self._request(
            method="POST",
            path=f"/plugins/{plugin_name}",
            json_data={"enabled": enabled},
            authenticated=True,
        )

    async def async_reload_plugins(self) -> Dict[str, Any]:
        """
        Triggers a full reload of all plugins.

        Corresponds to: POST /api/plugins/reload
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
        return await self._request(
            method="POST", path="/plugins/reload", authenticated=True
        )

    async def async_trigger_plugin_event(
        self, event_name: str, payload: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Triggers a custom plugin event.

        Corresponds to: POST /api/plugins/trigger_event
        Authentication: Required.

        Args:
            event_name (str): The namespaced name of the custom event to trigger.
            payload (Optional[Dict[str, Any]]): A JSON object containing data for event listeners.

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
        if not event_name:
            _LOGGER.error("Event name cannot be empty for trigger_plugin_event.")
            raise ValueError("Event name cannot be empty.")

        json_body: Dict[str, Any] = {"event_name": event_name}
        if payload is not None:
            json_body["payload"] = payload

        _LOGGER.info(
            "Triggering custom plugin event '%s' with payload: %s", event_name, payload
        )
        return await self._request(
            method="POST",
            path="/plugins/trigger_event",
            json_data=json_body,
            authenticated=True,
        )
