"""Scoped settings retain typed payloads and server identity over HTTP."""

import json

import httpx
import pytest

from bsm_api_client import BedrockServerManagerApi
from bsm_api_client.models import PluginSettingsPayload


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "scope,server", [("plugin", None), ("global", None), ("server", "alpha")]
)
async def test_scoped_settings_round_trip(scope, server):
    seen = []

    def handler(request):
        seen.append(request)
        return httpx.Response(
            200,
            json=(
                {"status": "success", "settings": {"count": 2}, "settings_schema": {}}
                if request.method == "GET"
                else {"status": "success", "message": "Saved"}
            ),
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as transport:
        async with BedrockServerManagerApi(
            "http://test", jwt_token="test", http_client=transport
        ) as client:
            result = await client.plugins.async_get_plugin_settings(
                "profiles", scope=scope, server_name=server
            )
            assert result.settings == {"count": 2}
            options = {"scope": scope, **({"server_name": server} if server else {})}
            await client.plugins.async_update_plugin_settings(
                "profiles", PluginSettingsPayload(settings={"count": 3}, **options)
            )
    assert seen[0].url.params.get("scope", "plugin") == scope
    assert seen[0].url.params.get("server_name") == server
    assert json.loads(seen[1].content)["scope"] == scope
    assert json.loads(seen[1].content).get("server_name") == server
