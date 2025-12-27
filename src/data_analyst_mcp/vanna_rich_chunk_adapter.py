import logging
from typing import Any, Dict, Iterable, List, Optional

import httpx
from vanna.servers.base.models import ChatStreamChunk

from data_analyst_mcp import config

logger = logging.getLogger(__name__)


_IMAGE_TYPES = {
    "image",
    "svg",
    "png",
    "jpg",
    "jpeg",
    "gif",
    "webp",
}


def _normalize_button_data(button: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    label = button.get("label") or button.get("title") or button.get("text")
    action = button.get("action") or button.get("value") or button.get("payload")
    if label is None and action is None:
        return None
    return {
        "label": label,
        "action": action,
        "variant": button.get("variant"),
        "size": button.get("size"),
        "icon": button.get("icon"),
        "disabled": button.get("disabled", False),
    }


def _buttons_event(buttons: Iterable[Dict[str, Any]], text: str = "") -> Optional[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for button in buttons:
        normalized_button = _normalize_button_data(button)
        if normalized_button:
            normalized.append(normalized_button)
    if not normalized:
        return None
    return {"type": "buttons", "text": text, "buttons": normalized}


def _progress_text(label: Optional[str], value: Any, description: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        pct = int(value * 100) if value <= 1 else int(value)
        base = f"{label or 'Progress'}: {pct}%"
    else:
        base = f"{label or 'Progress'}: {value}"
    if description:
        base += f" - {description}"
    return base


def _artifact_url(artifact_id: Optional[str], content: Any, data: Dict[str, Any]) -> Optional[str]:
    url = data.get("url") or data.get("path")
    if isinstance(content, str) and content.startswith(("http://", "https://")):
        return content
    if url:
        return url
    if artifact_id:
        return f"artifact://{artifact_id}"
    return None


def rich_component_to_events(rich: Dict[str, Any]) -> List[Dict[str, Any]]:
    events: List[Dict[str, Any]] = []

    component_type = (rich.get("type") or "").lower()
    data = rich.get("data", {}) or {}

    if component_type == "text":
        content = data.get("content")
        if content:
            events.append({"type": "text", "text": content})

    elif component_type == "card":
        title = data.get("title") or ""
        subtitle = data.get("subtitle") or ""
        content = data.get("content") or ""
        status = data.get("status")
        text = "\n\n".join([part for part in [title, subtitle, content] if part])
        if status:
            text = f"[{str(status).upper()}] {text}" if text else f"[{str(status).upper()}]"
        if text:
            events.append({"type": "text", "text": text})
        actions = data.get("actions") or []
        buttons_event = _buttons_event(actions, text=title or "")
        if buttons_event:
            events.append(buttons_event)

    elif component_type == "status_card":
        title = data.get("title") or ""
        status = (data.get("status") or "").lower()
        description = data.get("description") or ""
        if status in {"error", "failed"}:
            message = f"{title}: {description or status}" if title else description or status
            if message:
                events.append({"type": "error", "error": message})
        else:
            text = f"[{status.upper()}] {title}: {description}" if status else f"{title}: {description}"
            events.append({"type": "text", "text": text.strip()})
        actions = data.get("actions") or []
        buttons_event = _buttons_event(actions, text=title or "")
        if buttons_event:
            events.append(buttons_event)

    elif component_type in {"progress_display", "progress_bar"}:
        text = _progress_text(data.get("label"), data.get("value"), data.get("description"))
        if text:
            events.append({"type": "text", "text": text})
        if (data.get("status") or "").lower() == "error":
            if text:
                events.append({"type": "error", "error": text})

    elif component_type == "notification":
        message = data.get("message") or ""
        title = data.get("title") or ""
        level = (data.get("level") or "").lower()
        text = f"{title + ': ' if title else ''}{message}".strip()
        if level == "error":
            if text:
                events.append({"type": "error", "error": text})
        elif text:
            events.append({"type": "text", "text": text})

    elif component_type == "status_indicator":
        status = (data.get("status") or "").lower()
        message = data.get("message") or ""
        text = f"[{status.upper()}] {message}".strip()
        if status == "error":
            if text:
                events.append({"type": "error", "error": text})
        elif text:
            events.append({"type": "text", "text": text})

    elif component_type == "badge":
        text = data.get("text") or ""
        variant = data.get("variant")
        if variant and variant != "default":
            text = f"[{variant}] {text}"
        if text:
            events.append({"type": "text", "text": text})

    elif component_type == "icon_text":
        icon = data.get("icon")
        text = data.get("text") or ""
        if icon:
            text = f"{icon} {text}".strip()
        if text:
            events.append({"type": "text", "text": text})

    elif component_type == "log_viewer":
        lines: List[str] = []
        for entry in data.get("entries", []):
            level = (entry.get("level") or "info").upper()
            timestamp = entry.get("timestamp")
            message = entry.get("message") or ""
            prefix = f"[{timestamp}] [{level}] " if timestamp else f"[{level}] "
            lines.append(prefix + message)
        if lines:
            events.append({"type": "text", "text": "\n".join(lines)})

    elif component_type == "task_list":
        title = data.get("title", "Tasks")
        lines = [f"## {title}"] if title else []
        for task in data.get("tasks", []):
            status = task.get("status", "pending")
            task_title = task.get("title", "")
            progress = task.get("progress")
            if progress is not None:
                pct = int(progress * 100) if isinstance(progress, (int, float)) else progress
                lines.append(f"- [{status}] {task_title} ({pct}%)")
            else:
                lines.append(f"- [{status}] {task_title}")
        if lines:
            events.append({"type": "text", "text": "\n".join(lines)})

    elif component_type == "button":
        buttons_event = _buttons_event([data], text=data.get("label") or "")
        if buttons_event:
            events.append(buttons_event)

    elif component_type == "button_group":
        buttons = data.get("buttons") or []
        buttons_event = _buttons_event(buttons, text="")
        if buttons_event:
            events.append(buttons_event)

    elif component_type == "dataframe":
        events.append(_build_dataframe_event_from_rich(rich))

    elif component_type == "chart":
        events.append(_build_plotly_event_from_rich(rich))

    elif component_type == "artifact":
        artifact_id = data.get("artifact_id") or rich.get("id")
        artifact_type = (data.get("artifact_type") or "").lower()
        title = data.get("title") or data.get("name") or artifact_id or ""
        description = data.get("description")
        content = data.get("content")
        url = _artifact_url(artifact_id, content, data)
        if artifact_type in _IMAGE_TYPES:
            if url:
                events.append(
                    {
                        "type": "image",
                        "image_url": url,
                        "caption": title or description,
                    }
                )
        elif url:
            events.append(
                {
                    "type": "link",
                    "title": title or artifact_id or "Artifact",
                    "url": url,
                    "description": description,
                }
            )
        elif title:
            events.append({"type": "text", "text": title})

    elif component_type == "sql":
        query = data.get("query") or data.get("sql")
        if query:
            events.append({"type": "sql", "query": query})

    elif component_type == "status_bar_update":
        status = data.get("status")
        message = data.get("message") or ""
        detail = data.get("detail") or ""
        text_parts = [status, message, detail]
        text = " ".join([part for part in text_parts if part]).strip()
        if text:
            events.append({"type": "text", "text": text})

    return events


def _build_dataframe_event_from_rich(rich: Dict[str, Any]) -> Dict[str, Any]:
    data = rich.get("data", {}) or {}
    return {"type": "dataframe", "json_table": data}


def _build_plotly_event_from_rich(rich: Dict[str, Any]) -> Dict[str, Any]:
    data = rich.get("data", {}) or {}
    json_plotly = {
        "data": data.get("data"),
        "layout": data.get("layout"),
        "config": data.get("config"),
    }
    if "title" in data:
        json_plotly.setdefault("layout", {})
        json_plotly["layout"].setdefault("title", data["title"])
    return {"type": "plotly", "json_plotly": json_plotly}


def _build_link_event_for_dataframe(
    chunk: ChatStreamChunk,
    asset: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    url = asset.get("url")
    if not url:
        return None
    data = (chunk.rich or {}).get("data", {}) or {}
    title = data.get("title") or asset.get("filename") or "Download DataFrame"
    description = data.get("description") or "Download result data as file"
    return {
        "type": "link",
        "title": title,
        "url": url,
        "description": description,
    }


def _build_image_event_for_chart(
    chunk: ChatStreamChunk,
    asset: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    preview_url = asset.get("preview_url")
    if not preview_url:
        return None
    data = (chunk.rich or {}).get("data", {}) or {}
    caption = data.get("title") or "Chart Preview"
    return {
        "type": "image",
        "image_url": preview_url,
        "caption": caption,
    }


def _export_dataframe_asset(chunk: ChatStreamChunk) -> Optional[Dict[str, Any]]:
    rich = chunk.rich or {}
    data = rich.get("data", {}) or {}
    if not data.get("exportable", True):
        return None
    payload = {
        "conversation_id": chunk.conversation_id,
        "request_id": chunk.request_id,
        "rich": {
            "id": rich.get("id"),
            "type": "dataframe",
            "lifecycle": rich.get("lifecycle", "create"),
            "timestamp": rich.get("timestamp", chunk.timestamp),
            "visible": rich.get("visible", True),
            "interactive": rich.get("interactive", False),
            "data": data,
        },
        "export": {
            "format": "csv",
            "filename": data.get("title", "dataframe_export.csv"),
            "include_index": False,
            "encoding": "utf-8",
        },
    }
    try:
        response = httpx.post(
            f"{config.RICH_ASSET_BASE_URL}/api/v0/rich_assets/dataframe/export",
            json=payload,
            timeout=config.RICH_ASSET_TIMEOUT,
        )
        response.raise_for_status()
        return response.json().get("asset")
    except httpx.HTTPError as exc:
        logger.warning("export dataframe asset failed: %s", exc)
        return None


def _render_chart_asset(chunk: ChatStreamChunk) -> Optional[Dict[str, Any]]:
    rich = chunk.rich or {}
    data = rich.get("data", {}) or {}
    payload = {
        "conversation_id": chunk.conversation_id,
        "request_id": chunk.request_id,
        "rich": {
            "id": rich.get("id"),
            "type": "chart",
            "lifecycle": rich.get("lifecycle", "create"),
            "timestamp": rich.get("timestamp", chunk.timestamp),
            "visible": rich.get("visible", True),
            "interactive": rich.get("interactive", False),
            "data": data,
        },
        "render": {
            "format": "png",
            "scale": 2,
            "width": 1200,
            "height": 600,
            "background": "white",
        },
    }
    try:
        response = httpx.post(
            f"{config.RICH_ASSET_BASE_URL}/api/v0/rich_assets/chart/render",
            json=payload,
            timeout=config.RICH_ASSET_TIMEOUT,
        )
        response.raise_for_status()
        return response.json().get("asset")
    except httpx.HTTPError as exc:
        logger.warning("render chart asset failed: %s", exc)
        return None


def _attach_identifiers(chunk: ChatStreamChunk, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    for event in events:
        if chunk.conversation_id:
            event.setdefault("conversation_id", chunk.conversation_id)
        if chunk.request_id:
            event.setdefault("request_id", chunk.request_id)
    return events


def chunk_to_events(chunk: ChatStreamChunk) -> List[Dict[str, Any]]:
    """Convert a ChatStreamChunk to Vanna chat SSE events."""
    rich = chunk.rich or {}
    component_type = (rich.get("type") or "").lower()

    if component_type == "dataframe":
        events: List[Dict[str, Any]] = [_build_dataframe_event_from_rich(rich)]
        asset = _export_dataframe_asset(chunk)
        link_event = _build_link_event_for_dataframe(chunk, asset or {})
        if link_event:
            events.append(link_event)
        return _attach_identifiers(chunk, events)

    if component_type == "chart":
        events = [_build_plotly_event_from_rich(rich)]
        asset = _render_chart_asset(chunk)
        image_event = _build_image_event_for_chart(chunk, asset or {})
        if image_event:
            events.append(image_event)
        return _attach_identifiers(chunk, events)

    base_events = rich_component_to_events(rich)
    return _attach_identifiers(chunk, base_events)
