import pytest
import subprocess
import time
import aiohttp
import asyncio
import os
import sys

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
            host
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
                async with session.post(f"{base_url}/setup", json=payload) as response:
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
        if process.returncode != 0 and process.returncode != -15: # -15 is SIGTERM
            print("Server exited with an error.")
            print("STDOUT:", stdout.decode())
            print("STDERR:", stderr.decode())
