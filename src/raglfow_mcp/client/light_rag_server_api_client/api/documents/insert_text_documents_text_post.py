from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.insert_response import InsertResponse
from ...models.insert_text_request import InsertTextRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: InsertTextRequest,
    api_key_header_value: Union[None, Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_api_key_header_value: Union[None, Unset, str]
    if isinstance(api_key_header_value, Unset):
        json_api_key_header_value = UNSET
    else:
        json_api_key_header_value = api_key_header_value
    params["api_key_header_value"] = json_api_key_header_value

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/documents/text",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, InsertResponse]]:
    if response.status_code == 200:
        response_200 = InsertResponse.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, InsertResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: InsertTextRequest,
    api_key_header_value: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, InsertResponse]]:
    """Insert Text

     Insert text into the RAG system.

    This endpoint allows you to insert text data into the RAG system for later retrieval
    and use in generating responses.

    Args:
        request (InsertTextRequest): The request body containing the text to be inserted.
        background_tasks: FastAPI BackgroundTasks for async processing

    Returns:
        InsertResponse: A response object containing the status of the operation.

    Raises:
        HTTPException: If an error occurs during text processing (500).

    Args:
        api_key_header_value (Union[None, Unset, str]):
        body (InsertTextRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, InsertResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
        api_key_header_value=api_key_header_value,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: InsertTextRequest,
    api_key_header_value: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, InsertResponse]]:
    """Insert Text

     Insert text into the RAG system.

    This endpoint allows you to insert text data into the RAG system for later retrieval
    and use in generating responses.

    Args:
        request (InsertTextRequest): The request body containing the text to be inserted.
        background_tasks: FastAPI BackgroundTasks for async processing

    Returns:
        InsertResponse: A response object containing the status of the operation.

    Raises:
        HTTPException: If an error occurs during text processing (500).

    Args:
        api_key_header_value (Union[None, Unset, str]):
        body (InsertTextRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, InsertResponse]
    """

    return sync_detailed(
        client=client,
        body=body,
        api_key_header_value=api_key_header_value,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: InsertTextRequest,
    api_key_header_value: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, InsertResponse]]:
    """Insert Text

     Insert text into the RAG system.

    This endpoint allows you to insert text data into the RAG system for later retrieval
    and use in generating responses.

    Args:
        request (InsertTextRequest): The request body containing the text to be inserted.
        background_tasks: FastAPI BackgroundTasks for async processing

    Returns:
        InsertResponse: A response object containing the status of the operation.

    Raises:
        HTTPException: If an error occurs during text processing (500).

    Args:
        api_key_header_value (Union[None, Unset, str]):
        body (InsertTextRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, InsertResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
        api_key_header_value=api_key_header_value,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: InsertTextRequest,
    api_key_header_value: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, InsertResponse]]:
    """Insert Text

     Insert text into the RAG system.

    This endpoint allows you to insert text data into the RAG system for later retrieval
    and use in generating responses.

    Args:
        request (InsertTextRequest): The request body containing the text to be inserted.
        background_tasks: FastAPI BackgroundTasks for async processing

    Returns:
        InsertResponse: A response object containing the status of the operation.

    Raises:
        HTTPException: If an error occurs during text processing (500).

    Args:
        api_key_header_value (Union[None, Unset, str]):
        body (InsertTextRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, InsertResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            api_key_header_value=api_key_header_value,
        )
    ).parsed
