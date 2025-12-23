# Vanna MCP Server (with Ragflow retrieval)

MCP server for integrating Vanna chat and Ragflow retrieval with AI tools. Provides MCP tools for Ragflow's `/api/v1/retrieval` endpoint and a streaming bridge to Vanna's `/api/v0/chat_sse`.

## Description

The server bridges MCP-compatible clients with Ragflow retrieval and Vanna chat APIs. It keeps the original Ragflow retrieval tool for backward compatibility and adds streaming chat support.

### Key Features

- **Information Retrieval**: Execute semantic, keyword, and hybrid retrieval against Ragflow datasets/documents.
- **Vanna Chat Streaming**: Proxy Vanna `/api/v0/chat_sse` responses through MCP streaming.

## Installation

This server is designed to be used as an MCP server and should be installed in a virtual environment using uv, not as a system-wide package.

### Development Installation

```bash
# Create a virtual environment
uv venv --python 3.11

# Install the package in development mode
uv pip install -e .
```

## Requirements

- Python 3.11+
- Running Ragflow API server with `/api/v1/retrieval` enabled
- Running Vanna API server exposing `/api/v0/chat_sse`

## Environment Variables

```env
RAGFLOW_API_BASE=http://localhost:9621
RAGFLOW_API_KEY=your-api-key

VANNA_API_BASE=http://localhost:8000
VANNA_API_KEY=your_vanna_api_key
```

## Usage

**Important**: The MCP server should be run through an MCP client configuration file (e.g., `mcp-config.json`).

### Command Line Options

The following arguments are available when configuring the server (can also be provided via environment variables):

- `--host`: Ragflow API host (default: localhost)
- `--port`: Ragflow API port (default: 9621)
- `--api-key`: Ragflow API key (optional)
- `--base-url`: Full Ragflow API base URL (overrides host/port)
- `--vanna-api-key`: Vanna API key (optional)
- `--vanna-base-url`: Full Vanna API base URL

Both the legacy `raglfow-mcp` and the new `vanna-mcp` entry points map to the same server.

### Setting up as MCP server

#### Using uvenv (uvx):

```json
{
  "mcpServers": {
    "ragflow-mcp": {
      "command": "uvx",
      "args": [
        "vanna-mcp",
        "--host",
        "localhost",
        "--port",
        "9621",
        "--api-key",
        "your_api_key"
      ]
    }
  }
}
```

#### Development

```json
{
  "mcpServers": {
    "ragflow-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp",
        "run",
        "src/mcp/main.py",
        "--host",
        "localhost",
        "--port",
        "9621",
        "--api-key",
        "your_api_key"
      ]
    }
  }
}
```

Replace `/path/to/mcp` with the actual path to your MCP directory.

## Available MCP Tools

- `ragflow_retrieval`: Execute Ragflow `/api/v1/retrieval` against specified dataset or document IDs.
- `vanna_chat_sse`: Stream responses from Vanna `/api/v0/chat_sse` through MCP streaming.

### Streaming example

```python
from mcp.client.vanna_server_api_client.vanna_client import build_vanna_client, chat_sse_stream

client = build_vanna_client()

async for event in chat_sse_stream(client=client, message="Hello Vanna"):
    print(event)
```

## Development

### Installing development dependencies

```bash
uv pip install -e ".[dev]"
```

### Running linters

```bash
ruff check src/
mypy src/
```

## License

MIT
