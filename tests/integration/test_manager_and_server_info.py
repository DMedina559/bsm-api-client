import time

import pytest

from bsm_api_client.api_client import BedrockServerManagerApi
from bsm_api_client.models import (
    AddPlayersPayload,
    PruneDownloadsPayload,
    SettingItemResponse,
)


@pytest.mark.asyncio
class TestManagerAndServerInfo:
    """
    Integration tests for manager and server info methods.
    """

    async def test_get_info(self, server):
        """Tests the unauthenticated /info endpoint and themes."""
        client = BedrockServerManagerApi(server, "admin", "password")
        try:
            info = await client.async_get_info()
            assert info.status == "success"
            assert "app_version" in info.info

            themes = await client.async_get_themes()
            assert themes is not None

        finally:
            await client.close()

    async def test_prune_downloads(self, server):
        """Tests pruning downloads cache."""
        client = BedrockServerManagerApi(server, "admin", "password")
        try:
            payload = PruneDownloadsPayload(directory="stable", keep=1)
            res = await client.async_prune_downloads(payload)
            assert res.status == "success"
        finally:
            await client.close()

    async def test_player_management(self, server):
        """Tests getting and adding global players."""
        client = BedrockServerManagerApi(server, "admin", "password")
        try:
            unique_name = f"TestPlayer_{int(time.time())}"
            unique_xuid = f"{int(time.time())}"
            player_string = f"{unique_name}:{unique_xuid}"

            players_before_res = await client.async_get_players()
            players_before = players_before_res.players
            assert not any(p["name"] == unique_name for p in players_before)

            add_payload = AddPlayersPayload(players=[player_string])
            add_result = await client.async_add_players(add_payload)
            assert add_result.status == "success"

            players_after_res = await client.async_get_players()
            players_after = players_after_res.players
            assert any(
                p["name"] == unique_name and p["xuid"] == unique_xuid
                for p in players_after
            )

        finally:
            await client.close()

    async def test_settings_management(self, server):
        """Tests getting and setting global settings."""
        client = BedrockServerManagerApi(server, "admin", "password")
        try:
            setting_key = "custom.test_setting"
            setting_value = f"test_value_{int(time.time())}"

            setting_payload = SettingItemResponse(key=setting_key, value=setting_value)
            set_result = await client.async_set_setting(setting_payload)
            assert set_result.status == "success"

            reload_result = await client.async_reload_settings()
            assert reload_result.status == "success"

            settings_after = await client.async_get_all_settings()
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
        client = BedrockServerManagerApi(server, "admin", "password")
        server_name = bedrock_server
        try:
            # Ensure server is stopped before this test
            status_res = await client.async_get_server_running_status(server_name)
            if status_res.running:
                await client.async_stop_server(server_name)
                await wait_for_server_status(client, server_name, is_running=False)

            validate_result = await client.async_get_server_validate(server_name)
            assert validate_result is True

            version_res = await client.async_get_server_version(server_name)
            assert version_res.status == "success"
            # It's possible for the version to be None if the server is stopped or newly installed without being started,
            # but since we just checked the endpoint, we pass if the request is successful.

            config_status_res = await client.async_get_server_config_status(server_name)
            assert config_status_res.status == "success"
            assert config_status_res.config_status in [
                "INSTALLED",
                "STOPPED",
                None,
            ]

            process_info_res = await client.async_get_server_process_info(server_name)
            assert process_info_res.status == "success"

            running_status_res = await client.async_get_server_running_status(
                server_name
            )
            assert running_status_res.status == "success"
            assert (
                running_status_res.running is False
                or running_status_res.running is None
            )

        finally:
            await client.close()
