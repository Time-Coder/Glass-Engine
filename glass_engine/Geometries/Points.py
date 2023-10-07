from ..Mesh import Mesh

from glass import Vertex
from glass.utils import checktype

import glm
from OpenGL import GL

class Points(Mesh):
    
    def __init__(self, points:list=[], color:(glm.vec3,glm.vec4)=glm.vec4(0.396, 0.74151, 0.69102, 1), point_size:int=5,
                 name:str="", block:bool=True):
        Mesh.__init__(self, primitive_type=GL.GL_POINTS, color=color, name=name, block=block, shared=False)
        self.render_hints.point_size = point_size
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
            vertices[i] = Vertex(position=points[i], tex_coord=glm.vec3(length, 0, 0))

        del vertices[len_points:]

    @property
    def points(self):
        return self.__points
    
    @points.setter
    def points(self, points):
        self.__points = points
        self.start_building()

    @property
    def point_size(self):
        return self.render_hints.point_size
    
    @point_size.setter
    @checktype
    def point_size(self, point_size:int):
        self.render_hints.point_size = point_size