from .SingleShaderFilter import SingleShaderFilter
from glass import sampler2D

from OpenGL import GL

class HDRFilter(SingleShaderFilter):

    def __init__(self):
        SingleShaderFilter.__init__(self, "../glsl/Filters/hdr_filter.glsl")

    def __call__(self, screen_image:sampler2D)->sampler2D:
        screen_image.filter_mipmap = GL.GL_LINEAR
        return SingleShaderFilter.__call__(self, screen_image)
    
    def draw_to_active(self, screen_image: sampler2D) -> None:
        screen_image.filter_mipmap = GL.GL_LINEAR
        SingleShaderFilter.draw_to_active(self, screen_image)