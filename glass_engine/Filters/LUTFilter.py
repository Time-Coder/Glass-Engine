from .SingleShaderFilter import SingleShaderFilter
from glass import sampler2D

import numpy as np
import os
import glm
from OpenGL import GL

class LUTFilter(SingleShaderFilter):

    def __init__(self, LUT_image, block_shape:glm.ivec2=glm.ivec2(64, 64)):
        self_folder = os.path.dirname(os.path.abspath(__file__))
        SingleShaderFilter.__init__(self, self_folder + "/../glsl/Filters/lut_filter.glsl")

        if not isinstance(block_shape, glm.ivec2):
            block_shape = glm.ivec2(block_shape)

        if not isinstance(LUT_image, sampler2D):
            LUT_image = sampler2D(LUT_image)

        LUT_image.wrap = GL.GL_CLAMP_TO_EDGE

        self["block_shape"] = block_shape
        self["LUT_image"] = LUT_image
        self.__block_size = block_shape
        self.__LUT_image = LUT_image

    @property
    def block_shape(self):
        return self.__block_size
    
    @block_shape.setter
    def block_shape(self, block_shape:glm.ivec2):
        self.__block_size = block_shape
        self["block_shape"] = block_shape

    @property
    def LUT_image(self):
        return self.__LUT_image
    
    @LUT_image.setter
    def LUT_image(self, LUT_image):
        if not isinstance(LUT_image, sampler2D):
            LUT_image = sampler2D(LUT_image)
            
        LUT_image.wrap = GL.GL_CLAMP_TO_EDGE

        self.__LUT_image = LUT_image
        self["LUT_image"] = LUT_image

    