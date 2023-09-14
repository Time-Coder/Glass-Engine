from .PostProcessEffect import PostProcessEffect
from ..Frame import Frame
from glass.utils import checktype
from glass import ShaderProgram, FBO, sampler2D, sampler2DArray, samplerCube, GLConfig, ShaderStorageBlock

import numpy as np
from OpenGL import GL
import os

class KernelFilter(PostProcessEffect):

    class Kernel(ShaderStorageBlock.HostClass):
        def __init__(self, kernel:np.ndarray):
            ShaderStorageBlock.HostClass.__init__(self)
            
            self._rows = kernel.shape[0]
            self._cols = kernel.shape[1]
            self._data = list(kernel.flatten())
            self._kernel = kernel
        
        @property
        def rows(self):
            return self._rows
        
        @property
        def cols(self):
            return self._cols
        
        @property
        def data(self):
            return self._data
        
        @property
        def kernel(self):
            return self._kernel

        @kernel.setter
        @ShaderStorageBlock.HostClass.not_const
        def kernel(self, kernel:np.ndarray):
            self.rows = kernel.shape[0]
            self.cols = kernel.shape[1]
            self.data = list(kernel.flatten())
            self._kernel = kernel

    @checktype
    def __init__(self, kernel:np.ndarray):
        PostProcessEffect.__init__(self)
        self._kernel = KernelFilter.Kernel(kernel)

        self._program = None
        self._cube_program = None
        self._fbo = None
        self._array_fbo = None
        self._cube_fbo = None
        self.__array_programs = {}

    def need_pos_info(self) -> bool:
        return False

    @property
    def program(self):
        if self._program is None:
            self._program = ShaderProgram()
            self._program.compile(Frame.draw_frame_vs)
            self._program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/PostProcessEffects/kernel_filter.fs")
            self._program["Kernel"].bind(self._kernel)
        return self._program

    @property
    def cube_program(self):
        if self._cube_program is None:
            self._cube_program = ShaderProgram()
            self._cube_program.compile(Frame.draw_frame_vs)
            self._cube_program.compile(Frame.draw_frame_array_gs(6))
            self._cube_program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/PostProcessEffects/kernel_cube_filter.fs")
            self._cube_program["Kernel"].bind(self._kernel)
        return self._cube_program

    @property
    def fbo(self):
        if self._fbo is None:
            self._fbo = FBO()
            self._fbo.attach(0, sampler2D)
        return self._fbo

    @property
    def array_fbo(self):
        if self._array_fbo is None:
            self._array_fbo = FBO()
            self._array_fbo.attach(0, sampler2DArray)
        return self._array_fbo

    @property
    def cube_fbo(self):
        if self._cube_fbo is None:
            self._cube_fbo = FBO()
            self._cube_fbo.attach(0, samplerCube)
        return self._cube_fbo

    def __call__(self, screen_image:(sampler2D,sampler2DArray,samplerCube))->(sampler2D,sampler2DArray,samplerCube):
        if isinstance(screen_image, sampler2D):
            self.fbo.resize(screen_image.width, screen_image.height)
            with GLConfig.LocalConfig(depth_test=False, cull_face=None, polygon_mode=GL.GL_FILL):
                with self.fbo:
                    self.program["screen_image"] = screen_image
                    self.program.draw_triangles(Frame.vertices, Frame.indices)

            return self.fbo.color_attachment(0)
        elif isinstance(screen_image, sampler2DArray):
            self.array_fbo.resize(screen_image.width, screen_image.height, layers=screen_image.layers)
            program = self.array_program(screen_image.layers)
            with GLConfig.LocalConfig(depth_test=False, cull_face=None, polygon_mode=GL.GL_FILL):
                with self.array_fbo:
                    program["screen_image"] = screen_image
                    program.draw_triangles(Frame.vertices, Frame.indices)

            return self.array_fbo.color_attachment(0)
        elif isinstance(screen_image, samplerCube):
            self.cube_fbo.resize(screen_image.width, screen_image.height)
            with GLConfig.LocalConfig(depth_test=False, cull_face=None, polygon_mode=GL.GL_FILL):
                with self.cube_fbo:
                    self.cube_program["screen_image"] = screen_image
                    self.cube_program.draw_triangles(Frame.vertices, Frame.indices)

            return self.cube_fbo.color_attachment(0)
        
    def draw_to_active(self, screen_image: sampler2D) -> None:
        with GLConfig.LocalConfig(depth_test=False, cull_face=None, polygon_mode=GL.GL_FILL):
            self.program["screen_image"] = screen_image
            self.program.draw_triangles(Frame.vertices, Frame.indices)

    @property
    def kernel(self)->np.ndarray:
        return self._kernel.kernel
    
    @kernel.setter
    def kernel(self, kernel:np.ndarray):
        self._kernel.kernel = kernel
    
    def array_program(self, layers):
        if layers in self.__array_programs:
            return self.__array_programs[layers]

        program = ShaderProgram()
        program.compile(Frame.draw_frame_vs)
        program.compile(Frame.draw_frame_array_gs(layers))
        program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/PostProcessEffects/kernel_array_filter.fs")
        program["Kernel"].bind(self._kernel)

        self.__array_programs[layers] = program

        return program
    