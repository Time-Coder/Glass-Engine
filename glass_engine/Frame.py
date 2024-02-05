from glass import ShaderProgram, sampler2D, GLConfig, sampler2DArray

import os
from OpenGL import GL


class Frame:

    def __init__(self):
        self._program = None

    @property
    def program(self):
        if self._program is None:
            self._program = ShaderProgram()
            self._program.compile(self.draw_frame_vs)
            self._program.compile(self.draw_frame_fs)
            self._program.uniform_not_set_warning = False

        return self._program

    @property
    def draw_frame_vs(self) -> str:
        self_folder = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(self_folder + "/../glass/glsl/draw_frame.vs").replace(
            "\\", "/"
        )

    @property
    def draw_frame_fs(self) -> str:
        self_folder = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(self_folder + "/glsl/Pipelines/draw_frame.fs").replace(
            "\\", "/"
        )

    def draw(
        self,
        screen_image: (sampler2D, sampler2DArray),
        gray: bool = False,
        invert: bool = False,
        layer: int = -1,
        index: int = 0,
    ):
        with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):
            if isinstance(screen_image, sampler2D):
                self.program["screen_image"] = screen_image
                self.program["layer"] = -1
            else:
                self.program["screen_image_array"] = screen_image
                self.program["layer"] = layer

            self.program["gray"] = gray
            self.program["invert"] = invert
            self.program["index"] = index
            self.program.draw_triangles(vertices=self.vertices, indices=self.indices)


Frame = Frame()
