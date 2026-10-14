from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.diagnostic_history import DiagnosticHistory
from ...models.error_envelope import ErrorEnvelope
from ...models.get_diagnostic_history_outcome_type_0 import GetDiagnosticHistoryOutcomeType0
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    limit: int | Unset = 100,
    subsystem: None | str | Unset = UNSET,
    instance_id: None | str | Unset = UNSET,
    correlation_id: None | str | Unset = UNSET,
    cursor: None | str | Unset = UNSET,
    owner: None | str | Unset = UNSET,
    code: None | str | Unset = UNSET,
    outcome: GetDiagnosticHistoryOutcomeType0 | None | Unset = UNSET,
    operation_id: None | str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["limit"] = limit

    json_subsystem: None | str | Unset
    if isinstance(subsystem, Unset):
        json_subsystem = UNSET
    else:
        json_subsystem = subsystem
    params["subsystem"] = json_subsystem

    json_instance_id: None | str | Unset
    if isinstance(instance_id, Unset):
        json_instance_id = UNSET
    else:
        json_instance_id = instance_id
    params["instance_id"] = json_instance_id

    json_correlation_id: None | str | Unset
    if isinstance(correlation_id, Unset):
        json_correlation_id = UNSET
    else:
        json_correlation_id = correlation_id
    params["correlation_id"] = json_correlation_id

    json_cursor: None | str | Unset
    if isinstance(cursor, Unset):
        json_cursor = UNSET
    else:
        json_cursor = cursor
    params["cursor"] = json_cursor

    json_owner: None | str | Unset
    if isinstance(owner, Unset):
        json_owner = UNSET
    else:
        json_owner = owner
    params["owner"] = json_owner

    json_code: None | str | Unset
    if isinstance(code, Unset):
        json_code = UNSET
    else:
        json_code = code
    params["code"] = json_code

    json_outcome: None | str | Unset
    if isinstance(outcome, Unset):
        json_outcome = UNSET
    elif isinstance(outcome, GetDiagnosticHistoryOutcomeType0):
        json_outcome = outcome.value
    else:
        json_outcome = outcome
    params["outcome"] = json_outcome

    json_operation_id: None | str | Unset
    if isinstance(operation_id, Unset):
        json_operation_id = UNSET
    else:
        json_operation_id = operation_id
    params["operation_id"] = json_operation_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/diagnostics/history",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DiagnosticHistory | ErrorEnvelope | None:
    if response.status_code == 200:
        response_200 = DiagnosticHistory.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DiagnosticHistory | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    subsystem: None | str | Unset = UNSET,
    instance_id: None | str | Unset = UNSET,
    correlation_id: None | str | Unset = UNSET,
    cursor: None | str | Unset = UNSET,
    owner: None | str | Unset = UNSET,
    code: None | str | Unset = UNSET,
    outcome: GetDiagnosticHistoryOutcomeType0 | None | Unset = UNSET,
    operation_id: None | str | Unset = UNSET,

) -> Response[DiagnosticHistory | ErrorEnvelope]:
    """ Get Diagnostic History

    Args:
        limit (int | Unset):  Default: 100.
        subsystem (None | str | Unset):
        instance_id (None | str | Unset):
        correlation_id (None | str | Unset):
        cursor (None | str | Unset):
        owner (None | str | Unset):
        code (None | str | Unset):
        outcome (GetDiagnosticHistoryOutcomeType0 | None | Unset):
        operation_id (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DiagnosticHistory | ErrorEnvelope]
     """


    kwargs = _get_kwargs(
        limit=limit,
subsystem=subsystem,
instance_id=instance_id,
correlation_id=correlation_id,
cursor=cursor,
owner=owner,
code=code,
outcome=outcome,
operation_id=operation_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    subsystem: None | str | Unset = UNSET,
    instance_id: None | str | Unset = UNSET,
    correlation_id: None | str | Unset = UNSET,
    cursor: None | str | Unset = UNSET,
    owner: None | str | Unset = UNSET,
    code: None | str | Unset = UNSET,
    outcome: GetDiagnosticHistoryOutcomeType0 | None | Unset = UNSET,
    operation_id: None | str | Unset = UNSET,

) -> DiagnosticHistory | ErrorEnvelope | None:
    """ Get Diagnostic History

    Args:
        limit (int | Unset):  Default: 100.
        subsystem (None | str | Unset):
        instance_id (None | str | Unset):
        correlation_id (None | str | Unset):
        cursor (None | str | Unset):
        owner (None | str | Unset):
        code (None | str | Unset):
        outcome (GetDiagnosticHistoryOutcomeType0 | None | Unset):
        operation_id (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DiagnosticHistory | ErrorEnvelope
     """


    return sync_detailed(
        client=client,
limit=limit,
subsystem=subsystem,
instance_id=instance_id,
correlation_id=correlation_id,
cursor=cursor,
owner=owner,
code=code,
outcome=outcome,
operation_id=operation_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    subsystem: None | str | Unset = UNSET,
    instance_id: None | str | Unset = UNSET,
    correlation_id: None | str | Unset = UNSET,
    cursor: None | str | Unset = UNSET,
    owner: None | str | Unset = UNSET,
    code: None | str | Unset = UNSET,
    outcome: GetDiagnosticHistoryOutcomeType0 | None | Unset = UNSET,
    operation_id: None | str | Unset = UNSET,

) -> Response[DiagnosticHistory | ErrorEnvelope]:
    """ Get Diagnostic History

    Args:
        limit (int | Unset):  Default: 100.
        subsystem (None | str | Unset):
        instance_id (None | str | Unset):
        correlation_id (None | str | Unset):
        cursor (None | str | Unset):
        owner (None | str | Unset):
        code (None | str | Unset):
        outcome (GetDiagnosticHistoryOutcomeType0 | None | Unset):
        operation_id (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DiagnosticHistory | ErrorEnvelope]
     """


    kwargs = _get_kwargs(
        limit=limit,
subsystem=subsystem,
instance_id=instance_id,
correlation_id=correlation_id,
cursor=cursor,
owner=owner,
code=code,
outcome=outcome,
operation_id=operation_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    subsystem: None | str | Unset = UNSET,
    instance_id: None | str | Unset = UNSET,
    correlation_id: None | str | Unset = UNSET,
    cursor: None | str | Unset = UNSET,
    owner: None | str | Unset = UNSET,
    code: None | str | Unset = UNSET,
    outcome: GetDiagnosticHistoryOutcomeType0 | None | Unset = UNSET,
    operation_id: None | str | Unset = UNSET,

) -> DiagnosticHistory | ErrorEnvelope | None:
    """ Get Diagnostic History

    Args:
        limit (int | Unset):  Default: 100.
        subsystem (None | str | Unset):
        instance_id (None | str | Unset):
        correlation_id (None | str | Unset):
        cursor (None | str | Unset):
        owner (None | str | Unset):
        code (None | str | Unset):
        outcome (GetDiagnosticHistoryOutcomeType0 | None | Unset):
        operation_id (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DiagnosticHistory | ErrorEnvelope
     """


    return (await asyncio_detailed(
        client=client,
limit=limit,
subsystem=subsystem,
instance_id=instance_id,
correlation_id=correlation_id,
cursor=cursor,
owner=owner,
code=code,
outcome=outcome,
operation_id=operation_id,

    )).parsed
