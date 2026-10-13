from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_envelope import ErrorEnvelope
from ...models.event_diagnostics import EventDiagnostics
from ...models.get_event_activity_status_type_0 import GetEventActivityStatusType0
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    name: None | str | Unset = UNSET,
    owner: None | str | Unset = UNSET,
    correlation_id: None | str | Unset = UNSET,
    status: GetEventActivityStatusType0 | None | Unset = UNSET,
    limit: int | Unset = 200,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_name: None | str | Unset
    if isinstance(name, Unset):
        json_name = UNSET
    else:
        json_name = name
    params["name"] = json_name

    json_owner: None | str | Unset
    if isinstance(owner, Unset):
        json_owner = UNSET
    else:
        json_owner = owner
    params["owner"] = json_owner

    json_correlation_id: None | str | Unset
    if isinstance(correlation_id, Unset):
        json_correlation_id = UNSET
    else:
        json_correlation_id = correlation_id
    params["correlation_id"] = json_correlation_id

    json_status: None | str | Unset
    if isinstance(status, Unset):
        json_status = UNSET
    elif isinstance(status, GetEventActivityStatusType0):
        json_status = status.value
    else:
        json_status = status
    params["status"] = json_status

    params["limit"] = limit


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/events/activity",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorEnvelope | EventDiagnostics | None:
    if response.status_code == 200:
        response_200 = EventDiagnostics.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorEnvelope | EventDiagnostics]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    name: None | str | Unset = UNSET,
    owner: None | str | Unset = UNSET,
    correlation_id: None | str | Unset = UNSET,
    status: GetEventActivityStatusType0 | None | Unset = UNSET,
    limit: int | Unset = 200,

) -> Response[ErrorEnvelope | EventDiagnostics]:
    """ Get Event Activity

    Args:
        name (None | str | Unset):
        owner (None | str | Unset):
        correlation_id (None | str | Unset):
        status (GetEventActivityStatusType0 | None | Unset):
        limit (int | Unset):  Default: 200.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | EventDiagnostics]
     """


    kwargs = _get_kwargs(
        name=name,
owner=owner,
correlation_id=correlation_id,
status=status,
limit=limit,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    name: None | str | Unset = UNSET,
    owner: None | str | Unset = UNSET,
    correlation_id: None | str | Unset = UNSET,
    status: GetEventActivityStatusType0 | None | Unset = UNSET,
    limit: int | Unset = 200,

) -> ErrorEnvelope | EventDiagnostics | None:
    """ Get Event Activity

    Args:
        name (None | str | Unset):
        owner (None | str | Unset):
        correlation_id (None | str | Unset):
        status (GetEventActivityStatusType0 | None | Unset):
        limit (int | Unset):  Default: 200.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | EventDiagnostics
     """


    return sync_detailed(
        client=client,
name=name,
owner=owner,
correlation_id=correlation_id,
status=status,
limit=limit,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    name: None | str | Unset = UNSET,
    owner: None | str | Unset = UNSET,
    correlation_id: None | str | Unset = UNSET,
    status: GetEventActivityStatusType0 | None | Unset = UNSET,
    limit: int | Unset = 200,

) -> Response[ErrorEnvelope | EventDiagnostics]:
    """ Get Event Activity

    Args:
        name (None | str | Unset):
        owner (None | str | Unset):
        correlation_id (None | str | Unset):
        status (GetEventActivityStatusType0 | None | Unset):
        limit (int | Unset):  Default: 200.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | EventDiagnostics]
     """


    kwargs = _get_kwargs(
        name=name,
owner=owner,
correlation_id=correlation_id,
status=status,
limit=limit,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    name: None | str | Unset = UNSET,
    owner: None | str | Unset = UNSET,
    correlation_id: None | str | Unset = UNSET,
    status: GetEventActivityStatusType0 | None | Unset = UNSET,
    limit: int | Unset = 200,

) -> ErrorEnvelope | EventDiagnostics | None:
    """ Get Event Activity

    Args:
        name (None | str | Unset):
        owner (None | str | Unset):
        correlation_id (None | str | Unset):
        status (GetEventActivityStatusType0 | None | Unset):
        limit (int | Unset):  Default: 200.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | EventDiagnostics
     """


    return (await asyncio_detailed(
        client=client,
name=name,
owner=owner,
correlation_id=correlation_id,
status=status,
limit=limit,

    )).parsed
