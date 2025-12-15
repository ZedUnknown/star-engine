import os
import re
from engine import Logger

os.system('cls' if os.name == 'nt' else 'clear')
current_script_path = os.path.dirname(os.path.realpath(__file__))

log = Logger.get_logger(__name__)

class RVCUtilities:

    @staticmethod
    def get_indexes(models_folder: str) -> list:
        """
        get all indexes (.index) correspond to model.pth name

        return:
            list: list of index file names
        """
        indexes_list = [
            os.path.join(dirpath, filename)
            for dirpath, _, filenames in os.walk(models_folder)
            for filename in filenames
            if filename.endswith(".index") and "trained" not in filename
        ]
        return indexes_list if indexes_list else []

    @staticmethod
    def match_index(model_file_value: str, index_files: list):
        """
        match index file name (xxx.index) to model file name (xxx.pth)
        from the list of index files

        args:
            model_file_value (str): model file name
            indexes (list): list of index file names

        return:
            str: index file name
        """
        if model_file_value:
            model_folder = os.path.dirname(model_file_value)
            model_name = os.path.basename(model_file_value)
            pattern = r"^(.*?)_"
            match = re.match(pattern, model_name)
            for index_file in index_files:
                if os.path.dirname(index_file) == model_folder:
                    return index_file
                elif match and match.group(1) in os.path.basename(index_file):
                    return index_file
                elif model_name in os.path.basename(index_file):
                    return index_file
        return ""

    @staticmethod
    def get_models_info(path):
        """
        get all trained .pth and .onnx models

        args:
            models_folder (str): path to models folder

        return:
            dict: models info
            {
                model_name : {
                    'pth' : model.pth path,
                    'index' : model.index path
                }
            }
        """

        if not os.path.exists(path):
            log.warning(f"WARNING: Model directory not found: {path}")
            path = os.path.join(current_script_path, 'models')
            log.warning(f"Using default model directory: {path}")

        models_info = {}
        if os.path.exists(path):
            log.info(f"Model directory found: {path}")
            index_files = RVCUtilities.get_indexes(path)
            for root, _, files in os.walk(path, topdown=False):
                for file in files:
                    if file.endswith((".pth", ".onnx")) and not (file.startswith("G_") or file.startswith("D_")):
                        model_file = os.path.join(root, file)
                        model_name = os.path.basename(model_file).split('.')[0].lower()
                        index_file = RVCUtilities.match_index(str(model_file), index_files)

                        log.debug(f"model: {model_name}")

                        models_info[model_name] = {
                            'pth': model_file,
                            'index': index_file
                        }
        else:
            log.error("ERROR: Default model directory does not exist. Please check the path:", path)

        return models_info