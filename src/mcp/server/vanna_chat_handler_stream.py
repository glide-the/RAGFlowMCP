from typing import AsyncIterator, Dict, Optional

from vanna.servers.base.chat_handler import ChatHandler
from vanna.servers.base.models import ChatRequest, ChatStreamChunk

from vanna_rich_chunk_adapter import chunk_to_events


async def chat_stream_from_handler(
    chat_handler: ChatHandler,
    message: str,
    conversation_id: Optional[str] = None,
    request_id: Optional[str] = None,
) -> AsyncIterator[Dict[str, Any]]:
    """Stream Vanna chat events from a ChatHandler instance."""
    chat_request = ChatRequest(
        message=message,
        conversation_id=conversation_id,
        request_id=request_id,
    )
    last_chunk: ChatStreamChunk | None = None

    async for chunk in chat_handler.handle_stream(chat_request):
        last_chunk = chunk
        for event in chunk_to_events(chunk):
            yield event

    if last_chunk and last_chunk.conversation_id:
        yield {
            "type": "end",
            "conversation_id": last_chunk.conversation_id,
            "request_id": last_chunk.request_id,
        }
    else:
        yield {"type": "end"}
