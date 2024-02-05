from ..Mesh import Mesh

from glass import Vertex

import glm
import math


class Torus(Mesh):
    def __init__(
        self,
        radius_tube: float = 0.5,
        radius_torus: float = 1,
        color: (glm.vec3, glm.vec4) = glm.vec4(0.396, 0.74151, 0.69102, 1),
        back_color: (glm.vec3, glm.vec4) = None,
        vertical: bool = False,
        normalize_tex_coord=False,
        n_lon_divide: int = 100,
        start_lon: float = 0,
        span_lon: float = 360,
        n_lat_divide: int = 100,
        start_lat: float = 0,
        span_lat: float = 360,
        name: str = "",
        block: bool = True,
    ):
        Mesh.__init__(self, color=color, back_color=back_color, name=name, block=block)
        self.__r = radius_tube
        self.__R = radius_torus
        self.__start_lon = start_lon
        self.__span_lon = span_lon
        self.__n_lon_divide = n_lon_divide
        self.__start_lat = start_lat
        self.__span_lat = span_lat
        self.__n_lat_divide = n_lat_divide
        self.__vertical = vertical
        self.__normalize_tex_coord = normalize_tex_coord
        self.start_building()

    def build(self):
        self.is_closed = True
        self.self_calculated_normal = True

        vertices = self.vertices
        indices = self.indices
        r = self.__r
        R = self.__R
        start_lon = self.__start_lon / 180 * math.pi
        span_lon = self.__span_lon / 180 * math.pi
        n_lon_divide = self.__n_lon_divide
        start_lat = self.__start_lat / 180 * math.pi
        span_lat = self.__span_lat / 180 * math.pi
        n_lat_divide = self.__n_lat_divide
        vertical = self.__vertical
        normalize_tex_coord = self.__normalize_tex_coord

        i_vertex = 0
        i_index = 0

        tube_perimeter = 2 * math.pi * r

        for i in range(n_lon_divide):
            theta = start_lon + span_lon * i / (n_lon_divide - 1)
            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)

            tube_center = R * glm.vec3(cos_theta, sin_theta, 0)
            s = R / r * theta / (2 * math.pi)
            if not normalize_tex_coord:
                s = 2 * math.pi * R * theta / (2 * math.pi)

            for j in range(n_lat_divide):
                phi = start_lat + span_lat * j / (n_lat_divide - 1)
                cos_phi = math.cos(phi)
                sin_phi = math.sin(phi)

                t = phi / (2 * math.pi)
                if not normalize_tex_coord:
                    t = tube_perimeter * phi / (2 * math.pi)

                vertex = Vertex()
                vertex.normal = glm.vec3(
                    cos_phi * cos_theta, cos_phi * sin_theta, sin_phi
                )
                vertex.position = tube_center + r * vertex.normal
                vertex.tex_coord = glm.vec3(s, t, 0)

                if vertical:
                    vertex.position = glm.vec3(
                        vertex.position.x, -vertex.position.z, vertex.position.y
                    )
                    vertex.normal = glm.vec3(
                        vertex.normal.x, -vertex.normal.z, vertex.normal.y
                    )

                vertices[i_vertex] = vertex
                i_vertex += 1

                if i > 0 and j > 0:
                    triangle = glm.uvec3(0, 0, 0)
                    triangle[0] = i_vertex - 1
                    triangle[1] = i_vertex - 1 - n_lat_divide
                    triangle[2] = i_vertex - 1 - n_lat_divide - 1
                    indices[i_index] = triangle
                    i_index += 1
                    self.generate_temp_TBN(
                        vertices[triangle[0]],
                        vertices[triangle[1]],
                        vertices[triangle[2]],
                    )

                    triangle = glm.uvec3(0, 0, 0)
                    triangle[0] = i_vertex - 1
                    triangle[1] = i_vertex - 1 - n_lat_divide - 1
                    triangle[2] = i_vertex - 1 - 1
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
    def radius_tube(self):
        return self.__r

    @radius_tube.setter
    @Mesh.param_setter
    def radius_tube(self, r: float):
        self.__r = r

    @property
    def radius_torus(self):
        return self.__R

    @radius_torus.setter
    @Mesh.param_setter
    def radius_torus(self, R: float):
        self.__R = R

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
    def start_lat(self):
        return self.__start_lat

    @start_lat.setter
    @Mesh.param_setter
    def start_lat(self, angle: float):
        self.__start_lat = angle

    @property
    def span_lat(self):
        return self.__span_lat

    @span_lat.setter
    @Mesh.param_setter
    def span_lat(self, angle: float):
        self.__span_lat = angle

    @property
    def normalize_tex_coord(self):
        return self.__normalize_tex_coord

    @normalize_tex_coord.setter
    @Mesh.param_setter
    def normalize_tex_coord(self, flag: bool):
        self.__normalize_tex_coord = flag

    @property
    def vertical(self):
        return self.__vertical

    @vertical.setter
    @Mesh.param_setter
    def vertical(self, flag: bool):
        self.__vertical = flag
