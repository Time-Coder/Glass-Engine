from .Filters import Filter
from ..Frame import Frame
from glass import FBO, sampler2D
from glass.utils import checktype

import glm
from OpenGL import GL

class ResizeFilter(Filter):

    def __init__(self, dest_shape:(tuple,glm.vec2)):
        Filter.__init__(self)

        self.fbo = FBO(dest_shape[0], dest_shape[1])
        self.fbo.attach(0, sampler2D, GL.GL_RGBA32F)

    def __call__(self, screen_image:sampler2D)->sampler2D:
        with self.fbo:
            Frame.draw(screen_image)

        return self.fbo.color_attachment(0)

    @property
    def dest_shape(self):
        return (self.fbo.width, self.fbo.height)
    
    @dest_shape.setter
    @checktype
    def dest_shape(self, shape:(tuple,glm.vec2)):
        self.fbo.resize(shape[0], shape[1])