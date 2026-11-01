from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_envelope import ErrorEnvelope
from ...models.list_schedules_response import ListSchedulesResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    server_name: None | str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_server_name: None | str | Unset
    if isinstance(server_name, Unset):
        json_server_name = UNSET
    else:
        json_server_name = server_name
    params["server_name"] = json_server_name


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/scheduler/schedules",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorEnvelope | ListSchedulesResponse | None:
    if response.status_code == 200:
        response_200 = ListSchedulesResponse.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorEnvelope | ListSchedulesResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    server_name: None | str | Unset = UNSET,

) -> Response[ErrorEnvelope | ListSchedulesResponse]:
    """List Schedules
    
     List scheduled tasks.
    
    Requires unrestricted resource access and the ``scheduler:read`` capability.
    Principals restricted to specific servers cannot query or inspect schedules,
    even when filtering by an assigned server name.
    
    :param server_name: Value supplied to the operation.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: The parsed response."""


    kwargs = _get_kwargs(
        server_name=server_name,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    server_name: None | str | Unset = UNSET,

) -> ErrorEnvelope | ListSchedulesResponse | None:
    """List Schedules
    
     List scheduled tasks.
    
    Requires unrestricted resource access and the ``scheduler:read`` capability.
    Principals restricted to specific servers cannot query or inspect schedules,
    even when filtering by an assigned server name.
    
    :param server_name: Value supplied to the operation.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: ErrorEnvelope | ListSchedulesResponse"""


    return sync_detailed(
        client=client,
server_name=server_name,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    server_name: None | str | Unset = UNSET,

) -> Response[ErrorEnvelope | ListSchedulesResponse]:
    """List Schedules
    
     List scheduled tasks.
    
    Requires unrestricted resource access and the ``scheduler:read`` capability.
    Principals restricted to specific servers cannot query or inspect schedules,
    even when filtering by an assigned server name.
    
    :param server_name: Value supplied to the operation.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: The parsed response."""


    kwargs = _get_kwargs(
        server_name=server_name,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    server_name: None | str | Unset = UNSET,

) -> ErrorEnvelope | ListSchedulesResponse | None:
    """List Schedules
    
     List scheduled tasks.
    
    Requires unrestricted resource access and the ``scheduler:read`` capability.
    Principals restricted to specific servers cannot query or inspect schedules,
    even when filtering by an assigned server name.
    
    :param server_name: Value supplied to the operation.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: ErrorEnvelope | ListSchedulesResponse"""


    return (await asyncio_detailed(
        client=client,
server_name=server_name,

    )).parsed
