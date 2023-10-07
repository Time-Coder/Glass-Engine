from ..Mesh import Mesh

from glass import Vertex
from glass.utils import checktype

import glm
import math
from OpenGL import GL

class Circle(Mesh):
    
    def __init__(self, radius:float=1, vertical:bool=False, n_points:int=100,
                 start_angle:float=0, span_angle:float=360,
                 color:(glm.vec3,glm.vec4)=glm.vec4(0.396, 0.74151, 0.69102, 1),
                 line_width:int=2, name:str=""):
        Mesh.__init__(self, primitive_type=GL.GL_LINE_STRIP, color=color, name=name)
        self.render_hints.line_width = line_width
        self.__radius:float = radius
        self.__vertical:bool = vertical
        self.__n_points:int = n_points
        self.__start_angle:float = start_angle
        self.__span_angle:float = span_angle
        self.start_building()

    def build(self):
        vertices = self.vertices
        radius:float = self.__radius
        vertical:bool = self.__vertical
        n_points:int = self.__n_points
        start_angle:float = self.__start_angle
        span_angle:float = self.__span_angle

        for i in range(n_points):
            theta = (start_angle + i/(n_points-1)*span_angle)/180*math.pi

            position = radius * glm.vec3(math.cos(theta), math.sin(theta), 0)
            bitangent = glm.vec3(-math.sin(theta), math.cos(theta), 0)
            if vertical:
                position = radius * glm.vec3(math.cos(theta), 0, math.sin(theta))
                bitangent = glm.vec3(-math.sin(theta), 0, math.cos(theta))
                
            vertices[i] = Vertex(position=position, bitangent=bitangent, tex_coord=glm.vec3(radius*theta, 0, 0))

        del vertices[n_points:]

    @property
    def line_width(self)->int:
        return self.render_hints.line_width
    
    @line_width.setter
    @checktype
    def line_width(self, line_width:int)->None:
        self.render_hints.line_width = line_width

    @property
    def radius(self)->float:
        return self.__radius
    
    @radius.setter
    @Mesh.param_setter
    def radius(self, radius:float)->None:
        self.__radius = radius

    @property
    def vertical(self)->bool:
        return self.__vertical
    
    @vertical.setter
    @Mesh.param_setter
    def vertical(self, flag:bool)->None:
        self.__vertical = flag

    @property
    def n_points(self)->int:
        return self.__n_points
    
    @n_points.setter
    @Mesh.param_setter
    def n_points(self, n_points:int)->None:
        self.__n_points = n_points
    
    @property
    def start_angle(self)->float:
        return self.__start_angle
    
    @start_angle.setter
    @Mesh.param_setter
    def start_angle(self, angle:float)->None:
        self.__start_angle = angle

    @property
    def span_angle(self)->float:
        return self.__span_angle
    
    @span_angle.setter
    @Mesh.param_setter
    def span_angle(self, angle:float)->None:
        self.__span_angle = angle