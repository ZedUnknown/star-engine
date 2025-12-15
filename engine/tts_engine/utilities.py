import os
import uuid
from engine import Logger

os.system('cls' if os.name == 'nt' else 'clear')
current_script_path = os.path.dirname(os.path.realpath(__file__))

log = Logger.get_logger(__name__)

class TTSUtilities:

    @staticmethod
    def get_jsons(path, extension=False) ->  list:
        models = [
            os.path.basename(os.path.join(directory, filename))
            for directory, _, filenames in os.walk(path)
            for filename in filenames
            if filename.endswith('.json')
        ]
        if not extension:
            models = [model.replace('.onnx.json', '') for model in models]
        return models if models else []

    @staticmethod
    def match_json(model_file: str, json_files: list) -> str:
        # check constructed JSON file
        json_file_path = model_file + ".json"
        if os.path.basename(json_file_path) in json_files:
            if os.path.exists(json_file_path):
                return json_file_path

        return ""

    @staticmethod
    def get_models_info(path) -> dict:
        if not os.path.exists(path):
            log.warning(f"WARNING: Model directory not found: {path}")
            path = os.path.join(current_script_path, 'models')
            log.warning(f"Using default model directory: {path}")

        models_info = {}
        if os.path.exists(os.path.join(current_script_path, path)):
            log.info(f"Model directory found: {path}")
            json_files = TTSUtilities.get_jsons(path=path, extension=True)
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith('.onnx'):
                        model_file = os.path.join(root, file) # onnx
                        model_name = os.path.basename(model_file).replace('.onnx', '')
                        json_file = TTSUtilities.match_json(str(model_file), json_files)

                        log.debug(f"model: {model_name}")

                        models_info[model_name] = {
                            "onnx": model_file,
                            "json": json_file
                        }
        else:
            log.error(f"ERROR: Default model directory does not exist. Please check the path: {path}")

        return models_info

    @staticmethod
    def validate_config(config: dict) -> dict:
        default_config = {
            "volume": 1.0, # half as loud
            "length_scale": 1.5, # slow scale (higher the value slower the voice)
            "noise_scale": 0.667, # more audio variation
            "noise_w_scale": 0.8, # more speaking variation
            "normalize_audio": False, # use raw audio from voice
        }

        if config is None:
            return default_config

        validated_config = {}
        for key in config:
            if key in default_config:
                validated_config[key] = config[key]
            else:
                log.warning(f"WARNING: Unknown configuration key '{key}' ignored.")

        # default values for missing keys
        for key, value in default_config.items():
            if key not in validated_config:
                validated_config[key] = value

        return validated_config

    @staticmethod
    def get_uuid():
        """Generate a unique UUID string."""
        return uuid.uuid4().hex