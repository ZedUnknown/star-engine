import os
import sys
import json
from piper import PiperVoice, SynthesisConfig
import wave
from .utilities import TTSUtilities

from engine import Logger
log = Logger.get_logger(__name__)

os.system('cls' if os.name == 'nt' else 'clear')
current_script_path = os.path.dirname(os.path.realpath(__file__))

class EngineTTS:
    def __init__(self):
        # engine directory
        self.engine_directory = os.path.join(current_script_path, '..')

        # tts models info
        self.models_info = TTSUtilities.get_models_info()

        # outputs
        self.output_tts = os.path.join(self.engine_directory, "outputs", "tts")
        os.makedirs(self.output_tts, exist_ok=True) # ensure output folders exist

    def synthesize(self, voice: str, text: str, sanitize_text: bool = False, config=None, use_cuda: bool = False) -> str:
        if config is None:
            config = {}
        if voice not in self.models_info:
            log.error(f"ERROR: Voice {voice} not found in {list(self.models_info.keys())}. Please check the voice name.")
            return ""

        if text == "":
            log.error("ERROR: Text is empty. Please provide some text.")
            return ""

        if sanitize_text:
            pass

        log.info("Using 'cuda'") if use_cuda else log.info("Using 'cpu'")

        voice = PiperVoice.load(self.models_info[voice]["onnx"], use_cuda=use_cuda)
        config = TTSUtilities.validate_config(config)

        log.debug(f"\nConfig:{json.dumps(config, indent=4).replace('{', '').replace('}', '')}")

        syn_config = SynthesisConfig(
            volume=config.get('volume'),
            length_scale=config.get('length_scale'),
            noise_scale=config.get('noise_scale'),
            noise_w_scale=config.get('noise_w_scale'),
            normalize_audio=config.get('normalize_audio')
        )

        # output path
        file_id = TTSUtilities.get_uuid()
        save_path = os.path.join(self.output_tts, f"{file_id}.wav")

        # synthesize
        with wave.open(save_path, "wb") as wav_file:
            voice.synthesize_wav(text, wav_file, syn_config=syn_config)

        return file_id