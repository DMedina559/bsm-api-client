from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.download_content_file_category import DownloadContentFileCategory
from ...models.error_envelope import ErrorEnvelope
from ...types import File, FileTypes
from io import BytesIO
from typing import cast



def _get_kwargs(
    category: DownloadContentFileCategory,
    filename: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/content/{category}/{filename}/download".format(category=quote(str(category), safe=""),filename=quote(str(filename), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorEnvelope | File | None:
    if response.status_code == 200:
        response_200 = File(
             payload = BytesIO(response.content)
        )



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorEnvelope | File]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    category: DownloadContentFileCategory,
    filename: str,
    *,
    client: AuthenticatedClient,

) -> Response[ErrorEnvelope | File]:
    """Download Content File
    
     Download a world or addon archive from the content library.
    
    :param category: Value supplied to the operation.
    :param filename: Value supplied to the operation.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: The parsed response."""


    kwargs = _get_kwargs(
        category=category,
filename=filename,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    category: DownloadContentFileCategory,
    filename: str,
    *,
    client: AuthenticatedClient,

) -> ErrorEnvelope | File | None:
    """Download Content File
    
     Download a world or addon archive from the content library.
    
    :param category: Value supplied to the operation.
    :param filename: Value supplied to the operation.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: ErrorEnvelope | File"""


    return sync_detailed(
        category=category,
filename=filename,
client=client,

    ).parsed

async def asyncio_detailed(
    category: DownloadContentFileCategory,
    filename: str,
    *,
    client: AuthenticatedClient,

) -> Response[ErrorEnvelope | File]:
    """Download Content File
    
     Download a world or addon archive from the content library.
    
    :param category: Value supplied to the operation.
    :param filename: Value supplied to the operation.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: The parsed response."""


    kwargs = _get_kwargs(
        category=category,
filename=filename,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    category: DownloadContentFileCategory,
    filename: str,
    *,
    client: AuthenticatedClient,

) -> ErrorEnvelope | File | None:
    """Download Content File
    
     Download a world or addon archive from the content library.
    
    :param category: Value supplied to the operation.
    :param filename: Value supplied to the operation.
    
    :raises errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    :raises httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    :returns: ErrorEnvelope | File"""


    return (await asyncio_detailed(
        category=category,
filename=filename,
client=client,

    )).parsed
