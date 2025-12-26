from __future__ import annotations

from dataclasses import dataclass
from typing import Any, AsyncGenerator, Dict, List, Optional
from pydantic import Field

from data_analyst_mcp import config
from data_analyst_mcp.server import aggregate_vanna_events
from data_analyst_mcp.vanna_agent import get_vanna_agent
from data_analyst_mcp.vanna_chat_handler_stream import chat_stream_from_handler
from mcp.server.fastmcp import FastMCP
from vanna.servers.base.chat_handler import ChatHandler

import logging
import sys 
from mcp.server.session import ServerSession

####################################################################################
# Temporary monkeypatch which avoids crashing when a POST message is received
# before a connection has been initialized, e.g: after a deployment.
# pylint: disable-next=protected-access
old__received_request = ServerSession._received_request


async def _received_request(self, *args, **kwargs):
    try:
        return await old__received_request(self, *args, **kwargs)
    except RuntimeError:
        pass


# pylint: disable-next=protected-access
ServerSession._received_request = _received_request
####################################################################################

@dataclass
class AppState:
    agent: Any
    chat_handler: ChatHandler


# 全局 AppState 单例
_APP_STATE: Optional[AppState] = None


def get_app_state() -> AppState:
    """
    获取全局 AppState；如果还没初始化，则创建一个占位实例，
    实际 Vanna agent / ChatHandler 的构建仍由 ensure_initialized 完成。
    """
    global _APP_STATE
    if _APP_STATE is None:
        # 初始为 None，占位，保持与原来 lifespan 里的初始状态一致
        _APP_STATE = AppState(agent=None, chat_handler=None)  # type: ignore[arg-type]
    return _APP_STATE


mcp = FastMCP(
    "VannaMCP",
    stateless_http=True,
    json_response=True,
)


def ensure_initialized(state: AppState) -> AppState:
    """Initialize agent and chat handler on first use."""
    if state.agent is None:
        state.agent = get_vanna_agent()
        state.chat_handler = ChatHandler(state.agent)
    return state


@mcp.tool()
async def vanna_chat_stream(
    message: str,
    conversation_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    acceptable_responses: Optional[List[str]] = None,
) -> AsyncGenerator[Dict[str, Any], None]:
    """
    Stream responses from a local Vanna ChatHandler as chat SSE events.
    """
    _ = agent_id
    state = ensure_initialized(get_app_state())

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
) -> Dict[str, Any]:
    """Return aggregated chat output for a single message."""
    _ = agent_id
    state = ensure_initialized(get_app_state())
    events: List[Dict[str, Any]] = []
    async for event in chat_stream_from_handler(
        chat_handler=state.chat_handler,
        message=message,
        conversation_id=conversation_id,
    ):
        event_type = event.get("type")
        if event_type == "end":
            events.append(event)
            continue
        if acceptable_responses and event_type not in acceptable_responses:
            continue
        events.append(event)
    return aggregate_vanna_events(events)




logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        log_level = getattr(logging, "INFO")
        logging.getLogger().setLevel(log_level)
        logger.info("Starting Vanna MCP server")
        logger.info(f"Vanna API server is expected to be already running and available at: {config.VANNA_API_BASE_URL}")

        # Log and validate vanna_agent.py related environment variables
        logger.info("=" * 80)
        logger.info("Vanna Agent Configuration:")
        logger.info("=" * 80)

        # LLM Configuration
        logger.info(f"VANNA_LLM_MODEL: {config.VANNA_LLM_MODEL}")
        logger.info(f"VANNA_LLM_BASE_URL: {config.VANNA_LLM_BASE_URL}")
        if config.VANNA_LLM_API_KEY:
            logger.info(f"VANNA_LLM_API_KEY: {'*' * 20}{config.VANNA_LLM_API_KEY[-4:] if len(config.VANNA_LLM_API_KEY) > 4 else '****'}")
        else:
            logger.warning("VANNA_LLM_API_KEY is not set - this may cause authentication failures")

        # PostgreSQL Configuration
        if config.VANNA_PG_CONN_STR:
            logger.info(f"VANNA_PG_CONN_STR: {config.VANNA_PG_CONN_STR[:20]}...{config.VANNA_PG_CONN_STR[-10:] if len(config.VANNA_PG_CONN_STR) > 30 else config.VANNA_PG_CONN_STR}")
        else:
            logger.error("VANNA_PG_CONN_STR is not set - PostgreSQL connection is required for SQL execution")

        # ChromaDB Memory Configuration
        logger.info(f"VANNA_MEMORY_COLLECTION: {config.VANNA_MEMORY_COLLECTION}")
        logger.info(f"VANNA_CHROMA_DIR: {config.VANNA_CHROMA_DIR}")

        # Embedding Configuration
        logger.info(f"VANNA_EMBED_MODEL: {config.VANNA_EMBED_MODEL}")
        logger.info(f"VANNA_EMBED_BASE_URL: {config.VANNA_EMBED_BASE_URL}")
        if config.VANNA_EMBED_API_KEY:
            logger.info(f"VANNA_EMBED_API_KEY: {'*' * 20}{config.VANNA_EMBED_API_KEY[-4:] if len(config.VANNA_EMBED_API_KEY) > 4 else '****'}")
        else:
            logger.warning("VANNA_EMBED_API_KEY is not set - embedding functions may fail")

        logger.info("=" * 80)

        # Validate critical configurations
        critical_errors = []
        if not config.VANNA_LLM_API_KEY:
            critical_errors.append("VANNA_LLM_API_KEY is required but not set")
        if not config.VANNA_PG_CONN_STR:
            critical_errors.append("VANNA_PG_CONN_STR is required but not set")
        if not config.VANNA_EMBED_BASE_URL:
            critical_errors.append("VANNA_EMBED_BASE_URL is required but not set")
        if not config.VANNA_EMBED_API_KEY:
            critical_errors.append("VANNA_EMBED_API_KEY is required but not set")

        if critical_errors:
            logger.error("Critical configuration errors detected:")
            for error in critical_errors:
                logger.error(f"  - {error}")
            logger.error("Please set these environment variables before starting the server")
            sys.exit(1)

        logger.info("All critical configurations validated successfully")
        logger.info("=" * 80)
 

        mcp.run(transport="sse")

    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.exception(f"Error starting server: {str(e)}")
        sys.exit(1)
