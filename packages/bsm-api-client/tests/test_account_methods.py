# tests/test_account_methods.py
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio

from bsm_api_client.api_client import BedrockServerManagerApi
from bsm_api_client.models import (
    BaseApiResponse,
    ChangePasswordPayload,
    ProfileUpdatePayload,
    ThemeUpdatePayload,
    UserResponse,
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
    with patch.object(
        client, "async_call_generated", new_callable=AsyncMock
    ) as mock_request:
        mock_request.return_value = {
            "id": 1,
            "username": "admin",
            "identity_type": "local",
            "role": "admin",
            "is_active": True,
            "theme": "default",
        }
        result = await client.account.async_get_account_details()
        assert isinstance(result, UserResponse)
        assert result.username == "admin"
        mock_request.assert_called_once_with(
            "get_account", authenticated=True, typed=True
        )


@pytest.mark.asyncio
async def test_update_theme(client):
    """Test async_update_theme method."""
    with patch.object(
        client, "async_call_generated", new_callable=AsyncMock
    ) as mock_request:
        mock_request.return_value = {"status": "success"}
        payload = ThemeUpdatePayload(theme="dark")
        result = await client.account.async_update_theme(payload)
        assert isinstance(result, BaseApiResponse)
        assert result.status == "success"
        mock_request.assert_called_once_with(
            "update_account_theme",
            body={"theme": "dark"},
            authenticated=True,
            typed=True,
        )


@pytest.mark.asyncio
async def test_update_profile(client):
    """Test async_update_profile method."""
    with patch.object(
        client, "async_call_generated", new_callable=AsyncMock
    ) as mock_request:
        mock_request.return_value = {"status": "success"}
        payload = ProfileUpdatePayload(
            full_name="Admin User", email="admin@example.com"
        )
        result = await client.account.async_update_profile(payload)
        assert isinstance(result, BaseApiResponse)
        assert result.status == "success"
        mock_request.assert_called_once_with(
            "update_account_profile",
            body={"full_name": "Admin User", "email": "admin@example.com"},
            authenticated=True,
            typed=True,
        )


@pytest.mark.asyncio
async def test_change_password(client):
    """Test async_change_password method."""
    with patch.object(
        client, "async_call_generated", new_callable=AsyncMock
    ) as mock_request:
        mock_request.return_value = {"status": "success"}
        payload = ChangePasswordPayload(
            current_password="password", new_password="new_password"
        )
        result = await client.account.async_change_password(payload)
        assert isinstance(result, BaseApiResponse)
        assert result.status == "success"
        mock_request.assert_called_once_with(
            "change_password",
            body={"current_password": "password", "new_password": "new_password"},
            authenticated=True,
            typed=True,
        )


@pytest.mark.asyncio
async def test_get_account_details_error(client):
    """Test async_get_account_details method with an API error."""
    with patch.object(
        client, "async_call_generated", new_callable=AsyncMock
    ) as mock_request:
        mock_request.side_effect = Exception("API Error")
        with pytest.raises(Exception) as excinfo:
            await client.account.async_get_account_details()
        assert "API Error" in str(excinfo.value)


@pytest.mark.asyncio
async def test_update_theme_error(client):
    """Test async_update_theme method with an API error."""
    with patch.object(
        client, "async_call_generated", new_callable=AsyncMock
    ) as mock_request:
        mock_request.side_effect = Exception("API Error")
        with pytest.raises(Exception) as excinfo:
            await client.account.async_update_theme(ThemeUpdatePayload(theme="dark"))
        assert "API Error" in str(excinfo.value)


@pytest.mark.asyncio
async def test_update_profile_error(client):
    """Test async_update_profile method with an API error."""
    with patch.object(
        client, "async_call_generated", new_callable=AsyncMock
    ) as mock_request:
        mock_request.side_effect = Exception("API Error")
        with pytest.raises(Exception) as excinfo:
            await client.account.async_update_profile(
                ProfileUpdatePayload(full_name="Admin User", email="admin@example.com")
            )
        assert "API Error" in str(excinfo.value)


@pytest.mark.asyncio
async def test_change_password_error(client):
    """Test async_change_password method with an API error."""
    with patch.object(
        client, "async_call_generated", new_callable=AsyncMock
    ) as mock_request:
        mock_request.side_effect = Exception("API Error")
        with pytest.raises(Exception) as excinfo:
            await client.account.async_change_password(
                ChangePasswordPayload(
                    current_password="password", new_password="new_password"
                )
            )
        assert "API Error" in str(excinfo.value)


@pytest.mark.asyncio
async def test_integration_credentials_never_silently_fall_back_to_password_login(
    client,
):
    from unittest.mock import AsyncMock, patch

    from bsm_api_client.exceptions import AuthError

    client._jwt_token = "bsm_it_opaque.integration-secret"
    with patch.object(client, "authenticate", new_callable=AsyncMock) as login:
        with pytest.raises(AuthError, match="replace it explicitly"):
            await client._ensure_authenticated(stale_token=client._jwt_token)
        login.assert_not_awaited()
    with patch.object(
        client, "async_call_generated", new_callable=AsyncMock
    ) as operation:
        assert (await client.async_logout())["status"] == "success"
        operation.assert_not_awaited()
        assert client._jwt_token is None
