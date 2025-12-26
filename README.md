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

Additional environment variables are required when running the local Vanna MCP server
in `src/data_analyst_mcp/vanna_mcp_server.py` (see the section below). Copy
`.env.example` to `.env` and fill in the values.

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
        "/path/to/data_analyst_mcp",
        "run",
        "src/data_analyst_mcp/main.py",
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

Replace `/path/to/data_analyst_mcp` with the actual path to your MCP directory.

## Available MCP Tools

- `ragflow_retrieval`: Execute Ragflow `/api/v1/retrieval` against specified dataset or document IDs.
- `vanna_chat_sse`: Stream responses from Vanna `/api/v0/chat_sse` through MCP streaming.

### Streaming example

```python
from data_analyst_mcp.client.vanna_server_api_client.vanna_client import (
    build_vanna_client,
    chat_sse_stream,
)

client = build_vanna_client()

async for event in chat_sse_stream(client=client, message="Hello Vanna"):
    print(event)
```

## Vanna MCP Server (Local Agent)

This server exposes a local Vanna `Agent` as an MCP server using `FastMCP`. It wraps
`vanna_agent.get_vanna_agent()` and provides a streaming tool for fine-grained events
plus a single-shot tool that aggregates the stream into one response.

### Environment Setup

1. **Python & dependencies**

   Use the same Python version as the rest of the project (3.11+) and install the
   package in editable mode:

   ```bash
   uv pip install -e .
   ```

2. **Environment variables**

   ```bash
   cp .env.example .env
   ```

   Then fill in the required values, especially:

   - `VANNA_LLM_API_KEY`
   - `VANNA_PG_CONN_STR`
   - `VANNA_EMBED_API_KEY`

   Missing required values will cause the server to fail during startup or tool
   execution.

### Configuration

- **LLM**
  - `VANNA_LLM_MODEL` (default: `deepseek-chat`)
  - `VANNA_LLM_API_KEY` (**required**)
  - `VANNA_LLM_BASE_URL` (default: `https://api.deepseek.com/v1`)
- **PostgreSQL**
  - `VANNA_PG_CONN_STR` (**required**)
- **Memory / Chroma**
  - `VANNA_MEMORY_COLLECTION` (default: `vanna_memory`)
  - `VANNA_CHROMA_DIR` (default: `./chroma_db`)
- **Embeddings**
  - `VANNA_EMBED_BASE_URL` (required or depends on backend)
  - `VANNA_EMBED_API_KEY` (**required**)
  - `VANNA_EMBED_MODEL` (default: `qwen3-emb-0.6b`)

### How to Run

```bash
uv run src/data_analyst_mcp/vanna_mcp_server.py
```

or:

```bash
python -m data_analyst_mcp.vanna_mcp_server
```

The server runs with `streamable-http` transport:

```python
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

#### Docker

Build and run with the provided Dockerfile and compose file:

```bash
docker build -f Dockerfile.vanna_mcp_server -t vanna-mcp-server .
```

```bash
docker compose -f docker-compose.vanna_mcp_server.yml up --build
```

The compose file expects a `.env` file at the project root (copy from
`.env.example`) and exposes port `8000` by default.

#### Claude Code MCP example

```bash
claude mcp add vanna-mcp \
  --transport streamable-http \
  --command uv \
  --args "--directory" \
  "/path/to/your/project" \
  "run" \
  "src/data_analyst_mcp/vanna_mcp_server.py"
```

### Available Tools

#### `vanna_chat_stream`

- **Type**: streaming tool (`AsyncIterator[Dict[str, Any]]`)
- **Parameters**:
  - `message: str` – user input
  - `conversation_id: Optional[str]` – conversation ID for multi-turn chat
  - `agent_id: Optional[str]` – optional agent selection (currently ignored)
  - `acceptable_responses: Optional[List[str]]` – filter event types

Events are produced by `chat_stream_from_handler`, passing through the local Vanna
`ChatHandler`. Each event is a JSON dictionary representing text, SQL, images, tables,
etc.

#### `vanna_chat_once`

Single-call tool that aggregates all stream events into one response using
`aggregate_vanna_events`.

### Response Format

`vanna_chat_once` returns an aggregated JSON object with the following fields:

- `texts: List[str]`
- `images: List[Dict[str, Any]]`
- `links: List[Dict[str, Any]]`
- `buttons: List[Dict[str, Any]]`
- `dataframes: List[Dict[str, Any]]`
- `plotlies: List[Dict[str, Any]]`
- `sqls: List[str]`
- `errors: List[str]`
- `conversation_id: Optional[str]`

### MCP Tool Call Example

```json
{
  "tool": "vanna_chat_once",
  "params": {
    "message": "Show me top 10 customers by revenue",
    "conversation_id": null,
    "agent_id": null,
    "acceptable_responses": ["sql", "chart", "table", "text"]
  }
}
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
