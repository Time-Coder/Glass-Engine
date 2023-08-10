from .Filters import Filter
from ..Frame import Frame
from glass.utils import checktype
from glass import ShaderProgram, FBO, sampler2D, GLConfig

from OpenGL import GL
import os
import glm

class BackgroundFilter(Filter):

    @checktype
    def __init__(self, background_color:(glm.vec4,glm.vec3)=glm.vec4(0,0,0,0)):
        Filter.__init__(self)
        self._background_color = background_color

        self.program = ShaderProgram()
        self.program.compile(Frame.draw_frame_vs)
        self.program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/Filters/background_filter.fs")

        self.fbo = FBO()
        self.fbo.attach(0, sampler2D)

    def __call__(self, screen_image:sampler2D)->sampler2D:
        self.fbo.resize(screen_image.width, screen_image.height)
        with GLConfig.LocalConfig(depth_test=False, cull_face=None, polygon_mode=GL.GL_FILL):
            with self.fbo:
                self.program["screen_image"] = screen_image
                self.program["background_color"] = self._background_color
                self.program.draw_triangles(Frame.vertices, Frame.indices)

        return self.fbo.color_attachment(0)
        
    def draw_to_active(self, screen_image: sampler2D) -> None:
        with GLConfig.LocalConfig(depth_test=False, cull_face=None, polygon_mode=GL.GL_FILL):
            self.program["screen_image"] = screen_image
            self.program["background_color"] = self._background_color
            self.program.draw_triangles(Frame.vertices, Frame.indices)

    @property
    def background_color(self):
        return self._background_color
    
    @background_color.setter
    @checktype
    def background_color(self, color:(glm.vec3, glm.vec4)):
        if isinstance(color, glm.vec3):
            color = glm.vec4(color, 1)

        self._background_color = color
        self.program["background_color"] = self._background_color
