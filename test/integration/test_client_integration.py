import pytest
import asyncio
from bsm_api_client.api_client import BedrockServerManagerApi
from bsm_api_client.exceptions import APIError
from bsm_api_client.models import InstallServerPayload, PropertiesPayload

@pytest.mark.asyncio
async def test_login(server):
    """
    Tests that the client can successfully log in to the server.
    """
    client = BedrockServerManagerApi(server, "admin", "password")
    try:
        servers_response = await client.async_get_servers_details()
        assert servers_response is not None
        assert isinstance(servers_response.servers, list)
    finally:
        await client.close()

@pytest.mark.asyncio
async def test_login_invalid_credentials(server):
    """
    Tests that the client fails to log in with invalid credentials.
    """
    client = BedrockServerManagerApi(server, "admin", "wrong_password")
    try:
        with pytest.raises(APIError) as excinfo:
            await client.async_get_servers_details()
        assert excinfo.value.status_code == 401
    finally:
        await client.close()

@pytest.mark.asyncio
async def test_server_lifecycle(server):
    """
    Tests creating a server, managing its properties, and deleting it.
    """
    client = BedrockServerManagerApi(server, "admin", "password")
    server_name = "test-server-properties"
    try:
        # Create server
        payload = InstallServerPayload(server_name=server_name, version="LATEST", overwrite=True)
        install_result = await client.async_install_new_server(payload)
        assert install_result.status == "pending"
        await asyncio.sleep(15)
        servers = await client.async_get_server_names()
        assert server_name in servers

        # Get properties
        properties_response = await client.async_get_server_properties(server_name)
        assert properties_response.status == "success"
        original_properties = properties_response.properties
        assert "level-name" in original_properties

        # Update properties
        new_properties = {"level-name": "new-world-name"}
        update_payload = PropertiesPayload(properties=new_properties)
        update_result = await client.async_update_server_properties(server_name, update_payload)
        assert update_result.status == "success"

        # Get properties again to verify update
        properties_response_after_update = await client.async_get_server_properties(server_name)
        assert properties_response_after_update.properties["level-name"] == "new-world-name"

    finally:
        # Clean up
        delete_result = await client.async_delete_server(server_name)
        assert delete_result.status == "pending"
        await asyncio.sleep(5)
        servers = await client.async_get_server_names()
        assert server_name not in servers
        await client.close()
