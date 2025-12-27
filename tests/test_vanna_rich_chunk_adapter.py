import sys
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch

import httpx

sys.argv = [sys.argv[0]]

from data_analyst_mcp.vanna_rich_chunk_adapter import chunk_to_events


class TestVannaRichChunkAdapter(TestCase):
    def test_dataframe_adds_link_event(self) -> None:
        chunk = SimpleNamespace(
            conversation_id="conv-1",
            request_id="req-1",
            timestamp=1234567890,
            rich={
                "id": "df-1",
                "type": "dataframe",
                "data": {
                    "title": "Results",
                    "rows": [{"a": 1}],
                },
            },
        )

        with patch("data_analyst_mcp.vanna_rich_chunk_adapter.httpx.post") as mock_post:
            mock_post.return_value = httpx.Response(
                200,
                json={"asset": {"url": "https://files.example.com/export.csv"}},
            )

            events = chunk_to_events(chunk)

        event_types = [event["type"] for event in events]
        self.assertIn("dataframe", event_types)
        self.assertIn("link", event_types)
        link_event = next(event for event in events if event["type"] == "link")
        self.assertEqual(link_event["url"], "https://files.example.com/export.csv")

    def test_chart_adds_image_event(self) -> None:
        chunk = SimpleNamespace(
            conversation_id="conv-2",
            request_id="req-2",
            timestamp=1234567891,
            rich={
                "id": "chart-1",
                "type": "chart",
                "data": {
                    "title": "Chart Title",
                    "data": [{"x": [1], "y": [2]}],
                    "layout": {"title": "Chart Title"},
                    "config": {"displayModeBar": False},
                },
            },
        )

        with patch("data_analyst_mcp.vanna_rich_chunk_adapter.httpx.post") as mock_post:
            mock_post.return_value = httpx.Response(
                200,
                json={"asset": {"preview_url": "https://files.example.com/chart.png"}},
            )

            events = chunk_to_events(chunk)

        event_types = [event["type"] for event in events]
        self.assertEqual(event_types[:2], ["plotly", "image"])
        image_event = next(event for event in events if event["type"] == "image")
        self.assertEqual(image_event["image_url"], "https://files.example.com/chart.png")

    def test_export_failure_still_returns_dataframe(self) -> None:
        chunk = SimpleNamespace(
            conversation_id="conv-3",
            request_id="req-3",
            timestamp=1234567892,
            rich={
                "id": "df-2",
                "type": "dataframe",
                "data": {"rows": [{"a": 1}]},
            },
        )

        with patch("data_analyst_mcp.vanna_rich_chunk_adapter.httpx.post") as mock_post:
            mock_post.side_effect = httpx.RequestError("boom")

            events = chunk_to_events(chunk)

        event_types = [event["type"] for event in events]
        self.assertEqual(event_types, ["dataframe"])
