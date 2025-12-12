"""
Configuration module for Ragflow MCP server.
"""

import argparse
import os

DEFAULT_HOST = os.getenv("RAGFLOW_API_HOST", "localhost")
DEFAULT_PORT = int(os.getenv("RAGFLOW_API_PORT", 9621))
DEFAULT_API_KEY = os.getenv("RAGFLOW_API_KEY", "")
DEFAULT_API_BASE = os.getenv("RAGFLOW_API_BASE")


def parse_args():
    """Parse command line arguments for Ragflow MCP server."""

    parser = argparse.ArgumentParser(description="Ragflow MCP Server")
    parser.add_argument(
        "--host", default=DEFAULT_HOST, help=f"Ragflow API host (default: {DEFAULT_HOST})"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Ragflow API port (default: {DEFAULT_PORT})",
    )
    parser.add_argument("--api-key", default=DEFAULT_API_KEY, help="Ragflow API key (optional)")
    parser.add_argument(
        "--base-url",
        default=DEFAULT_API_BASE,
        help="Full Ragflow API base URL (overrides host/port if provided)",
    )
    return parser.parse_args()


args = parse_args()

RAGFLOW_API_HOST = args.host
RAGFLOW_API_PORT = args.port
RAGFLOW_API_KEY = args.api_key
RAGFLOW_API_BASE_URL = args.base_url or f"http://{RAGFLOW_API_HOST}:{RAGFLOW_API_PORT}"
