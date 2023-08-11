from .Filters import Filter
from ..Frame import Frame
from glass import sampler2D, ShaderProgram, FBO, ShaderStorageBlock, GLConfig
from glass.utils import id_to_var

from OpenGL import GL
import time
import os

class HDRFilter(Filter):

    class CurrentLuma(ShaderStorageBlock.HostClass):
        def __init__(self):
            ShaderStorageBlock.HostClass.__init__(self)
            self._current_luma = 0

        @property
        def current_luma(self):
            return self._current_luma
        
        @current_luma.setter
        @ShaderStorageBlock.HostClass.not_const
        def current_luma(self, luma:float):
            self._current_luma = luma

    def __init__(self):
        Filter.__init__(self)

        self.current_luma = HDRFilter.CurrentLuma()

        self._camera_id = id(None)

        self.program = ShaderProgram()
        self.program.compile(Frame.draw_frame_vs)
        self.program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/Filters/hdr_filter.fs")
        self.program["CurrentLuma"].bind(self.current_luma)

        self.fbo = FBO()
        self.fbo.attach(0, sampler2D)

    @property
    def camera(self):        
        return id_to_var(self._camera_id)
    
    @camera.setter
    def camera(self, camera):
        self._camera_id = id(camera)

    def __call__(self, screen_image:sampler2D)->sampler2D:
        screen_image.filter_mipmap = GL.GL_LINEAR
        self.fbo.resize(screen_image.width, screen_image.height)
        with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):
            with self.fbo:
                self.program["camera"] = self.camera
                self.program["screen_image"] = screen_image
                self.program["fps"] = self.camera.screen.smooth_fps
                self.program.draw_triangles(Frame.vertices, Frame.indices)

        return self.fbo.color_attachment(0)
    
    def draw_to_active(self, screen_image: sampler2D) -> None:
        screen_image.filter_mipmap = GL.GL_LINEAR
        with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):
            self.program["camera"] = self.camera
            self.program["screen_image"] = screen_image
            self.program["fps"] = self.camera.screen.smooth_fps
            self.program.draw_triangles(Frame.vertices, Frame.indices)

    @property
    def should_update(self) -> bool:
        return self._enabled and (self.screen_update_time == 0 or time.time()-self.screen_update_time <= 2)
    
    @should_update.setter
    def should_update(self, flag:bool):
        pass
