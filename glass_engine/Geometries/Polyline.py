from ..Mesh import Mesh

from glass import Vertex
from glass.utils import checktype

import glm
from OpenGL import GL

class Polyline(Mesh):
    
    def __init__(self, points:list=[], color:(glm.vec3,glm.vec4)=glm.vec4(0.396, 0.74151, 0.69102, 1),
                 line_width:int=2, loop:bool=False,
                 name:str="", block:bool=True):
        primitive_type = (GL.GL_LINE_STRIP if not loop else GL.GL_LINE_LOOP)
        Mesh.__init__(self, primitive_type=primitive_type, color=color, name=name, block=block, shared=False)
        self.render_hints.line_width = line_width
        self.__points = points
        self.start_building()

    def build(self):
        points = self.__points
        vertices = self.vertices

        length = 0
        len_points = len(points)
        for i in range(len_points):
            if i > 0:
                length += glm.length(points[i]-points[i-1])
            bitangent = None
            if i < len_points-1:
                bitangent = glm.normalize(points[i+1] - points[i])
            else:
                bitangent = glm.normalize(points[i] - points[i-1])
            vertices[i] = Vertex(position=points[i], bitangent=bitangent, tex_coord=glm.vec3(length, 0, 0))

        del vertices[len_points:]

    @property
    def points(self):
        return self.__points
    
    @points.setter
    def points(self, points):
        self.__points = points
        self.start_building()

    @property
    def line_width(self):
        return self.render_hints.line_width
    
    @line_width.setter
    @checktype
    def line_width(self, line_width:int):
        self.render_hints.line_width = line_width

    @property
    def loop(self):
        return (self.primitive_type == GL.GL_LINE_LOOP)
    
    @loop.setter
    @Mesh.param_setter
    def loop(self, flag:bool):
        self.primitive_type = (GL.GL_LINE_STRIP if not flag else GL.GL_LINE_LOOP)