from ..Mesh import Mesh

from glass.utils import checktype
from glass import Vertex

import glm
import math
from typing import Union


class CylinderSide(Mesh):

    @checktype
    def __init__(
        self,
        radius: float = 1,
        height: float = 1,
        start_angle: float = 0,
        span_angle: float = 360,
        n_divide: int = 100,
        color: Union[glm.vec3, glm.vec4] = glm.vec4(0.396, 0.74151, 0.69102, 1),
        back_color: Union[glm.vec3, glm.vec4, None] = None,
        normalize_st=False,
        st_per_unit=1,
        name: str = "",
        block=True,
    ):
        Mesh.__init__(
            self, color=color, back_color=back_color,
            normalize_st=normalize_st,
            st_per_unit=st_per_unit,
            name=name, block=block
        )
        self.__radius = radius
        self.__height = height
        self.__start_angle = start_angle
        self.__span_angle = span_angle
        self.__n_divide = n_divide

    def build(self):
        self.is_closed = False
        self.self_calculated_normal = True

        vertices = self._vertices
        indices = self._indices

        i_vertex = 0
        i_index = 0

        radius = self.__radius
        height = self.__height
        start_angle = self.__start_angle / 180 * math.pi
        span_angle = self.__span_angle / 180 * math.pi
        n_divide = self.__n_divide

        t = 1 if self.normalize_st else self.t_per_unit * height

        for j in range(n_divide):
            theta = start_angle + span_angle * j / (n_divide - 1)
            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)

            if self.normalize_st:
                s = (start_angle + theta) / (start_angle + span_angle)
            else:
                s = (start_angle + theta) * radius * self.s_per_unit

            top = glm.vec3(radius * cos_theta, radius * sin_theta, height)
            bottom = glm.vec3(radius * cos_theta, radius * sin_theta, 0)
            normal = glm.vec3(cos_theta, sin_theta, 0)

            vertex_top = Vertex()
            vertex_top.position = top
            vertex_top.normal = normal
            vertex_top.tex_coord = glm.vec3(s, t, 0)

            vertex_bottom = Vertex()
            vertex_bottom.position = bottom
            vertex_bottom.normal = normal
            vertex_bottom.tex_coord = glm.vec3(s, 0, 0)

            vertices[i_vertex] = vertex_top  # 2*j
            i_vertex += 1

            vertices[i_vertex] = vertex_bottom  # 2*j + 1
            i_vertex += 1

            if j > 0:
                # 侧面三角形 1
                triangle = glm.uvec3(0, 0, 0)
                triangle[0] = 2 * j + 1
                triangle[1] = 2 * j
                triangle[2] = 2 * j - 2
                indices[i_index] = triangle
                i_index += 1
                self.generate_temp_TBN(
                    vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]]
                )

                # 侧面三角形 2
                triangle = glm.uvec3(0, 0, 0)
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
    def n_divide(self):
        return self.__n_divide

    @n_divide.setter
    @Mesh.param_setter
    def n_divide(self, n_divide: int):
        self.__n_divide = n_divide

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
