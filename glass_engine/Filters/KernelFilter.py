from .Filters import Filter
from ..Frame import Frame
from glass.utils import checktype
from glass import ShaderProgram, FBO, sampler2D, sampler2DArray, GLConfig, ShaderStorageBlock

import numpy as np
from OpenGL import GL

class KernelFilter(Filter):

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
        Filter.__init__(self)
        self._kernel = KernelFilter.Kernel(kernel)

        self.program = ShaderProgram()
        self.program.compile(Frame.draw_frame_vs)
        self.program.compile("glsl/Filters/kernel_filter.fs")
        self.program["Kernel"].bind(self._kernel)

        self.fbo = FBO()
        self.fbo.attach(0, sampler2D)

        self.array_fbo = FBO()
        self.array_fbo.attach(0, sampler2DArray)

        self.__array_programs = {}

    def __call__(self, screen_image:(sampler2D,sampler2DArray))->(sampler2D,sampler2DArray):
        if isinstance(screen_image, sampler2D):
            self.fbo.resize(screen_image.width, screen_image.height)
            with GLConfig.LocalConfig(depth_test=False, cull_face=None, polygon_mode=GL.GL_FILL):
                with self.fbo:
                    self.program["screen_image"] = screen_image
                    self.program.draw_triangles(Frame.vertices, Frame.indices)

            return self.fbo.color_attachment(0)
        elif isinstance(screen_image, sampler2DArray):
            self.array_fbo.resize(screen_image.width, screen_image.height)
            self.array_fbo.color_attachment(0).layers = screen_image.layers
            program = self.array_program(screen_image.layers)
            with GLConfig.LocalConfig(depth_test=False, cull_face=None, polygon_mode=GL.GL_FILL):
                with self.array_fbo:
                    program["screen_image"] = screen_image
                    program.draw_triangles(Frame.vertices, Frame.indices)

            return self.fbo.color_attachment(0)
        
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
        program.compile("../glsl/Pipelines/draw_frame.vs")
        program.compile(Frame.draw_frame_array_gs(layers))
        program.compile("../glsl/Filters/array_kernel_filter.fs")
        program["Kernel"].bind(self._kernel)

        self.__array_programs[layers] = program

        return program
    