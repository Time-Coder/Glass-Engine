from .Filters import Filter
from ..Frame import Frame

from glass import FBO, ShaderProgram, sampler2D, GLConfig
from glass.utils import checktype, di
from glass.ShaderStorageBlock import ShaderStorageBlock

from OpenGL import GL
import time
import os

class DOFFilter(Filter):

    class CurrentFocus(ShaderStorageBlock.HostClass):
        def __init__(self):
            ShaderStorageBlock.HostClass.__init__(self)

            self._current_focus = 0

        @property
        def current_focus(self):
            return self._current_focus
        
        @current_focus.setter
        @ShaderStorageBlock.HostClass.not_const
        def current_focus(self, focus:float):
            self._current_focus = focus

    def __init__(self, camera=None, view_pos_map:sampler2D=None):
        Filter.__init__(self)
        
        self._camera_id = id(camera)

        self.__view_pos_map = view_pos_map
        self._last_not_should_update_time = 0

        self.current_focus = DOFFilter.CurrentFocus()

        self._horizontal_fbo = None
        self._vertical_fbo = None
        self._program = None

    @property
    def horizontal_fbo(self):
        if self._horizontal_fbo is None:
            self._horizontal_fbo = FBO()
            self._horizontal_fbo.attach(0, sampler2D, GL.GL_RGBA32F)
        return self._horizontal_fbo

    @property
    def vertical_fbo(self):
        if self._vertical_fbo is None:
            self._vertical_fbo = FBO()
            self._vertical_fbo.attach(0, sampler2D, GL.GL_RGBA32F)
        return self._vertical_fbo

    @property
    def program(self):
        if self._program is None:
            self._program = ShaderProgram()
            self._program.compile(Frame.draw_frame_vs)
            self._program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/Filters/dof_filter.fs")
            self._program["CurrentFocus"].bind(self.current_focus)
        return self._program
    
    @property
    def camera(self):        
        return di(self._camera_id)
    
    @camera.setter
    def camera(self, camera):
        self._camera_id = id(camera)

    def __call__(self, screen_image:sampler2D)->sampler2D:
        self.horizontal_fbo.resize(screen_image.width, screen_image.height)
        self.vertical_fbo.resize(screen_image.width, screen_image.height)

        with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):
            self.program["camera"] = self.camera
            self.program["view_pos_map"] = self.__view_pos_map
            self.program["fps"] = self.camera.screen.smooth_fps
            with self.horizontal_fbo:
                self.program["screen_image"] = screen_image
                self.program["horizontal"] = True
                self.program.draw_triangles(Frame.vertices, Frame.indices)

            with self.vertical_fbo:
                self.program["screen_image"] = self.horizontal_fbo.color_attachment(0)
                self.program["horizontal"] = False
                self.program.draw_triangles(Frame.vertices, Frame.indices)

        return self.vertical_fbo.color_attachment(0)

    def draw_to_active(self, screen_image:sampler2D)->None:
        self.horizontal_fbo.resize(screen_image.width, screen_image.height)
        self.vertical_fbo.resize(screen_image.width, screen_image.height)

        with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):
            self.program["camera"] = self.camera
            self.program["view_pos_map"] = self.__view_pos_map
            self.program["fps"] = self.camera.screen.smooth_fps
            with self.horizontal_fbo:
                self.program["screen_image"] = screen_image
                self.program["horizontal"] = True
                self.program.draw_triangles(Frame.vertices, Frame.indices)

            GLConfig.clear_buffers()
            self.program["screen_image"] = self.horizontal_fbo.color_attachment(0)
            self.program["horizontal"] = False
            self.program.draw_triangles(Frame.vertices, Frame.indices)

    @property
    def view_pos_map(self):
        return self.__view_pos_map
    
    @view_pos_map.setter
    @checktype
    def view_pos_map(self, view_pos_map:sampler2D):
        if self.__view_pos_map == view_pos_map:
            return
        
        self.__view_pos_map = view_pos_map
    
    @property
    def should_update(self) -> bool:
        return self._enabled and (self.screen_update_time == 0 or time.time()-self.screen_update_time <= 2)
    
    @should_update.setter
    @checktype
    def should_update(self, flag:bool):
        pass
