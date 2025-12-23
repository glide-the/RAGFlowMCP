"""SSE chat endpoint wrapper for Vanna API."""

from __future__ import annotations

import json
from typing import Any, AsyncIterator, Dict, List, Optional

import httpx

from ...client import AuthenticatedClient


async def chat_sse_stream(
    client: AuthenticatedClient,
    message: str,
    user_email: Optional[str] = None,
    conversation_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    acceptable_responses: Optional[List[str]] = None,
    timeout: Optional[float | httpx.Timeout] = None,
) -> AsyncIterator[Dict[str, Any]]:
    """Stream responses from Vanna `/api/v0/chat_sse` endpoint."""

    url = client.base_url + "/api/v0/chat_sse"

    headers = {
        "Content-Type": "application/json",
        "VANNA-API-KEY": client.token,
    }

    payload = {
        "message": message,
        "user_email": user_email,
        "id": conversation_id,
        "agent_id": agent_id,
        "acceptable_responses": acceptable_responses,
    }
    payload = {key: value for key, value in payload.items() if value is not None}

    async with client.get_async_httpx_client().stream(
        "POST", url, headers=headers, json=payload, timeout=timeout
    ) as response:
        response.raise_for_status()

        async for line in response.aiter_lines():
            if not line or not line.startswith("data:"):
                continue

            raw_json = line[len("data:") :].strip()
            if not raw_json or raw_json == "[DONE]":
                break

            data = json.loads(raw_json)
            yield data
