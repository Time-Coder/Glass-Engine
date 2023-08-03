from .Filters import Filter
from ..Frame import Frame

from glass import FBO, ShaderProgram, sampler2D, GLConfig, sampler2DArray, samplerCube
from glass.utils import checktype

from OpenGL import GL
import glm

def _init_GaussFilter(cls):
    cls.program = ShaderProgram()
    cls.program.compile(Frame.draw_frame_vs)
    cls.program.compile("../glsl/Filters/gauss_filter.fs")

    cls.cube_program = ShaderProgram()
    cls.cube_program.compile(Frame.draw_frame_vs)
    cls.cube_program.compile(Frame.draw_frame_array_gs(6))
    cls.cube_program.compile("../glsl/Filters/gauss_cube_filter.fs")

    return cls

@_init_GaussFilter
class GaussFilter(Filter):

    __array_programs = {}

    @checktype
    def __init__(self, kernel_shape:(int,tuple)=32, sigma:(float,tuple)=0):
        Filter.__init__(self)
        
        self.__kernel_shape = glm.uvec2()
        self.__sigma = glm.vec2()

        if isinstance(kernel_shape, tuple):
            self.__kernel_shape.x, self.__kernel_shape.y = kernel_shape
        else:
            self.__kernel_shape.x, self.__kernel_shape.y = kernel_shape, kernel_shape

        if isinstance(sigma, tuple):
            self.__sigma.x, self.__sigma.y = sigma
        else:
            self.__sigma.x, self.__sigma.y = sigma, sigma

        self.horizontal_fbo = FBO()
        self.horizontal_fbo.attach(0, sampler2D)

        self.vertical_fbo = FBO()
        self.vertical_fbo.attach(0, sampler2D)

        self.horizontal_array_fbo = FBO()
        self.horizontal_array_fbo.attach(0, sampler2DArray)

        self.vertical_array_fbo = FBO()
        self.vertical_array_fbo.attach(0, sampler2DArray)

        self.horizontal_cube_fbo = FBO()
        self.horizontal_cube_fbo.attach(0, samplerCube)

        self.vertical_cube_fbo = FBO()
        self.vertical_cube_fbo.attach(0, samplerCube)

    def __call__(self, screen_image:(sampler2D,sampler2DArray,samplerCube))->(sampler2D,sampler2DArray,samplerCube):
        if self.__sigma.x == 0:
            self.__sigma.x = 0.3 * ((self.__kernel_shape.x-1)*0.5 - 1) + 0.8
        if self.__sigma.y == 0:
            self.__sigma.y = 0.3 * ((self.__kernel_shape.y-1)*0.5 - 1) + 0.8
        
        if isinstance(screen_image, sampler2D):
            self.horizontal_fbo.resize(screen_image.width, screen_image.height)
            self.vertical_fbo.resize(screen_image.width, screen_image.height)

            with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):

                GaussFilter.program["kernel_shape"] = self.__kernel_shape
                GaussFilter.program["sigma"] = self.__sigma

                with self.horizontal_fbo:
                    GaussFilter.program["screen_image"] = screen_image
                    GaussFilter.program["horizontal"] = True
                    GaussFilter.program.draw_triangles(Frame.vertices, Frame.indices)

                with self.vertical_fbo:
                    GaussFilter.program["screen_image"] = self.horizontal_fbo.color_attachment(0)
                    GaussFilter.program["horizontal"] = False
                    GaussFilter.program.draw_triangles(Frame.vertices, Frame.indices)

            return self.vertical_fbo.color_attachment(0)
        elif isinstance(screen_image, sampler2DArray):
            self.horizontal_array_fbo.resize(screen_image.width, screen_image.height, layers=screen_image.layers)
            self.vertical_array_fbo.resize(screen_image.width, screen_image.height, layers=screen_image.layers)

            program = GaussFilter.array_program(screen_image.layers)

            with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):
                
                program["kernel_shape"] = self.__kernel_shape
                program["sigma"] = self.__sigma

                with self.horizontal_array_fbo:
                    program["screen_image"] = screen_image
                    program["horizontal"] = True
                    program.draw_triangles(Frame.vertices, Frame.indices)

                with self.vertical_array_fbo:
                    program["screen_image"] = self.horizontal_array_fbo.color_attachment(0)
                    program["horizontal"] = False
                    program.draw_triangles(Frame.vertices, Frame.indices)

            return self.vertical_array_fbo.color_attachment(0)
        elif isinstance(screen_image, samplerCube):
            self.horizontal_cube_fbo.resize(screen_image.width, screen_image.height)
            self.vertical_cube_fbo.resize(screen_image.width, screen_image.height)

            program = GaussFilter.cube_program

            with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):
                
                program["kernel_shape"] = self.__kernel_shape
                program["sigma"] = self.__sigma

                with self.horizontal_cube_fbo:
                    program["screen_image"] = screen_image
                    program["horizontal"] = True
                    program.draw_triangles(Frame.vertices, Frame.indices)

                with self.vertical_cube_fbo:
                    program["screen_image"] = self.horizontal_cube_fbo.color_attachment(0)
                    program["horizontal"] = False
                    program.draw_triangles(Frame.vertices, Frame.indices)

            return self.vertical_cube_fbo.color_attachment(0)
    
    def draw_to_active(self, screen_image: sampler2D) -> None:
        self.horizontal_fbo.resize(screen_image.width, screen_image.height)
        self.vertical_fbo.resize(screen_image.width, screen_image.height)

        if self.__sigma.x == 0:
            self.__sigma.x = 0.3 * ((self.__kernel_shape.x-1)*0.5 - 1) + 0.8
        if self.__sigma.y == 0:
            self.__sigma.y = 0.3 * ((self.__kernel_shape.y-1)*0.5 - 1) + 0.8

        with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):

            GaussFilter.program["kernel_shape"] = self.__kernel_shape
            GaussFilter.program["sigma"] = self.__sigma

            with self.horizontal_fbo:
                GaussFilter.program["screen_image"] = screen_image
                GaussFilter.program["horizontal"] = True
                GaussFilter.program.draw_triangles(Frame.vertices, Frame.indices)

            GLConfig.clear_buffers()
            GaussFilter.program["screen_image"] = self.horizontal_fbo.color_attachment(0)
            GaussFilter.program["horizontal"] = False
            GaussFilter.program.draw_triangles(Frame.vertices, Frame.indices)

    @property
    def kernel_shape(self)->tuple:
        return (self.__kernel_shape.x, self.__kernel_shape.y)
    
    @kernel_shape.setter
    @checktype
    def kernel_shape(self, shape:(int, tuple)):
        if isinstance(shape, tuple):
            self.__kernel_shape.x, self.__kernel_shape.y = shape
        else:
            self.__kernel_shape.x, self.__kernel_shape.y = shape, shape
    
    @property
    def kernel_width(self)->int:
        return self.__kernel_shape.x
    
    @kernel_width.setter
    @checktype
    def kernel_width(self, width:int):
        self.__kernel_shape.x = width
    
    @property
    def kernel_height(self)->int:
        return self.__kernel_shape.y
    
    @kernel_height.setter
    @checktype
    def kernel_height(self, height:int):
        self.__kernel_shape.y = height

    @property
    def sigma(self)->tuple:
        return (self.__sigma.x, self.__sigma.y)
    
    @sigma.setter
    @checktype
    def sigma(self, sigma:(float,tuple)):
        if isinstance(sigma, tuple):
            self.__sigma.x, self.__sigma.y = sigma
        else:
            self.__sigma.x, self.__sigma.y = sigma, sigma

    @property
    def sigma_x(self)->float:
        return self.__sigma.x
    
    @sigma_x.setter
    def sigma_x(self, value:float):
        self.__sigma.x = value

    @property
    def sigma_y(self)->float:
        return self.__sigma.y
    
    @sigma_y.setter
    def sigma_y(self, value:float):
        self.__sigma.y = value
    
    @staticmethod
    def array_program(layers):
        if layers in GaussFilter.__array_programs:
            return GaussFilter.__array_programs[layers]

        program = ShaderProgram()
        program.compile(Frame.draw_frame_vs)
        program.compile(Frame.draw_frame_array_gs(layers))
        program.compile("../glsl/Filters/gauss_array_filter.fs")

        GaussFilter.__array_programs[layers] = program

        return program