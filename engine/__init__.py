import os

from .logger import Logger
from .utilities import CoreUtilities

root = os.path.dirname(os.path.realpath(__file__))

Logger.setup(level="DEBUG", log_dir="logs")

__all__ = ["Logger", "CoreUtilities", "root"]