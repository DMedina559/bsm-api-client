from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.diagnostic_trace import DiagnosticTrace
from ...models.error_envelope import ErrorEnvelope
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    correlation_id: str,
    *,
    limit: int | Unset = 100,
    cursor: None | str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["limit"] = limit

    json_cursor: None | str | Unset
    if isinstance(cursor, Unset):
        json_cursor = UNSET
    else:
        json_cursor = cursor
    params["cursor"] = json_cursor


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/diagnostics/trace/{correlation_id}".format(correlation_id=quote(str(correlation_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DiagnosticTrace | ErrorEnvelope | None:
    if response.status_code == 200:
        response_200 = DiagnosticTrace.from_dict(response.json())



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

    if response.status_code == 503:
        response_503 = ErrorEnvelope.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DiagnosticTrace | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    correlation_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    cursor: None | str | Unset = UNSET,

) -> Response[DiagnosticTrace | ErrorEnvelope]:
    """ Get Diagnostic Trace

    Args:
        correlation_id (str):
        limit (int | Unset):  Default: 100.
        cursor (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DiagnosticTrace | ErrorEnvelope]
     """


    kwargs = _get_kwargs(
        correlation_id=correlation_id,
limit=limit,
cursor=cursor,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    correlation_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    cursor: None | str | Unset = UNSET,

) -> DiagnosticTrace | ErrorEnvelope | None:
    """ Get Diagnostic Trace

    Args:
        correlation_id (str):
        limit (int | Unset):  Default: 100.
        cursor (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DiagnosticTrace | ErrorEnvelope
     """


    return sync_detailed(
        correlation_id=correlation_id,
client=client,
limit=limit,
cursor=cursor,

    ).parsed

async def asyncio_detailed(
    correlation_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    cursor: None | str | Unset = UNSET,

) -> Response[DiagnosticTrace | ErrorEnvelope]:
    """ Get Diagnostic Trace

    Args:
        correlation_id (str):
        limit (int | Unset):  Default: 100.
        cursor (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DiagnosticTrace | ErrorEnvelope]
     """


    kwargs = _get_kwargs(
        correlation_id=correlation_id,
limit=limit,
cursor=cursor,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    correlation_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    cursor: None | str | Unset = UNSET,

) -> DiagnosticTrace | ErrorEnvelope | None:
    """ Get Diagnostic Trace

    Args:
        correlation_id (str):
        limit (int | Unset):  Default: 100.
        cursor (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DiagnosticTrace | ErrorEnvelope
     """


    return (await asyncio_detailed(
        correlation_id=correlation_id,
client=client,
limit=limit,
cursor=cursor,

    )).parsed
