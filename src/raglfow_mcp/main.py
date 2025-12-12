"""
Entry point for Ragflow MCP server.
"""

import logging
import sys

from raglfow_mcp import config
from raglfow_mcp.server import mcp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def main():
    """Main function for server startup."""
    try:
        log_level = getattr(logging, "INFO")
        logging.getLogger().setLevel(log_level)

        logger.info("Starting Ragflow MCP server")
        logger.info(
            f"Ragflow API server is expected to be already running and available at: {config.RAGFLOW_API_BASE_URL}"
        )
        if config.RAGFLOW_API_KEY:
            logger.info("API key is configured")
        else:
            logger.warning("No API key provided")

        mcp.run(transport="stdio")

    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.exception(f"Error starting server: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
