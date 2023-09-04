from glass import Vertex, Vertices, Indices, ShaderProgram, sampler2D, GLConfig, sampler2DArray
from glass.utils import modify_time, cat
from glass.GlassConfig import GlassConfig

import glm
import os
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

    self_folder = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
    cls.draw_frame_vs = os.path.abspath(self_folder + "/glsl/Pipelines/draw_frame.vs")
    cls.draw_frame_fs = os.path.abspath(self_folder + "/glsl/Pipelines/draw_frame.fs")

    cls.program = ShaderProgram()
    cls.program.compile(cls.draw_frame_vs)
    cls.program.compile(cls.draw_frame_fs)
    cls.program.uniform_not_set_warning = False

    return cls

@_init_Frame
class Frame:

    __array_geo_shader_template_content = None

    @staticmethod
    def draw(screen_image:(sampler2D,sampler2DArray), gray:bool=False, invert:bool=False, layer:int=-1, index:int=0):
        with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):
            if isinstance(screen_image, sampler2D):
                Frame.program["screen_image"] = screen_image
                Frame.program["layer"] = -1
            else:
                Frame.program["screen_image_array"] = screen_image
                Frame.program["layer"] = layer

            Frame.program["gray"] = gray
            Frame.program["invert"] = invert
            Frame.program["index"] = index
            Frame.program.draw_triangles(Frame.vertices, Frame.indices)

    @staticmethod
    def draw_frame_array_gs(layers):
        self_folder = os.path.dirname(os.path.abspath(__file__))

        target_filename = GlassConfig.cache_folder + f"/draw_frame_array{layers}.gs"
        template_filename = self_folder + "/glsl/Pipelines/draw_frame_array.gs"
        if modify_time(template_filename) > modify_time(target_filename):
            if Frame.__array_geo_shader_template_content is None:
                Frame.__array_geo_shader_template_content = cat(template_filename)
            
            target_file = open(target_filename, "w")
            target_file.write(Frame.__array_geo_shader_template_content.replace("{layers}", str(layers)))
            target_file.close()

        return target_filename