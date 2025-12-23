"""
Entry point for Vanna MCP server with Ragflow compatibility.
"""

import logging
import sys

from mcp import config
from mcp.server import mcp

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

        logger.info("Starting Vanna MCP server (with Ragflow retrieval)")
        logger.info(
            f"Ragflow API server is expected to be already running and available at: {config.RAGFLOW_API_BASE_URL}"
        )
        logger.info(
            f"Vanna API server is expected to be already running and available at: {config.VANNA_API_BASE_URL}"
        )
        if config.RAGFLOW_API_KEY:
            logger.info("Ragflow API key is configured")
        else:
            logger.warning("No Ragflow API key provided")

        if config.VANNA_API_KEY:
            logger.info("Vanna API key is configured")
        else:
            logger.warning("No Vanna API key provided")

        mcp.run(transport="stdio")

    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.exception(f"Error starting server: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
