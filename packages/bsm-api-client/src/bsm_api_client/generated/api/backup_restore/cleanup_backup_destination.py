from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.destination_cleanup_payload import DestinationCleanupPayload
from ...models.error_envelope import ErrorEnvelope
from ...models.task_accepted_response import TaskAcceptedResponse
from typing import cast



def _get_kwargs(
    server_name: str,
    destination: str,
    *,
    body: DestinationCleanupPayload,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/server/{server_name}/backup-destinations/{destination}/cleanup".format(server_name=quote(str(server_name), safe=""),destination=quote(str(destination), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorEnvelope | TaskAcceptedResponse | None:
    if response.status_code == 202:
        response_202 = TaskAcceptedResponse.from_dict(response.json())



        return response_202

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    server_name: str,
    destination: str,
    *,
    client: AuthenticatedClient,
    body: DestinationCleanupPayload,

) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
    """Cleanup Destination
    
     Preview external cleanup; a reviewed token explicitly authorizes deletion.
    
    :param server_name: Value supplied to the operation.
    :param destination: Value supplied to the operation.
    :param body: Value supplied to the operation.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: The parsed response."""


    kwargs = _get_kwargs(
        server_name=server_name,
destination=destination,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    server_name: str,
    destination: str,
    *,
    client: AuthenticatedClient,
    body: DestinationCleanupPayload,

) -> ErrorEnvelope | TaskAcceptedResponse | None:
    """Cleanup Destination
    
     Preview external cleanup; a reviewed token explicitly authorizes deletion.
    
    :param server_name: Value supplied to the operation.
    :param destination: Value supplied to the operation.
    :param body: Value supplied to the operation.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: ErrorEnvelope | TaskAcceptedResponse"""


    return sync_detailed(
        server_name=server_name,
destination=destination,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    server_name: str,
    destination: str,
    *,
    client: AuthenticatedClient,
    body: DestinationCleanupPayload,

) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
    """Cleanup Destination
    
     Preview external cleanup; a reviewed token explicitly authorizes deletion.
    
    :param server_name: Value supplied to the operation.
    :param destination: Value supplied to the operation.
    :param body: Value supplied to the operation.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: The parsed response."""


    kwargs = _get_kwargs(
        server_name=server_name,
destination=destination,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    server_name: str,
    destination: str,
    *,
    client: AuthenticatedClient,
    body: DestinationCleanupPayload,

) -> ErrorEnvelope | TaskAcceptedResponse | None:
    """Cleanup Destination
    
     Preview external cleanup; a reviewed token explicitly authorizes deletion.
    
    :param server_name: Value supplied to the operation.
    :param destination: Value supplied to the operation.
    :param body: Value supplied to the operation.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: ErrorEnvelope | TaskAcceptedResponse"""


    return (await asyncio_detailed(
        server_name=server_name,
destination=destination,
client=client,
body=body,

    )).parsed
