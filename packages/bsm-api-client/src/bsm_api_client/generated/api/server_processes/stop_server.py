from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_envelope import ErrorEnvelope
from ...models.stop_server_response import StopServerResponse
from typing import cast



def _get_kwargs(
    server_name: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/server/{server_name}/stop".format(server_name=quote(str(server_name), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorEnvelope | StopServerResponse | None:
    if response.status_code == 200:
        response_200 = StopServerResponse.from_dict(response.json())



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

    if response.status_code == 500:
        response_500 = ErrorEnvelope.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorEnvelope | StopServerResponse]:
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

) -> Response[ErrorEnvelope | StopServerResponse]:
    """ Post Stop Server

     Await server stop and return its completed operation result.

    Args:
        server_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | StopServerResponse]
     """


    kwargs = _get_kwargs(
        server_name=server_name,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    server_name: str,
    *,
    client: AuthenticatedClient,

) -> ErrorEnvelope | StopServerResponse | None:
    """ Post Stop Server

     Await server stop and return its completed operation result.

    Args:
        server_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | StopServerResponse
     """


    return sync_detailed(
        server_name=server_name,
client=client,

    ).parsed

async def asyncio_detailed(
    server_name: str,
    *,
    client: AuthenticatedClient,

) -> Response[ErrorEnvelope | StopServerResponse]:
    """ Post Stop Server

     Await server stop and return its completed operation result.

    Args:
        server_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | StopServerResponse]
     """


    kwargs = _get_kwargs(
        server_name=server_name,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    server_name: str,
    *,
    client: AuthenticatedClient,

) -> ErrorEnvelope | StopServerResponse | None:
    """ Post Stop Server

     Await server stop and return its completed operation result.

    Args:
        server_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | StopServerResponse
     """


    return (await asyncio_detailed(
        server_name=server_name,
client=client,

    )).parsed
