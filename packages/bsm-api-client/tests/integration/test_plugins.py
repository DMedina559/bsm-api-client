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
            assert isinstance(status_res.plugins, dict) or status_res.plugins is None
            if status_res.plugins is not None:
                assert DEFAULT_PLUGIN_NAME in status_res.plugins
            else:
                pytest.skip("No plugins found")
        finally:
            await client.close()

    async def test_set_plugin_status(self, server):
        """Tests enabling and disabling a default plugin."""
        client = BedrockServerManagerApi(server, "admin", "password")
        try:
            # 1. Get initial status
            status_res = await client.async_get_plugin_statuses()
            plugin_data = status_res.plugins
            if plugin_data is None:
                pytest.skip("No plugins found")
            assert DEFAULT_PLUGIN_NAME in plugin_data
            original_status = plugin_data[DEFAULT_PLUGIN_NAME]["enabled"]

            # 2. Toggle the status
            new_status = not original_status
            payload = PluginStatusSetPayload(enabled=new_status)
            set_res = await client.async_set_plugin_status(DEFAULT_PLUGIN_NAME, payload)
            assert set_res.status == "success"

            # 3. Verify the status changed
            status_res_after = await client.async_get_plugin_statuses()
            assert (
                status_res_after.plugins[DEFAULT_PLUGIN_NAME]["enabled"] is new_status
            )

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


@pytest.mark.parametrize(
    "module,class_name,tag,paths",
    [
        (
            "download_page_plugin",
            "DownloadPagePlugin",
            "Download Page Plugin",
            {"/api/download_page/ui", "/api/download_page/download"},
        ),
        (
            "content_uploader_plugin",
            "ContentUploaderPlugin",
            "Content Uploader Plugin",
            {"/content/upload/ui", "/api/content/upload"},
        ),
    ],
)
def test_builtin_plugin_operation_discovery(
    monkeypatch, tmp_path, module, class_name, tag, paths
):
    """Discover actual backend router schemas without starting plugin tasks."""
    import importlib
    import json
    from unittest.mock import AsyncMock

    from click.testing import CliRunner
    from fastapi import APIRouter, FastAPI

    from bsm_cli.__main__ import cli
    from bsm_cli.config import Config

    plugin_class = getattr(
        importlib.import_module(f"bedrock_server_manager.plugins.default.{module}"),
        class_name,
    )
    plugin = plugin_class.__new__(plugin_class)
    plugin.router = APIRouter(tags=[tag])
    plugin._define_routes()
    app = FastAPI()
    app.include_router(plugin.router)
    schema = app.openapi()
    monkeypatch.setattr(
        BedrockServerManagerApi, "_fetch_openapi_schema", AsyncMock(return_value=schema)
    )
    monkeypatch.setattr("bsm_cli.config.get_config_path", lambda: tmp_path / "cli.json")
    Config().update(base_url="http://localhost", username="admin", password="password")
    result = CliRunner().invoke(cli, ["--json", "plugin", "operations", module])
    assert result.exit_code == 0, result.output
    rows = json.loads(result.stdout)
    assert {row["path"] for row in rows} == paths
    assert all(row["plugin"] == module for row in rows)
    assert not result.stderr


@pytest.mark.asyncio
async def test_typed_plugin_settings_round_trip(server):
    from bsm_api_client.exceptions import InvalidInputError
    from bsm_api_client.models import PluginSettingsPayload

    async with BedrockServerManagerApi(server, "admin", "password") as client:
        name = "backup_on_start"
        original = await client.async_get_plugin_settings(name)
        assert original.settings_schema
        try:
            updated = {
                **original.settings,
                "enable_backup_on_start": not original.settings[
                    "enable_backup_on_start"
                ],
            }
            await client.async_update_plugin_settings(
                name, PluginSettingsPayload(settings=updated)
            )
            assert (await client.async_get_plugin_settings(name)).settings == updated
            with pytest.raises(InvalidInputError):
                await client.async_update_plugin_settings(
                    name,
                    PluginSettingsPayload(
                        settings={**updated, "servers": ["does_not_exist"]}
                    ),
                )
        finally:
            await client.async_update_plugin_settings(
                name, PluginSettingsPayload(settings=original.settings)
            )
