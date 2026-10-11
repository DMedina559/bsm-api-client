from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_envelope import ErrorEnvelope
from ...models.log_history_page import LogHistoryPage
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    topic: str,
    before: int | None | Unset = UNSET,
    file_id: None | str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["topic"] = topic

    json_before: int | None | Unset
    if isinstance(before, Unset):
        json_before = UNSET
    else:
        json_before = before
    params["before"] = json_before

    json_file_id: None | str | Unset
    if isinstance(file_id, Unset):
        json_file_id = UNSET
    else:
        json_file_id = file_id
    params["file_id"] = json_file_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/logs/history",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorEnvelope | LogHistoryPage | None:
    if response.status_code == 200:
        response_200 = LogHistoryPage.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorEnvelope | LogHistoryPage]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    topic: str,
    before: int | None | Unset = UNSET,
    file_id: None | str | Unset = UNSET,

) -> Response[ErrorEnvelope | LogHistoryPage]:
    """ Get Log History

    Args:
        topic (str):
        before (int | None | Unset):
        file_id (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | LogHistoryPage]
     """


    kwargs = _get_kwargs(
        topic=topic,
before=before,
file_id=file_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    topic: str,
    before: int | None | Unset = UNSET,
    file_id: None | str | Unset = UNSET,

) -> ErrorEnvelope | LogHistoryPage | None:
    """ Get Log History

    Args:
        topic (str):
        before (int | None | Unset):
        file_id (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | LogHistoryPage
     """


    return sync_detailed(
        client=client,
topic=topic,
before=before,
file_id=file_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    topic: str,
    before: int | None | Unset = UNSET,
    file_id: None | str | Unset = UNSET,

) -> Response[ErrorEnvelope | LogHistoryPage]:
    """ Get Log History

    Args:
        topic (str):
        before (int | None | Unset):
        file_id (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | LogHistoryPage]
     """


    kwargs = _get_kwargs(
        topic=topic,
before=before,
file_id=file_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    topic: str,
    before: int | None | Unset = UNSET,
    file_id: None | str | Unset = UNSET,

) -> ErrorEnvelope | LogHistoryPage | None:
    """ Get Log History

    Args:
        topic (str):
        before (int | None | Unset):
        file_id (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | LogHistoryPage
     """


    return (await asyncio_detailed(
        client=client,
topic=topic,
before=before,
file_id=file_id,

    )).parsed
