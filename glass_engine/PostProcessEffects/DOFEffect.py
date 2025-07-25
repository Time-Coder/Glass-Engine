from .PostProcessEffect import PostProcessEffect
from ..Frame import Frame

from glass import FBO, ShaderProgram, sampler2D, GLConfig, Block

from OpenGL import GL
import os


class DOFEffect(PostProcessEffect):

    class CurrentFocus(Block.HostClass):
        def __init__(self):
            Block.HostClass.__init__(self)

            self._current_focus = 0

        @property
        def current_focus(self):
            return self._current_focus

        @current_focus.setter
        @Block.HostClass.not_const
        def current_focus(self, focus: float):
            self._current_focus = focus

    def __init__(self):
        PostProcessEffect.__init__(self)
        self.current_focus = DOFEffect.CurrentFocus()

        self._horizontal_fbo = None
        self._vertical_fbo = None
        self._program = None

    def need_pos_info(self) -> bool:
        return True

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
            self._program.compile(
                os.path.dirname(os.path.abspath(__file__))
                + "/../glsl/PostProcessEffects/dof.frag"
            )
            self._program["CurrentFocus"].bind(self.current_focus)
        return self._program

    def apply(self, screen_image: sampler2D) -> sampler2D:
        self.horizontal_fbo.resize(screen_image.width, screen_image.height)
        self.vertical_fbo.resize(screen_image.width, screen_image.height)

        with GLConfig.LocalEnv():
            GLConfig.cull_face = None
            GLConfig.polygon_mode = GL.GL_FILL

            self.program["camera"] = self.camera
            self.program["world_pos_map"] = self.world_pos_map
            self.program["fps"] = self.camera.screen.smooth_fps
            with self.horizontal_fbo:
                self.program["screen_image"] = screen_image
                self.program["horizontal"] = True
                self.program.draw_triangles(start_index=0, total=6)

            with self.vertical_fbo:
                self.program["screen_image"] = self.horizontal_fbo.color_attachment(0)
                self.program["horizontal"] = False
                self.program.draw_triangles(start_index=0, total=6)

        return self.vertical_fbo.color_attachment(0)

    def draw_to_active(self, screen_image: sampler2D) -> None:
        self.horizontal_fbo.resize(screen_image.width, screen_image.height)
        self.vertical_fbo.resize(screen_image.width, screen_image.height)

        with GLConfig.LocalEnv():
            GLConfig.cull_face = None
            GLConfig.polygon_mode = GL.GL_FILL
            
            self.program["camera"] = self.camera
            self.program["world_pos_map"] = self.world_pos_map
            self.program["fps"] = self.camera.screen.smooth_fps
            with self.horizontal_fbo:
                self.program["screen_image"] = screen_image
                self.program["horizontal"] = True
                self.program.draw_triangles(start_index=0, total=6)

            GLConfig.clear_buffers()
            self.program["screen_image"] = self.horizontal_fbo.color_attachment(0)
            self.program["horizontal"] = False
            self.program.draw_triangles(start_index=0, total=6)

    @property
    def should_update_until(self)->float:
        if not self._enabled:
            return 0
        
        if self.camera is None:
            return 0

        if not self.camera.lens.auto_focus:
            return 0

        return self.camera.screen._scene_update_time + self.camera.lens.focus_change_time + 1
