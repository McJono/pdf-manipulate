#!/usr/bin/env python3
"""
PDF Manipulate - Main Entry Point

An intelligent PDF manipulation program that automates document processing
with features for auto-rotation, merging, and smart file naming.
"""

import sys
from pathlib import Path

# Add parent directory to path to enable imports
sys.path.insert(0, str(Path(__file__).parent))

from src.ui.main_window import create_main_window
from src.config.manager import config
from src.utils.logger import setup_logger


def main():
    """Main entry point for the application"""
    # Setup logging
    log_config = config.get("logging", {})
    logger = setup_logger(
        name="pdf-manipulate",
        log_file=log_config.get("log_file") if log_config.get("enabled") else None,
        level=log_config.get("level", "INFO"),
        max_size_mb=log_config.get("max_log_size_mb", 10),
    )

    logger.info("=" * 60)
    logger.info("PDF Manipulate v0.1.0")
    logger.info("=" * 60)

    try:
        # Create and run main window
        window = create_main_window()
        window.run()
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        sys.exit(1)

    logger.info("Application closed")


if __name__ == "__main__":
    main()
