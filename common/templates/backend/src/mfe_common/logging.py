"""JSON structured logging configuration."""

import logging
import sys

from pythonjsonlogger.json import JsonFormatter


def setup_logging(log_level: str = "INFO", app_name: str = "mfe-app") -> logging.Logger:
    """Configure JSON structured logging to console.

    Args:
        log_level: Log level string (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        app_name: Application name included in log records.

    Returns:
        Configured root logger.
    """
    logger = logging.getLogger(app_name)
    logger.setLevel(log_level.upper())

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = JsonFormatter(
            fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
            rename_fields={"asctime": "timestamp", "levelname": "level"},
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
