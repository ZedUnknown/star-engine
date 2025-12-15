import os
import json
import wave
from piper import PiperVoice, SynthesisConfig
from .utilities import TTSUtilities
from engine import Logger

current_script_path = os.path.dirname(os.path.realpath(__file__))

log = Logger.get_logger(__name__)


class EngineTTS:
    def __init__(self, models_folder: str):
        # engine directory
        self.engine_directory = os.path.join(current_script_path, '..')

        # tts models info
        self.models_info = TTSUtilities.get_models_info(path=models_folder)

        # outputs
        self.output_tts = os.path.join(self.engine_directory, "outputs", "tts")
        os.makedirs(self.output_tts, exist_ok=True) # ensure output folders exist

    def synthesize(self, voice: str, text: str, sanitize_text: bool = False, config=None, use_cuda: bool = False) -> str:
        if config is None:
            config = {}

        if voice == "__fallback__":
            voice = list(self.models_info.keys())[0]

        if voice not in self.models_info:
            log.warning(f"WARNING: Voice {voice} not found in {list(self.models_info.keys())}. Proceeding with fallback voice.")
            voice = list(self.models_info.keys())[0]

        if text == "":
            log.warning("WARNING: Text is empty.")
            text = "Testing 1 2 3"

        if sanitize_text:
            pass

        log.info(f"Using {'cuda' if use_cuda else 'cpu'}")

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