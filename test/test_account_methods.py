# tests/test_account_methods.py
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch
from bsm_api_client.api_client import BedrockServerManagerApi
from bsm_api_client.models import (
    User,
    ThemeUpdate,
    ProfileUpdate,
    ChangePasswordRequest,
    BaseApiResponse,
)


@pytest_asyncio.fixture
async def client():
    """Async fixture for a BedrockServerManagerApi instance."""
    client = BedrockServerManagerApi("http://localhost", "admin", "password")
    yield client
    await client.close()


@pytest.mark.asyncio
async def test_get_account_details(client):
    """Test async_get_account_details method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {
            "id": 1,
            "username": "admin",
            "identity_type": "local",
            "role": "admin",
            "is_active": True,
            "theme": "default",
        }
        result = await client.async_get_account_details()
        assert isinstance(result, User)
        assert result.username == "admin"
        mock_request.assert_called_once_with(method="GET", path="/account", authenticated=True)


@pytest.mark.asyncio
async def test_update_theme(client):
    """Test async_update_theme method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {"status": "success"}
        payload = ThemeUpdate(theme="dark")
        result = await client.async_update_theme(payload)
        assert isinstance(result, BaseApiResponse)
        assert result.status == "success"
        mock_request.assert_called_once_with(
            method="POST", path="/account/theme", json_data={"theme": "dark"}, authenticated=True
        )


@pytest.mark.asyncio
async def test_update_profile(client):
    """Test async_update_profile method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {"status": "success"}
        payload = ProfileUpdate(full_name="Admin User", email="admin@example.com")
        result = await client.async_update_profile(payload)
        assert isinstance(result, BaseApiResponse)
        assert result.status == "success"
        mock_request.assert_called_once_with(
            method="POST",
            path="/account/profile",
            json_data={"full_name": "Admin User", "email": "admin@example.com"},
            authenticated=True,
        )


@pytest.mark.asyncio
async def test_change_password(client):
    """Test async_change_password method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {"status": "success"}
        payload = ChangePasswordRequest(
            current_password="password", new_password="new_password"
        )
        result = await client.async_change_password(payload)
        assert isinstance(result, BaseApiResponse)
        assert result.status == "success"
        mock_request.assert_called_once_with(
            method="POST",
            path="/account/change-password",
            json_data={
                "current_password": "password",
                "new_password": "new_password",
            },
            authenticated=True,
        )
