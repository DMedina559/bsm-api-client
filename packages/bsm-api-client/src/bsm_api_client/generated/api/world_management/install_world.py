from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_envelope import ErrorEnvelope
from ...models.file_name_payload import FileNamePayload
from ...models.task_accepted_response import TaskAcceptedResponse
from typing import cast



def _get_kwargs(
    server_name: str,
    *,
    body: FileNamePayload,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/server/{server_name}/world/install".format(server_name=quote(str(server_name), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorEnvelope | TaskAcceptedResponse | None:
    if response.status_code == 202:
        response_202 = TaskAcceptedResponse.from_dict(response.json())



        return response_202

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
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
    body: FileNamePayload,

) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
    """ Post World Install

     Initiates a background task to install a world from a .mcworld file to a server.

    Args:
        server_name (str):
        body (FileNamePayload): Payload for file-based operations.

            Attributes:
                filename (str): The name of the file to operate on.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | TaskAcceptedResponse]
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
    body: FileNamePayload,

) -> ErrorEnvelope | TaskAcceptedResponse | None:
    """ Post World Install

     Initiates a background task to install a world from a .mcworld file to a server.

    Args:
        server_name (str):
        body (FileNamePayload): Payload for file-based operations.

            Attributes:
                filename (str): The name of the file to operate on.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | TaskAcceptedResponse
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
    body: FileNamePayload,

) -> Response[ErrorEnvelope | TaskAcceptedResponse]:
    """ Post World Install

     Initiates a background task to install a world from a .mcworld file to a server.

    Args:
        server_name (str):
        body (FileNamePayload): Payload for file-based operations.

            Attributes:
                filename (str): The name of the file to operate on.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | TaskAcceptedResponse]
     """


    kwargs = _get_kwargs(
        server_name=server_name,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    server_name: str,
    *,
    client: AuthenticatedClient,
    body: FileNamePayload,

) -> ErrorEnvelope | TaskAcceptedResponse | None:
    """ Post World Install

     Initiates a background task to install a world from a .mcworld file to a server.

    Args:
        server_name (str):
        body (FileNamePayload): Payload for file-based operations.

            Attributes:
                filename (str): The name of the file to operate on.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | TaskAcceptedResponse
     """


    return (await asyncio_detailed(
        server_name=server_name,
client=client,
body=body,

    )).parsed
