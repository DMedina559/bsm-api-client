from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.diagnostic_snapshot import DiagnosticSnapshot
from ...models.error_envelope import ErrorEnvelope
from typing import cast



def _get_kwargs(
    subsystem: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/diagnostics/{subsystem}".format(subsystem=quote(str(subsystem), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DiagnosticSnapshot | ErrorEnvelope | None:
    if response.status_code == 200:
        response_200 = DiagnosticSnapshot.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DiagnosticSnapshot | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    subsystem: str,
    *,
    client: AuthenticatedClient,

) -> Response[DiagnosticSnapshot | ErrorEnvelope]:
    """Get Subsystem Diagnostics
    
    :param subsystem: Value supplied to the operation.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: The parsed response."""


    kwargs = _get_kwargs(
        subsystem=subsystem,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    subsystem: str,
    *,
    client: AuthenticatedClient,

) -> DiagnosticSnapshot | ErrorEnvelope | None:
    """Get Subsystem Diagnostics
    
    :param subsystem: Value supplied to the operation.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: DiagnosticSnapshot | ErrorEnvelope"""


    return sync_detailed(
        subsystem=subsystem,
client=client,

    ).parsed

async def asyncio_detailed(
    subsystem: str,
    *,
    client: AuthenticatedClient,

) -> Response[DiagnosticSnapshot | ErrorEnvelope]:
    """Get Subsystem Diagnostics
    
    :param subsystem: Value supplied to the operation.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: The parsed response."""


    kwargs = _get_kwargs(
        subsystem=subsystem,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    subsystem: str,
    *,
    client: AuthenticatedClient,

) -> DiagnosticSnapshot | ErrorEnvelope | None:
    """Get Subsystem Diagnostics
    
    :param subsystem: Value supplied to the operation.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: DiagnosticSnapshot | ErrorEnvelope"""


    return (await asyncio_detailed(
        subsystem=subsystem,
client=client,

    )).parsed
