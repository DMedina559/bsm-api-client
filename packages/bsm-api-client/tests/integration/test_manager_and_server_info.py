import time

import pytest

from bsm_api_client.api_client import BedrockServerManagerApi
from bsm_api_client.models import (
    AddPlayersPayload,
    PruneDownloadsPayload,
    SettingItemPayload,
)


@pytest.mark.asyncio
class TestManagerAndServerInfo:
    """
    Integration tests for manager and server info methods.
    """

    async def test_get_info(self, server):
        """Tests the unauthenticated /info endpoint and themes."""
        client = BedrockServerManagerApi(
            server, "admin", "integration secure passphrase"
        )
        try:
            info = await client.application.async_get_info()
            assert info.status == "success"
            assert "app_version" in info.info

            themes = await client.application.async_get_themes()
            assert themes is not None

        finally:
            await client.close()

    async def test_prune_downloads(self, server, server_data_dir):
        """Tests pruning downloads cache."""
        (server_data_dir / ".downloads" / "stable").mkdir(parents=True, exist_ok=True)
        client = BedrockServerManagerApi(
            server, "admin", "integration secure passphrase"
        )
        try:
            payload = PruneDownloadsPayload(directory="stable", keep=1)
            res = await client.application.async_prune_downloads(payload)
            assert res.status == "skipped"
            assert res.files_deleted == 0
            assert not res.failures
        finally:
            await client.close()

    async def test_player_management(self, server):
        """Tests getting and adding global players."""
        client = BedrockServerManagerApi(
            server, "admin", "integration secure passphrase"
        )
        try:
            unique_name = f"TestPlayer_{int(time.time())}"
            unique_xuid = f"{int(time.time())}"
            player_string = f"{unique_name}:{unique_xuid}"

            players_before_res = await client.players.async_get_players()
            players_before = players_before_res.players
            assert not any(p["name"] == unique_name for p in players_before)

            add_payload = AddPlayersPayload(players=[player_string])
            add_result = await client.players.async_add_players(add_payload)
            assert add_result.status == "success"

            players_after_res = await client.players.async_get_players()
            players_after = players_after_res.players
            assert any(
                p["name"] == unique_name and p["xuid"] == unique_xuid
                for p in players_after
            )

        finally:
            await client.close()

    async def test_settings_management(self, server):
        """Tests getting and setting global settings."""
        client = BedrockServerManagerApi(
            server, "admin", "integration secure passphrase"
        )
        try:
            setting_key = "custom.test_setting"
            setting_value = f"test_value_{int(time.time())}"

            setting_payload = SettingItemPayload(key=setting_key, value=setting_value)
            set_result = await client.application.async_set_setting(setting_payload)
            assert set_result.status == "success"

            reload_result = await client.application.async_reload_settings()
            assert reload_result.status == "success"

            settings_after = await client.application.async_get_all_settings()
            assert settings_after.status == "success"

            keys = setting_key.split(".")
            value = settings_after.settings
            for k in keys:
                value = value[k]

            assert value == setting_value

        finally:
            await client.close()

    async def test_server_info_endpoints(
        self, server, bedrock_server, wait_for_server_status
    ):
        """Tests various server-specific informational endpoints."""
        client = BedrockServerManagerApi(
            server, "admin", "integration secure passphrase"
        )
        server_name = bedrock_server
        try:
            # Ensure server is stopped before this test
            status_res = await client.servers.async_get_server_running_status(
                server_name
            )
            if status_res.running:
                await client.servers.async_stop_server(server_name)
                await wait_for_server_status(client, server_name, is_running=False)

            validate_result = await client.servers.async_get_server_validate(
                server_name
            )
            assert validate_result is True

            process_info_res = await client.servers.async_get_server_process_info(
                server_name
            )
            assert process_info_res.status == "success"

            running_status_res = await client.servers.async_get_server_running_status(
                server_name
            )
            assert running_status_res.status == "success"
            assert (
                running_status_res.running is False
                or running_status_res.running is None
            )

        finally:
            await client.close()


@pytest.mark.asyncio
async def test_standalone_event_and_web_runtime_contracts_against_backend(server):
    from bsm_api_client.exceptions import InvalidInputError

    async with BedrockServerManagerApi(
        server, "admin", "integration secure passphrase"
    ) as client:
        runtime = await client.application.async_get_web_runtime()
        assert runtime.phase == "ready" and not runtime.shutdown_requested
        snapshot = await client.diagnostics.async_get_application_diagnostics()
        assert snapshot.summary.ready is True
        assert {"runtime", "events", "plugins"} <= {
            section.name for section in snapshot.sections
        }
        filtered = await client.diagnostics.async_get_subsystem_diagnostics("runtime")
        assert [section.name for section in filtered.sections] == ["runtime"]
        report = await client.diagnostics.async_get_diagnostic_report()
        assert report.snapshot.instance_id == snapshot.instance_id
        catalog = await client.events.async_list_application_events()
        assert any(event.name == "before_server_start" for event in catalog.events)
        activity = await client.events.async_get_event_activity(
            owner="application", limit=5
        )
        assert activity.accepting
        assert len(activity.recent) <= 5
        assert all("data" not in event.model_dump() for event in activity.recent)
        with pytest.raises(InvalidInputError):
            await client.events.async_get_event_activity(limit=0)
