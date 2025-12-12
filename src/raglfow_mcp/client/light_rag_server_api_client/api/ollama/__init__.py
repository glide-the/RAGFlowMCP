"""Contains endpoint functions for accessing the API"""

# Импортируем модули для удобства использования
from .chat_api_chat_post import asyncio as async_chat
from .chat_api_chat_post import sync as chat
from .generate_api_generate_post import asyncio as async_generate
from .generate_api_generate_post import sync as generate
from .get_tags_api_tags_get import asyncio as async_get_tags
from .get_tags_api_tags_get import sync as get_tags
from .get_version_api_version_get import asyncio as async_get_version
from .get_version_api_version_get import sync as get_version

__all__ = [
    "chat",
    "async_chat",
    "generate",
    "async_generate",
    "get_tags",
    "async_get_tags",
    "get_version",
    "async_get_version",
]
