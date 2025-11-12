import pytest
import pytest_asyncio
import subprocess
import time
import aiohttp
import asyncio
import os
import sys
from bsm_api_client.api_client import BedrockServerManagerApi
from bsm_api_client.models import InstallServerPayload


@pytest.fixture(scope="session")
def server():
    """
    A pytest fixture that starts the bedrock-server-manager web server
    and sets it up for testing.
    """
    host = "0.0.0.0"
    port = 11325
    # When binding to 0.0.0.0, we connect to 127.0.0.1
    connect_host = "127.0.0.1"
    base_url = f"http://{connect_host}:{port}"

    # Remove the database file if it exists, to ensure a clean setup
    db_path = os.path.expanduser("~/bedrock-server-manager/bedrock_server_manager.db")
    if os.path.exists(db_path):
        os.remove(db_path)

    # Start the server
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "bedrock_server_manager",
            "web",
            "start",
            "--host",
            host,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:

        async def wait_and_setup():
            # Wait for the server to start
            for _ in range(60):  # 60 * 0.5s = 30s timeout
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(f"{base_url}/setup") as response:
                            if response.status == 200:
                                break
                except aiohttp.ClientConnectorError:
                    await asyncio.sleep(0.5)
            else:
                pytest.fail("Server did not start within 30 seconds.")

            # Perform initial setup
            async with aiohttp.ClientSession() as session:
                payload = {"username": "admin", "password": "password"}
                async with session.post(f"{base_url}/setup/create-first-user", json=payload) as response:
                    if response.status == 400:
                        text = await response.text()
                        if "Setup already completed" in text:
                            pass
                        else:
                            pytest.fail(f"Failed to setup server: {text}")
                    elif response.status != 200:
                        pytest.fail(f"Failed to setup server: {await response.text()}")

        asyncio.run(wait_and_setup())
        yield base_url
    finally:
        process.terminate()
        process.wait()
        stdout, stderr = process.communicate()
        if process.returncode != 0 and process.returncode != -15:  # -15 is SIGTERM
            print("Server exited with an error.")
            print("STDOUT:", stdout.decode())
            print("STDERR:", stderr.decode())


@pytest_asyncio.fixture(scope="session")
async def bedrock_server(server):
    """
    A pytest fixture that creates a single bedrock server instance for all tests to use.
    The server is deleted at the end of the test session.
    """
    server_name = "test-server"
    client = BedrockServerManagerApi(server, "admin", "password")
    try:
        payload = InstallServerPayload(
            server_name=server_name, version="LATEST", overwrite=True
        )
        install_result = await client.async_install_new_server(payload)

        if install_result.task_id:
            for _ in range(90):  # 90s timeout for installation task
                await asyncio.sleep(2)  # Poll every 2 seconds
                status_response = await client.async_get_task_status(
                    install_result.task_id
                )
                if status_response["status"] == "success":
                    break
                elif status_response["status"] == "error":
                    pytest.fail(
                        f"Installation task failed: {status_response['message']}"
                    )
            else:
                pytest.fail("Installation task timed out after 180 seconds.")
        elif install_result.status != "success":
            pytest.fail(f"Failed to install server: {install_result.message}")

        yield server_name

    finally:
        try:
            # Ensure the server is stopped before trying to delete it
            status_res = await client.async_get_server_running_status(server_name)
            if status_res.data.get("running"):
                await client.async_stop_server(server_name)
                # Give it a moment to stop
                for _ in range(30):
                    await asyncio.sleep(1)
                    status_res = await client.async_get_server_running_status(
                        server_name
                    )
                    if not status_res.data.get("running"):
                        break
                else:
                    pytest.fail(
                        f"Server {server_name} did not stop within 30 seconds before deletion."
                    )

            delete_result = await client.async_delete_server(server_name)
            assert delete_result.status in ["pending", "success"]

            for _ in range(10):
                await asyncio.sleep(1)
                servers = await client.async_get_server_names()
                if server_name not in servers:
                    break
            else:
                pytest.fail(f"Server {server_name} was not deleted within 10 seconds.")
        finally:
            await client.close()


@pytest_asyncio.fixture(scope="session")
async def wait_for_server_status():
    """Provides a helper function to wait for server status."""

    async def _wait_for_server_status(client, server_name, is_running, timeout=60):
        """Helper to wait for the server to reach a desired running state."""
        for _ in range(timeout):
            status_res = await client.async_get_server_running_status(server_name)
            if status_res.data.get("running") == is_running:
                return
            await asyncio.sleep(1)
        status_str = "running" if is_running else "stopped"
        pytest.fail(
            f"Server did not enter '{status_str}' state within {timeout} seconds."
        )

    return _wait_for_server_status
