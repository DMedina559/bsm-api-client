from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.control_schedule_payload import ControlSchedulePayload
from ...models.error_envelope import ErrorEnvelope
from ...models.success_response import SuccessResponse
from typing import cast



def _get_kwargs(
    schedule_id: str,
    *,
    body: ControlSchedulePayload,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/scheduler/schedules/{schedule_id}/action".format(schedule_id=quote(str(schedule_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorEnvelope | SuccessResponse | None:
    if response.status_code == 200:
        response_200 = SuccessResponse.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorEnvelope | SuccessResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    schedule_id: str,
    *,
    client: AuthenticatedClient,
    body: ControlSchedulePayload,

) -> Response[ErrorEnvelope | SuccessResponse]:
    """Control Schedule
    
    :param schedule_id: Value supplied to the operation.
    :param body: Value supplied to the operation.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: The parsed response."""


    kwargs = _get_kwargs(
        schedule_id=schedule_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    schedule_id: str,
    *,
    client: AuthenticatedClient,
    body: ControlSchedulePayload,

) -> ErrorEnvelope | SuccessResponse | None:
    """Control Schedule
    
    :param schedule_id: Value supplied to the operation.
    :param body: Value supplied to the operation.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: ErrorEnvelope | SuccessResponse"""


    return sync_detailed(
        schedule_id=schedule_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    schedule_id: str,
    *,
    client: AuthenticatedClient,
    body: ControlSchedulePayload,

) -> Response[ErrorEnvelope | SuccessResponse]:
    """Control Schedule
    
    :param schedule_id: Value supplied to the operation.
    :param body: Value supplied to the operation.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: The parsed response."""


    kwargs = _get_kwargs(
        schedule_id=schedule_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    schedule_id: str,
    *,
    client: AuthenticatedClient,
    body: ControlSchedulePayload,

) -> ErrorEnvelope | SuccessResponse | None:
    """Control Schedule
    
    :param schedule_id: Value supplied to the operation.
    :param body: Value supplied to the operation.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: ErrorEnvelope | SuccessResponse"""


    return (await asyncio_detailed(
        schedule_id=schedule_id,
client=client,
body=body,

    )).parsed
