import os
import json

from engine import Logger, CoreUtilities
from tts_engine import EngineTTS
from rvc_engine import EngineRVC

from dotenv import load_dotenv

current_script_path = os.path.dirname(os.path.realpath(__file__))

log = Logger.get_logger(__name__)

# extract env variables
load_dotenv()
TTS_MODEL_PATH = os.getenv("TTS_MODEL_PATH")
RVC_MODEL_PATH = os.getenv("RVC_MODEL_PATH")

class Core:
    def __init__(self):
        self.tts_models_path = TTS_MODEL_PATH if TTS_MODEL_PATH else ''
        self.rvc_models_path = RVC_MODEL_PATH if RVC_MODEL_PATH else ''

        self.tts_engine = EngineTTS(self.tts_models_path)
        self.rvc_engine = EngineRVC(self.rvc_models_path)

        self.rvc_tts_voice_map = CoreUtilities.get_json(os.path.join(current_script_path, 'rvc_tts_voice_map.json'))

    def get_tts(self, rvc_voice, text: str = "") -> str:
        if rvc_voice in self.rvc_tts_voice_map:
            tts_model = list(self.rvc_tts_voice_map[rvc_voice]['tts_model'].keys())[0]
            tts_model_config = self.rvc_tts_voice_map[rvc_voice]['tts_model'][tts_model]

            tts_result = self.tts_engine.synthesize(
                voice=tts_model,
                text=text,
                config=tts_model_config,
                use_cuda=False
            )

        else:
            log.warning(f"WARNING: Voice '{rvc_voice}' not found in `rvc_tts_voice_map`. Proceeding with fallback voice.")
            tts_result = self.tts_engine.synthesize(
                voice='__fallback__',
                text=text,
                config={},
                use_cuda=False
            )

        log.info(f"tts id: {tts_result}")
        return tts_result

    # def get_rvc(self, rvc_voice, audio) -> str:


if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    core = Core()
    core.get_tts('k')
