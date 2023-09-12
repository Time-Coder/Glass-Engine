from .ShaderEffect import ShaderEffect
import os

class ACESToneMapper(ShaderEffect):

    def __init__(self):
        self_folder = os.path.dirname(os.path.abspath(__file__))
        ShaderEffect.__init__(self, self_folder + "/../glsl/PostProcessEffects/ACES_tone_mapper.glsl")
