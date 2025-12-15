# engine/logger.py
import json
import sys
import logging
from pathlib import Path
from typing import TYPE_CHECKING
from loguru import logger

if TYPE_CHECKING:
    from loguru import Record


def stdout_format(record: "Record") -> str:
    base_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    # Add extra data if present
    if record["extra"]:
        try:
            extra_json = json.dumps(record["extra"])
            # Escape curly braces in the JSON to prevent format string issues
            extra_json_escaped = extra_json.replace("{", "{{").replace("}", "}}")
            base_format += f" - {extra_json_escaped}"
        except Exception:
            pass

    base_format += "\n{exception}"

    return base_format


def file_format(record: "Record") -> str:
    """
    Formats log records into a plain text format for file output.

    Parameters:
    record (Record): A Loguru record.

    Returns:
    str: A formatted string for file logging.
    """
    if record["extra"]:
        extra_json = json.dumps(record["extra"])
        extra_format = f" - {extra_json}"
    else:
        extra_format = ""

    return (
        f"{record['time']:YYYY-MM-DD HH:mm:ss.SSS} | "
        f"{record['level'].name: <8} | "
        f"{record['name']}:{record['function']}:{record['line']} - "
        f"{record['message']}"
        f"{extra_format}\n"
    )


class InterceptHandler(logging.Handler):
    """
    Intercepts log records from Python's standard logging module
    and redirects them to Loguru's logger.
    """

    def emit(self, record: logging.LogRecord):
        """
        Called by the standard logging module for each log event.
        """
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


class Logger:
    """Centralized logging for Star Engine using Loguru"""

    _initialized = False

    @classmethod
    def setup(cls, level="DEBUG", log_dir="logs"):
        """
        Initialize logging configuration

        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_dir: Directory for log files
        """
        if cls._initialized:
            return

        # Remove default logger
        logger.remove()

        # Add console handler with colors
        logger.add(
            sys.stdout,
            level=level,
            format=stdout_format,
            colorize=True,
            backtrace=True,
            diagnose=True,
        )

        # Add file handler (plain text, no colors)
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)

        logger.add(
            log_path / "star_engine.log",
            level=level,
            format=file_format,
            rotation="10 MB",  # Rotate when file reaches 10MB
            retention="7 days",  # Keep logs for 7 days
            compression="zip",  # Compress rotated logs
            backtrace=True,
            diagnose=True,
            )

        # Intercept standard logging
        logging.basicConfig(
            handlers=[InterceptHandler()],
            level=logging.getLevelName(level),
            force=True
        )

        cls._initialized = True
        logger.info(f"Star Engine Logger initialized - Level: {level}")

    @classmethod
    def get_logger(cls, name: str = None):
        """
        Get logger instance (Loguru uses a singleton, so this just ensures setup)

        Args:
            name: Module name (for context, but Loguru handles this automatically)

        Returns:
            The Loguru logger instance
        """
        if not cls._initialized:
            cls.setup()

        # Loguru uses a global logger, so we just return it
        # The 'name' will be captured automatically by Loguru from the calling module
        return logger


# Convenience functions
def get_logger(name: str = None):
    """Get a logger instance"""
    return Logger.get_logger(name)


# Example usage functions
def log_with_extra(level: str, message: str, **extra):
    """
    Log with extra context data
    
    Example:
        log_with_extra("INFO", "Processing file", filename="test.wav", size=1024)
    """
    Logger.get_logger().bind(**extra).log(level, message)


def log_exception(message: str, **extra):
    """
    Log an exception with traceback
    
    Example:
        try:
            # some code
        except Exception:
            log_exception("Failed to process")
    """
    Logger.get_logger().bind(**extra).exception(message)