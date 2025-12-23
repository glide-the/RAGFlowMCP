from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.body_upload_to_input_dir_documents_upload_post import (
    BodyUploadToInputDirDocumentsUploadPost,
)
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: BodyUploadToInputDirDocumentsUploadPost,
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
        "url": "/documents/upload",
        "params": params,
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = response.json()
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
) -> Response[Union[Any, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: BodyUploadToInputDirDocumentsUploadPost,
    api_key_header_value: Union[None, Unset, str] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    r"""Upload To Input Dir

     Upload a file to the input directory and index it.

    This API endpoint accepts a file through an HTTP POST request, checks if the
    uploaded file is of a supported type, saves it in the specified input directory,
    indexes it for retrieval, and returns a success status with relevant details.

    Args:
        background_tasks: FastAPI BackgroundTasks for async processing
        file (UploadFile): The file to be uploaded. It must have an allowed extension.

    Returns:
        InsertResponse: A response object containing the upload status and a message.
            status can be \"success\", \"duplicated\", or error is thrown.

    Raises:
        HTTPException: If the file type is not supported (400) or other errors occur (500).

    Args:
        api_key_header_value (Union[None, Unset, str]):
        body (BodyUploadToInputDirDocumentsUploadPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
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
    body: BodyUploadToInputDirDocumentsUploadPost,
    api_key_header_value: Union[None, Unset, str] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    r"""Upload To Input Dir

     Upload a file to the input directory and index it.

    This API endpoint accepts a file through an HTTP POST request, checks if the
    uploaded file is of a supported type, saves it in the specified input directory,
    indexes it for retrieval, and returns a success status with relevant details.

    Args:
        background_tasks: FastAPI BackgroundTasks for async processing
        file (UploadFile): The file to be uploaded. It must have an allowed extension.

    Returns:
        InsertResponse: A response object containing the upload status and a message.
            status can be \"success\", \"duplicated\", or error is thrown.

    Raises:
        HTTPException: If the file type is not supported (400) or other errors occur (500).

    Args:
        api_key_header_value (Union[None, Unset, str]):
        body (BodyUploadToInputDirDocumentsUploadPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        body=body,
        api_key_header_value=api_key_header_value,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: BodyUploadToInputDirDocumentsUploadPost,
    api_key_header_value: Union[None, Unset, str] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    r"""Upload To Input Dir

     Upload a file to the input directory and index it.

    This API endpoint accepts a file through an HTTP POST request, checks if the
    uploaded file is of a supported type, saves it in the specified input directory,
    indexes it for retrieval, and returns a success status with relevant details.

    Args:
        background_tasks: FastAPI BackgroundTasks for async processing
        file (UploadFile): The file to be uploaded. It must have an allowed extension.

    Returns:
        InsertResponse: A response object containing the upload status and a message.
            status can be \"success\", \"duplicated\", or error is thrown.

    Raises:
        HTTPException: If the file type is not supported (400) or other errors occur (500).

    Args:
        api_key_header_value (Union[None, Unset, str]):
        body (BodyUploadToInputDirDocumentsUploadPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
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
    body: BodyUploadToInputDirDocumentsUploadPost,
    api_key_header_value: Union[None, Unset, str] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    r"""Upload To Input Dir

     Upload a file to the input directory and index it.

    This API endpoint accepts a file through an HTTP POST request, checks if the
    uploaded file is of a supported type, saves it in the specified input directory,
    indexes it for retrieval, and returns a success status with relevant details.

    Args:
        background_tasks: FastAPI BackgroundTasks for async processing
        file (UploadFile): The file to be uploaded. It must have an allowed extension.

    Returns:
        InsertResponse: A response object containing the upload status and a message.
            status can be \"success\", \"duplicated\", or error is thrown.

    Raises:
        HTTPException: If the file type is not supported (400) or other errors occur (500).

    Args:
        api_key_header_value (Union[None, Unset, str]):
        body (BodyUploadToInputDirDocumentsUploadPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            api_key_header_value=api_key_header_value,
        )
    ).parsed
