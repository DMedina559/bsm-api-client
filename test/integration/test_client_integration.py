import pytest
from bsm_api_client.api_client import BedrockServerManagerApi
from bsm_api_client.exceptions import APIError
from bsm_api_client.models import (
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
        servers_response = await client.async_get_servers()
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
            await client.async_get_servers()
        assert excinfo.value.status_code == 401
    finally:
        await client.close()


@pytest.mark.asyncio
async def test_server_operations(server, bedrock_server):
    """
    Tests creating a server, managing its properties, allowlist, permissions, and then deleting it.
    This test relies on the `bedrock_server` fixture to create and tear down the server.
    """
    client = BedrockServerManagerApi(server, "admin", "password")
    server_name = bedrock_server

    try:
        # Verify server exists
        servers = await client.async_get_server_names()
        assert server_name in servers

        # -- Test Properties Management --
        properties_response = await client.async_get_server_properties(server_name)
        assert properties_response.status == "success"
        original_properties = properties_response.properties
        assert "level-name" in original_properties

        new_properties = {"level-name": "new-world-name"}
        update_payload = PropertiesPayload(properties=new_properties)
        update_result = await client.async_update_server_properties(
            server_name, update_payload
        )
        assert update_result.status == "success"

        properties_response_after_update = await client.async_get_server_properties(
            server_name
        )
        assert (
            properties_response_after_update.properties["level-name"]
            == "new-world-name"
        )

        # -- Test Allowlist Management --
        allowlist_response = await client.async_get_server_allowlist(server_name)
        assert allowlist_response.status == "success"
        if allowlist_response.players:
            assert allowlist_response.players == []

        add_payload = AllowlistAddPayload(players=["TestPlayer"])
        add_result = await client.async_add_server_allowlist(server_name, add_payload)
        assert add_result.status == "success"

        allowlist_response_after_add = await client.async_get_server_allowlist(
            server_name
        )
        assert allowlist_response_after_add.players is not None
        assert "TestPlayer" in [p["name"] for p in allowlist_response_after_add.players]

        remove_payload = AllowlistRemovePayload(players=["TestPlayer"])
        remove_result = await client.async_remove_server_allowlist_players(
            server_name, remove_payload
        )
        assert remove_result.status == "success"

        allowlist_response_after_remove = await client.async_get_server_allowlist(
            server_name
        )
        if allowlist_response_after_remove.players:
            assert allowlist_response_after_remove.players == []

        # -- Test Permissions Management --
        permissions_response = await client.async_get_server_permissions_data(
            server_name
        )
        assert permissions_response.status == "success"
        if permissions_response.data:
            assert permissions_response.data.get("permissions", []) == []

        permission = PlayerPermission(
            name="TestPlayer", xuid="123456789", permission_level="operator"
        )
        set_payload = PermissionsSetPayload(permissions=[permission])
        set_result = await client.async_set_server_permissions(server_name, set_payload)
        assert set_result.status == "success"

        permissions_response_after_set = await client.async_get_server_permissions_data(
            server_name
        )
        assert permissions_response_after_set.data is not None
        assert len(permissions_response_after_set.data["permissions"]) == 1
        player_permission = permissions_response_after_set.data["permissions"][0]
        assert player_permission["name"] == "Unknown (XUID: 123456789)"
        assert player_permission["permission_level"] == "operator"

    finally:
        await client.close()
