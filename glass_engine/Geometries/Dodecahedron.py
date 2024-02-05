from ..Mesh import Mesh

from glass.utils import checktype
from glass import Vertex

import glm
import math


def init_Dodecahedron(cls):
    phi1 = (math.sqrt(5) - 1) / 2
    phi2 = (math.sqrt(5) + 1) / 2
    cls.base_positions = [
        glm.normalize(glm.vec3(-1, -1, -1)),  # 0
        glm.normalize(glm.vec3(1, -1, -1)),  # 1
        glm.normalize(glm.vec3(1, 1, -1)),  # 2
        glm.normalize(glm.vec3(-1, 1, -1)),  # 3
        glm.normalize(glm.vec3(-1, -1, 1)),  # 4
        glm.normalize(glm.vec3(1, -1, 1)),  # 5
        glm.normalize(glm.vec3(1, 1, 1)),  # 6
        glm.normalize(glm.vec3(-1, 1, 1)),  # 7
        glm.normalize(glm.vec3(0, -phi2, -phi1)),  # 8
        glm.normalize(glm.vec3(0, phi2, -phi1)),  # 9
        glm.normalize(glm.vec3(0, phi2, phi1)),  # 10
        glm.normalize(glm.vec3(0, -phi2, phi1)),  # 11
        glm.normalize(glm.vec3(-phi1, 0, -phi2)),  # 12
        glm.normalize(glm.vec3(phi1, 0, -phi2)),  # 13
        glm.normalize(glm.vec3(phi1, 0, phi2)),  # 14
        glm.normalize(glm.vec3(-phi1, 0, phi2)),  # 15
        glm.normalize(glm.vec3(-phi2, -phi1, 0)),  # 16
        glm.normalize(glm.vec3(phi2, -phi1, 0)),  # 17
        glm.normalize(glm.vec3(phi2, phi1, 0)),  # 18
        glm.normalize(glm.vec3(-phi2, phi1, 0)),  # 19
    ]

    cls.base_indices = [
        # 0
        glm.uvec3(4, 11, 5),
        glm.uvec3(4, 5, 14),
        glm.uvec3(4, 14, 15),
        # 1
        glm.uvec3(8, 1, 17),
        glm.uvec3(8, 17, 5),
        glm.uvec3(8, 5, 11),
        # 2
        glm.uvec3(0, 8, 11),
        glm.uvec3(0, 11, 4),
        glm.uvec3(0, 4, 16),
        # 3
        glm.uvec3(17, 18, 6),
        glm.uvec3(17, 6, 14),
        glm.uvec3(17, 14, 5),
        # 4
        glm.uvec3(13, 2, 18),
        glm.uvec3(13, 18, 17),
        glm.uvec3(13, 17, 1),
        # 5
        glm.uvec3(12, 13, 1),
        glm.uvec3(12, 1, 8),
        glm.uvec3(12, 8, 0),
        # 6
        glm.uvec3(3, 12, 0),
        glm.uvec3(3, 0, 16),
        glm.uvec3(3, 16, 19),
        # 7
        glm.uvec3(19, 16, 4),
        glm.uvec3(19, 4, 15),
        glm.uvec3(19, 15, 7),
        # 8
        glm.uvec3(6, 10, 7),
        glm.uvec3(6, 7, 15),
        glm.uvec3(6, 15, 14),
        # 9
        glm.uvec3(2, 9, 10),
        glm.uvec3(2, 10, 6),
        glm.uvec3(2, 6, 18),
        # 10
        glm.uvec3(13, 12, 3),
        glm.uvec3(13, 3, 9),
        glm.uvec3(13, 9, 2),
        # 11
        glm.uvec3(9, 3, 19),
        glm.uvec3(9, 19, 7),
        glm.uvec3(9, 7, 10),
    ]

    cls.edge_length = 2 * phi1 / math.sqrt(3)

    cls.fixed_vertices = []
    theta = 2 / 5 * math.pi
    for i, index in enumerate(cls.base_indices):
        pos0 = cls.base_positions[index[0]]
        pos1 = cls.base_positions[index[1]]
        pos2 = cls.base_positions[index[2]]

        tex_coord0 = None
        tex_coord1 = None
        tex_coord2 = None
        if i % 3 == 0:
            tex_coord0 = 0.5 * glm.vec3(
                1 - math.sin(2 * theta), 1 + math.cos(2 * theta), 0
            )
            tex_coord1 = 0.5 * glm.vec3(
                1 + math.sin(2 * theta), 1 + math.cos(2 * theta), 0
            )
            tex_coord2 = 0.5 * glm.vec3(1 + math.sin(theta), 1 + math.cos(theta), 0)
        elif i % 3 == 1:
            tex_coord0 = 0.5 * glm.vec3(
                1 - math.sin(2 * theta), 1 + math.cos(2 * theta), 0
            )
            tex_coord1 = 0.5 * glm.vec3(1 + math.sin(theta), 1 + math.cos(theta), 0)
            tex_coord2 = glm.vec3(0.5, 1, 0)
        elif i % 3 == 2:
            tex_coord0 = 0.5 * glm.vec3(
                1 - math.sin(2 * theta), 1 + math.cos(2 * theta), 0
            )
            tex_coord1 = glm.vec3(0.5, 1, 0)
            tex_coord2 = 0.5 * glm.vec3(1 - math.sin(theta), 1 + math.cos(theta), 0)

        v1 = pos1 - pos0
        v2 = pos2 - pos0
        normal = glm.normalize(glm.cross(v1, v2))

        vertex1 = Vertex(position=pos0, normal=normal, tex_coord=tex_coord0)
        vertex2 = Vertex(position=pos1, normal=normal, tex_coord=tex_coord1)
        vertex3 = Vertex(position=pos2, normal=normal, tex_coord=tex_coord2)
        cls.fixed_vertices.append(vertex1)
        cls.fixed_vertices.append(vertex2)
        cls.fixed_vertices.append(vertex3)

    return cls


