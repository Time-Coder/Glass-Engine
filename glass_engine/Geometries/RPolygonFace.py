from ..Mesh import Mesh

from glass.utils import checktype
from glass import Vertex

import glm
import math


class RPolygonFace(Mesh):

    @checktype
    def __init__(
        self,
        n_sides: int = 5,
        start_side: int = 0,
        total_sides: int = None,
        radius: float = 1,
        color: (glm.vec3, glm.vec4) = glm.vec4(0.396, 0.74151, 0.69102, 1),
        back_color: (glm.vec3, glm.vec4) = None,
        vertical: bool = False,
        normalize_tex_coord: bool = False,
        name: str = "",
        block: bool = True,
    ):
        Mesh.__init__(self, color=color, back_color=back_color, name=name, block=block)
        self.__radius = radius
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
        radius = self.__radius
        start_side = self.__start_side
        total_sides = self.__total_sides
        if total_sides is None:
            total_sides = self.__n_sides
        total_sides = min(self.__n_sides, total_sides)
        n_sides = self.__n_sides
        vertical = self.__vertical
        normalize_tex_coord = self.__normalize_tex_coord

        i_vertex = 0
        i_index = 0

        normal = glm.vec3(0, 0, 1)
        if vertical:
            normal = glm.vec3(0, -1, 0)

        # 中心点
        vertex_center = Vertex()
        vertex_center.position = glm.vec3(0)
        vertex_center.normal = normal
        vertex_center.tex_coord = glm.vec3(0.5, 0.5, 0)

        vertices[i_vertex] = vertex_center
        i_vertex += 1

        tex_coord_radius = 0.5 if normalize_tex_coord else radius

        for j in range(total_sides + 1):
            theta = 2 * math.pi * (j + start_side) / n_sides
            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)

            edge = radius * glm.vec3(cos_theta, sin_theta, 0)
            if vertical:
                edge = radius * glm.vec3(cos_theta, 0, sin_theta)

            vertex_edge = Vertex()
            vertex_edge.position = edge
            vertex_edge.normal = normal
            vertex_edge.tex_coord = glm.vec3(
                0.5 + tex_coord_radius * cos_theta,
                0.5 + tex_coord_radius * sin_theta,
                0,
            )

            vertices[i_vertex] = vertex_edge  # 1 + j
            i_vertex += 1

            if j > 0:
                triangle = glm.uvec3(0, 0, 0)
                triangle[0] = 1 + j
                triangle[1] = 0
                triangle[2] = 1 + j - 1
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
    def n_sides(self, n_sides: int):
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
    def normalize_tex_coord(self):
        return self.__normalize_tex_coord

    @normalize_tex_coord.setter
    @Mesh.param_setter
    def normalize_tex_coord(self, flag: bool):
        self.__normalize_tex_coord = flag
