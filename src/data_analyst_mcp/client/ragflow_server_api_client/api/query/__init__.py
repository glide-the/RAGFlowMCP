"""Contains endpoint functions for accessing the API"""

# Импортируем модули для удобства использования
from .query_text_query_post import asyncio as async_query_document
from .query_text_query_post import sync as query_document
from .query_text_stream_query_stream_post import asyncio as async_query_document_stream
from .query_text_stream_query_stream_post import sync as query_document_stream

__all__ = [
    "query_document",
    "async_query_document",
    "query_document_stream",
    "async_query_document_stream",
]
