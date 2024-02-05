from .ShaderEffect import ShaderEffect
import os


class MedianBlur(ShaderEffect):

    def __init__(self):
        self_folder = os.path.dirname(os.path.abspath(__file__))
        ShaderEffect.__init__(
            self, self_folder + "/../glsl/PostProcessEffects/median_gray_blur5.glsl"
        )
