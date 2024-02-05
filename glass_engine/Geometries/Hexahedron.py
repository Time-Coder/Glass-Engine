from ..Mesh import Mesh

from glass.utils import checktype
from glass import Vertex

import glm
import math


def init_Hexahedron(cls):
    cls.edge_length = 2 / 3 * math.sqrt(3)
    cls.base_positions = [
        glm.normalize(glm.vec3(-1, -1, -1)),  # 0
        glm.normalize(glm.vec3(1, -1, -1)),  # 1
        glm.normalize(glm.vec3(1, 1, -1)),  # 2
        glm.normalize(glm.vec3(-1, 1, -1)),  # 3
        glm.normalize(glm.vec3(-1, -1, 1)),  # 4
        glm.normalize(glm.vec3(1, -1, 1)),  # 5
        glm.normalize(glm.vec3(1, 1, 1)),  # 6
        glm.normalize(glm.vec3(-1, 1, 1)),  # 7
    ]

    cls.base_indices = [
        # 下面
        glm.uvec3(3, 2, 1),
        glm.uvec3(3, 1, 0),
        # 上面
        glm.uvec3(4, 5, 6),
        glm.uvec3(4, 6, 7),
        # 左面
        glm.uvec3(3, 0, 4),
        glm.uvec3(3, 4, 7),
        # 右面
        glm.uvec3(1, 2, 6),
        glm.uvec3(1, 6, 5),
        # 前面
        glm.uvec3(0, 1, 5),
        glm.uvec3(0, 5, 4),
        # 后面
        glm.uvec3(2, 3, 7),
        glm.uvec3(2, 7, 6),
    ]

    cls.fixed_vertices = []
    for i, index in enumerate(cls.base_indices):
        pos0 = cls.base_positions[index[0]]
        pos1 = cls.base_positions[index[1]]
        pos2 = cls.base_positions[index[2]]

        tex_coord0 = glm.vec3(0)
        tex_coord1 = glm.vec3(1, 0, 0)
        tex_coord2 = glm.vec3(1, 1, 0)
        if i % 2 == 1:
            tex_coord0 = glm.vec3(0)
            tex_coord1 = glm.vec3(1, 1, 0)
            tex_coord2 = glm.vec3(0, 1, 0)

        v1 = pos1 - pos0
        v2 = pos2 - pos0
        normal = glm.normalize(glm.cross(v1, v2))

        vertex0 = Vertex(position=pos0, normal=normal, tex_coord=tex_coord0)
        vertex1 = Vertex(position=pos1, normal=normal, tex_coord=tex_coord1)
        vertex2 = Vertex(position=pos2, normal=normal, tex_coord=tex_coord2)
        cls.fixed_vertices.append(vertex0)
        cls.fixed_vertices.append(vertex1)
        cls.fixed_vertices.append(vertex2)

    return cls


@init_Hexahedron
class Hexahedron(Mesh):

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
        self.self_calculated_normal = True

        vertices = self.vertices
        indices = self.indices
        radius = self.__radius
        normalize_tex_coord = self.__normalize_tex_coord

        for i, fix_vert in enumerate(Hexahedron.fixed_vertices):
            tex_coord = fix_vert.tex_coord
            if not normalize_tex_coord:
                tex_coord = tex_coord * Hexahedron.edge_length

            vertices[i] = Vertex(
                position=radius * fix_vert.position,
                normal=fix_vert.normal,
                tex_coord=tex_coord,
            )

        for i in range(0, len(Hexahedron.fixed_vertices), 3):
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
