from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import Response
from ...models.ragflow_retrieval_request import RagflowRetrievalRequest
from ...models.ragflow_retrieval_response import RagflowRetrievalResponse


def _get_kwargs(*, json_body: RagflowRetrievalRequest) -> Dict[str, Any]:
    headers: Dict[str, Any] = {"Content-Type": "application/json"}

    return {
        "method": "post",
        "url": "/api/v1/retrieval",
        "json": json_body.to_payload(),
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[RagflowRetrievalResponse]:
    if response.status_code == 200:
        return RagflowRetrievalResponse.model_validate(response.json())

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[RagflowRetrievalResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient, json_body: RagflowRetrievalRequest
) -> Response[RagflowRetrievalResponse]:
    """Call Ragflow retrieval endpoint."""

    kwargs = _get_kwargs(json_body=json_body)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(*, client: AuthenticatedClient, json_body: RagflowRetrievalRequest) -> RagflowRetrievalResponse:
    """Call Ragflow retrieval endpoint."""

    return sync_detailed(client=client, json_body=json_body).parsed


async def asyncio_detailed(
    *, client: AuthenticatedClient, json_body: RagflowRetrievalRequest
) -> Response[RagflowRetrievalResponse]:
    """Call Ragflow retrieval endpoint asynchronously."""

    kwargs = _get_kwargs(json_body=json_body)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: AuthenticatedClient, json_body: RagflowRetrievalRequest
) -> RagflowRetrievalResponse:
    """Call Ragflow retrieval endpoint asynchronously."""

    detailed_response = await asyncio_detailed(client=client, json_body=json_body)
    if detailed_response.parsed is None:
        raise errors.UnexpectedStatus(detailed_response.status_code, detailed_response.content)
    return detailed_response.parsed
