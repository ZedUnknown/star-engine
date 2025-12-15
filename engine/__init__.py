from .logger import Logger
from .utilities import CoreUtilities

Logger.setup(level="DEBUG", log_dir="logs")

__all__ = ["Logger", "CoreUtilities"]