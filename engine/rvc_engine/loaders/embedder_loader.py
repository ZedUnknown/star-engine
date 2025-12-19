import os
import torch
from engine import Logger

current_script_path = os.path.dirname(os.path.realpath(__file__))

log = Logger.get_logger(__name__)

class EmbedderLoader:
    def __init__(self):
        pass