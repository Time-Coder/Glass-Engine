from ..Mesh import Mesh

from glass import Vertex

import glm
import math


class TrefoilKnot(Mesh):

    def __init__(
        self,
        tube_radius: float = 0.2,
        knot_radius: float = 1,
        color: (glm.vec3, glm.vec4) = glm.vec4(0.396, 0.74151, 0.69102, 1),
        back_color: (glm.vec3, glm.vec4) = None,
        vertical: bool = False,
        normalize_tex_coord=False,
        n_lon_divide: int = 200,
        start_lon: float = 0,
        span_lon: float = 360,
        n_lat_divide: int = 36,
        start_lat: float = 0,
        span_lat: float = 360,
        name: str = "",
        block: bool = True,
    ):

        Mesh.__init__(self, color=color, back_color=back_color, name=name, block=block)
        self.__tube_radius = tube_radius
        self.__knot_radius = knot_radius
        self.__vertical = vertical
        self.__normalize_tex_coord = normalize_tex_coord
        self.__n_lon_divide = n_lon_divide
        self.__start_lon = start_lon
        self.__span_lon = span_lon
        self.__n_lat_divide = n_lat_divide
        self.__start_lat = start_lat
        self.__span_lat = span_lat
        self.start_building()

    def build(self):
        self.is_closed = True
        self.self_calculated_normal = True

        vertices = self.vertices
        indices = self.indices
        r = self.__tube_radius
        R = self.__knot_radius / 3
        vertical = self.__vertical
        normalize_tex_coord = self.__normalize_tex_coord
        n_lon_divide = self.__n_lon_divide
        start_lon = self.__start_lon / 180 * math.pi
        span_lon = self.__span_lon / 180 * math.pi
        n_lat_divide = self.__n_lat_divide
        start_lat = self.__start_lat / 180 * math.pi
        span_lat = self.__span_lat / 180 * math.pi

        i_vertex = 0
        i_index = 0

        L = 0
        last_normalized_center = None
        for i in range(n_lon_divide):
            theta = start_lon + span_lon * i / (n_lon_divide - 1)
            sin_theta = math.sin(theta)
            cos_theta = math.cos(theta)
            sin_2theta = math.sin(2 * theta)
            cos_2theta = math.cos(2 * theta)
            sin_3theta = math.sin(3 * theta)
            cos_3theta = math.cos(3 * theta)

            x0 = sin_theta + 2 * sin_2theta
            y0 = cos_theta - 2 * cos_2theta
            z0 = -sin_3theta
            normalized_center = glm.vec3(x0, y0, z0)

            if i > 0:
                L += glm.length(normalized_center - last_normalized_center)

            last_normalized_center = normalized_center

            x0 *= R
            y0 *= R
            z0 *= R

            dx = cos_theta + 4 * cos_2theta
            dy = -sin_theta + 4 * sin_2theta
            dz = -3 * cos_3theta

            ddx = -sin_theta - 8 * sin_2theta
            ddy = -cos_theta + 8 * cos_2theta
            ddz = 9 * sin_3theta

            alpha = glm.normalize(glm.vec3(dx, dy, dz))
            gamma = glm.normalize(
                glm.cross(glm.vec3(dx, dy, dz), glm.vec3(ddx, ddy, ddz))
            )
            beta = glm.cross(gamma, alpha)

            for j in range(n_lat_divide):
                phi = start_lat + span_lat * j / (n_lat_divide - 1)

                normal = math.cos(phi) * gamma + math.sin(phi) * beta
                x = x0 + r * normal.x
                y = y0 + r * normal.y
                z = z0 + r * normal.z
                s = L
                t = r * phi
                if normalize_tex_coord:
                    t = t / r / (2 * math.pi)
                    s = s / r / (2 * math.pi)

                vertex = Vertex()
                vertex.position = glm.vec3(x, y, z)
                vertex.normal = normal
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
                    triangle[1] = i_vertex - 1 - 1 - n_lat_divide
                    triangle[2] = i_vertex - 1 - 1
                    indices[i_index] = triangle
                    i_index += 1
                    self.generate_temp_TBN(
                        vertices[triangle[0]],
                        vertices[triangle[1]],
                        vertices[triangle[2]],
                    )

                    triangle = glm.uvec3(0, 0, 0)
                    triangle[0] = i_vertex - 1
                    triangle[1] = i_vertex - 1 - n_lat_divide
                    triangle[2] = i_vertex - 1 - 1 - n_lat_divide
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
    def tube_radius(self):
        return self.__tube_radius

    @tube_radius.setter
    @Mesh.param_setter
    def tube_radius(self, radius: float):
        self.__tube_radius = radius

    @property
    def knot_radius(self):
        return self.__knot_radius

    @knot_radius.setter
    @Mesh.param_setter
    def knot_radius(self, radius: float):
        self.__knot_radius = radius

    @property
    def vertical(self):
        return self.__vertical

    @vertical.setter
    @Mesh.param_setter
    def vertical(self, flag: bool):
        self.__vertical = flag

    @property
    def normalize_tex_coord(self):
        return self.__normalize_tex_coord

    @normalize_tex_coord.setter
    @Mesh.param_setter
    def normalize_tex_coord(self, flag: bool):
        self.__normalize_tex_coord = flag

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
    def start_lon(self, angle_deg: float):
        self.__start_lon = angle_deg

    @property
    def span_lon(self):
        return self.__span_lon

    @span_lon.setter
    @Mesh.param_setter
    def span_lon(self, angle_deg: float):
        self.__span_lon = angle_deg

    @property
    def n_lat_divide(self):
        return self.__n_lat_divide

    @n_lat_divide.setter
    @Mesh.param_setter
    def n_lat_divide(self, n: int):
        self.__n_lat_divide = n

    @property
    def start_lat(self):
        return self.__start_lat

    @start_lat.setter
    @Mesh.param_setter
    def start_lat(self, angle_deg: float):
        self.__start_lat = angle_deg

    @property
    def span_lat(self):
        return self.__span_lat

    @span_lat.setter
    @Mesh.param_setter
    def span_lat(self, angle_deg: float):
        self.__span_lat = angle_deg
