from ..Mesh import Mesh

from glass.utils import checktype
from glass import Vertex

import glm
import math

class EllipseFace(Mesh):

    @checktype
    def __init__(self, a:float=2, b:float=1,
                 color:(glm.vec3,glm.vec4)=glm.vec4(0.396, 0.74151, 0.69102, 1), back_color:(glm.vec3,glm.vec4)=None,
                 start_angle:float=0, span_angle:float=360, n_divide:int=100,
                 vertical=False, normalize_tex_coord=False,
                 name:str="", block=True):
        Mesh.__init__(self, color=color, back_color=back_color, name=name, block=block)
        self.__a = a
        self.__b = b
        self.__start_angle = start_angle
        self.__span_angle = span_angle
        self.__n_divide = n_divide
        self.__vertical = vertical
        self.__normalize_tex_coord = normalize_tex_coord
        self.start_building()

    def build(self):
        self.is_closed = False
        self.self_calculated_normal = True

        vertices = self.vertices
        indices = self.indices
        a = self.__a
        b = self.__b
        start_angle = self.__start_angle / 180 * math.pi
        span_angle = self.__span_angle / 180 * math.pi
        n_divide = self.__n_divide
        vertical = self.__vertical
        normalize_tex_coord = self.__normalize_tex_coord

        i_vertex = 0
        i_index = 0
        
        normal = glm.vec3(0, 0, 1)
        if vertical:
            normal = glm.vec3(0, -1, 0)

        vertex_center = Vertex()
        vertex_center.position = glm.vec3(0)
        vertex_center.normal = normal
        vertex_center.tex_coord = glm.vec3(0.5, 0.5, 0)
        vertices[i_vertex] = vertex_center
        i_vertex += 1

        max_len = max(a, b)

        for j in range(n_divide):
            theta = start_angle + span_angle*j/(n_divide-1)
            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)
            cos2_theta = cos_theta**2
            sin2_theta = sin_theta**2

            r = 1/math.sqrt(cos2_theta/a**2 + sin2_theta/b**2)
            tex_coord_radius = r if not normalize_tex_coord else r / max_len * 0.5

            edge = r * glm.vec3(cos_theta, sin_theta, 0)
            if vertical:
                edge = r * glm.vec3(cos_theta, 0, sin_theta)
            
            vertex_edge = Vertex()
            vertex_edge.position = edge
            vertex_edge.normal = normal
            vertex_edge.tex_coord = glm.vec3(0.5+tex_coord_radius*cos_theta, 0.5+tex_coord_radius*sin_theta, 0)

            vertices[i_vertex] = vertex_edge # 1 + j
            i_vertex += 1

            if j > 0:
                triangle = glm.uvec3(0, 0, 0)
                triangle[0] = 1 + j
                triangle[1] = 0
                triangle[2] = 1 + j - 1

                indices[i_index] = triangle
                i_index += 1
                self.generate_temp_TBN(vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]])

                yield
        
        del vertices[i_vertex:]
        del indices[i_index:]

    @property
    def n_divide(self):
        return self.__n_divide
    
    @n_divide.setter
    @Mesh.param_setter
    def n_divide(self, n_divide):
        self.__n_divide = n_divide

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
    def vertical(self):
        return self.__vertical
    
    @vertical.setter
    @Mesh.param_setter
    def vertical(self, flag:bool):
        self.__vertical = flag

    @property
    def a(self):
        return self.__a
    
    @a.setter
    @Mesh.param_setter
    def a(self, a:float):
        self.__a = a

    @property
    def b(self):
        return self.__b
    
    @b.setter
    @Mesh.param_setter
    def b(self, b:float):
        self.__b = b

    @property
    def normalize_tex_coord(self):
        return self.__normalize_tex_coord
    
    @normalize_tex_coord.setter
    @Mesh.param_setter
    def normalize_tex_coord(self, flag:bool):
        self.__normalize_tex_coord = flag