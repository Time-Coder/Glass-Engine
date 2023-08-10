from .Filters import Filter
from glass import ShaderProgram, FBO, sampler2D, GLInfo
from ..Frame import Frame
import os

def init_MedianFilter(cls):
    cls.program = ShaderProgram()
    cls.program.compile(Frame.draw_frame_vs)
    cls.program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/Filters/median_filter.fs")

    return cls

@init_MedianFilter
class MedianFilter(Filter):

    def __init__(self, internal_format:GLInfo.internal_formats=None):
        Filter.__init__(self)
        
        self.fbo = FBO()
        self.fbo.attach(0, sampler2D, internal_format)

    def __call__(self, screen_image:sampler2D)->sampler2D:
        self.fbo.resize(screen_image.width, screen_image.height)
        with self.fbo:
            MedianFilter.program["screen_image"] = screen_image
            MedianFilter.program.draw_triangles(Frame.vertices, Frame.indices)
            
        return self.fbo.color_attachment(0)
    
    def draw_to_active(self, screen_image: sampler2D) -> None:
        MedianFilter.program["screen_image"] = screen_image
        MedianFilter.program.draw_triangles(Frame.vertices, Frame.indices)
