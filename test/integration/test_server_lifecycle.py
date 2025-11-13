import pytest
import pytest_asyncio
import asyncio
from bsm_api_client.api_client import BedrockServerManagerApi


@pytest_asyncio.fixture
async def client_fixture(server, bedrock_server, wait_for_server_status):
    """
    Provides a client and ensures the server is in a known (stopped)
    state before and after each test.
    """
    client = BedrockServerManagerApi(server, "admin", "password")
    server_name = bedrock_server
    try:
        # Ensure server is stopped before the test begins
        status_res = await client.async_get_server_running_status(server_name)
        if status_res.data.get("running"):
            await client.async_stop_server(server_name)
            await wait_for_server_status(client, server_name, is_running=False)

        yield client

    finally:
        # Ensure server is stopped after the test
        status_res = await client.async_get_server_running_status(server_name)
        if status_res.data.get("running"):
            await client.async_stop_server(server_name)
            await wait_for_server_status(
                client, server_name, is_running=False, timeout=30
            )
        await client.close()


@pytest.mark.asyncio
class TestServerLifecycle:
    """
    Integration tests for server lifecycle methods.
    """

    async def test_start_and_stop(
        self, bedrock_server, wait_for_server_status, client_fixture
    ):
        """Tests starting and stopping the server."""
        client = client_fixture
        server_name = bedrock_server

        start_res = await client.async_start_server(server_name)
        assert start_res.status == "success"
        await wait_for_server_status(client, server_name, is_running=True, timeout=90)

        stop_res = await client.async_stop_server(server_name)
        assert stop_res.status in ["success", "pending"]
        await wait_for_server_status(client, server_name, is_running=False, timeout=90)

    async def test_restart(
        self, bedrock_server, wait_for_server_status, client_fixture
    ):
        """Tests restarting the server."""
        client = client_fixture
        server_name = bedrock_server

        await client.async_start_server(server_name)
        await wait_for_server_status(client, server_name, is_running=True, timeout=90)

        restart_res = await client.async_restart_server(server_name)
        assert restart_res.status in ["success", "pending"]

        await asyncio.sleep(5)
        await wait_for_server_status(client, server_name, is_running=True, timeout=90)

    async def test_service_methods(self, bedrock_server, client_fixture):
        """Tests the service-related methods."""
        client = client_fixture
        server_name = bedrock_server

        details_res = await client.async_get_servers()
        server_details = next(
            s for s in details_res.servers if s["name"] == server_name
        )

        original_autostart = server_details.get("autostart_service", False)
        original_autoupdate = server_details.get("autoupdate", False)

        if original_autostart:
            await client.async_disable_server_service(server_name)
        else:
            await client.async_enable_server_service(server_name)

        await client.async_set_server_autoupdate(server_name, not original_autoupdate)

        details_after_res = await client.async_get_servers()
        server_details_after = next(
            s for s in details_after_res.servers if s["name"] == server_name
        )

        assert server_details_after.get("autostart_service") is not original_autostart
        assert server_details_after.get("autoupdate") is not original_autoupdate

    async def test_update_server(self, bedrock_server, client_fixture):
        """Tests the server update method."""
        client = client_fixture
        server_name = bedrock_server

        # The ActionResponse for this endpoint does not contain a task_id,
        # so we can only verify that the command is accepted.
        update_res = await client.async_update_server(server_name)
        assert update_res.status in ["success", "pending"]
