from .logger import Logger

Logger.setup(level="DEBUG", log_dir="logs")

__all__ = ["Logger"]