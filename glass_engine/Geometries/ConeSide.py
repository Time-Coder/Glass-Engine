from ..Mesh import Mesh

from glass.utils import checktype
from glass import Vertex

import glm
import math

class ConeSide(Mesh):

    @checktype
    def __init__(self, radius:float=1, height:float=1,
                 start_angle:float=0, span_angle:float=360, n_divide:int=100,
                 color:(glm.vec3,glm.vec4)=glm.vec4(0.396, 0.74151, 0.69102, 1), back_color:(glm.vec3,glm.vec4)=None,
                 normalize_tex_coord=False, name:str="", block=True):
        Mesh.__init__(self, color=color, back_color=back_color, name=name, block=block)
        self.__radius = radius
        self.__height = height
        self.__start_angle = start_angle
        self.__span_angle = span_angle
        self.__n_divide = n_divide
        self.__normalize_tex_coord = normalize_tex_coord
        self.start_building()

    def build(self):
        self.is_closed = False
        self.self_calculated_normal = True

        vertices = self.vertices
        indices = self.indices

        radius = self.__radius
        height = self.__height
        start_angle = self.__start_angle/180*math.pi
        span_angle = self.__span_angle/180*math.pi
        n_divide = self.__n_divide
        normalize_tex_coord = self.__normalize_tex_coord

        i_vertex = 0
        i_index = 0

        tex_coord_radius = 0.5 if normalize_tex_coord else math.sqrt(radius**2 + height**2)

        for j in range(n_divide):
            theta = start_angle + j/(n_divide-1)*span_angle
            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)

            top = glm.vec3(0, 0, height)
            bottom = radius * glm.vec3(cos_theta, sin_theta, 0)

            to_right = glm.vec3(-sin_theta, cos_theta, 0)
            to_top = top - bottom
            normal = glm.normalize(glm.cross(to_right, to_top))

            vertex_top = Vertex()
            vertex_top.position = top
            vertex_top.normal = normal
            vertex_top.tex_coord = glm.vec3(0.5, 0.5, 0)

            vertex_bottom = Vertex()
            vertex_bottom.position = bottom
            vertex_bottom.normal = normal
            vertex_bottom.tex_coord = glm.vec3(0.5+tex_coord_radius*cos_theta, 0.5+tex_coord_radius*sin_theta, 0)

            vertices[i_vertex] = vertex_top
            i_vertex += 1

            vertices[i_vertex] = vertex_bottom
            i_vertex += 1

            if j > 0:
                triangle = glm.uvec3(0, 0, 0)
                triangle[0] = 2*j + 1
                triangle[1] = 2*j
                triangle[2] = 2*j - 1

                indices[i_index] = triangle
                i_index += 1
                self.generate_temp_TBN(vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]])
            
                yield
        
        del vertices[i_vertex:]
        del indices[i_index:]

    @property
    def start_angle(self):
        return self.__start_angle
    
    @start_angle.setter
    @Mesh.param_setter
    def start_angle(self, angle:float):
        self.__start_angle = angle

    @property
    def span_angle(self):
        return self.__span_angle
    
    @span_angle.setter
    @Mesh.param_setter
    def span_angle(self, angle:float):
        self.__span_angle = angle

    @property
    def n_divide(self):
        return self.__n_divide
    
    @n_divide.setter
    @Mesh.param_setter
    def n_divide(self, n_divide):
        self.__n_divide = n_divide

    @property
    def radius(self):
        return self.__radius
    
    @radius.setter
    @Mesh.param_setter
    def radius(self, radius:float):
        self.__radius = radius

    @property
    def height(self):
        return self.__height
    
    @height.setter
    @Mesh.param_setter
    def height(self, height:float):
        self.__height = height

    @property
    def normalize_tex_coord(self):
        return self.__normalize_tex_coord
    
    @normalize_tex_coord.setter
    @Mesh.param_setter
    def normalize_tex_coord(self, flag:bool):
        self.__normalize_tex_coord = flag