import os
import sys
import json

from engine import Logger
log = Logger.get_logger(__name__)

os.system('cls' if os.name == 'nt' else 'clear')
current_script_path = os.path.dirname(os.path.realpath(__file__))

from tts_engine import EngineTTS
# from rvc_engine.main import EngineRVC

class Core:
    def __init__(self):
        self.tts_engine = EngineTTS()
        # self.rvc_engine = EngineRVC()

        self.rvc_tts_voice_map = json.load(open(os.path.join(current_script_path, 'rvc_tts_voice_map.json'), 'r'))


    def synthesize(self, rvc_voice, text) -> bin:
        if rvc_voice not in self.rvc_tts_voice_map:
            log.warning(f"WARNING: Voice '{rvc_voice}' not found in `rvc_tts_voice_map`. Proceeding with fallback voice.")

        tts_model = list(self.rvc_tts_voice_map[rvc_voice]['tts_model'].keys())[0]
        tts_model_config = self.rvc_tts_voice_map[rvc_voice]['tts_model'][tts_model]

        tts_result = self.tts_engine.synthesize(
            voice=tts_model,
            text=text,
            config=tts_model_config,
            use_cuda=False
        )

        log.info(f"TTS ID: {tts_result}")

if __name__ == '__main__':
    core = Core()
    core.synthesize('k', 'testing 1 2 3')
