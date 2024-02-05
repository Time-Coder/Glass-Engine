from ..Mesh import Mesh

from glass.utils import checktype
from glass import Vertex

import glm
import math


class ConeTrustum(Mesh):

    @checktype
    def __init__(
        self,
        bottom_radius: float = 2,
        top_radius: float = 1,
        height: float = 1,
        start_angle: float = 0,
        span_angle: float = 360,
        n_divide: int = 100,
        color: (glm.vec3, glm.vec4) = glm.vec4(0.396, 0.74151, 0.69102, 1),
        back_color: (glm.vec3, glm.vec4) = None,
        normalize_tex_coord=False,
        name: str = "",
        block=True,
    ):
        Mesh.__init__(self, color=color, back_color=back_color, name=name, block=block)
        self.__bottom_radius = bottom_radius
        self.__top_radius = top_radius
        self.__height = height
        self.__start_angle = start_angle
        self.__span_angle = span_angle
        self.__n_divide = n_divide
        self.__normalize_tex_coord = normalize_tex_coord
        self.start_building()

    def build(self):
        self.is_closed = True
        self.self_calculated_normal = True

        vertices = self.vertices
        indices = self.indices

        bottom_radius = self.__bottom_radius
        top_radius = self.__top_radius
        height = self.__height
        start_angle = self.__start_angle / 180 * math.pi
        span_angle = self.__span_angle / 180 * math.pi
        n_divide = self.__n_divide
        normalize_tex_coord = self.__normalize_tex_coord

        i_vertex = 0
        i_index = 0

        # 圆台顶面中心点
        vertex_top_center = Vertex()
        vertex_top_center.position = glm.vec3(0, 0, height)
        vertex_top_center.normal = glm.vec3(0, 0, 1)
        vertex_top_center.tex_coord = glm.vec3(0.5, 0.5, 0)

        vertices[i_vertex] = vertex_top_center
        i_vertex += 1

        # 圆台底面中心点
        vertex_bottom_center = Vertex()
        vertex_bottom_center.position = glm.vec3(0)
        vertex_bottom_center.normal = glm.vec3(0, 0, -1)
        vertex_bottom_center.tex_coord = glm.vec3(0.5, 0.5, 0)

        vertices[i_vertex] = vertex_bottom_center
        i_vertex += 1

        k = math.sqrt(1 + (height / (bottom_radius - top_radius)) ** 2)
        tex_coord_top_side_radius = 0.5 / bottom_radius * top_radius
        if not normalize_tex_coord:
            tex_coord_top_side_radius = top_radius * k

        tex_coord_bottom_side_radius = 0.5
        if not normalize_tex_coord:
            tex_coord_bottom_side_radius = bottom_radius * k

        tex_coord_bottom_radius = 0.5
        if not normalize_tex_coord:
            tex_coord_bottom_radius = bottom_radius

        tex_coord_top_radius = 0.5 / bottom_radius * top_radius
        if not normalize_tex_coord:
            tex_coord_top_radius = top_radius

        for j in range(n_divide):
            theta = start_angle + span_angle * j / (n_divide - 1)
            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)

            top = glm.vec3(top_radius * cos_theta, top_radius * sin_theta, height)
            bottom = glm.vec3(bottom_radius * cos_theta, bottom_radius * sin_theta, 0)

            to_right = glm.vec3(-sin_theta, cos_theta, 0)
            to_top = top - bottom
            normal = glm.normalize(glm.cross(to_right, to_top))

            vertex_top_top = Vertex()
            vertex_top_top.position = top
            vertex_top_top.normal = glm.vec3(0, 0, 1)
            vertex_top_top.tex_coord = glm.vec3(
                0.5 + tex_coord_top_radius * cos_theta,
                0.5 + tex_coord_top_radius * sin_theta,
                0,
            )

            vertex_top_side = Vertex()
            vertex_top_side.position = top
            vertex_top_side.normal = normal
            vertex_top_side.tex_coord = glm.vec3(
                0.5 + tex_coord_top_side_radius * cos_theta,
                0.5 + tex_coord_top_side_radius * sin_theta,
                0,
            )

            vertex_bottom_side = Vertex()
            vertex_bottom_side.position = bottom
            vertex_bottom_side.normal = normal
            vertex_bottom_side.tex_coord = glm.vec3(
                0.5 + tex_coord_bottom_side_radius * cos_theta,
                0.5 + tex_coord_bottom_side_radius * sin_theta,
                0,
            )

            vertex_bottom_bottom = Vertex()
            vertex_bottom_bottom.position = bottom
            vertex_bottom_bottom.normal = glm.vec3(0, 0, -1)
            vertex_bottom_bottom.tex_coord = glm.vec3(
                0.5 + tex_coord_bottom_radius * cos_theta,
                0.5 + tex_coord_bottom_radius * sin_theta,
                0,
            )

            vertices[i_vertex] = vertex_top_top  # 2 + 4*j
            i_vertex += 1

            vertices[i_vertex] = vertex_top_side  # 2 + 4*j + 1
            i_vertex += 1

            vertices[i_vertex] = vertex_bottom_side  # 2 + 4*j + 2
            i_vertex += 1

            vertices[i_vertex] = vertex_bottom_bottom  # 2 + 4*j + 3
            i_vertex += 1

            if j > 0:
                # 圆台顶面
                triangle = glm.uvec3(0, 0, 0)
                triangle[0] = 2 + 4 * j
                triangle[1] = 0
                triangle[2] = 2 + 4 * j - 4
                indices[i_index] = triangle
                i_index += 1
                self.generate_temp_TBN(
                    vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]]
                )

                # 圆台侧面 1
                triangle = glm.uvec3(0, 0, 0)
                triangle[0] = 2 + 4 * j + 2
                triangle[1] = 2 + 4 * j + 1
                triangle[2] = 2 + 4 * j - 3
                indices[i_index] = triangle
                i_index += 1
                self.generate_temp_TBN(
                    vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]]
                )

                # 圆台侧面 2
                triangle = glm.uvec3(0, 0, 0)
                triangle[0] = 2 + 4 * j + 2
                triangle[1] = 2 + 4 * j - 3
                triangle[2] = 2 + 4 * j - 2
                indices[i_index] = triangle
                i_index += 1
                self.generate_temp_TBN(
                    vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]]
                )

                # 圆台底面
                triangle = glm.uvec3(0, 0, 0)
                triangle[0] = 2 + 4 * j + 3
                triangle[1] = 2 + 4 * j - 1
                triangle[2] = 1
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
    def bottom_radius(self):
        return self.__bottom_radius

    @bottom_radius.setter
    @Mesh.param_setter
    def bottom_radius(self, bottom_radius: float):
        self.__bottom_radius = bottom_radius

    @property
    def top_radius(self):
        return self.__top_radius

    @top_radius.setter
    @Mesh.param_setter
    def top_radius(self, top_radius: float):
        self.__top_radius = top_radius

    @property
    def height(self):
        return self.__height

    @height.setter
    @Mesh.param_setter
    def height(self, height: float):
        self.__height = height

    @property
    def normalize_tex_coord(self):
        return self.__normalize_tex_coord

    @normalize_tex_coord.setter
    @Mesh.param_setter
    def normalize_tex_coord(self, flag: bool):
        self.__normalize_tex_coord = flag