@init_Dodecahedron
class Dodecahedron(Mesh):

    @checktype
    def __init__(
        self,
        radius=1,
        color: (glm.vec3, glm.vec4) = glm.vec4(0.396, 0.74151, 0.69102, 1),
        back_color: (glm.vec3, glm.vec4) = None,
        stable=False,
        normalize_tex_coord=False,
        name: str = "",
    ):
        Mesh.__init__(self, color=color, back_color=back_color, name=name, block=True)
        self.__radius = radius
        self.__stable = stable
        self.__normalize_tex_coord = normalize_tex_coord
        self.start_building()

    def build(self):
        self.is_closed = True
        self.self_calculated_normal = True

        vertices = self.vertices
        indices = self.indices
        radius = self.__radius
        stable = self.__stable
        normalize_tex_coord = self.__normalize_tex_coord

        quat = glm.quat(1, 0, 0, 0)
        if stable:
            half_theta = 0.25 * math.asin(2 / 5 * math.sqrt(5))
            quat = glm.quat(math.cos(half_theta), math.sin(half_theta), 0, 0)

        sin_pi_5 = math.sin(math.pi / 5)
        for i, fix_vert in enumerate(Dodecahedron.fixed_vertices):
            tex_coord = fix_vert.tex_coord
            if not normalize_tex_coord:
                tex_coord = radius * (
                    tex_coord - glm.vec3(0.5, 0.5, 0)
                ) * Dodecahedron.edge_length / sin_pi_5 + glm.vec3(0.5, 0.5, 0)

            vertices[i] = Vertex(
                position=radius * (quat * fix_vert.position),
                normal=quat * fix_vert.normal,
                tex_coord=tex_coord,
            )

        n_vertices = len(Dodecahedron.fixed_vertices)
        for i in range(0, n_vertices, 3):
            indices[int(i / 3)] = glm.uvec3(i, i + 1, i + 2)
            self.generate_temp_TBN(vertices[i], vertices[i + 1], vertices[i + 2])

        del vertices[n_vertices:]
        del indices[int(n_vertices / 3) :]

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

    @property
    def is_stable(self):
        return self.__stable

    @is_stable.setter
    @Mesh.param_setter
    def is_stable(self, flag: bool):
        self.__stable = flag
