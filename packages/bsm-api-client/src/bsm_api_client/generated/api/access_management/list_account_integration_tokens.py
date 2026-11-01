from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_envelope import ErrorEnvelope
from ...models.integration_token_info import IntegrationTokenInfo
from ...models.list_account_integration_tokens_status import ListAccountIntegrationTokensStatus
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    user_id: int,
    *,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    status: ListAccountIntegrationTokensStatus | Unset = ListAccountIntegrationTokensStatus.ALL,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    json_status: str | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

    params["status"] = json_status


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/access/users/{user_id}/tokens".format(user_id=quote(str(user_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorEnvelope | list[IntegrationTokenInfo] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = IntegrationTokenInfo.from_dict(response_200_item_data)



            response_200.append(response_200_item)

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorEnvelope | list[IntegrationTokenInfo]]:
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
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    status: ListAccountIntegrationTokensStatus | Unset = ListAccountIntegrationTokensStatus.ALL,

) -> Response[ErrorEnvelope | list[IntegrationTokenInfo]]:
    """List User Tokens
    
    :param user_id: Value supplied to the operation.
    :param limit: Default: 100.
    :param offset: Default: 0.
    :param status: Default: ListAccountIntegrationTokensStatus.ALL.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: The parsed response."""


    kwargs = _get_kwargs(
        user_id=user_id,
limit=limit,
offset=offset,
status=status,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    user_id: int,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    status: ListAccountIntegrationTokensStatus | Unset = ListAccountIntegrationTokensStatus.ALL,

) -> ErrorEnvelope | list[IntegrationTokenInfo] | None:
    """List User Tokens
    
    :param user_id: Value supplied to the operation.
    :param limit: Default: 100.
    :param offset: Default: 0.
    :param status: Default: ListAccountIntegrationTokensStatus.ALL.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: ErrorEnvelope | list[IntegrationTokenInfo]"""


    return sync_detailed(
        user_id=user_id,
client=client,
limit=limit,
offset=offset,
status=status,

    ).parsed

async def asyncio_detailed(
    user_id: int,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    status: ListAccountIntegrationTokensStatus | Unset = ListAccountIntegrationTokensStatus.ALL,

) -> Response[ErrorEnvelope | list[IntegrationTokenInfo]]:
    """List User Tokens
    
    :param user_id: Value supplied to the operation.
    :param limit: Default: 100.
    :param offset: Default: 0.
    :param status: Default: ListAccountIntegrationTokensStatus.ALL.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: The parsed response."""


    kwargs = _get_kwargs(
        user_id=user_id,
limit=limit,
offset=offset,
status=status,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    user_id: int,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    status: ListAccountIntegrationTokensStatus | Unset = ListAccountIntegrationTokensStatus.ALL,

) -> ErrorEnvelope | list[IntegrationTokenInfo] | None:
    """List User Tokens
    
    :param user_id: Value supplied to the operation.
    :param limit: Default: 100.
    :param offset: Default: 0.
    :param status: Default: ListAccountIntegrationTokensStatus.ALL.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: ErrorEnvelope | list[IntegrationTokenInfo]"""


    return (await asyncio_detailed(
        user_id=user_id,
client=client,
limit=limit,
offset=offset,
status=status,

    )).parsed
