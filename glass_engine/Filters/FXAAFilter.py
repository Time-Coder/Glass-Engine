from .Filters import Filter
from glass import ShaderProgram, FBO, sampler2D, GLInfo, samplerCube, sampler2DArray
from ..Frame import Frame

import os

def init_FXAAFilter(cls):
    cls.program = ShaderProgram()
    cls.program.compile(Frame.draw_frame_vs)
    cls.program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/Filters/FXAA_filter.fs")

    cls.cube_program = ShaderProgram()
    cls.cube_program.compile(Frame.draw_frame_vs)
    cls.cube_program.compile(Frame.draw_frame_array_gs(6))
    cls.cube_program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/Filters/FXAA_cube_filter.fs")

    return cls

@init_FXAAFilter
class FXAAFilter(Filter):

    __array_programs = {}

    def __init__(self, internal_format:GLInfo.internal_formats=None):
        Filter.__init__(self)
        
        self.fbo = FBO()
        self.fbo.attach(0, sampler2D, internal_format)

        self.array_fbo = FBO()
        self.array_fbo.attach(0, sampler2DArray, internal_format)

        self.cube_fbo = FBO()
        self.cube_fbo.attach(0, samplerCube, internal_format)

    def __call__(self, screen_image:(sampler2D,samplerCube,sampler2DArray))->(sampler2D,samplerCube,sampler2DArray):
        if isinstance(screen_image, sampler2D):
            self.fbo.resize(screen_image.width, screen_image.height)
            with self.fbo:
                FXAAFilter.program["screen_image"] = screen_image
                FXAAFilter.program.draw_triangles(Frame.vertices, Frame.indices)
                
            return self.fbo.color_attachment(0)
        elif isinstance(screen_image, samplerCube):
            self.cube_fbo.resize(screen_image.width, screen_image.height)
            with self.cube_fbo:
                FXAAFilter.cube_program["screen_image"] = screen_image
                FXAAFilter.cube_program.draw_triangles(Frame.vertices, Frame.indices)

            return self.cube_fbo.color_attachment(0)
        elif isinstance(screen_image, sampler2DArray):
            self.array_fbo.resize(screen_image.width, screen_image.height, layers=screen_image.layers)
            with self.array_fbo:
                program = FXAAFilter.array_program(screen_image.layers)
                program["screen_image"] = screen_image
                program.draw_triangles(Frame.vertices, Frame.indices)

            return self.array_fbo.color_attachment(0)
    
    def draw_to_active(self, screen_image: sampler2D) -> None:
        FXAAFilter.program["screen_image"] = screen_image
        FXAAFilter.program.draw_triangles(Frame.vertices, Frame.indices)
    
    @staticmethod
    def array_program(layers):
        if layers in FXAAFilter.__array_programs:
            return FXAAFilter.__array_programs[layers]

        program = ShaderProgram()
        program.compile(Frame.draw_frame_vs)
        program.compile(Frame.draw_frame_array_gs(layers))
        program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/Filters/FXAA_array_filter.fs")

        FXAAFilter.__array_programs[layers] = program

        return program