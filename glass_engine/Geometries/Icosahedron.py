from ..Mesh import Mesh

from glass.utils import checktype
from glass import Vertex

import cgmath as cgm
import math
from typing import Union


def init_Icosahedron(cls):
    phi = (1 + math.sqrt(5)) / 2
    cls.base_positions = [
        cgm.normalize(cgm.vec3(-1, 0, phi)),  # 0
        cgm.normalize(cgm.vec3(1, 0, phi)),  # 1
        cgm.normalize(cgm.vec3(-1, 0, -phi)),  # 2
        cgm.normalize(cgm.vec3(1, 0, -phi)),  # 3
        cgm.normalize(cgm.vec3(0, phi, 1)),  # 4
        cgm.normalize(cgm.vec3(0, phi, -1)),  # 5
        cgm.normalize(cgm.vec3(0, -phi, 1)),  # 6
        cgm.normalize(cgm.vec3(0, -phi, -1)),  # 7
        cgm.normalize(cgm.vec3(phi, 1, 0)),  # 8
        cgm.normalize(cgm.vec3(-phi, 1, 0)),  # 9
        cgm.normalize(cgm.vec3(phi, -1, 0)),  # 10
        cgm.normalize(cgm.vec3(-phi, -1, 0)),  # 11
    ]

    cls.base_indices = [
        cgm.uvec3(1, 4, 0),
        cgm.uvec3(4, 9, 0),
        cgm.uvec3(4, 5, 9),
        cgm.uvec3(8, 5, 4),
        cgm.uvec3(1, 8, 4),
        cgm.uvec3(1, 10, 8),
        cgm.uvec3(10, 3, 8),
        cgm.uvec3(8, 3, 5),
        cgm.uvec3(3, 2, 5),
        cgm.uvec3(3, 7, 2),
        cgm.uvec3(3, 10, 7),
        cgm.uvec3(10, 6, 7),
        cgm.uvec3(6, 11, 7),
        cgm.uvec3(6, 0, 11),
        cgm.uvec3(6, 1, 0),
        cgm.uvec3(10, 1, 6),
        cgm.uvec3(11, 0, 9),
        cgm.uvec3(2, 11, 9),
        cgm.uvec3(5, 2, 9),
        cgm.uvec3(11, 2, 7),
    ]

    cls.edge_length = 2 / math.sqrt(1 + phi * phi)

    cls.fixed_vertices = []
    for index in cls.base_indices:
        pos0 = cls.base_positions[index[0]]
        pos1 = cls.base_positions[index[1]]
        pos2 = cls.base_positions[index[2]]

        v1 = pos1 - pos0
        v2 = pos2 - pos0
        normal = cgm.normalize(cgm.cross(v1, v2))

        vertex1 = Vertex(position=pos0, normal=normal, tex_coord=cgm.vec3(0.5, 1, 0))
        vertex2 = Vertex(
            position=pos1,
            normal=normal,
            tex_coord=cgm.vec3(0.5 - math.sqrt(3) / 4, 0.25, 0),
        )
        vertex3 = Vertex(
            position=pos2,
            normal=normal,
            tex_coord=cgm.vec3(0.5 + math.sqrt(3) / 4, 0.25, 0),
        )
        cls.fixed_vertices.append(vertex1)
        cls.fixed_vertices.append(vertex2)
        cls.fixed_vertices.append(vertex3)

    return cls


@init_Icosahedron
class Icosahedron(Mesh):

    @checktype
    def __init__(
        self,
        radius=1,
        color: Union[cgm.vec3, cgm.vec4] = cgm.vec4(0.396, 0.74151, 0.69102, 1),
        back_color: Union[cgm.vec3, cgm.vec4, None] = None,
        stable=False,
        normalize_st:bool=False,
        st_per_unit:float=1,
        name: str = "",
    ):
        Mesh.__init__(
            self, color=color, back_color=back_color,
            normalize_st=normalize_st,
            st_per_unit=st_per_unit,
            name=name, block=True
        )
        self.__radius = radius
        self.__stable = stable

    def build(self):
        self.is_closed = True
        self.self_calculated_normal = True

        vertices = self._vertices
        indices = self._indices
        radius = self.__radius
        stable = self.__stable

        quat = cgm.quat(1, 0, 0, 0)
        if stable:
            half_theta = 0.25 * math.asin(2 / 3)
            quat = cgm.quat(math.cos(half_theta), math.sin(half_theta), 0, 0)

        for i, fix_vert in enumerate(Icosahedron.fixed_vertices):
            tex_coord = fix_vert.tex_coord
            if not self.normalize_st:
                tex_coord = 2 * self.str_per_unit * radius * (
                    tex_coord - cgm.vec3(0.5, 0.5, 0)
                ) * Icosahedron.edge_length / math.sqrt(3) + cgm.vec3(0.5, 0.5, 0)

            vertices[i] = Vertex(
                position=radius * (quat * fix_vert.position),
                normal=quat * fix_vert.normal,
                tex_coord=tex_coord,
            )

        n_vertices = len(Icosahedron.fixed_vertices)
        for i in range(0, n_vertices, 3):
            indices[int(i / 3)] = cgm.uvec3(i, i + 1, i + 2)
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
    def is_stable(self):
        return self.__stable

    @is_stable.setter
    @Mesh.param_setter
    def is_stable(self, flag: bool):
        self.__stable = flag
