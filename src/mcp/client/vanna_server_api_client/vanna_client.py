"""Convenience helpers for constructing Vanna clients."""

from __future__ import annotations

import os
from typing import Optional

from .api.chat.chat_sse_post import chat_sse_stream
from .client import AuthenticatedClient

__all__ = ["build_vanna_client", "chat_sse_stream"]


def build_vanna_client(base_url: Optional[str] = None, api_key: Optional[str] = None) -> AuthenticatedClient:
    """Build an authenticated Vanna client from parameters or environment variables."""

    resolved_base_url = base_url or os.getenv("VANNA_API_BASE")
    resolved_api_key = api_key or os.getenv("VANNA_API_KEY")

    if not resolved_base_url or not resolved_api_key:
        raise RuntimeError("VANNA_API_BASE and VANNA_API_KEY must be set")

    return AuthenticatedClient(
        base_url=resolved_base_url,
        token=resolved_api_key,
        verify_ssl=False,
    )
