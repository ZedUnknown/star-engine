import os
import json
import torch

class Config:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.gpu_model = torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
        self.gpu_memory = (
            round(torch.cuda.get_device_properties(0).total_memory / (1024 ** 3))
        ) if torch.cuda.is_available() else None