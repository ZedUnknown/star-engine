import os
from .utilities import RVCUtilities

from engine import Logger
log = Logger.get_logger(__name__)

os.system('cls' if os.name == 'nt' else 'clear')
current_script_path = os.path.dirname(os.path.realpath(__file__))


class EngineRVC:
    def __init__(self, models_folder: str):
        # engine directory
        self.engine_directory = os.path.join(current_script_path, '..')

        # rvc models info
        self.models_info = RVCUtilities.get_models_info(path=models_folder)

        # outputs
        self.output_rvc = os.path.join(self.engine_directory, "outputs", "rvc")
        os.makedirs(self.output_rvc, exist_ok=True) # ensure output folders exist