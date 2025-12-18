import os
import sys
import torch
import librosa
import soundfile as sf
import numpy as np
from engine import Logger

current_script_path = os.path.dirname(os.path.realpath(__file__))

from engine.rvc_engine import Config

log = Logger.get_logger(__name__)

class RVCInference:
    """

    """
    def __init__(self):
        self.config = Config()


    def load_embedding(self, embedding_path):
        """
        Loads the embedding model for speaker embedding extraction. (default: HuBERT model)
        """
        pass


