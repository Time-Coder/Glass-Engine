from ..Mesh import Mesh

from glass.utils import checktype
from glass import Vertex

import glm
import math
from typing import Union, Optional


class Pyramid(Mesh):

    @checktype
    def __init__(
        self,
        n_sides: int = 4,
        start_side: int = 0,
        total_sides: Optional[int] = None,
        radius: float = 1,
        height: float = 1,
        color: Union[glm.vec3, glm.vec4] = glm.vec4(0.396, 0.74151, 0.69102, 1),
        back_color: Union[glm.vec3, glm.vec4, None] = None,
        normalize_st: bool = False,
        st_per_unit: float = 1,
        name: str = "",
        block: bool = True,
    ):
        Mesh.__init__(
            self, color=color, back_color=back_color,
            normalize_st=normalize_st,
            st_per_unit=st_per_unit,
            name=name, block=block
        )
        self.__radius = radius
        self.__height = height
        self.__start_side = start_side
        self.__total_sides = total_sides
        self.__n_sides = n_sides

    def build(self):
        self.is_closed = True
        vertices = self._vertices
        indices = self._indices
        radius = self.__radius
        height = self.__height
        start_side = self.__start_side
        total_sides = self.__total_sides
        if total_sides is None:
            total_sides = self.__n_sides
        total_sides = min(self.__n_sides, total_sides)
        n_sides = self.__n_sides

        i_vertex = 0
        i_index = 0

        # 棱锥底面中心点
        vertex_bottom_center = Vertex()
        vertex_bottom_center.position = glm.vec3(0)
        vertex_bottom_center.normal = glm.vec3(0, 0, -1)
        vertex_bottom_center.tex_coord = glm.vec3(0.5, 0.5, 0)

        vertices[i_vertex] = vertex_bottom_center
        i_vertex += 1

        tex_coord_bottom_radius = 0.5 if self.normalize_st else radius

        internal_radius = radius * math.cos(math.pi / n_sides)
        side_height = math.sqrt(internal_radius**2 + height**2)
        half_side_width = radius * math.sin(math.pi / n_sides)

        s1 = 0.5 - self.s_per_unit * half_side_width
        s2 = 0.5 + self.s_per_unit * half_side_width
        t = self.t_per_unit * side_height
        if self.normalize_st:
            t = 1
            s1 = 0.5 - half_side_width / side_height
            s2 = 0.5 + half_side_width / side_height

        for j in range(total_sides + 1):
            theta = 2 * math.pi * (j + start_side) / n_sides
            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)

            top = glm.vec3(0, 0, height)
            bottom = radius * glm.vec3(cos_theta, sin_theta, 0)

            vertex_top = Vertex()
            vertex_top.position = top
            vertex_top.tex_coord = glm.vec3(0.5, t, 0)

            vertex_side_bottom1 = Vertex()
            vertex_side_bottom1.position = bottom
            vertex_side_bottom1.tex_coord = glm.vec3(s1, 0, 0)

            vertex_side_bottom2 = Vertex()
            vertex_side_bottom2.position = bottom
            vertex_side_bottom2.tex_coord = glm.vec3(s2, 0, 0)

            vertex_bottom_bottom = Vertex()
            vertex_bottom_bottom.position = bottom
            vertex_bottom_bottom.normal = glm.vec3(0, 0, -1)
            vertex_bottom_bottom.tex_coord = glm.vec3(
                0.5 + self.s_per_unit * tex_coord_bottom_radius * cos_theta,
                0.5 + self.t_per_unit * tex_coord_bottom_radius * sin_theta,
                0,
            )

            vertices[i_vertex] = vertex_top  # 1 + 4*j
            i_vertex += 1

            vertices[i_vertex] = vertex_side_bottom1  # 1 + 4*j + 1
            i_vertex += 1

            vertices[i_vertex] = vertex_side_bottom2  # 1 + 4*j + 2
            i_vertex += 1

            vertices[i_vertex] = vertex_bottom_bottom  # 1 + 4*j + 3
            i_vertex += 1

            if j > 0:
                # 侧面
                triangle = glm.uvec3(0, 0, 0)
                triangle[0] = 1 + 4 * j + 1
                triangle[1] = 1 + 4 * j
                triangle[2] = 1 + 4 * j - 2
                indices[i_index] = triangle
                i_index += 1
                self.generate_temp_TBN(
                    vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]]
                )

                # 底面
                triangle = glm.uvec3(0, 0, 0)
                triangle[0] = 1 + 4 * j + 3
                triangle[1] = 1 + 4 * j - 1
                triangle[2] = 0
                indices[i_index] = triangle
                i_index += 1
                self.generate_temp_TBN(
                    vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]]
                )

                yield

        del vertices[i_vertex:]
        del indices[i_index:]

    @property
    def n_sides(self):
        return self.__n_sides

    @n_sides.setter
    @Mesh.param_setter
    def n_sides(self, n_sides):
        self.__n_sides = n_sides

    @property
    def start_side(self):
        return self.__start_side

    @start_side.setter
    @Mesh.param_setter
    def start_side(self, start_side: int):
        self.__start_side = start_side

    @property
    def total_sides(self):
        return self.__total_sides

    @total_sides.setter
    @Mesh.param_setter
    def total_sides(self, total_sides: int):
        self.__total_sides = total_sides

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    @Mesh.param_setter
    def radius(self, radius: float):
        self.__radius = radius

    @property
    def height(self):
        return self.__height

    @height.setter
    @Mesh.param_setter
    def height(self, height: float):
        self.__height = height
