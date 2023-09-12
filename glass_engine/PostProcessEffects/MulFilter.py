from .ShaderEffect import ShaderEffect
import os

class MulFilter(ShaderEffect):

    def __init__(self):
        self_folder = os.path.dirname(os.path.abspath(__file__))
        ShaderEffect.__init__(self, self_folder + "/../glsl/PostProcessEffects/mul_filter.glsl")
