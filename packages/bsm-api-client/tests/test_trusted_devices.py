"""Remembered factors are opt-in and sent only to account security routes."""

import httpx
import pytest

from bsm_api_client import BedrockServerManagerApi


@pytest.mark.asyncio
async def test_remembered_factor_login_and_scoped_transport():
    observed = []

    async def handler(request):
        observed.append(request)
        return httpx.Response(200, json={"status": "success"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as transport:
        async with BedrockServerManagerApi(
            "https://manager.example",
            username="owner",
            password="password",
            jwt_token="jwt",
            http_client=transport,
            remember_device=True,
            trusted_device_token="remembered-proof",
        ) as client:
            called = {}

            async def generated(operation, **kwargs):
                called.update(kwargs)
                return {
                    "access_token": "next-jwt",
                    "token_type": "bearer",
                    "trusted_device_token": "replacement-proof",
                    "trusted_device_expires_at": 2000000000,
                }

            client.async_call_generated = generated
            await client.authenticate()
            assert called["body"]["remember_device"] is True
            assert called["body"]["trusted_device_token"] == "remembered-proof"
            for path, authenticated, expected in [
                ("/api/account/security", True, "replacement-proof"),
                ("/api/account/security/mfa/recovery-codes", True, "replacement-proof"),
                ("/api/account/security/devices", True, "replacement-proof"),
                ("/api/account/security-extra", True, None),
                ("/api/servers", True, None),
                ("/api/account/security", False, None),
            ]:
                await client._dynamic_request("GET", path, authenticated=authenticated)
                assert (
                    observed[-1].headers.get("X-BSM-Trusted-Device-Token") == expected
                )
            await client._dynamic_request(
                "GET",
                "/api/account/security",
                headers={"x-bsm-trusted-device-token": "explicit"},
            )
            assert observed[-1].headers["X-BSM-Trusted-Device-Token"] == "explicit"
            client._jwt_token = "bsm_it_integration"
            await client._dynamic_request("GET", "/api/account/security")
            assert "X-BSM-Trusted-Device-Token" not in observed[-1].headers
