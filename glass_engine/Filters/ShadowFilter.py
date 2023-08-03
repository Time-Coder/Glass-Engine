from .Filters import Filter
from ..Frame import Frame

from glass import FBO, ShaderProgram, sampler2D, GLConfig
from glass.utils import checktype

from OpenGL import GL
import glm

def _init_ShadowFilter(cls):
    cls.program = ShaderProgram()
    cls.program.compile(Frame.draw_frame_vs)
    cls.program.compile("../glsl/Filters/shadow_filter.fs")
    return cls

@_init_ShadowFilter
class ShadowFilter(Filter):

    @checktype
    def __init__(self):
        Filter.__init__(self)

        self.horizontal_fbo = FBO()
        self.horizontal_fbo.attach(0, sampler2D, GL.GL_RG32F)

        self.vertical_fbo = FBO()
        self.vertical_fbo.attach(0, sampler2D, GL.GL_RG32F)

    def __call__(self, screen_image:sampler2D)->sampler2D:
        self.horizontal_fbo.resize(screen_image.width, screen_image.height)
        self.vertical_fbo.resize(screen_image.width, screen_image.height)

        with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):

            with self.horizontal_fbo:
                ShadowFilter.program["screen_image"] = screen_image
                ShadowFilter.program["horizontal"] = True
                ShadowFilter.program.draw_triangles(Frame.vertices, Frame.indices)

            with self.vertical_fbo:
                ShadowFilter.program["screen_image"] = self.horizontal_fbo.color_attachment(0)
                ShadowFilter.program["horizontal"] = False
                ShadowFilter.program.draw_triangles(Frame.vertices, Frame.indices)

        return self.vertical_fbo.color_attachment(0)
    
    def draw_to_active(self, screen_image: sampler2D) -> None:
        self.horizontal_fbo.resize(screen_image.width, screen_image.height)
        self.vertical_fbo.resize(screen_image.width, screen_image.height)

        with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):

            with self.horizontal_fbo:
                ShadowFilter.program["screen_image"] = screen_image
                ShadowFilter.program["horizontal"] = True
                ShadowFilter.program.draw_triangles(Frame.vertices, Frame.indices)

            GLConfig.clear_buffers()
            ShadowFilter.program["screen_image"] = self.horizontal_fbo.color_attachment(0)
            ShadowFilter.program["horizontal"] = False
            ShadowFilter.program.draw_triangles(Frame.vertices, Frame.indices)
