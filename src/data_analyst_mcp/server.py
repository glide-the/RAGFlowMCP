"""Main module for Vanna MCP server (with Ragflow retrieval)."""

import logging
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, Awaitable, Dict, List, Optional, cast

from mcp.server.fastmcp import Context, FastMCP
from pydantic import Field

from data_analyst_mcp import config
from data_analyst_mcp.client.ragflow_server_api_client.client import AuthenticatedClient
from data_analyst_mcp.client.ragflow_server_api_client.models import RagflowRetrievalResponse
from data_analyst_mcp.client.ragflow_server_api_client.ragflow_client import (
    build_ragflow_client,
    ragflow_retrieve_chunks,
)
from data_analyst_mcp.client.vanna_server_api_client.client import (
    AuthenticatedClient as VannaClient,
)
from data_analyst_mcp.client.vanna_server_api_client.vanna_client import (
    build_vanna_client,
    chat_sse_stream,
)

logger = logging.getLogger(__name__)


@dataclass
class AppContext:
    """Application context with typed resources."""

    ragflow_client: AuthenticatedClient
    vanna_client: VannaClient


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with typed context."""

    ragflow_client = build_ragflow_client(
        base_url=config.RAGFLOW_API_BASE_URL,
        api_key=config.RAGFLOW_API_KEY,
    )
    vanna_client = build_vanna_client(
        base_url=config.VANNA_API_BASE_URL,
        api_key=config.VANNA_API_KEY,
    )

    try:
        yield AppContext(ragflow_client=ragflow_client, vanna_client=vanna_client)
    finally:
        await ragflow_client.get_async_httpx_client().aclose()
        await vanna_client.get_async_httpx_client().aclose()
        logger.info("Vanna MCP Server stopped")


mcp = FastMCP("Vanna MCP Server", lifespan=app_lifespan)


def format_response(result: Any, is_error: bool = False) -> Dict[str, Any]:
    """Format responses for MCP tools."""

    if is_error:
        if isinstance(result, str):
            return {"status": "error", "error": result}
        return {"status": "error", "error": str(result)}

    if isinstance(result, dict):
        return {"status": "success", "response": result}

    if hasattr(result, "model_dump"):
        return {"status": "success", "response": result.model_dump()}
    if hasattr(result, "dict") and callable(getattr(result, "dict")):
        return {"status": "success", "response": result.dict()}
    if hasattr(result, "__dict__"):
        return {"status": "success", "response": result.__dict__}
    if hasattr(result, "to_dict") and callable(getattr(result, "to_dict")):
        return {"status": "success", "response": result.to_dict()}

    return {"status": "success", "response": str(result)}


async def execute_ragflow_operation(
    operation_name: str,
    operation_func: Callable[[AuthenticatedClient], Awaitable[Any]],
    ctx: Context,
) -> Dict[str, Any]:
    """Wrapper for executing Ragflow operations with standard formatting."""

    try:
        if not ctx or not ctx.request_context or not ctx.request_context.lifespan_context:
            return format_response(
                f"Error: Request context is not available for {operation_name}", is_error=True
            )

        app_ctx = cast(AppContext, ctx.request_context.lifespan_context)
        client = app_ctx.ragflow_client

        logger.info(f"Executing operation: {operation_name}")
        result = await operation_func(client)

        return format_response(result)
    except Exception as e:  # noqa: BLE001
        logger.exception(f"Error during {operation_name}: {str(e)}")
        return format_response(str(e), is_error=True)


async def execute_vanna_operation(
    operation_name: str,
    operation_func: Callable[[VannaClient], Awaitable[Any]],
    ctx: Context,
) -> Dict[str, Any]:
    """Wrapper for executing Vanna operations with standard formatting."""

    try:
        if not ctx or not ctx.request_context or not ctx.request_context.lifespan_context:
            return format_response(
                f"Error: Request context is not available for {operation_name}", is_error=True
            )

        app_ctx = cast(AppContext, ctx.request_context.lifespan_context)
        client = app_ctx.vanna_client

        logger.info(f"Executing operation: {operation_name}")
        result = await operation_func(client)

        return format_response(result)
    except Exception as e:  # noqa: BLE001
        logger.exception(f"Error during {operation_name}: {str(e)}")
        return format_response(str(e), is_error=True)


@mcp.tool(name="ragflow_retrieval", description="Execute retrieval query through Ragflow /api/v1/retrieval")
async def ragflow_retrieval(
    ctx: Context,
    question: str = Field(description="Query text for retrieval"),
    dataset_ids: Optional[List[str]] = Field(
        default=None, description="List of dataset IDs to search within"
    ),
    document_ids: Optional[List[str]] = Field(
        default=None, description="Specific document IDs to constrain search"
    ),
    page: int = Field(default=1, description="Page number for paginated results"),
    page_size: int = Field(default=30, description="Page size for paginated results"),
    similarity_threshold: float = Field(
        default=0.2, description="Similarity threshold for vector retrieval"
    ),
    vector_similarity_weight: float = Field(
        default=0.3, description="Weight for vector similarity in ranking"
    ),
    top_k: int = Field(default=1024, description="Maximum chunks to consider"),
    keyword: bool = Field(default=False, description="Enable keyword retrieval"),
    highlight: bool = Field(default=False, description="Include highlight snippets"),
    use_kg: bool = Field(default=False, description="Use knowledge graph retrieval"),
) -> Dict[str, Any]:
    """Call Ragflow retrieval endpoint and normalize the response."""

    if not dataset_ids and not document_ids:
        return format_response("dataset_ids or document_ids must be provided", is_error=True)

    async def _operation(client: AuthenticatedClient) -> Dict[str, Any]:
        response: RagflowRetrievalResponse = await ragflow_retrieve_chunks(
            client=client,
            question=question,
            dataset_ids=dataset_ids,
            document_ids=document_ids,
            page=page,
            page_size=page_size,
            similarity_threshold=similarity_threshold,
            vector_similarity_weight=vector_similarity_weight,
            top_k=top_k,
            keyword=keyword,
            highlight=highlight,
            use_kg=use_kg,
        )

        if not response.is_success():
            raise RuntimeError(f"Ragflow retrieval failed: {response.message}")

        data = response.data
        if data is None:
            return {"total": 0, "chunks": [], "doc_aggs": []}

        return {
            "total": data.total,
            "chunks": [
                {
                    "content": chunk.content,
                    "highlight": chunk.highlight,
                    "document_id": chunk.document_id,
                    "doc_keyword": chunk.document_keyword,
                    "similarity": chunk.similarity,
                }
                for chunk in data.chunks
            ],
            "doc_aggs": [
                {"doc_id": agg.doc_id, "doc_name": agg.doc_name, "count": agg.count}
                for agg in data.doc_aggs
            ],
        }

    return await execute_ragflow_operation(
        operation_name=f"ragflow retrieval: {question[:50]}...",
        operation_func=_operation,
        ctx=ctx,
    )


@mcp.tool(
    name="vanna_chat_sse",
    description="Call Vanna /api/v0/chat_sse and stream responses end-to-end",
)
async def vanna_chat_sse(
    ctx: Context,
    message: str = Field(description="User message to send to Vanna"),
    user_email: Optional[str] = Field(default=None, description="User email"),
    conversation_id: Optional[str] = Field(
        default=None,
        description="Existing conversation id to continue; if omitted a new conversation is started",
    ),
    agent_id: Optional[str] = Field(default=None, description="Optional Vanna agent id"),
    acceptable_responses: Optional[List[str]] = Field(
        default=None,
        description="Filter response types: text/image/link/error/dataframe/plotly/sql",
    ),
) -> AsyncIterator[Dict[str, Any]]:
    """Stream chat responses from Vanna via SSE."""

    if not ctx or not ctx.request_context or not ctx.request_context.lifespan_context:
        raise RuntimeError("Request context is not available for vanna_chat_sse")

    app_ctx = cast(AppContext, ctx.request_context.lifespan_context)
    vanna_client = app_ctx.vanna_client

    await ctx.debug(f"Calling Vanna chat_sse with message: {message[:50]}...")

    async for event in chat_sse_stream(
        client=vanna_client,
        message=message,
        user_email=user_email,
        conversation_id=conversation_id,
        agent_id=agent_id,
        acceptable_responses=acceptable_responses,
    ):
        yield event


__all__ = ["mcp"]
