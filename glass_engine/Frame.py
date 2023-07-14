from glass import Vertex, Vertices, Indices, ShaderProgram, sampler2D, GLConfig

import glm
from OpenGL import GL

def _init_Frame(cls):
    cls.vertices = Vertices()
    cls.indices = Indices()

    cls.vertices[0] = Vertex(position=glm.vec2(-1, -1))
    cls.vertices[1] = Vertex(position=glm.vec2(1, -1))
    cls.vertices[2] = Vertex(position=glm.vec2(1, 1))
    cls.vertices[3] = Vertex(position=glm.vec2(-1, 1))

    cls.indices[0] = glm.uvec3(0, 1, 2)
    cls.indices[1] = glm.uvec3(0, 2, 3)

    cls.program = ShaderProgram()
    cls.program.compile("glsl/Pipelines/draw_frame.vs")
    cls.program.compile("glsl/Pipelines/draw_frame.fs")

    return cls

@_init_Frame
class Frame:
    @staticmethod
    def draw(screen_image:sampler2D, gray:bool=False, invert:bool=False):
        with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):
            Frame.program["screen_image"] = screen_image
            Frame.program["gray"] = gray
            Frame.program["invert"] = invert
            Frame.program.draw_triangles(Frame.vertices, Frame.indices)