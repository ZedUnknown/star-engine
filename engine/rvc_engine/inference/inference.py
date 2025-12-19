import os
import sys
import torch
import librosa
import soundfile as sf
import numpy as np
from engine import Logger

current_script_path = os.path.dirname(os.path.realpath(__file__))

from engine.rvc_engine import Config
from engine import root

log = Logger.get_logger(__name__)

class RVCInference:
    """

    """
    def __init__(self):
        self.config = Config()

    @staticmethod
    def load_embedding(self, embedding_model):
        """
        Loads the embedding model for speaker embedding extraction. (default: HuBERT model)
        """

        print(root)

