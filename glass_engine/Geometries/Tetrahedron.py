from ..Mesh import Mesh

from glass.utils import checktype
from glass import Vertex

import glm
import math


def init_Tetrahedron(cls):
    sqrt_6 = math.sqrt(6)
    sqrt_2 = math.sqrt(2)
    sqrt_3 = math.sqrt(3)
    cls.edge_length = 2 / 3 * sqrt_6
    cls.base_positions = [
        glm.normalize(glm.vec3(2 / 3 * sqrt_2, 0, -1 / 3)),  # 0
        glm.normalize(glm.vec3(-sqrt_2 / 3, sqrt_6 / 3, -1 / 3)),  # 1
        glm.normalize(glm.vec3(-sqrt_2 / 3, -sqrt_6 / 3, -1 / 3)),  # 2
        glm.normalize(glm.vec3(0, 0, 1)),  # 3
    ]

    cls.base_indices = [
        glm.uvec3(0, 2, 1),
        glm.uvec3(3, 0, 1),
        glm.uvec3(3, 1, 2),
        glm.uvec3(3, 2, 0),
    ]

    cls.fixed_vertices = []
    for index in cls.base_indices:
        v1 = cls.base_positions[index[1]] - cls.base_positions[index[0]]
        v2 = cls.base_positions[index[2]] - cls.base_positions[index[0]]
        normal = glm.normalize(glm.cross(v1, v2))

        vertex1 = Vertex(
            position=cls.base_positions[index[0]],
            normal=normal,
            tex_coord=glm.vec3(0.5, 1, 0),
        )
        vertex2 = Vertex(
            position=cls.base_positions[index[1]],
            normal=normal,
            tex_coord=glm.vec3(0.5 - sqrt_3 / 4, 0.25, 0),
        )
        vertex3 = Vertex(
            position=cls.base_positions[index[2]],
            normal=normal,
            tex_coord=glm.vec3(0.5 + sqrt_3 / 4, 0.25, 0),
        )
        cls.fixed_vertices.append(vertex1)
        cls.fixed_vertices.append(vertex2)
        cls.fixed_vertices.append(vertex3)

    return cls


@init_Tetrahedron
class Tetrahedron(Mesh):

    @checktype
    def __init__(
        self,
        radius=1,
        color: (glm.vec3, glm.vec4) = glm.vec4(0.396, 0.74151, 0.69102, 1),
        back_color: (glm.vec3, glm.vec4) = None,
        normalize_tex_coord=False,
        name: str = "",
    ):
        Mesh.__init__(self, color=color, back_color=back_color, name=name, block=True)
        self.__radius = radius
        self.__normalize_tex_coord = normalize_tex_coord
        self.start_building()

    def build(self):
        self.is_closed = True
        vertices = self.vertices
        indices = self.indices
        radius = self.__radius
        normalize_tex_coord = self.__normalize_tex_coord

        for i, fix_vert in enumerate(Tetrahedron.fixed_vertices):
            tex_coord = fix_vert.tex_coord
            if not normalize_tex_coord:
                tex_coord = 2 * radius * (
                    tex_coord - glm.vec3(0.5, 0.5, 0)
                ) * Tetrahedron.edge_length / math.sqrt(3) + glm.vec3(0.5, 0.5, 0)

            vertices[i] = Vertex(
                position=radius * fix_vert.position,
                normal=fix_vert.normal,
                tex_coord=tex_coord,
            )

        for i in range(0, len(Tetrahedron.fixed_vertices), 3):
            indices[int(i / 3)] = glm.uvec3(i, i + 1, i + 2)
            self.generate_temp_TBN(vertices[i], vertices[i + 1], vertices[i + 2])

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
