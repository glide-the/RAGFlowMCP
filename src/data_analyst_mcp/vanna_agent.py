from typing import Optional

from chromadb.utils import embedding_functions
from data_analyst_mcp import config
from vanna import Agent
from vanna.core.registry import ToolRegistry
from vanna.core.user import RequestContext, User, UserResolver
from vanna.integrations.chromadb import ChromaAgentMemory
from vanna.integrations.openai import OpenAILlmService
from vanna.integrations.postgres import PostgresRunner
from vanna.tools import RunSqlTool, VisualizeDataTool
from vanna.tools.agent_memory import (
    SaveQuestionToolArgsTool,
    SaveTextMemoryTool,
    SearchSavedCorrectToolUsesTool,
)


class SimpleUserResolver(UserResolver):
    async def resolve_user(self, request_context: RequestContext) -> User:
        user_email = request_context.get_cookie("vanna_email") or "guest@example.com"
        group = "admin" if user_email == "admin@example.com" else "user"
        return User(id=user_email, email=user_email, group_memberships=[group])


def _build_agent() -> Agent:
    llm = OpenAILlmService(
        model=config.VANNA_LLM_MODEL,
        api_key=config.VANNA_LLM_API_KEY,
        base_url=config.VANNA_LLM_BASE_URL,
    )

    db_conn_str = config.VANNA_PG_CONN_STR
    db_tool = RunSqlTool(sql_runner=PostgresRunner(connection_string=db_conn_str))

    agent_memory = ChromaAgentMemory(
        collection_name=config.VANNA_MEMORY_COLLECTION,
        persist_directory=config.VANNA_CHROMA_DIR,
        embedding_function=embedding_functions.OpenAIEmbeddingFunction(
            api_base=config.VANNA_EMBED_BASE_URL,
            api_key=config.VANNA_EMBED_API_KEY,
            model_name=config.VANNA_EMBED_MODEL,
        ),
    )

    tools = ToolRegistry()
    tools.register_local_tool(db_tool, access_groups=["admin", "user"])
    tools.register_local_tool(SaveQuestionToolArgsTool(), access_groups=["admin"])
    tools.register_local_tool(SearchSavedCorrectToolUsesTool(), access_groups=["admin", "user"])
    tools.register_local_tool(SaveTextMemoryTool(), access_groups=["admin", "user"])
    tools.register_local_tool(VisualizeDataTool(), access_groups=["admin", "user"])

    return Agent(
        llm_service=llm,
        tool_registry=tools,
        user_resolver=SimpleUserResolver(),
        agent_memory=agent_memory,
    )


_agent: Optional[Agent] = None


def get_vanna_agent() -> Agent:
    global _agent
    if _agent is None:
        _agent = _build_agent()
    return _agent
