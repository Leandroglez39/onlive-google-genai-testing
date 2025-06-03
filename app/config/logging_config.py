"""
Centralized logging configuration for the OnLive Agent application.
This module ensures logging is configured only once to prevent duplicate log messages.
"""

import logging
from typing import Optional
from livekit.agents.log import logger

# Global flag to track if logging has been configured
_logging_configured = False


def configure_logging(level: int = logging.INFO, format_string: Optional[str] = None) -> None:
    """
    Configure logging for the entire application using the logger from livekit.agents.log.
    This function should only be called once, typically at application startup.
    Args:
        level: The logging level (default: INFO)
        format_string: Custom format string for log messages (ignored, uses livekit logger)
    """
    global _logging_configured
    if _logging_configured:
        return
    # Set the logger level
    logger.setLevel(level)
    # Optionally, set format if needed (but livekit logger may already be configured)
    # Set specific logger levels to reduce noise
    logging.getLogger("httpcore.connection").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger('openai').setLevel(logging.WARNING)
    logging.getLogger('botocore').setLevel(logging.INFO)
    logging.getLogger("aiormq.connection").setLevel(logging.INFO)
    logging.getLogger("aiormq.channel").setLevel(logging.INFO)
    _logging_configured = True


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name, ensuring logging is configured.
    Args:
        name: The name for the logger
    Returns:
        A configured logger instance
    """
    if not _logging_configured:
        configure_logging()
    # Always return the livekit logger for consistency
    return logger


def is_logging_configured() -> bool:
    """Check if logging has been configured."""
    return _logging_configured
