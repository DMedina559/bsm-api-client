"""SDK errors retain actionable auth hints without retaining arbitrary headers."""

import httpx
import pytest

from bsm_api_client import BedrockServerManagerApi
from bsm_api_client.exceptions import AuthError

pytestmark = pytest.mark.asyncio


async def test_server_challenge_headers_reach_sdk_callers():
    async with BedrockServerManagerApi(
        "http://localhost", jwt_token="synthetic"
    ) as client:
        response = httpx.Response(
            401,
            json={"detail": "Factor required"},
            headers={
                "X-BSM-MFA": "passkey",
                "X-BSM-Recent-Auth": "required",
                "Retry-After": "30",
                "Set-Cookie": "private=secret",
            },
        )
        with pytest.raises(AuthError) as caught:
            await client._handle_api_error(response, "/api/account/security/verify")
        error = caught.value
        assert error.passkey_required and error.recent_auth_required
        assert not error.mfa_required
        assert error.retry_after == "30"
        assert "set-cookie" not in error.response_headers
