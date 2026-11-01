from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.allowlist_remove_payload import AllowlistRemovePayload
from ...models.error_envelope import ErrorEnvelope
from ...models.remove_from_allowlist_response import RemoveFromAllowlistResponse
from typing import cast



def _get_kwargs(
    server_name: str,
    *,
    body: AllowlistRemovePayload,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/server/{server_name}/allowlist/remove".format(server_name=quote(str(server_name), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorEnvelope | RemoveFromAllowlistResponse | None:
    if response.status_code == 200:
        response_200 = RemoveFromAllowlistResponse.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = ErrorEnvelope.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = ErrorEnvelope.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = ErrorEnvelope.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = ErrorEnvelope.from_dict(response.json())



        return response_404

    if response.status_code == 409:
        response_409 = ErrorEnvelope.from_dict(response.json())



        return response_409

    if response.status_code == 422:
        response_422 = ErrorEnvelope.from_dict(response.json())



        return response_422

    if response.status_code == 429:
        response_429 = ErrorEnvelope.from_dict(response.json())



        return response_429

    if response.status_code == 500:
        response_500 = ErrorEnvelope.from_dict(response.json())



        return response_500

    if response.status_code == 503:
        response_503 = ErrorEnvelope.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorEnvelope | RemoveFromAllowlistResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    server_name: str,
    *,
    client: AuthenticatedClient,
    body: AllowlistRemovePayload,

) -> Response[ErrorEnvelope | RemoveFromAllowlistResponse]:
    """Delete Allowlist
    
    :param server_name: Value supplied to the operation.
    :param body: Request model for removing players from the allowlist.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: The parsed response."""


    kwargs = _get_kwargs(
        server_name=server_name,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    server_name: str,
    *,
    client: AuthenticatedClient,
    body: AllowlistRemovePayload,

) -> ErrorEnvelope | RemoveFromAllowlistResponse | None:
    """Delete Allowlist
    
    :param server_name: Value supplied to the operation.
    :param body: Request model for removing players from the allowlist.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: ErrorEnvelope | RemoveFromAllowlistResponse"""


    return sync_detailed(
        server_name=server_name,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    server_name: str,
    *,
    client: AuthenticatedClient,
    body: AllowlistRemovePayload,

) -> Response[ErrorEnvelope | RemoveFromAllowlistResponse]:
    """Delete Allowlist
    
    :param server_name: Value supplied to the operation.
    :param body: Request model for removing players from the allowlist.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: The parsed response."""


    kwargs = _get_kwargs(
        server_name=server_name,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    server_name: str,
    *,
    client: AuthenticatedClient,
    body: AllowlistRemovePayload,

) -> ErrorEnvelope | RemoveFromAllowlistResponse | None:
    """Delete Allowlist
    
    :param server_name: Value supplied to the operation.
    :param body: Request model for removing players from the allowlist.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: ErrorEnvelope | RemoveFromAllowlistResponse"""


    return (await asyncio_detailed(
        server_name=server_name,
client=client,
body=body,

    )).parsed
