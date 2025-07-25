from ..Mesh import Mesh
from ..algorithm import cos_angle_of

from glass import Vertex

import math
import glm
import numpy as np
from typing import Union


class Rotator(Mesh):
    def __init__(
        self,
        section: Union[list, tuple, np.ndarray],
        axis_start: glm.vec3 = glm.vec3(0),
        axis_stop: glm.vec3 = glm.vec3(0, 0, 1),
        n_divide: int = 100,
        start_angle: float = 0,
        span_angle: float = 360,
        color: Union[glm.vec3, glm.vec4] = glm.vec4(0.396, 0.74151, 0.69102, 1),
        back_color: Union[glm.vec3, glm.vec4, None] = None,
        surf_type: Mesh.SurfType = Mesh.SurfType.Auto,
        normalize_st: bool = False,
        st_per_unit: float = 1,
        name: str = "",
        block=True,
    ):
        Mesh.__init__(
            self, color=color, back_color=back_color,
            surf_type=surf_type,
            normalize_st=normalize_st,
            st_per_unit=st_per_unit,
            name=name, block=block,
        )
        self.__section = section
        self.__axis_start = axis_start
        self.__axis_stop = axis_stop
        self.__start_angle = start_angle
        self.__span_angle = span_angle
        self.__n_divide = n_divide

    def build(self):
        vertices = self._vertices
        indices = self._indices
        section = self.__used_section
        axis_start = self.__axis_start
        axis_stop = self.__axis_stop
        start_angle = self.__start_angle / 180 * math.pi
        span_angle = self.__span_angle / 180 * math.pi
        n_divide = self.__n_divide

        i_vertex = 0
        i_index = 0

        # 计算原点到轴的垂足 H
        A = axis_start
        B = axis_stop
        C = glm.vec3(0)
        AC = C - A
        AB = B - A
        AB = glm.normalize(AB)
        H = A + glm.dot(AC, AB) * AB

        # 计算 section 长度 L，section 距轴的最长距离 D
        L, D = 0, 0
        len_AB = glm.length(AB)
        len_section = len(section)
        for i in range(len_section):
            if i > 0:
                L += glm.length(section[i] - section[i - 1])

            d = glm.length(glm.cross(AB, section[i] - A)) / len_AB
            if d > D:
                D = d

        for i in range(n_divide):
            theta = start_angle + span_angle * i / (n_divide - 1)
            half_theta = theta / 2
            quat = glm.quat(math.cos(half_theta), math.sin(half_theta) * AB)

            l = 0
            for j in range(len_section):
                pos = quat * (section[j] - H) + H
                vertex = Vertex()
                vertex.position = pos
                vertex.normal = glm.vec3(0)

                if j > 0:
                    l += glm.length(section[j] - section[j - 1])

                if not self.normalize_st:
                    vertex.tex_coord = glm.vec3(
                        self.s_per_unit * D * theta,
                        1 - self.t_per_unit * l, 0
                    )
                else:
                    vertex.tex_coord = glm.vec3(D / L * theta, 1 - l / L, 0)

                vertices[i_vertex] = vertex
                i_vertex += 1

                if i > 0 and j > 0:
                    triangle = glm.uvec3(0, 0, 0)
                    triangle[0] = i_vertex - 1
                    triangle[1] = i_vertex - 2
                    triangle[2] = i_vertex - 2 - len_section
                    indices[i_index] = triangle
                    i_index += 1
                    self.generate_temp_TBN(
                        vertices[triangle[0]],
                        vertices[triangle[1]],
                        vertices[triangle[2]],
                    )

                    triangle = glm.uvec3(0, 0, 0)
                    triangle[0] = i_vertex - 1
                    triangle[1] = i_vertex - 2 - len_section
                    triangle[2] = i_vertex - 1 - len_section
                    indices[i_index] = triangle
                    i_index += 1
                    self.generate_temp_TBN(
                        vertices[triangle[0]],
                        vertices[triangle[1]],
                        vertices[triangle[2]],
                    )

                    yield

        del vertices[i_vertex:]
        del indices[i_index:]

    @property
    def section(self):
        return self.__section

    @section.setter
    @Mesh.param_setter
    def section(self, section: Union[list, tuple, np.ndarray]):
        self.__section = section

    @property
    def __used_section(self):
        should_duplicate_indices = set()
        for i in range(1, len(self.__section) - 1):
            v1 = self.__section[i - 1] - self.__section[i]
            v2 = self.__section[i + 1] - self.__section[i]
            cos_angle = cos_angle_of(v1, v2)
            if cos_angle > -0.9:
                should_duplicate_indices.add(i)

        used_section = []
        for i in range(len(self.__section)):
            used_section.append(self.__section[i])
            if i in should_duplicate_indices:
                used_section.append(self.__section[i])

        return used_section

    @property
    def axis_start(self):
        return self.__axis_start

    @axis_start.setter
    @Mesh.param_setter
    def axis_start(self, axis_start: glm.vec3):
        self.__axis_start = axis_start

    @property
    def axis_stop(self):
        return self.__axis_stop

    @axis_stop.setter
    @Mesh.param_setter
    def axis_stop(self, axis_stop: glm.vec3):
        self.__axis_stop = axis_stop

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
    def start_angle(self, start_angle: float):
        self.__start_angle = start_angle

    @property
    def span_angle(self):
        return self.__span_angle

    @span_angle.setter
    @Mesh.param_setter
    def span_angle(self, span_angle: float):
        self.__span_angle = span_angle
