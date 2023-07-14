from .Filters import Filter
from glass import ShaderProgram, FBO, sampler2D, GLInfo
from ..Frame import Frame

class FXAAFilter(Filter):

    program = ShaderProgram()
    program.compile("../glsl/Pipelines/draw_frame.vs")
    program.compile("../glsl/Filters/FXAA_filter.fs")

    def __init__(self, internal_format:GLInfo.internal_formats=None):
        self.fbo = FBO()
        self.fbo.attach(0, sampler2D, internal_format)

    def __call__(self, screen_image:sampler2D):
        self.fbo.resize(screen_image.width, screen_image.height)
        with self.fbo:
            FXAAFilter.program["screen_image"] = screen_image
            FXAAFilter.program.draw_triangles(Frame.vertices, Frame.indices)
            
        return self.fbo.color_attachment(0)