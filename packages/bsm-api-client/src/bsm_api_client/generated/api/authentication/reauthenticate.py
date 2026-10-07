from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_envelope import ErrorEnvelope
from ...models.token_response import TokenResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    remember_me: bool | None | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_remember_me: bool | None | Unset
    if isinstance(remember_me, Unset):
        json_remember_me = UNSET
    else:
        json_remember_me = remember_me
    params["remember_me"] = json_remember_me

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/auth/reauth",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorEnvelope | TokenResponse | None:
    if response.status_code == 200:
        response_200 = TokenResponse.from_dict(response.json())

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
) -> Response[ErrorEnvelope | TokenResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    remember_me: bool | None | Unset = UNSET,
) -> Response[ErrorEnvelope | TokenResponse]:
    """Reauth

     Refreshes the JWT access token for an already authenticated user.
    Supports form data, JSON body, or query parameters.

    Args:
        remember_me (bool | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | TokenResponse]
    """

    kwargs = _get_kwargs(
        remember_me=remember_me,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    remember_me: bool | None | Unset = UNSET,
) -> ErrorEnvelope | TokenResponse | None:
    """Reauth

     Refreshes the JWT access token for an already authenticated user.
    Supports form data, JSON body, or query parameters.

    Args:
        remember_me (bool | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | TokenResponse
    """

    return sync_detailed(
        client=client,
        remember_me=remember_me,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    remember_me: bool | None | Unset = UNSET,
) -> Response[ErrorEnvelope | TokenResponse]:
    """Reauth

     Refreshes the JWT access token for an already authenticated user.
    Supports form data, JSON body, or query parameters.

    Args:
        remember_me (bool | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | TokenResponse]
    """

    kwargs = _get_kwargs(
        remember_me=remember_me,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    remember_me: bool | None | Unset = UNSET,
) -> ErrorEnvelope | TokenResponse | None:
    """Reauth

     Refreshes the JWT access token for an already authenticated user.
    Supports form data, JSON body, or query parameters.

    Args:
        remember_me (bool | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | TokenResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            remember_me=remember_me,
        )
    ).parsed
