import pytest
import asyncio
from bsm_api_client.api_client import BedrockServerManagerApi
from bsm_api_client.exceptions import APIError
from bsm_api_client.models import (
    InstallServerPayload,
    PropertiesPayload,
    AllowlistAddPayload,
    AllowlistRemovePayload,
    PermissionsSetPayload,
    PlayerPermission,
)

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


@pytest.mark.asyncio
async def test_allowlist_management(server):
    """
    Tests managing the allowlist for a server.
    """
    client = BedrockServerManagerApi(server, "admin", "password")
    server_name = "test-server-allowlist"
    try:
        # Create server
        payload = InstallServerPayload(server_name=server_name, version="LATEST", overwrite=True)
        install_result = await client.async_install_new_server(payload)
        assert install_result.status == "pending"
        await asyncio.sleep(15)
        servers = await client.async_get_server_names()
        assert server_name in servers

        # Get initial allowlist
        allowlist_response = await client.async_get_server_allowlist(server_name)
        assert allowlist_response.status == "success"
        if allowlist_response.players:
            assert allowlist_response.players == []

        # Add player to allowlist
        add_payload = AllowlistAddPayload(players=["TestPlayer"])
        add_result = await client.async_add_server_allowlist(server_name, add_payload)
        assert add_result.status == "success"

        # Get allowlist again to verify addition
        allowlist_response_after_add = await client.async_get_server_allowlist(server_name)
        assert allowlist_response_after_add.players is not None
        assert "TestPlayer" in [p["name"] for p in allowlist_response_after_add.players]

        # Remove player from allowlist
        remove_payload = AllowlistRemovePayload(players=["TestPlayer"])
        remove_result = await client.async_remove_server_allowlist_players(server_name, remove_payload)
        assert remove_result.status == "success"

        # Get allowlist again to verify removal
        allowlist_response_after_remove = await client.async_get_server_allowlist(server_name)
        if allowlist_response_after_remove.players:
            assert allowlist_response_after_remove.players == []

    finally:
        # Clean up
        delete_result = await client.async_delete_server(server_name)
        assert delete_result.status == "pending"
        await asyncio.sleep(5)
        servers = await client.async_get_server_names()
        assert server_name not in servers
        await client.close()

@pytest.mark.asyncio
async def test_permissions_management(server):
    """
    Tests managing permissions for a server.
    """
    client = BedrockServerManagerApi(server, "admin", "password")
    server_name = "test-server-permissions"
    try:
        # Create server
        payload = InstallServerPayload(server_name=server_name, version="LATEST", overwrite=True)
        install_result = await client.async_install_new_server(payload)
        assert install_result.status == "pending"
        await asyncio.sleep(15)
        servers = await client.async_get_server_names()
        assert server_name in servers

        # Get initial permissions
        permissions_response = await client.async_get_server_permissions_data(server_name)
        assert permissions_response.status == "success"
        if permissions_response.data:
            assert permissions_response.data.get("permissions", []) == []

        # Set permissions for a player
        permission = PlayerPermission(name="TestPlayer", xuid="123456789", permission_level="operator")
        set_payload = PermissionsSetPayload(permissions=[permission])
        set_result = await client.async_set_server_permissions(server_name, set_payload)
        assert set_result.status == "success"

        # Get permissions again to verify
        permissions_response_after_set = await client.async_get_server_permissions_data(server_name)
        assert permissions_response_after_set.data is not None
        assert len(permissions_response_after_set.data["permissions"]) == 1
        player_permission = permissions_response_after_set.data["permissions"][0]
        assert player_permission["name"] == "Unknown (XUID: 123456789)"
        assert player_permission["permission_level"] == "operator"

    finally:
        # Clean up
        delete_result = await client.async_delete_server(server_name)
        assert delete_result.status == "pending"
        await asyncio.sleep(5)
        servers = await client.async_get_server_names()
        assert server_name not in servers
        await client.close()
