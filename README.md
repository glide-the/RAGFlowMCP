[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/shemhamforash23-lightrag-mcp-badge.png)](https://mseep.ai/app/shemhamforash23-lightrag-mcp)

# Ragflow Retrieval MCP Server

MCP server for integrating Ragflow retrieval with AI tools. Provides a unified interface for interacting with the Ragflow `/api/v1/retrieval` endpoint through the MCP protocol.

## Description

Ragflow MCP Server is a bridge between Ragflow retrieval API and MCP-compatible clients. It focuses on exposing a single retrieval tool that mirrors Ragflow's `/api/v1/retrieval` capabilities.

### Key Features

- **Information Retrieval**: Execute semantic, keyword, and hybrid retrieval against Ragflow datasets/documents

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

## Usage

**Important**: Ragflow MCP server should only be run as an MCP server through an MCP client configuration file (mcp-config.json).

### Command Line Options

The following arguments are available when configuring the server in mcp-config.json (can also be provided via environment variables `RAGFLOW_API_BASE` and `RAGFLOW_API_KEY`):

- `--host`: Ragflow API host (default: localhost)
- `--port`: Ragflow API port (default: 9621)
- `--api-key`: Ragflow API key (optional)
- `--base-url`: Full Ragflow API base URL (overrides host/port)

### Integration with Ragflow API

The MCP server requires a running Ragflow API server. Start it as follows:

```bash
# Create virtual environment
uv venv --python 3.11

# Install dependencies for Ragflow API
uv pip install -r requirements.txt

# Start Ragflow API (example command)
uv run ragflow_api.py --host localhost --port 9621 --working-dir ./rag_storage --input-dir ./input --log-level DEBUG
```

### Setting up as MCP server

To set up Ragflow MCP as an MCP server, add the following configuration to your MCP client configuration file (e.g., `mcp-config.json`):

#### Using uvenv (uvx):

```json
{
  "mcpServers": {
    "ragflow-mcp": {
      "command": "uvx",
      "args": [
        "lightrag_mcp",
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
        "/path/to/lightrag_mcp",
        "run",
        "src/lightrag_mcp/main.py",
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

Replace `/path/to/lightrag_mcp` with the actual path to your lightrag-mcp directory.

## Available MCP Tools

- `ragflow_retrieval`: Execute Ragflow `/api/v1/retrieval` against specified dataset or document IDs

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
