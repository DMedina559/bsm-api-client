"""Opt-in response metadata and local schema discovery remain isolated."""

import copy

import httpx
import pytest

from bsm_api_client import BedrockServerManagerApi
from bsm_api_client.exceptions import InvalidInputError

SCHEMA = {
    "openapi": "3.1.0",
    "info": {"title": "Test", "version": "1"},
    "paths": {"/api/probe": {"get": {"operationId": "probe"}}},
}


@pytest.mark.asyncio
@pytest.mark.parametrize("status", [200, 204])
async def test_details_are_opt_in_and_include_empty_responses(status):
    def handler(request):
        assert request.url.host == "backend"
        return (
            httpx.Response(
                status,
                json={"ok": True} if status == 200 else None,
                headers={"x-probe": "yes"},
            )
            if status == 200
            else httpx.Response(204, headers={"x-probe": "yes"})
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        async with BedrockServerManagerApi(
            "http://backend", jwt_token="token", http_client=http
        ) as client:
            document = copy.deepcopy(SCHEMA)
            await client.async_discover_api(schema=document)
            document["paths"].clear()
            expected = {"ok": True} if status == 200 else None
            assert (
                await client.async_call_operation("probe", authenticated=False)
                == expected
            )
            result = await client.async_call_operation(
                "probe", authenticated=False, detailed=True
            )
            assert result["status_code"] == status and result["data"] == expected
            assert result["headers"]["x-probe"] == "yes"
            with pytest.raises(InvalidInputError):
                await client.async_discover_api(schema={"paths": []})
            assert "probe" in client.operations
