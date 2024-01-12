from glass import Vertex, Vertices, Indices, ShaderProgram, sampler2D, GLConfig, sampler2DArray
from glass.utils import modify_time, cat
from glass.GlassConfig import GlassConfig

import glm
import os
from OpenGL import GL

class _MetaFrame(type):

    _vertices = None
    _indices = None
    _program = None
    _draw_frame_vs = None
    _draw_frame_fs = None
    
    @property
    def program(cls)->ShaderProgram:
        if _MetaFrame._program is None:
            _MetaFrame._program = ShaderProgram()
            _MetaFrame._program.compile(cls.draw_frame_vs)
            _MetaFrame._program.compile(cls.draw_frame_fs)
            _MetaFrame._program.uniform_not_set_warning = False

        return _MetaFrame._program
    
    @property
    def vertices(cls)->Vertices:
        if _MetaFrame._vertices is None:
            _MetaFrame._vertices = Vertices()
            _MetaFrame._vertices[0] = Vertex(position=glm.vec2(-1, -1))
            _MetaFrame._vertices[1] = Vertex(position=glm.vec2(1, -1))
            _MetaFrame._vertices[2] = Vertex(position=glm.vec2(1, 1))
            _MetaFrame._vertices[3] = Vertex(position=glm.vec2(-1, 1))

        return _MetaFrame._vertices
    
    @property
    def indices(cls)->Indices:
        if _MetaFrame._indices is None:
            _MetaFrame._indices = Indices()
            _MetaFrame._indices[0] = glm.uvec3(0, 1, 2)
            _MetaFrame._indices[1] = glm.uvec3(0, 2, 3)

        return _MetaFrame._indices
    
    @property
    def draw_frame_vs(cls)->str:
        if _MetaFrame._draw_frame_vs is None:
            self_folder = os.path.dirname(os.path.abspath(__file__))
            _MetaFrame._draw_frame_vs = os.path.abspath(self_folder + "/glsl/Pipelines/draw_frame.vs").replace("\\", "/")

        return _MetaFrame._draw_frame_vs
    
    @property
    def draw_frame_fs(cls)->str:
        if _MetaFrame._draw_frame_fs is None:
            self_folder = os.path.dirname(os.path.abspath(__file__))
            _MetaFrame._draw_frame_fs = os.path.abspath(self_folder + "/glsl/Pipelines/draw_frame.fs").replace("\\", "/")

        return _MetaFrame._draw_frame_fs

class Frame(metaclass=_MetaFrame):

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