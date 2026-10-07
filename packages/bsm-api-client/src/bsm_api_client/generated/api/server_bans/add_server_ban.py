from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.add_server_ban_response import AddServerBanResponse
from ...models.ban_add_request import BanAddRequest
from ...models.error_envelope import ErrorEnvelope
from ...types import Response


def _get_kwargs(
    server_name: str,
    *,
    body: BanAddRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/server/{server_name}/bans/add".format(
            server_name=quote(str(server_name), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AddServerBanResponse | ErrorEnvelope | None:
    if response.status_code == 200:
        response_200 = AddServerBanResponse.from_dict(response.json())

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
) -> Response[AddServerBanResponse | ErrorEnvelope]:
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
    body: BanAddRequest,
) -> Response[AddServerBanResponse | ErrorEnvelope]:
    """Post Add Server Ban

     Add a player to the server ban list.

    Args:
        server_name (str):
        body (BanAddRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AddServerBanResponse | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        server_name=server_name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    server_name: str,
    *,
    client: AuthenticatedClient,
    body: BanAddRequest,
) -> AddServerBanResponse | ErrorEnvelope | None:
    """Post Add Server Ban

     Add a player to the server ban list.

    Args:
        server_name (str):
        body (BanAddRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AddServerBanResponse | ErrorEnvelope
    """

    return sync_detailed(
        server_name=server_name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    server_name: str,
    *,
    client: AuthenticatedClient,
    body: BanAddRequest,
) -> Response[AddServerBanResponse | ErrorEnvelope]:
    """Post Add Server Ban

     Add a player to the server ban list.

    Args:
        server_name (str):
        body (BanAddRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AddServerBanResponse | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        server_name=server_name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    server_name: str,
    *,
    client: AuthenticatedClient,
    body: BanAddRequest,
) -> AddServerBanResponse | ErrorEnvelope | None:
    """Post Add Server Ban

     Add a player to the server ban list.

    Args:
        server_name (str):
        body (BanAddRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AddServerBanResponse | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            server_name=server_name,
            client=client,
            body=body,
        )
    ).parsed
