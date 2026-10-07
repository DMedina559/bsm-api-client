import asyncio
import os
import subprocess
import sys
import tempfile

import aiohttp
import pytest
import pytest_asyncio

from bsm_api_client.api_client import BedrockServerManagerApi
from bsm_api_client.models import InstallServerPayload


@pytest.fixture(scope="session")
def server_data_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("bsm-data")


@pytest.fixture(scope="session")
def server(server_data_dir):  # noqa: C901
    """
    A pytest fixture that starts the bedrock-server-manager web server
    and sets it up for testing in an isolated temporary directory.
    """
    host = "0.0.0.0"
    port = 11325
    # When binding to 0.0.0.0, we connect to 127.0.0.1
    connect_host = "127.0.0.1"
    base_url = f"http://{connect_host}:{port}"

    # Use a temporary directory for complete isolation
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        import socket
        from pathlib import Path

        root = Path(temp_dir)
        config_dir = root / "config"
        data_dir = server_data_dir
        config_dir.mkdir()
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            port = listener.getsockname()[1]
        base_url = f"http://{connect_host}:{port}"
        env = os.environ.copy()

        process = None
        server_log = None
        try:
            print(f"\n[Test Server] Starting isolated instance in: {temp_dir}")
            server_log = open("bedrock_server_manager_test.log", "w")
            process = subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "bedrock_server_manager",
                    "--config-dir",
                    str(config_dir),
                    "--data-dir",
                    str(data_dir),
                    "--db-url",
                    f"sqlite+aiosqlite:///{data_dir / 'bsm.db'}",
                    "web",
                    "start",
                    "--host",
                    host,
                    "--port",
                    str(port),
                ],
                env=env,
                stdout=server_log,
                stderr=server_log,
            )

            async def wait_and_setup():
                needs_setup = False
                # Wait for the server to start
                for _ in range(60):  # 60 * 0.5s = 30s timeout
                    try:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(
                                f"{base_url}/api/setup/status"
                            ) as response:
                                if response.status == 200:
                                    data = await response.json()
                                    needs_setup = data.get("needs_setup", False)
                                    print(
                                        f"[Test Server] Reached API. needs_setup = {needs_setup}"
                                    )
                                    break
                    except aiohttp.ClientConnectorError:
                        await asyncio.sleep(0.5)
                else:
                    pytest.fail("Server did not start within 30 seconds.")

                # Perform initial setup
                if needs_setup:
                    print("[Test Server] Creating first user: admin / password")
                    async with aiohttp.ClientSession() as session:
                        payload = {"username": "admin", "password": "password"}
                        async with session.post(
                            f"{base_url}/api/setup/create-first-user", json=payload
                        ) as response:
                            if response.status == 400:
                                text = await response.text()
                                if "Setup already completed" in text:
                                    print("[Test Server] Setup was already completed.")
                                else:
                                    pytest.fail(f"Failed to setup server (400): {text}")
                            elif response.status != 200:
                                pytest.fail(
                                    f"Failed to setup server ({response.status}): {await response.text()}"
                                )
                            else:
                                print("[Test Server] First user created successfully.")
                else:
                    print(
                        "[Test Server] WARNING: Server skipped setup on a fresh database!"
                    )

            asyncio.run(wait_and_setup())
            yield base_url
        finally:
            if process is not None:
                process.terminate()
                process.wait()
                if process.returncode not in (0, 15, -15):
                    print(
                        f"Server exited with an error (code {process.returncode}). Check bedrock_server_manager_test.log for details."
                    )
            if server_log is not None:
                server_log.close()


@pytest_asyncio.fixture(scope="session")
async def bedrock_server(server):
    """
    A pytest fixture that creates a single bedrock server instance for all tests to use.
    The server is deleted at the end of the test session.
    """
    server_name = "test-server"
    client = BedrockServerManagerApi(server, "admin", "password")
    installed = False
    try:
        payload = InstallServerPayload(
            server_name=server_name, server_version="LATEST", overwrite=True
        )
        install_result = await client.async_install_new_server(payload)

        if install_result.task_id:
            for _ in range(90):  # 90s timeout for installation task
                await asyncio.sleep(2)  # Poll every 2 seconds
                status_response = await client.async_get_task_status(
                    install_result.task_id
                )
                if status_response["status"] == "success":
                    result = status_response.get("result") or {}
                    if isinstance(result, dict) and result.get("status") == "error":
                        pytest.fail(
                            f"Installation task failed: {result.get('message')}"
                        )
                    break
                elif status_response["status"] == "error":
                    pytest.fail(
                        f"Installation task failed: {status_response['message']}"
                    )
            else:
                pytest.fail("Installation task timed out after 180 seconds.")
        elif install_result.status != "success":
            pytest.fail(f"Failed to install server: {install_result.message}")

        assert await client.async_get_server_validate(server_name)
        installed = True
        yield server_name

    finally:
        try:
            if installed:
                # Ensure the server is stopped before trying to delete it
                status_res = await client.async_get_server_running_status(server_name)
                if status_res.running:
                    await client.async_stop_server(server_name)
                    # Give it a moment to stop
                    for _ in range(30):
                        await asyncio.sleep(1)
                        status_res = await client.async_get_server_running_status(
                            server_name
                        )
                        if not status_res.running:
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
                    pytest.fail(
                        f"Server {server_name} was not deleted within 10 seconds."
                    )
        finally:
            await client.close()


@pytest_asyncio.fixture(scope="session")
async def wait_for_server_status(server_data_dir):
    """Provides a helper function to wait for server status."""

    async def _wait_for_server_status(client, server_name, is_running, timeout=60):
        """Helper to wait for the server to reach a desired running state."""
        for _ in range(timeout):
            status_res = await client.async_get_server_running_status(server_name)
            if status_res.running == is_running:
                if not is_running:
                    return
                # A spawned process is running before Bedrock accepts commands.
                log = server_data_dir / "servers" / server_name / "server_output.txt"
                if log.exists() and "Server started" in log.read_text(errors="replace"):
                    return
            await asyncio.sleep(1)
        status_str = "running" if is_running else "stopped"
        pytest.fail(
            f"Server did not enter '{status_str}' state within {timeout} seconds."
        )

    return _wait_for_server_status
