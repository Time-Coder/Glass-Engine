from .ShaderEffect import ShaderEffect
from .. import lut
from glass import sampler2D
from glass.utils import extname

import numpy as np
import os
from OpenGL import GL


class LUTEffect(ShaderEffect):

    def __init__(self, LUT: (str, np.ndarray, sampler2D), contribute: float = 1.0):
        self_folder = os.path.dirname(os.path.abspath(__file__))
        ShaderEffect.__init__(
            self, self_folder + "/../glsl/PostProcessEffects/lut.glsl"
        )

        if isinstance(LUT, str) and extname(LUT) == "cube":
            LUT = lut.cube_to_LUT(LUT)

        if not isinstance(LUT, sampler2D):
            LUT = sampler2D(LUT)

        LUT.wrap = GL.GL_CLAMP_TO_EDGE
        self["LUT"] = LUT
        self["contribute"] = contribute
        self.__LUT = LUT
        self.__contribute = contribute

    @property
    def LUT(self):
        return self.__LUT

    @LUT.setter
    def LUT(self, LUT: (str, np.ndarray, sampler2D)):
        if isinstance(LUT, str) and extname(LUT) == "cube":
            LUT = lut.cube_to_LUT(LUT)

        if not isinstance(LUT, sampler2D):
            LUT = sampler2D(LUT)

        LUT.wrap = GL.GL_CLAMP_TO_EDGE
        self.__LUT = LUT
        self["LUT"] = LUT

    @property
    def contribute(self):
        return self.__contribute

    @contribute.setter
    def contribute(self, contribute: float):
        self.__contribute = contribute
        self["contribute"] = contribute
