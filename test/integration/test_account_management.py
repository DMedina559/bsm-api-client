import pytest
from bsm_api_client.api_client import BedrockServerManagerApi
from bsm_api_client.models import ThemeUpdatePayload, ProfileUpdatePayload


@pytest.mark.asyncio
class TestAccountManagement:
    """
    Integration tests for account management methods.
    """

    async def test_account_methods(self, server):
        """Tests account management methods."""
        client = BedrockServerManagerApi(server, "admin", "password")
        try:
            # Get Account Details
            account = await client.async_get_account_details()
            assert account is not None
            assert account.username == "admin"

            # Update Theme
            theme_payload = ThemeUpdatePayload(theme="dark")
            theme_res = await client.async_update_theme(theme_payload)
            assert theme_res.status == "success"

            # Update Profile
            profile_payload = ProfileUpdatePayload(
                full_name="Admin Admin", email="admin@example.com"
            )
            profile_res = await client.async_update_profile(profile_payload)
            assert profile_res.status == "success"

            # NOTE: We are not testing password change to not break other tests that depend on the password.
        finally:
            await client.close()
