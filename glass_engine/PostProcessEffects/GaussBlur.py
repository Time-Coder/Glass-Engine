from .PostProcessEffect import PostProcessEffect
from ..Frame import Frame

from glass import (
    FBO,
    ShaderProgram,
    sampler2D,
    GLConfig,
    sampler2DArray,
    samplerCube,
    GLInfo,
)
from glass.utils import checktype
from glass.helper import get_channels

from OpenGL import GL
import glm
import os


class GaussBlur(PostProcessEffect):

    __array_programs = {}
    __program = None
    __cube_program = None

    @staticmethod
    def program():
        if GaussBlur.__program is None:
            GaussBlur.__program = ShaderProgram()
            GaussBlur.__program.compile(Frame.draw_frame_vs)
            GaussBlur.__program.compile(
                os.path.dirname(os.path.abspath(__file__))
                + "/../glsl/PostProcessEffects/gauss_blur.fs"
            )
        return GaussBlur.__program

    @checktype
    def __init__(
        self,
        kernel_shape: (int, tuple) = 32,
        sigma: (float, tuple) = 0,
        internal_format: GLInfo.internal_formats = GL.GL_RGBA32F,
    ):
        PostProcessEffect.__init__(self)

        self.__kernel_shape = glm.uvec2()
        self.__sigma = glm.vec2()
        self.__channels = get_channels(internal_format)
        self.__internal_format = internal_format

        if isinstance(kernel_shape, tuple):
            self.__kernel_shape.x, self.__kernel_shape.y = kernel_shape
        else:
            self.__kernel_shape.x, self.__kernel_shape.y = kernel_shape, kernel_shape

        if isinstance(sigma, tuple):
            self.__sigma.x, self.__sigma.y = sigma
        else:
            self.__sigma.x, self.__sigma.y = sigma, sigma

        self._horizontal_fbo = None
        self._vertical_fbo = None
        self._horizontal_array_fbo = None
        self._vertical_array_fbo = None
        self._horizontal_cube_fbo = None
        self._vertical_cube_fbo = None

    def need_pos_info(self):
        return False

    @property
    def horizontal_fbo(self):
        if self._horizontal_fbo is None:
            self._horizontal_fbo = FBO()
            self._horizontal_fbo.attach(0, sampler2D, self.__internal_format)
        return self._horizontal_fbo

    @property
    def vertical_fbo(self):
        if self._vertical_fbo is None:
            self._vertical_fbo = FBO()
            self._vertical_fbo.attach(0, sampler2D, self.__internal_format)
        return self._vertical_fbo

    @property
    def horizontal_array_fbo(self):
        if self._horizontal_array_fbo is None:
            self._horizontal_array_fbo = FBO()
            self._horizontal_array_fbo.attach(0, sampler2DArray, self.__internal_format)
        return self._horizontal_array_fbo

    @property
    def vertical_array_fbo(self):
        if self._vertical_array_fbo is None:
            self._vertical_array_fbo = FBO()
            self._vertical_array_fbo.attach(0, sampler2DArray, self.__internal_format)
        return self._vertical_array_fbo

    @property
    def horizontal_cube_fbo(self):
        if self._horizontal_cube_fbo is None:
            self._horizontal_cube_fbo = FBO()
            self._horizontal_cube_fbo.attach(0, samplerCube, self.__internal_format)
        return self._horizontal_cube_fbo

    @property
    def vertical_cube_fbo(self):
        if self._vertical_cube_fbo is None:
            self._vertical_cube_fbo = FBO()
            self._vertical_cube_fbo.attach(0, samplerCube, self.__internal_format)
        return self._vertical_cube_fbo

    def apply(
        self, screen_image: (sampler2D, sampler2DArray, samplerCube)
    ) -> (sampler2D, sampler2DArray, samplerCube):
        if self.__sigma.x == 0:
            self.__sigma.x = 0.3 * ((self.__kernel_shape.x - 1) * 0.5 - 1) + 0.8
        if self.__sigma.y == 0:
            self.__sigma.y = 0.3 * ((self.__kernel_shape.y - 1) * 0.5 - 1) + 0.8

        if isinstance(screen_image, sampler2D):
            self.horizontal_fbo.resize(screen_image.width, screen_image.height)
            self.vertical_fbo.resize(screen_image.width, screen_image.height)

            program = GaussBlur.program()
            with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):

                program["kernel_shape"] = self.__kernel_shape
                program["sigma"] = self.__sigma
                program["channels"] = self.__channels

                with self.horizontal_fbo:
                    program["screen_image"] = screen_image
                    program["horizontal"] = True
                    program.draw_triangles(start_index=0, total=6)

                with self.vertical_fbo:
                    program["screen_image"] = self.horizontal_fbo.color_attachment(0)
                    program["horizontal"] = False
                    program.draw_triangles(start_index=0, total=6)

            return self.vertical_fbo.color_attachment(0)
        elif isinstance(screen_image, sampler2DArray):
            self.horizontal_array_fbo.resize(
                screen_image.width, screen_image.height, layers=screen_image.layers
            )
            self.vertical_array_fbo.resize(
                screen_image.width, screen_image.height, layers=screen_image.layers
            )

            program = GaussBlur.array_program(screen_image.layers)

            with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):

                program["kernel_shape"] = self.__kernel_shape
                program["sigma"] = self.__sigma
                program["channels"] = self.__channels

                with self.horizontal_array_fbo:
                    program["screen_image"] = screen_image
                    program["horizontal"] = True
                    program.draw_triangles(start_index=0, total=6)

                with self.vertical_array_fbo:
                    program["screen_image"] = (
                        self.horizontal_array_fbo.color_attachment(0)
                    )
                    program["horizontal"] = False
                    program.draw_triangles(start_index=0, total=6)

            return self.vertical_array_fbo.color_attachment(0)
        elif isinstance(screen_image, samplerCube):
            self.horizontal_cube_fbo.resize(screen_image.width, screen_image.height)
            self.vertical_cube_fbo.resize(screen_image.width, screen_image.height)

            program = GaussBlur.cube_program()

            with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):

                program["kernel_shape"] = self.__kernel_shape
                program["sigma"] = self.__sigma
                program["channels"] = self.__channels

                with self.horizontal_cube_fbo:
                    program["screen_image"] = screen_image
                    program["horizontal"] = True
                    program.draw_triangles(start_index=0, total=6)

                with self.vertical_cube_fbo:
                    program["screen_image"] = self.horizontal_cube_fbo.color_attachment(
                        0
                    )
                    program["horizontal"] = False
                    program.draw_triangles(start_index=0, total=6)

            return self.vertical_cube_fbo.color_attachment(0)

    def draw_to_active(self, screen_image: sampler2D) -> None:
        self.horizontal_fbo.resize(screen_image.width, screen_image.height)
        self.vertical_fbo.resize(screen_image.width, screen_image.height)

        if self.__sigma.x == 0:
            self.__sigma.x = ((self.__kernel_shape.x - 1) * 0.5 - 1) / 3
        if self.__sigma.y == 0:
            self.__sigma.y = ((self.__kernel_shape.y - 1) * 0.5 - 1) / 3

        program = GaussBlur.program()

        with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):

            program["kernel_shape"] = self.__kernel_shape
            program["sigma"] = self.__sigma
            program["channels"] = self.__channels

            with self.horizontal_fbo:
                program["screen_image"] = screen_image
                program["horizontal"] = True
                program.draw_triangles(start_index=0, total=6)

            GLConfig.clear_buffers()
            program["screen_image"] = self.horizontal_fbo.color_attachment(0)
            program["horizontal"] = False
            program.draw_triangles(start_index=0, total=6)

    @property
    def kernel_shape(self) -> tuple:
        return (self.__kernel_shape.x, self.__kernel_shape.y)

    @kernel_shape.setter
    @checktype
    def kernel_shape(self, shape: (int, tuple)):
        if isinstance(shape, tuple):
            self.__kernel_shape.x, self.__kernel_shape.y = shape
        else:
            self.__kernel_shape.x, self.__kernel_shape.y = shape, shape

    @property
    def kernel_width(self) -> int:
        return self.__kernel_shape.x

    @kernel_width.setter
    @checktype
    def kernel_width(self, width: int):
        self.__kernel_shape.x = width

    @property
    def kernel_height(self) -> int:
        return self.__kernel_shape.y

    @kernel_height.setter
    @checktype
    def kernel_height(self, height: int):
        self.__kernel_shape.y = height

    @property
    def sigma(self) -> tuple:
        return (self.__sigma.x, self.__sigma.y)

    @sigma.setter
    @checktype
    def sigma(self, sigma: (float, tuple)):
        if isinstance(sigma, tuple):
            self.__sigma.x, self.__sigma.y = sigma
        else:
            self.__sigma.x, self.__sigma.y = sigma, sigma

    @property
    def sigma_x(self) -> float:
        return self.__sigma.x

    @sigma_x.setter
    def sigma_x(self, value: float):
        self.__sigma.x = value

    @property
    def sigma_y(self) -> float:
        return self.__sigma.y

    @sigma_y.setter
    def sigma_y(self, value: float):
        self.__sigma.y = value
