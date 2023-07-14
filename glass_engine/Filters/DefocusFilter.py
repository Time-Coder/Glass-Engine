from .Filters import Filter
from ..Frame import Frame

from glass import FBO, ShaderProgram, sampler2D, GLConfig
from glass.utils import checktype

from OpenGL import GL

class DefocusFilter(Filter):

    def __init__(self, camera:'Camera'=None, view_pos_map:sampler2D=None):
        self.__camera = camera
        self.__view_pos_map = view_pos_map

        self.horizontal_fbo = FBO()
        self.horizontal_fbo.attach(0, sampler2D, GL.GL_RGBA32F)

        self.vertical_fbo = FBO()
        self.vertical_fbo.attach(0, sampler2D, GL.GL_RGBA32F)

        self.program = ShaderProgram()
        self.program.compile("../glsl/Pipelines/draw_frame.vs")
        self.program.compile("../glsl/Filters/defocus_filter.fs")

    def __call__(self, screen_image:sampler2D)->sampler2D:
        self.horizontal_fbo.resize(screen_image.width, screen_image.height)
        self.vertical_fbo.resize(screen_image.width, screen_image.height)

        with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):
            self.program["camera"] = self.__camera
            self.program["view_pos_map"] = self.__view_pos_map
            with self.horizontal_fbo:
                self.program["screen_image"] = screen_image
                self.program["horizontal"] = True
                self.program.draw_triangles(Frame.vertices, Frame.indices)

            with self.vertical_fbo:
                self.program["screen_image"] = self.horizontal_fbo.color_attachment(0)
                self.program["horizontal"] = False
                self.program.draw_triangles(Frame.vertices, Frame.indices)

        return self.vertical_fbo.color_attachment(0)
    
    @property
    def camera(self):
        return self.__camera
    
    @camera.setter
    def camera(self, camera:'Camera'):
        if self.__camera is camera:
            return
        
        self.__camera = camera

    @property
    def view_pos_map(self):
        return self.__view_pos_map
    
    @view_pos_map.setter
    @checktype
    def view_pos_map(self, view_pos_map:sampler2D):
        if self.__view_pos_map == view_pos_map:
            return
        
        self.__view_pos_map = view_pos_map
        