"""Contains endpoint functions for accessing the API"""

# Импортируем модули для удобства использования
from .get_auth_status_auth_status_get import asyncio_detailed as async_get_auth_status
from .get_auth_status_auth_status_get import sync_detailed as get_auth_status
from .get_status_health_get import asyncio as async_get_health
from .get_status_health_get import sync as get_health
from .login_login_post import asyncio as async_login
from .login_login_post import sync as login
from .redirect_to_webui_get import asyncio_detailed as async_redirect_to_webui
from .redirect_to_webui_get import sync_detailed as redirect_to_webui

__all__ = [
    "get_health",
    "async_get_health",
    "get_auth_status",
    "async_get_auth_status",
    "login",
    "async_login",
    "redirect_to_webui",
    "async_redirect_to_webui",
]
