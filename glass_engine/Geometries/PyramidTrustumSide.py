from ..Mesh import Mesh

from glass.utils import checktype
from glass import Vertex

import glm
import math

class PyramidTrustumSide(Mesh):

    @checktype
    def __init__(self, n_sides:int=5, start_side:int=0, total_sides:int=None,
                 bottom_radius:float=2, top_radius:float=1, height:float=1,
                 color:(glm.vec3,glm.vec4)=glm.vec4(0.396, 0.74151, 0.69102, 1), back_color:(glm.vec3,glm.vec4)=None,
                 normalize_tex_coord:bool=False, name:str="", block:bool=True):
        Mesh.__init__(self, color=color, back_color=back_color, name=name, block=block)
        self.__bottom_radius = bottom_radius
        self.__top_radius = top_radius
        self.__height = height
        self.__start_side = start_side
        self.__total_sides = total_sides
        self.__n_sides = n_sides
        self.__normalize_tex_coord = normalize_tex_coord
        self.start_building()

    def build(self):
        self.is_closed = False
        vertices = self.vertices
        indices = self.indices
        bottom_radius = self.__bottom_radius
        top_radius = self.__top_radius
        height = self.__height
        start_side = self.__start_side
        total_sides = self.__total_sides
        if total_sides is None:
            total_sides = self.__n_sides
        total_sides = min(self.__n_sides, total_sides)
        n_sides = self.__n_sides
        normalize_tex_coord = self.__normalize_tex_coord

        i_vertex = 0
        i_index = 0

        half_top_side_width = top_radius * math.sin(math.pi/n_sides)
        half_bottom_side_width = bottom_radius * math.sin(math.pi/n_sides)
        side_height = math.sqrt(height**2 + ((bottom_radius-top_radius)*math.cos(math.pi/n_sides))**2)
        s1_top = 0.5 - half_top_side_width
        s2_top = 0.5 + half_top_side_width
        s1_bottom = 0.5 - half_bottom_side_width
        s2_bottom = 0.5 + half_bottom_side_width
        t = side_height
        if normalize_tex_coord:
            t = 1
            s1_top = 0.5 - half_top_side_width/side_height
            s2_top = 0.5 + half_top_side_width/side_height
            s1_bottom = 0.5 - half_bottom_side_width/side_height
            s2_bottom = 0.5 + half_bottom_side_width/side_height

        for j in range(total_sides+1):
            theta = 2*math.pi*(j+start_side)/n_sides
            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)

            top = glm.vec3(top_radius*cos_theta, top_radius*sin_theta, height)
            bottom = bottom_radius * glm.vec3(cos_theta, sin_theta, 0)

            vertex_side_top1 = Vertex()
            vertex_side_top1.position = top
            vertex_side_top1.tex_coord = glm.vec3(s1_top, t, 0)

            vertex_side_top2 = Vertex()
            vertex_side_top2.position = top
            vertex_side_top2.tex_coord = glm.vec3(s2_top, t, 0)

            vertex_side_bottom1 = Vertex()
            vertex_side_bottom1.position = bottom
            vertex_side_bottom1.tex_coord = glm.vec3(s1_bottom, 0, 0)

            vertex_side_bottom2 = Vertex()
            vertex_side_bottom2.position = bottom
            vertex_side_bottom2.tex_coord = glm.vec3(s2_bottom, 0, 0)

            vertices[i_vertex] = vertex_side_top1 # 4*j
            i_vertex += 1

            vertices[i_vertex] = vertex_side_top2 # 4*j + 1
            i_vertex += 1

            vertices[i_vertex] = vertex_side_bottom1 # 4*j + 2
            i_vertex += 1

            vertices[i_vertex] = vertex_side_bottom2 # 4*j + 3
            i_vertex += 1

            if j > 0:
                # 棱台侧面 1
                triangle = glm.uvec3(0, 0, 0)
                triangle[0] = 4*j + 2
                triangle[1] = 4*j
                triangle[2] = 4*j - 3
                indices[i_index] = triangle
                i_index += 1
                self.generate_temp_TBN(vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]])

                # 棱台侧面 2
                triangle = glm.uvec3(0, 0, 0)
                triangle[0] = 4*j + 2
                triangle[1] = 4*j - 3
                triangle[2] = 4*j - 1
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
    def bottom_radius(self):
        return self.__bottom_radius
    
    @bottom_radius.setter
    @Mesh.param_setter
    def bottom_radius(self, bottom_radius:float):
        self.__bottom_radius = bottom_radius

    @property
    def top_radius(self):
        return self.__top_radius
    
    @top_radius.setter
    @Mesh.param_setter
    def top_radius(self, top_radius:float):
        self.__top_radius = top_radius

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