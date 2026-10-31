from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.account_server_access_info import AccountServerAccessInfo
from ...models.error_envelope import ErrorEnvelope
from ...models.set_server_access import SetServerAccess
from typing import cast



def _get_kwargs(
    user_id: int,
    *,
    body: SetServerAccess,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/access/users/{user_id}/servers".format(user_id=quote(str(user_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AccountServerAccessInfo | ErrorEnvelope | None:
    if response.status_code == 200:
        response_200 = AccountServerAccessInfo.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AccountServerAccessInfo | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_id: int,
    *,
    client: AuthenticatedClient,
    body: SetServerAccess,

) -> Response[AccountServerAccessInfo | ErrorEnvelope]:
    """Set Server Access
    
    :param user_id: Value supplied to the operation.
    :param body: Value supplied to the operation.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: The parsed response."""


    kwargs = _get_kwargs(
        user_id=user_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    user_id: int,
    *,
    client: AuthenticatedClient,
    body: SetServerAccess,

) -> AccountServerAccessInfo | ErrorEnvelope | None:
    """Set Server Access
    
    :param user_id: Value supplied to the operation.
    :param body: Value supplied to the operation.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: AccountServerAccessInfo | ErrorEnvelope"""


    return sync_detailed(
        user_id=user_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    user_id: int,
    *,
    client: AuthenticatedClient,
    body: SetServerAccess,

) -> Response[AccountServerAccessInfo | ErrorEnvelope]:
    """Set Server Access
    
    :param user_id: Value supplied to the operation.
    :param body: Value supplied to the operation.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: The parsed response."""


    kwargs = _get_kwargs(
        user_id=user_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    user_id: int,
    *,
    client: AuthenticatedClient,
    body: SetServerAccess,

) -> AccountServerAccessInfo | ErrorEnvelope | None:
    """Set Server Access
    
    :param user_id: Value supplied to the operation.
    :param body: Value supplied to the operation.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: AccountServerAccessInfo | ErrorEnvelope"""


    return (await asyncio_detailed(
        user_id=user_id,
client=client,
body=body,

    )).parsed
