# main class
from .engine import EngineTTS

# utilities class
from .utilities import TTSUtilities

# classes which get imported with "from tts_engine import *"
__all__ = ['EngineTTS', 'TTSUtilities']