from ..Mesh import Mesh

from glass.utils import checktype
from glass import Vertex

import glm
import math

class HollowRPolygonFace(Mesh):

    @checktype
    def __init__(self, n_sides:int=5, start_side:int=0, total_sides:int=None,
                 inner_radius:float=1, outer_radius:float=2,
                 color:(glm.vec3,glm.vec4)=glm.vec4(0.396, 0.74151, 0.69102, 1), back_color:(glm.vec3,glm.vec4)=None,
                 vertical:bool=False,
                 normalize_tex_coord=False, name:str="", block:bool=True):
        Mesh.__init__(self, color=color, back_color=back_color, name=name, block=block)
        self.__inner_radius = inner_radius
        self.__outer_radius = outer_radius
        self.__start_side = start_side
        self.__total_sides = total_sides
        self.__n_sides = n_sides
        self.__vertical = vertical
        self.__normalize_tex_coord = normalize_tex_coord
        self.start_building()

    def build(self):
        self.is_closed = False
        self.self_calculated_normal = True

        vertices = self.vertices
        indices = self.indices
        inner_radius = self.__inner_radius
        outer_radius = self.__outer_radius
        start_side = self.__start_side
        total_sides = self.__total_sides
        if total_sides is None:
            total_sides = self.__n_sides
        total_sides = min(total_sides, self.__n_sides)

        n_sides = self.__n_sides
        vertical = self.__vertical
        normalize_tex_coord = self.__normalize_tex_coord

        i_vertex = 0
        i_index = 0

        normal = glm.vec3(0, 0, 1)
        if vertical:
            normal = glm.vec3(0, -1, 0)

        tex_coord_inner_radius = inner_radius
        tex_coord_outer_radius = outer_radius
        if normalize_tex_coord:
            tex_coord_outer_radius = 0.5
            tex_coord_inner_radius = 0.5 * inner_radius / outer_radius

        for j in range(total_sides+1):
            theta = 2*math.pi*(j + start_side)/n_sides
            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)

            edge_inner = inner_radius*glm.vec3(cos_theta, sin_theta, 0)
            edge_outer = outer_radius*glm.vec3(cos_theta, sin_theta, 0)
            if vertical:
                edge_inner = inner_radius*glm.vec3(cos_theta, 0, sin_theta)
                edge_outer = outer_radius*glm.vec3(cos_theta, 0, sin_theta)

            vertex_inner = Vertex()
            vertex_inner.position = edge_inner
            vertex_inner.normal = normal
            vertex_inner.tex_coord = glm.vec3(0.5+tex_coord_inner_radius*cos_theta, 0.5+tex_coord_inner_radius*sin_theta, 0)

            vertex_outer = Vertex()
            vertex_outer.position = edge_outer
            vertex_outer.normal = normal
            vertex_outer.tex_coord = glm.vec3(0.5+tex_coord_outer_radius*cos_theta, 0.5+tex_coord_outer_radius*sin_theta, 0)

            vertices[i_vertex] = vertex_inner # 2*j
            i_vertex += 1

            vertices[i_vertex] = vertex_outer # 2*j + 1
            i_vertex += 1

            if j > 0:
                triangle = glm.uvec3(0, 0, 0)
                triangle[0] = 2*j + 1
                triangle[1] = 2*j
                triangle[2] = 2*j - 2
                indices[i_index] = triangle
                i_index += 1
                self.generate_temp_TBN(vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]])

                triangle = glm.uvec3(0, 0, 0)
                triangle[0] = 2*j + 1
                triangle[1] = 2*j - 2
                triangle[2] = 2*j - 1
                indices[i_index] = triangle
                i_index += 1
                self.generate_temp_TBN(vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]])

                yield

        del vertices[i_vertex:]
        del indices[i_index:]

    @property
    def n_sides(self):
        return self.__n_sides
    
    @n_sides.setter
    @Mesh.param_setter
    def n_sides(self, n_sides:int):        
        self.__n_sides = n_sides

    @property
    def start_side(self):
        return self.__start_side
    
    @start_side.setter
    @Mesh.param_setter
    def start_side(self, start_side:int):
        self.__start_side = start_side

    @property
    def total_sides(self):
        return self.__total_sides

    @total_sides.setter
    @Mesh.param_setter
    def total_sides(self, total_sides:int):
        self.__total_sides = total_sides

    @property
    def inner_radius(self):
        return self.__inner_radius
    
    @inner_radius.setter
    @Mesh.param_setter
    def inner_radius(self, inner_radius:float):
        self.__inner_radius = inner_radius

    @property
    def outer_radius(self):
        return self.__outer_radius
    
    @outer_radius.setter
    @Mesh.param_setter
    def outer_radius(self, outer_radius:float):
        self.__outer_radius = outer_radius

    @property
    def normalize_tex_coord(self):
        return self.__normalize_tex_coord
    
    @normalize_tex_coord.setter
    @Mesh.param_setter
    def normalize_tex_coord(self, flag:bool):
        self.__normalize_tex_coord = flag