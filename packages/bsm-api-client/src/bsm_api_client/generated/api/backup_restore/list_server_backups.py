from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.backup_files_response import BackupFilesResponse
from ...models.error_envelope import ErrorEnvelope
from typing import cast



def _get_kwargs(
    server_name: str,
    backup_type: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/server/{server_name}/backup/list/{backup_type}".format(server_name=quote(str(server_name), safe=""),backup_type=quote(str(backup_type), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> BackupFilesResponse | ErrorEnvelope | None:
    if response.status_code == 200:
        response_200 = BackupFilesResponse.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[BackupFilesResponse | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    server_name: str,
    backup_type: str,
    *,
    client: AuthenticatedClient,

) -> Response[BackupFilesResponse | ErrorEnvelope]:
    """ Get List Server Backups

     Lists available backup files for a specific server and backup type.

    Args:
        server_name (str):
        backup_type (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BackupFilesResponse | ErrorEnvelope]
     """


    kwargs = _get_kwargs(
        server_name=server_name,
backup_type=backup_type,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    server_name: str,
    backup_type: str,
    *,
    client: AuthenticatedClient,

) -> BackupFilesResponse | ErrorEnvelope | None:
    """ Get List Server Backups

     Lists available backup files for a specific server and backup type.

    Args:
        server_name (str):
        backup_type (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BackupFilesResponse | ErrorEnvelope
     """


    return sync_detailed(
        server_name=server_name,
backup_type=backup_type,
client=client,

    ).parsed

async def asyncio_detailed(
    server_name: str,
    backup_type: str,
    *,
    client: AuthenticatedClient,

) -> Response[BackupFilesResponse | ErrorEnvelope]:
    """ Get List Server Backups

     Lists available backup files for a specific server and backup type.

    Args:
        server_name (str):
        backup_type (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BackupFilesResponse | ErrorEnvelope]
     """


    kwargs = _get_kwargs(
        server_name=server_name,
backup_type=backup_type,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    server_name: str,
    backup_type: str,
    *,
    client: AuthenticatedClient,

) -> BackupFilesResponse | ErrorEnvelope | None:
    """ Get List Server Backups

     Lists available backup files for a specific server and backup type.

    Args:
        server_name (str):
        backup_type (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BackupFilesResponse | ErrorEnvelope
     """


    return (await asyncio_detailed(
        server_name=server_name,
backup_type=backup_type,
client=client,

    )).parsed
