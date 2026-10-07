from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_envelope import ErrorEnvelope
from ...models.trigger_event_payload import TriggerEventPayload
from ...models.trigger_event_response import TriggerEventResponse
from ...types import Response


def _get_kwargs(
    *,
    body: TriggerEventPayload,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/plugins/trigger_event",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorEnvelope | TriggerEventResponse | None:
    if response.status_code == 200:
        response_200 = TriggerEventResponse.from_dict(response.json())

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


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorEnvelope | TriggerEventResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: TriggerEventPayload,
) -> Response[ErrorEnvelope | TriggerEventResponse]:
    """Post Trigger Event

     Allows an external source to trigger a custom plugin event within the system.

    Args:
        body (TriggerEventPayload): Request model for triggering a custom plugin event.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | TriggerEventResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: TriggerEventPayload,
) -> ErrorEnvelope | TriggerEventResponse | None:
    """Post Trigger Event

     Allows an external source to trigger a custom plugin event within the system.

    Args:
        body (TriggerEventPayload): Request model for triggering a custom plugin event.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | TriggerEventResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: TriggerEventPayload,
) -> Response[ErrorEnvelope | TriggerEventResponse]:
    """Post Trigger Event

     Allows an external source to trigger a custom plugin event within the system.

    Args:
        body (TriggerEventPayload): Request model for triggering a custom plugin event.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | TriggerEventResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: TriggerEventPayload,
) -> ErrorEnvelope | TriggerEventResponse | None:
    """Post Trigger Event

     Allows an external source to trigger a custom plugin event within the system.

    Args:
        body (TriggerEventPayload): Request model for triggering a custom plugin event.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | TriggerEventResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
