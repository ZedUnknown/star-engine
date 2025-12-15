import os
import json
from engine import Logger

os.system('cls' if os.name == 'nt' else 'clear')
current_script_path = os.path.dirname(os.path.realpath(__file__))

log = Logger.get_logger(__name__)

class CoreUtilities:

    @staticmethod
    def get_json(path) -> dict:
        """
        safe JSON loading
        """
        try:
            with open(path, 'r') as f:
                content = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            log.error(f"Failed to load JSON file: {os.path.basename(path)} - {str(e)}")
            content = {}
        return content