from .PostProcessEffect import PostProcessEffect
from ..Frame import Frame
from glass.utils import checktype
from glass import (
    ShaderProgram,
    FBO,
    sampler2D,
    sampler2DArray,
    samplerCube,
    GLConfig,
    Block,
)

import numpy as np
from OpenGL import GL
import os
from typing import Union


class KernelFilter(PostProcessEffect):

    class Kernel(Block.HostClass):
        def __init__(self, kernel: np.ndarray):
            Block.HostClass.__init__(self)

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
        @Block.HostClass.not_const
        def kernel(self, kernel: np.ndarray):
            self.rows = kernel.shape[0]
            self.cols = kernel.shape[1]
            self.data = list(kernel.flatten())
            self._kernel = kernel

    @checktype
    def __init__(self, kernel: np.ndarray):
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
            self._program.compile(
                os.path.dirname(os.path.abspath(__file__))
                + "/../glsl/PostProcessEffects/kernel_filter.frag"
            )
            self._program["Kernel"].bind(self._kernel)
        return self._program

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

    def __call__(
        self, screen_image: Union[sampler2D, sampler2DArray, samplerCube]
    ) -> Union[sampler2D, sampler2DArray, samplerCube]:
        if isinstance(screen_image, sampler2D):
            self.fbo.resize(screen_image.width, screen_image.height)
            with GLConfig.LocalEnv():
                GLConfig.depth_test = False
                GLConfig.cull_face = None
                GLConfig.polygon_mode = GL.GL_FILL

                with self.fbo:
                    self.program["screen_image"] = screen_image
                    self.program.draw_triangles(start_index=0, total=6)

            return self.fbo.color_attachment(0)
        elif isinstance(screen_image, sampler2DArray):
            self.array_fbo.resize(
                screen_image.width, screen_image.height, layers=screen_image.layers
            )
            program = self.array_program(screen_image.layers)
            with GLConfig.LocalEnv():
                GLConfig.depth_test = False
                GLConfig.cull_face = None
                GLConfig.polygon_mode = GL.GL_FILL

                with self.array_fbo:
                    program["screen_image"] = screen_image
                    program.draw_triangles(start_index=0, total=6)

            return self.array_fbo.color_attachment(0)
        elif isinstance(screen_image, samplerCube):
            self.cube_fbo.resize(screen_image.width, screen_image.height)
            with GLConfig.LocalEnv():
                GLConfig.depth_test = False
                GLConfig.cull_face = None
                GLConfig.polygon_mode = GL.GL_FILL

                with self.cube_fbo:
                    self.cube_program["screen_image"] = screen_image
                    self.cube_program.draw_triangles(start_index=0, total=6)

            return self.cube_fbo.color_attachment(0)

    def draw_to_active(self, screen_image: sampler2D) -> None:
        with GLConfig.LocalEnv():
            GLConfig.depth_test = False
            GLConfig.cull_face = None
            GLConfig.polygon_mode = GL.GL_FILL
            
            self.program["screen_image"] = screen_image
            self.program.draw_triangles(start_index=0, total=6)

    @property
    def kernel(self) -> np.ndarray:
        return self._kernel.kernel

    @kernel.setter
    @PostProcessEffect.param_setter
    def kernel(self, kernel: np.ndarray):
        self._kernel.kernel = kernel
