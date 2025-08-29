from ..Mesh import Mesh

from glass.utils import checktype
from glass import Vertex

import cgmath as cgm
import math
from typing import Union


class TorusFace(Mesh):

    @checktype
    def __init__(
        self,
        inner_radius: float = 1,
        outer_radius: float = 2,
        color: Union[cgm.vec3, cgm.vec4] = cgm.vec4(0.396, 0.74151, 0.69102, 1),
        back_color: Union[cgm.vec3, cgm.vec4, None] = None,
        n_divide: int = 100,
        start_angle: float = 0,
        span_angle: float = 360,
        vertical: bool = False,
        normalize_st: bool = False,
        st_per_unit:float = 1,
        name: str = "",
        block: bool = True,
    ):
        Mesh.__init__(self, color=color, back_color=back_color, name=name, block=block)
        self.__inner_radius = inner_radius
        self.__outer_radius = outer_radius
        self.__start_angle = start_angle
        self.__span_angle = span_angle
        self.__n_divide = n_divide
        self.__vertical = vertical

    def build(self):
        self.is_closed = False
        self.self_calculated_normal = True

        vertices = self._vertices
        indices = self._indices
        inner_radius = self.__inner_radius
        outer_radius = self.__outer_radius
        start_angle = self.__start_angle / 180 * math.pi
        span_angle = self.__span_angle / 180 * math.pi
        n_divide = self.__n_divide
        vertical = self.__vertical

        i_vertex = 0
        i_index = 0

        tex_coord_outer_radius = outer_radius
        tex_coord_inner_radius = inner_radius
        if self.normalize_st:
            tex_coord_outer_radius = 0.5
            tex_coord_inner_radius = 0.5 * inner_radius / outer_radius

        normal = cgm.vec3(0, 0, 1)
        if vertical:
            normal = cgm.vec3(0, -1, 0)

        for j in range(n_divide):
            theta = start_angle + span_angle * j / (n_divide - 1)
            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)

            edge_inner = inner_radius * cgm.vec3(cos_theta, sin_theta, 0)
            edge_outer = outer_radius * cgm.vec3(cos_theta, sin_theta, 0)
            if vertical:
                edge_inner = inner_radius * cgm.vec3(cos_theta, 0, sin_theta)
                edge_outer = outer_radius * cgm.vec3(cos_theta, 0, sin_theta)

            vertex_inner = Vertex()
            vertex_inner.position = edge_inner
            vertex_inner.normal = normal
            vertex_inner.tex_coord = cgm.vec3(
                0.5 + tex_coord_inner_radius * cos_theta,
                0.5 + tex_coord_inner_radius * sin_theta,
                0,
            )

            vertex_outer = Vertex()
            vertex_outer.position = edge_outer
            vertex_outer.normal = normal
            vertex_outer.tex_coord = cgm.vec3(
                0.5 + self.s_per_unit * tex_coord_outer_radius * cos_theta,
                0.5 + self.t_per_unit * tex_coord_outer_radius * sin_theta,
                0,
            )

            vertices[i_vertex] = vertex_inner  # 2*j
            i_vertex += 1

            vertices[i_vertex] = vertex_outer  # 2*j + 1
            i_vertex += 1

            if j > 0:
                triangle = cgm.uvec3(0, 0, 0)
                triangle[0] = 2 * j + 1
                triangle[1] = 2 * j
                triangle[2] = 2 * j - 2
                indices[i_index] = triangle
                i_index += 1
                self.generate_temp_TBN(
                    vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]]
                )

                triangle = cgm.uvec3(0, 0, 0)
                triangle[0] = 2 * j + 1
                triangle[1] = 2 * j - 2
                triangle[2] = 2 * j - 1
                indices[i_index] = triangle
                i_index += 1
                self.generate_temp_TBN(
                    vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]]
                )

                yield

        del vertices[i_vertex:]
        del indices[i_index:]

    @property
    def start_angle(self):
        return self.__start_angle

    @start_angle.setter
    @Mesh.param_setter
    def start_angle(self, angle: float):
        self.__start_angle = angle

    @property
    def span_angle(self):
        return self.__span_angle

    @span_angle.setter
    @Mesh.param_setter
    def span_angle(self, angle: float):
        self.__span_angle = angle

    @property
    def n_divide(self):
        return self.__n_divide

    @n_divide.setter
    @Mesh.param_setter
    def n_divide(self, n_divide):
        self.__n_divide = n_divide

    @property
    def vertical(self):
        return self.__vertical

    @vertical.setter
    @Mesh.param_setter
    def vertical(self, flag: bool):
        self.__vertical = flag

    @property
    def inner_radius(self):
        return self.__inner_radius

    @inner_radius.setter
    @Mesh.param_setter
    def inner_radius(self, inner_radius: float):
        self.__inner_radius = inner_radius

    @property
    def outer_radius(self):
        return self.__outer_radius

    @outer_radius.setter
    @Mesh.param_setter
    def outer_radius(self, outer_radius: float):
        self.__outer_radius = outer_radius
