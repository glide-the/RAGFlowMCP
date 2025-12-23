from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    label: str,
    max_depth: Union[Unset, int] = 3,
    min_degree: Union[Unset, int] = 0,
    inclusive: Union[Unset, bool] = False,
    api_key_header_value: Union[None, Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["label"] = label

    params["max_depth"] = max_depth

    params["min_degree"] = min_degree

    params["inclusive"] = inclusive

    json_api_key_header_value: Union[None, Unset, str]
    if isinstance(api_key_header_value, Unset):
        json_api_key_header_value = UNSET
    else:
        json_api_key_header_value = api_key_header_value
    params["api_key_header_value"] = json_api_key_header_value

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/graphs",
        "params": params,
    }

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
    label: str,
    max_depth: Union[Unset, int] = 3,
    min_degree: Union[Unset, int] = 0,
    inclusive: Union[Unset, bool] = False,
    api_key_header_value: Union[None, Unset, str] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    """Get Knowledge Graph

     Retrieve a connected subgraph of nodes where the label includes the specified label.
    Maximum number of nodes is constrained by the environment variable `MAX_GRAPH_NODES` (default:
    1000).
    When reducing the number of nodes, the prioritization criteria are as follows:
        1. min_degree does not affect nodes directly connected to the matching nodes
        2. Label matching nodes take precedence
        3. Followed by nodes directly connected to the matching nodes
        4. Finally, the degree of the nodes
    Maximum number of nodes is limited to env MAX_GRAPH_NODES(default: 1000)

    Args:
        label (str): Label to get knowledge graph for
        max_depth (int, optional): Maximum depth of graph. Defaults to 3.
        inclusive_search (bool, optional): If True, search for nodes that include the label. Defaults to
    False.
        min_degree (int, optional): Minimum degree of nodes. Defaults to 0.

    Returns:
        Dict[str, List[str]]: Knowledge graph for label

    Args:
        label (str):
        max_depth (Union[Unset, int]):  Default: 3.
        min_degree (Union[Unset, int]):  Default: 0.
        inclusive (Union[Unset, bool]):  Default: False.
        api_key_header_value (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        label=label,
        max_depth=max_depth,
        min_degree=min_degree,
        inclusive=inclusive,
        api_key_header_value=api_key_header_value,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    label: str,
    max_depth: Union[Unset, int] = 3,
    min_degree: Union[Unset, int] = 0,
    inclusive: Union[Unset, bool] = False,
    api_key_header_value: Union[None, Unset, str] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Get Knowledge Graph

     Retrieve a connected subgraph of nodes where the label includes the specified label.
    Maximum number of nodes is constrained by the environment variable `MAX_GRAPH_NODES` (default:
    1000).
    When reducing the number of nodes, the prioritization criteria are as follows:
        1. min_degree does not affect nodes directly connected to the matching nodes
        2. Label matching nodes take precedence
        3. Followed by nodes directly connected to the matching nodes
        4. Finally, the degree of the nodes
    Maximum number of nodes is limited to env MAX_GRAPH_NODES(default: 1000)

    Args:
        label (str): Label to get knowledge graph for
        max_depth (int, optional): Maximum depth of graph. Defaults to 3.
        inclusive_search (bool, optional): If True, search for nodes that include the label. Defaults to
    False.
        min_degree (int, optional): Minimum degree of nodes. Defaults to 0.

    Returns:
        Dict[str, List[str]]: Knowledge graph for label

    Args:
        label (str):
        max_depth (Union[Unset, int]):  Default: 3.
        min_degree (Union[Unset, int]):  Default: 0.
        inclusive (Union[Unset, bool]):  Default: False.
        api_key_header_value (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        label=label,
        max_depth=max_depth,
        min_degree=min_degree,
        inclusive=inclusive,
        api_key_header_value=api_key_header_value,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    label: str,
    max_depth: Union[Unset, int] = 3,
    min_degree: Union[Unset, int] = 0,
    inclusive: Union[Unset, bool] = False,
    api_key_header_value: Union[None, Unset, str] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    """Get Knowledge Graph

     Retrieve a connected subgraph of nodes where the label includes the specified label.
    Maximum number of nodes is constrained by the environment variable `MAX_GRAPH_NODES` (default:
    1000).
    When reducing the number of nodes, the prioritization criteria are as follows:
        1. min_degree does not affect nodes directly connected to the matching nodes
        2. Label matching nodes take precedence
        3. Followed by nodes directly connected to the matching nodes
        4. Finally, the degree of the nodes
    Maximum number of nodes is limited to env MAX_GRAPH_NODES(default: 1000)

    Args:
        label (str): Label to get knowledge graph for
        max_depth (int, optional): Maximum depth of graph. Defaults to 3.
        inclusive_search (bool, optional): If True, search for nodes that include the label. Defaults to
    False.
        min_degree (int, optional): Minimum degree of nodes. Defaults to 0.

    Returns:
        Dict[str, List[str]]: Knowledge graph for label

    Args:
        label (str):
        max_depth (Union[Unset, int]):  Default: 3.
        min_degree (Union[Unset, int]):  Default: 0.
        inclusive (Union[Unset, bool]):  Default: False.
        api_key_header_value (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        label=label,
        max_depth=max_depth,
        min_degree=min_degree,
        inclusive=inclusive,
        api_key_header_value=api_key_header_value,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    label: str,
    max_depth: Union[Unset, int] = 3,
    min_degree: Union[Unset, int] = 0,
    inclusive: Union[Unset, bool] = False,
    api_key_header_value: Union[None, Unset, str] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Get Knowledge Graph

     Retrieve a connected subgraph of nodes where the label includes the specified label.
    Maximum number of nodes is constrained by the environment variable `MAX_GRAPH_NODES` (default:
    1000).
    When reducing the number of nodes, the prioritization criteria are as follows:
        1. min_degree does not affect nodes directly connected to the matching nodes
        2. Label matching nodes take precedence
        3. Followed by nodes directly connected to the matching nodes
        4. Finally, the degree of the nodes
    Maximum number of nodes is limited to env MAX_GRAPH_NODES(default: 1000)

    Args:
        label (str): Label to get knowledge graph for
        max_depth (int, optional): Maximum depth of graph. Defaults to 3.
        inclusive_search (bool, optional): If True, search for nodes that include the label. Defaults to
    False.
        min_degree (int, optional): Minimum degree of nodes. Defaults to 0.

    Returns:
        Dict[str, List[str]]: Knowledge graph for label

    Args:
        label (str):
        max_depth (Union[Unset, int]):  Default: 3.
        min_degree (Union[Unset, int]):  Default: 0.
        inclusive (Union[Unset, bool]):  Default: False.
        api_key_header_value (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            label=label,
            max_depth=max_depth,
            min_degree=min_degree,
            inclusive=inclusive,
            api_key_header_value=api_key_header_value,
        )
    ).parsed
