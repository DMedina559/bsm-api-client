import pytest
from bsm_api_client.api_client import BedrockServerManagerApi
from bsm_api_client.models import PluginStatusSetPayload, TriggerEventPayload

# The name of the default plugin we will use for testing.
DEFAULT_PLUGIN_NAME = "autostart_plugin"


@pytest.mark.asyncio
class TestPluginSystem:
    """
    Integration tests for the plugin system, using a default plugin.
    """

    async def test_get_plugin_statuses(self, server):
        """Tests that we can get the status of all plugins."""
        client = BedrockServerManagerApi(server, "admin", "password")
        try:
            await client.async_reload_plugins()
            status_res = await client.async_get_plugin_statuses()

            assert status_res.status == "success"
            # The data is a dictionary of plugins, not a list.
            assert isinstance(status_res.data, dict)
            assert DEFAULT_PLUGIN_NAME in status_res.data
        finally:
            await client.close()

    async def test_set_plugin_status(self, server):
        """Tests enabling and disabling a default plugin."""
        client = BedrockServerManagerApi(server, "admin", "password")
        try:
            # 1. Get initial status
            status_res = await client.async_get_plugin_statuses()
            plugin_data = status_res.data
            assert DEFAULT_PLUGIN_NAME in plugin_data
            original_status = plugin_data[DEFAULT_PLUGIN_NAME]["enabled"]

            # 2. Toggle the status
            new_status = not original_status
            payload = PluginStatusSetPayload(enabled=new_status)
            set_res = await client.async_set_plugin_status(DEFAULT_PLUGIN_NAME, payload)
            assert set_res.status == "success"

            # 3. Verify the status changed
            status_res_after = await client.async_get_plugin_statuses()
            assert status_res_after.data[DEFAULT_PLUGIN_NAME]["enabled"] is new_status

            # 4. Revert to original state for test idempotency
            revert_payload = PluginStatusSetPayload(enabled=original_status)
            await client.async_set_plugin_status(DEFAULT_PLUGIN_NAME, revert_payload)

        finally:
            await client.close()

    async def test_trigger_plugin_event(self, server):
        """Tests triggering a custom plugin event."""
        client = BedrockServerManagerApi(server, "admin", "password")
        try:
            payload = TriggerEventPayload(
                event_name="any_event", payload={"data": "some_value"}
            )
            trigger_res = await client.async_trigger_plugin_event(payload)
            assert trigger_res.status == "success"
        finally:
            await client.close()

    async def test_reload_plugins(self, server):
        """Tests the reload plugins endpoint."""
        client = BedrockServerManagerApi(server, "admin", "password")
        try:
            reload_res = await client.async_reload_plugins()
            assert reload_res.status == "success"
        finally:
            await client.close()
