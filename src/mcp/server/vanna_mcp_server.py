from __future__ import annotations

from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, AsyncGenerator, AsyncIterator, Dict, List, Optional, cast

from mcp.server.fastmcp import Context, FastMCP
from vanna.servers.base.chat_handler import ChatHandler
from data_analyst_mcp.server import aggregate_vanna_events
from vanna_agent import get_vanna_agent
from vanna_chat_handler_stream import chat_stream_from_handler


@dataclass
class AppState:
    agent: Any
    chat_handler: ChatHandler


@asynccontextmanager
async def app_lifespan(_: FastMCP) -> AsyncIterator[AppState]:
    agent = get_vanna_agent()
    chat_handler = ChatHandler(agent)
    state = AppState(agent=agent, chat_handler=chat_handler)
    try:
        yield state
    finally:
        pass


mcp = FastMCP(
    "VannaMCP",
    stateless_http=True,
    json_response=True,
    lifespan=app_lifespan,
)


def get_state(ctx: Context) -> AppState:
    if ctx.request_context and ctx.request_context.lifespan_context:
        return cast(AppState, ctx.request_context.lifespan_context)
    if getattr(ctx.server, "lifespan_state", None) is not None:
        return cast(AppState, ctx.server.lifespan_state)
    raise RuntimeError("Lifespan state is not available")


@mcp.tool()
async def vanna_chat_stream(
    ctx: Context,
    message: str,
    conversation_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    acceptable_responses: Optional[List[str]] = None,
) -> AsyncGenerator[Dict[str, Any], None]:
    """
    Stream responses from a local Vanna ChatHandler as chat SSE events.
    """
    _ = agent_id
    state = get_state(ctx)

    async for event in chat_stream_from_handler(
        chat_handler=state.chat_handler,
        message=message,
        conversation_id=conversation_id,
    ):
        event_type = event.get("type")
        if event_type == "end":
            yield event
            continue
        if acceptable_responses and event_type not in acceptable_responses:
            continue
        yield event


@mcp.tool()
async def vanna_chat_once(
    ctx: Context,
    message: str,
    conversation_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    acceptable_responses: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Return aggregated chat output for a single message."""
    events: List[Dict[str, Any]] = []
    async for event in vanna_chat_stream(
        ctx=ctx,
        message=message,
        conversation_id=conversation_id,
        agent_id=agent_id,
        acceptable_responses=acceptable_responses,
    ):
        events.append(event)
    return aggregate_vanna_events(events)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
