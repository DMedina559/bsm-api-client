import pytest
import pytest_asyncio
import asyncio
import os
from bsm_api_client.api_client import BedrockServerManagerApi
from bsm_api_client.models import (
    BackupActionPayload,
    RestoreActionPayload,
    FileNamePayload,
)


@pytest_asyncio.fixture(scope="class")
async def content_files():
    """
    Fixture to create dummy content files for testing world/addon installation.
    """
    bsm_dir = os.path.expanduser("~/bedrock-server-manager")
    worlds_dir = os.path.join(bsm_dir, "content", "worlds")
    addons_dir = os.path.join(bsm_dir, "content", "addons")
    os.makedirs(worlds_dir, exist_ok=True)
    os.makedirs(addons_dir, exist_ok=True)
    dummy_world_file = "test_world.mcworld"
    dummy_addon_file = "test_addon.mcpack"
    world_path = os.path.join(worlds_dir, dummy_world_file)
    addon_path = os.path.join(addons_dir, dummy_addon_file)
    with open(world_path, "w") as f:
        f.write("dummy world content")
    with open(addon_path, "w") as f:
        f.write("dummy addon content")
    yield {"world_file": dummy_world_file, "addon_file": dummy_addon_file}
    if os.path.exists(world_path):
        os.remove(world_path)
    if os.path.exists(addon_path):
        os.remove(addon_path)


@pytest_asyncio.fixture
async def content_client(server, bedrock_server, wait_for_server_status):
    """
    Provides a client and ensures the server is stopped before and after each test.
    """
    client = BedrockServerManagerApi(server, "admin", "password")
    server_name = bedrock_server
    try:
        status_res = await client.async_get_server_running_status(server_name)
        if status_res.data.get("running"):
            await client.async_stop_server(server_name)
            await wait_for_server_status(
                client, server_name, is_running=False, timeout=90
            )
        yield client
    finally:
        status_res = await client.async_get_server_running_status(server_name)
        if status_res.data.get("running"):
            await client.async_stop_server(server_name)
            await wait_for_server_status(
                client, server_name, is_running=False, timeout=90
            )
        await client.close()


@pytest.mark.asyncio
@pytest.mark.usefixtures("content_files")
class TestContentManagement:
    """
    Integration tests for content management methods.
    """

    async def test_backup_and_restore(
        self, bedrock_server, wait_for_server_status, content_client
    ):
        """
        Tests creating a backup, listing it, and then restoring it.
        """
        client = content_client
        server_name = bedrock_server
        await client.async_start_server(server_name)
        await wait_for_server_status(client, server_name, is_running=True, timeout=90)
        backup_payload = BackupActionPayload(backup_type="world")
        backup_result = await client.async_trigger_server_backup(
            server_name, backup_payload
        )
        assert backup_result.status in ["success", "pending"]
        list_response = None
        for _ in range(90):  # Increased timeout
            list_response = await client.async_list_server_backups(server_name, "world")
            if list_response.backups and len(list_response.backups) > 0:
                break
            await asyncio.sleep(1)
        else:
            pytest.fail("Backup file did not appear in the backup list in time.")
        backup_file = list_response.backups[0]
        restore_payload = RestoreActionPayload(
            restore_type="world", backup_file=backup_file
        )
        restore_result = await client.async_restore_server_backup(
            server_name, restore_payload
        )
        assert restore_result.status in ["success", "pending"]

    async def test_world_and_addon_management(
        self, bedrock_server, content_files, content_client
    ):
        """
        Tests listing and installing worlds and addons.
        """
        client = content_client
        server_name = bedrock_server
        dummy_world_file = content_files["world_file"]
        dummy_addon_file = content_files["addon_file"]
        worlds_list = await client.async_get_content_worlds()
        assert worlds_list.status == "success"
        assert dummy_world_file in worlds_list.files
        install_world_payload = FileNamePayload(filename=dummy_world_file)
        install_world_result = await client.async_install_server_world(
            server_name, install_world_payload
        )
        assert install_world_result.status in ["success", "pending"]
        addons_list = await client.async_get_content_addons()
        assert addons_list.status == "success"
        assert dummy_addon_file in addons_list.files
        install_addon_payload = FileNamePayload(filename=dummy_addon_file)
        install_addon_result = await client.async_install_server_addon(
            server_name, install_addon_payload
        )
        assert install_addon_result.status in ["success", "pending"]

    async def test_other_content_actions(
        self, bedrock_server, wait_for_server_status, content_client
    ):
        """
        Tests other content-related actions like export, prune, and reset.
        """
        client = content_client
        server_name = bedrock_server
        await client.async_start_server(server_name)
        await wait_for_server_status(client, server_name, is_running=True, timeout=90)
        worlds_before_list = await client.async_get_content_worlds()
        worlds_before = worlds_before_list.files or []
        export_result = await client.async_export_server_world(server_name)
        assert export_result.status in ["success", "pending"]
        for _ in range(90):  # Increased timeout
            worlds_after_list = await client.async_get_content_worlds()
            worlds_after = worlds_after_list.files or []
            if len(worlds_after) > len(worlds_before):
                break
            await asyncio.sleep(1)
        else:
            pytest.fail("World export did not result in a new file in time.")
        await client.async_stop_server(server_name)
        await wait_for_server_status(client, server_name, is_running=False, timeout=90)
        prune_result = await client.async_prune_server_backups(server_name)
        assert prune_result.status in ["success", "pending"]
        reset_result = await client.async_reset_server_world(server_name)
        assert reset_result.status in ["success", "pending"]
