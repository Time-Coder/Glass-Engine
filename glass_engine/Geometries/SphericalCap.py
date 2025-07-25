from ..Mesh import Mesh

from glass.utils import checktype
from glass import Vertex

import glm
import math
from typing import Union


class SphericalCap(Mesh):

    @checktype
    def __init__(
        self,
        base_radius: float = 1,
        height: float = 0.5,
        color: Union[glm.vec3, glm.vec4] = glm.vec4(0.396, 0.74151, 0.69102, 1),
        back_color: Union[glm.vec3, glm.vec4, None] = None,
        n_lon_divide: int = 100,
        start_lon: float = 0,
        span_lon: float = 360,
        n_lat_divide: int = 50,
        name: str = "",
        block=True,
    ):
        Mesh.__init__(
            self, color=color, back_color=back_color,
            name=name, block=block
        )
        self.__base_radius = base_radius
        self.__height = height
        self.__start_lon = start_lon
        self.__span_lon = span_lon
        self.__n_lon_divide = n_lon_divide
        self.__n_lat_divide = n_lat_divide

    def build(self):
        self.is_closed = True
        vertices = self._vertices
        indices = self._indices
        base_radius = self.__base_radius
        height = self.__height
        radius = (base_radius**2 + height**2) / (2 * height)
        start_lon = self.__start_lon / 180 * math.pi
        span_lon = self.__span_lon / 180 * math.pi
        start_lat = math.asin(
            (base_radius**2 - height**2) / (base_radius**2 + height**2)
        )
        span_lat = math.pi / 2 - start_lat
        n_lon_divide = self.__n_lon_divide
        n_lat_divide = self.__n_lat_divide
        h_delta = (base_radius**2 - height**2) / (2 * height)

        i_vertex = 0
        i_index = 0

        vertex_bottom_center = Vertex()
        vertex_bottom_center.position = glm.vec3(0)
        vertex_bottom_center.normal = glm.vec3(0, 0, -1)
        vertex_bottom_center.tex_coord = glm.vec3(0.5, 0.5, 0)
        vertices[i_vertex] = vertex_bottom_center
        i_vertex += 1

        for i in range(n_lon_divide):
            theta = start_lon + span_lon * i / (n_lon_divide - 1)
            s = theta / (2 * math.pi)
            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)

            for j in range(n_lat_divide):
                phi = start_lat + span_lat * j / (n_lat_divide - 1)
                t = phi / math.pi + 0.5
                cos_phi = math.cos(phi)
                sin_phi = math.sin(phi)

                vertex_top = Vertex()
                vertex_top.tangent = (
                    2 * math.pi * radius * cos_phi * glm.vec3(-sin_theta, cos_theta, 0)
                )
                vertex_top.bitangent = (
                    math.pi
                    * radius
                    * glm.vec3(-sin_phi * cos_theta, -sin_phi * sin_theta, cos_phi)
                )
                vertex_top.normal = glm.vec3(
                    cos_phi * cos_theta, cos_phi * sin_theta, sin_phi
                )
                vertex_top.position = radius * vertex_top.normal
                vertex_top.position.z -= h_delta
                vertex_top.tex_coord = glm.vec3(s, t, 0)

                vertices[i_vertex] = vertex_top
                i_vertex += 1

                if i > 0 and j > 0:
                    triangle = glm.uvec3(0, 0, 0)
                    triangle[0] = i_vertex - 1
                    triangle[1] = i_vertex - 1 - n_lat_divide - 1
                    triangle[2] = i_vertex - 1 - n_lat_divide - 1 - 1
                    indices[i_index] = triangle
                    i_index += 1

                    triangle = glm.uvec3(0, 0, 0)
                    triangle[0] = i_vertex - 1
                    triangle[1] = i_vertex - 1 - n_lat_divide - 1 - 1
                    triangle[2] = i_vertex - 1 - 1
                    indices[i_index] = triangle
                    i_index += 1

                    yield

            vertex_bottom = Vertex()
            vertex_bottom.position = glm.vec3(
                base_radius * cos_theta, base_radius * sin_theta, 0
            )
            vertex_bottom.normal = glm.vec3(0, 0, -1)
            s = 0.5 + base_radius * cos_theta
            t = 0.5 + base_radius * sin_theta
            vertex_bottom.tex_coord = glm.vec3(s, t, 0)
            vertices[i_vertex] = vertex_bottom
            i_vertex += 1

            if i > 0:
                triangle = glm.uvec3(0, 0, 0)
                triangle[0] = i_vertex - 1
                triangle[1] = i_vertex - 1 - n_lat_divide - 1
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
    def n_lat_divide(self):
        return self.__n_lat_divide

    @n_lat_divide.setter
    @Mesh.param_setter
    def n_lat_divide(self, n: int):
        self.__n_lat_divide = n

    @property
    def n_lon_divide(self):
        return self.__n_lon_divide

    @n_lon_divide.setter
    @Mesh.param_setter
    def n_lon_divide(self, n: int):
        self.__n_lon_divide = n

    @property
    def start_lon(self):
        return self.__start_lon

    @start_lon.setter
    @Mesh.param_setter
    def start_lon(self, angle: float):
        self.__start_lon = angle

    @property
    def span_lon(self):
        return self.__span_lon

    @span_lon.setter
    @Mesh.param_setter
    def span_lon(self, angle: float):
        self.__span_lon = angle

    @property
    def base_radius(self):
        return self.__base_radius

    @base_radius.setter
    @Mesh.param_setter
    def base_radius(self, base_radius: float):
        self.__base_radius = base_radius

    @property
    def height(self):
        return self.__height

    @height.setter
    @Mesh.param_setter
    def height(self, height: float):
        self.__height = height
