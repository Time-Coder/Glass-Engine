from .Filters import Filter
from ..Frame import Frame

from glass import FBO, ShaderProgram, sampler2D, GLConfig
from glass.utils import checktype

from OpenGL import GL
import glm

class GaussFilter(Filter):

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
        self.horizontal_fbo.attach(0, sampler2D, GL.GL_RGBA32F)

        self.vertical_fbo = FBO()
        self.vertical_fbo.attach(0, sampler2D, GL.GL_RGBA32F)

        self.program = ShaderProgram()
        self.program.compile("../glsl/Pipelines/draw_frame.vs")
        self.program.compile("../glsl/Filters/gauss_kernel.fs")
        self.program["kernel_shape"].bind(self.__kernel_shape)
        self.program["sigma"].bind(self.__sigma)

    def __call__(self, screen_image:sampler2D)->sampler2D:
        self.horizontal_fbo.resize(screen_image.width, screen_image.height)
        self.vertical_fbo.resize(screen_image.width, screen_image.height)

        if self.__sigma.x == 0:
            self.__sigma.x = 0.3 * ((self.__kernel_shape.x-1)*0.5 - 1) + 0.8
        if self.__sigma.y == 0:
            self.__sigma.y = 0.3 * ((self.__kernel_shape.y-1)*0.5 - 1) + 0.8

        with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):
            with self.horizontal_fbo:
                self.program["screen_image"] = screen_image
                self.program["horizontal"] = True
                self.program.draw_triangles(Frame.vertices, Frame.indices)

            with self.vertical_fbo:
                self.program["screen_image"] = self.horizontal_fbo.color_attachment(0)
                self.program["horizontal"] = False
                self.program.draw_triangles(Frame.vertices, Frame.indices)

        return self.vertical_fbo.color_attachment(0)
    
    def draw_to_active(self, screen_image: sampler2D) -> None:
        self.horizontal_fbo.resize(screen_image.width, screen_image.height)
        self.vertical_fbo.resize(screen_image.width, screen_image.height)

        if self.__sigma.x == 0:
            self.__sigma.x = 0.3 * ((self.__kernel_shape.x-1)*0.5 - 1) + 0.8
        if self.__sigma.y == 0:
            self.__sigma.y = 0.3 * ((self.__kernel_shape.y-1)*0.5 - 1) + 0.8

        with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):
            with self.horizontal_fbo:
                self.program["screen_image"] = screen_image
                self.program["horizontal"] = True
                self.program.draw_triangles(Frame.vertices, Frame.indices)

            GLConfig.clear_buffers()
            self.program["screen_image"] = self.horizontal_fbo.color_attachment(0)
            self.program["horizontal"] = False
            self.program.draw_triangles(Frame.vertices, Frame.indices)

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
        