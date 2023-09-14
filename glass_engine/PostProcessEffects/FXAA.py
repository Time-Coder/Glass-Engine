from .PostProcessEffect import PostProcessEffect
from glass import ShaderProgram, FBO, sampler2D, GLInfo, samplerCube, sampler2DArray
from ..Frame import Frame

import os

class FXAA(PostProcessEffect):

    __array_programs = {}
    __program = None
    __cube_program = None

    @staticmethod
    def program():
        if FXAA.__program is None:
            FXAA.__program = ShaderProgram()
            FXAA.__program.compile(Frame.draw_frame_vs)
            FXAA.__program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/PostProcessEffects/FXAA.fs")
        return FXAA.__program
    
    @staticmethod
    def cube_program():
        if FXAA.__cube_program is None:
            FXAA.__cube_program = ShaderProgram()
            FXAA.__cube_program.compile(Frame.draw_frame_vs)
            FXAA.__cube_program.compile(Frame.draw_frame_array_gs(6))
            FXAA.__cube_program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/PostProcessEffects/FXAA_cube_filter.fs")
        return FXAA.__cube_program
    
    def __init__(self, internal_format:GLInfo.internal_formats=None):
        PostProcessEffect.__init__(self)
        
        self._internal_format = internal_format
        self._fbo = None
        self._array_fbo = None
        self._cube_fbo = None

    @property
    def fbo(self):
        if self._fbo is None:
            self._fbo = FBO()
            self._fbo.attach(0, sampler2D, self._internal_format)
        return self._fbo

    @property
    def array_fbo(self):
        if self._array_fbo is None:
            self._array_fbo = FBO()
            self._array_fbo.attach(0, sampler2DArray, self._internal_format)
        return self._array_fbo

    @property
    def cube_fbo(self):
        if self._cube_fbo is None:
            self._cube_fbo = FBO()
            self._cube_fbo.attach(0, samplerCube, self._internal_format)
        return self._cube_fbo

    def need_pos_info(self) -> bool:
        return False

    def apply(self, screen_image:(sampler2D,samplerCube,sampler2DArray))->(sampler2D,samplerCube,sampler2DArray):
        if isinstance(screen_image, sampler2D):
            self.fbo.resize(screen_image.width, screen_image.height)
            with self.fbo:
                FXAA.program()["screen_image"] = screen_image
                FXAA.program().draw_triangles(Frame.vertices, Frame.indices)
                
            return self.fbo.color_attachment(0)
        elif isinstance(screen_image, samplerCube):
            self.cube_fbo.resize(screen_image.width, screen_image.height)
            with self.cube_fbo:
                FXAA.cube_program()["screen_image"] = screen_image
                FXAA.cube_program().draw_triangles(Frame.vertices, Frame.indices)

            return self.cube_fbo.color_attachment(0)
        elif isinstance(screen_image, sampler2DArray):
            self.array_fbo.resize(screen_image.width, screen_image.height, layers=screen_image.layers)
            with self.array_fbo:
                program = FXAA.array_program(screen_image.layers)
                program["screen_image"] = screen_image
                program.draw_triangles(Frame.vertices, Frame.indices)

            return self.array_fbo.color_attachment(0)
    
    def draw_to_active(self, screen_image: sampler2D) -> None:
        FXAA.program()["screen_image"] = screen_image
        FXAA.program().draw_triangles(Frame.vertices, Frame.indices)
    
    @staticmethod
    def array_program(layers):
        if layers in FXAA.__array_programs:
            return FXAA.__array_programs[layers]

        program = ShaderProgram()
        program.compile(Frame.draw_frame_vs)
        program.compile(Frame.draw_frame_array_gs(layers))
        program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/PostProcessEffects/FXAA_array_filter.fs")

        FXAA.__array_programs[layers] = program

        return program