from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.diagnostic_activity import DiagnosticActivity
from ...models.error_envelope import ErrorEnvelope
from ...models.get_diagnostic_activity_phase_type_0 import GetDiagnosticActivityPhaseType0
from ...models.get_diagnostic_activity_status_type_0 import GetDiagnosticActivityStatusType0
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    operation_id: None | str | Unset = UNSET,
    sequence_id: None | str | Unset = UNSET,
    operation_name: None | str | Unset = UNSET,
    server_name: None | str | Unset = UNSET,
    source: None | str | Unset = UNSET,
    phase: GetDiagnosticActivityPhaseType0 | None | Unset = UNSET,
    name: None | str | Unset = UNSET,
    owner: None | str | Unset = UNSET,
    correlation_id: None | str | Unset = UNSET,
    status: GetDiagnosticActivityStatusType0 | None | Unset = UNSET,
    limit: int | Unset = 100,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_operation_id: None | str | Unset
    if isinstance(operation_id, Unset):
        json_operation_id = UNSET
    else:
        json_operation_id = operation_id
    params["operation_id"] = json_operation_id

    json_sequence_id: None | str | Unset
    if isinstance(sequence_id, Unset):
        json_sequence_id = UNSET
    else:
        json_sequence_id = sequence_id
    params["sequence_id"] = json_sequence_id

    json_operation_name: None | str | Unset
    if isinstance(operation_name, Unset):
        json_operation_name = UNSET
    else:
        json_operation_name = operation_name
    params["operation_name"] = json_operation_name

    json_server_name: None | str | Unset
    if isinstance(server_name, Unset):
        json_server_name = UNSET
    else:
        json_server_name = server_name
    params["server_name"] = json_server_name

    json_source: None | str | Unset
    if isinstance(source, Unset):
        json_source = UNSET
    else:
        json_source = source
    params["source"] = json_source

    json_phase: None | str | Unset
    if isinstance(phase, Unset):
        json_phase = UNSET
    elif isinstance(phase, GetDiagnosticActivityPhaseType0):
        json_phase = phase.value
    else:
        json_phase = phase
    params["phase"] = json_phase

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
    elif isinstance(status, GetDiagnosticActivityStatusType0):
        json_status = status.value
    else:
        json_status = status
    params["status"] = json_status

    params["limit"] = limit


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/diagnostics/activity",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DiagnosticActivity | ErrorEnvelope | None:
    if response.status_code == 200:
        response_200 = DiagnosticActivity.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DiagnosticActivity | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    operation_id: None | str | Unset = UNSET,
    sequence_id: None | str | Unset = UNSET,
    operation_name: None | str | Unset = UNSET,
    server_name: None | str | Unset = UNSET,
    source: None | str | Unset = UNSET,
    phase: GetDiagnosticActivityPhaseType0 | None | Unset = UNSET,
    name: None | str | Unset = UNSET,
    owner: None | str | Unset = UNSET,
    correlation_id: None | str | Unset = UNSET,
    status: GetDiagnosticActivityStatusType0 | None | Unset = UNSET,
    limit: int | Unset = 100,

) -> Response[DiagnosticActivity | ErrorEnvelope]:
    """Get Diagnostic Activity
    
     Read global activity, optionally narrowing by event, server, sequence, or correlation.
    
    :param operation_id: Value supplied to the operation.
    :param sequence_id: Value supplied to the operation.
    :param operation_name: Value supplied to the operation.
    :param server_name: Value supplied to the operation.
    :param source: Value supplied to the operation.
    :param phase: Value supplied to the operation.
    :param name: Value supplied to the operation.
    :param owner: Value supplied to the operation.
    :param correlation_id: Value supplied to the operation.
    :param status: Value supplied to the operation.
    :param limit: Default: 100.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: The parsed response."""


    kwargs = _get_kwargs(
        operation_id=operation_id,
sequence_id=sequence_id,
operation_name=operation_name,
server_name=server_name,
source=source,
phase=phase,
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
    operation_id: None | str | Unset = UNSET,
    sequence_id: None | str | Unset = UNSET,
    operation_name: None | str | Unset = UNSET,
    server_name: None | str | Unset = UNSET,
    source: None | str | Unset = UNSET,
    phase: GetDiagnosticActivityPhaseType0 | None | Unset = UNSET,
    name: None | str | Unset = UNSET,
    owner: None | str | Unset = UNSET,
    correlation_id: None | str | Unset = UNSET,
    status: GetDiagnosticActivityStatusType0 | None | Unset = UNSET,
    limit: int | Unset = 100,

) -> DiagnosticActivity | ErrorEnvelope | None:
    """Get Diagnostic Activity
    
     Read global activity, optionally narrowing by event, server, sequence, or correlation.
    
    :param operation_id: Value supplied to the operation.
    :param sequence_id: Value supplied to the operation.
    :param operation_name: Value supplied to the operation.
    :param server_name: Value supplied to the operation.
    :param source: Value supplied to the operation.
    :param phase: Value supplied to the operation.
    :param name: Value supplied to the operation.
    :param owner: Value supplied to the operation.
    :param correlation_id: Value supplied to the operation.
    :param status: Value supplied to the operation.
    :param limit: Default: 100.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: DiagnosticActivity | ErrorEnvelope"""


    return sync_detailed(
        client=client,
operation_id=operation_id,
sequence_id=sequence_id,
operation_name=operation_name,
server_name=server_name,
source=source,
phase=phase,
name=name,
owner=owner,
correlation_id=correlation_id,
status=status,
limit=limit,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    operation_id: None | str | Unset = UNSET,
    sequence_id: None | str | Unset = UNSET,
    operation_name: None | str | Unset = UNSET,
    server_name: None | str | Unset = UNSET,
    source: None | str | Unset = UNSET,
    phase: GetDiagnosticActivityPhaseType0 | None | Unset = UNSET,
    name: None | str | Unset = UNSET,
    owner: None | str | Unset = UNSET,
    correlation_id: None | str | Unset = UNSET,
    status: GetDiagnosticActivityStatusType0 | None | Unset = UNSET,
    limit: int | Unset = 100,

) -> Response[DiagnosticActivity | ErrorEnvelope]:
    """Get Diagnostic Activity
    
     Read global activity, optionally narrowing by event, server, sequence, or correlation.
    
    :param operation_id: Value supplied to the operation.
    :param sequence_id: Value supplied to the operation.
    :param operation_name: Value supplied to the operation.
    :param server_name: Value supplied to the operation.
    :param source: Value supplied to the operation.
    :param phase: Value supplied to the operation.
    :param name: Value supplied to the operation.
    :param owner: Value supplied to the operation.
    :param correlation_id: Value supplied to the operation.
    :param status: Value supplied to the operation.
    :param limit: Default: 100.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: The parsed response."""


    kwargs = _get_kwargs(
        operation_id=operation_id,
sequence_id=sequence_id,
operation_name=operation_name,
server_name=server_name,
source=source,
phase=phase,
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
    operation_id: None | str | Unset = UNSET,
    sequence_id: None | str | Unset = UNSET,
    operation_name: None | str | Unset = UNSET,
    server_name: None | str | Unset = UNSET,
    source: None | str | Unset = UNSET,
    phase: GetDiagnosticActivityPhaseType0 | None | Unset = UNSET,
    name: None | str | Unset = UNSET,
    owner: None | str | Unset = UNSET,
    correlation_id: None | str | Unset = UNSET,
    status: GetDiagnosticActivityStatusType0 | None | Unset = UNSET,
    limit: int | Unset = 100,

) -> DiagnosticActivity | ErrorEnvelope | None:
    """Get Diagnostic Activity
    
     Read global activity, optionally narrowing by event, server, sequence, or correlation.
    
    :param operation_id: Value supplied to the operation.
    :param sequence_id: Value supplied to the operation.
    :param operation_name: Value supplied to the operation.
    :param server_name: Value supplied to the operation.
    :param source: Value supplied to the operation.
    :param phase: Value supplied to the operation.
    :param name: Value supplied to the operation.
    :param owner: Value supplied to the operation.
    :param correlation_id: Value supplied to the operation.
    :param status: Value supplied to the operation.
    :param limit: Default: 100.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: DiagnosticActivity | ErrorEnvelope"""


    return (await asyncio_detailed(
        client=client,
operation_id=operation_id,
sequence_id=sequence_id,
operation_name=operation_name,
server_name=server_name,
source=source,
phase=phase,
name=name,
owner=owner,
correlation_id=correlation_id,
status=status,
limit=limit,

    )).parsed
