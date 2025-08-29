from ..Mesh import Mesh

from glass.utils import checktype
from glass import Vertex

import cgmath as cgm
import math
from typing import Union


def init_Tetrahedron(cls):
    sqrt_6 = math.sqrt(6)
    sqrt_2 = math.sqrt(2)
    sqrt_3 = math.sqrt(3)
    cls.edge_length = 2 / 3 * sqrt_6
    cls.base_positions = [
        cgm.normalize(cgm.vec3(2 / 3 * sqrt_2, 0, -1 / 3)),  # 0
        cgm.normalize(cgm.vec3(-sqrt_2 / 3, sqrt_6 / 3, -1 / 3)),  # 1
        cgm.normalize(cgm.vec3(-sqrt_2 / 3, -sqrt_6 / 3, -1 / 3)),  # 2
        cgm.normalize(cgm.vec3(0, 0, 1)),  # 3
    ]

    cls.base_indices = [
        cgm.uvec3(0, 2, 1),
        cgm.uvec3(3, 0, 1),
        cgm.uvec3(3, 1, 2),
        cgm.uvec3(3, 2, 0),
    ]

    cls.fixed_vertices = []
    for index in cls.base_indices:
        v1 = cls.base_positions[index[1]] - cls.base_positions[index[0]]
        v2 = cls.base_positions[index[2]] - cls.base_positions[index[0]]
        normal = cgm.normalize(cgm.cross(v1, v2))

        vertex1 = Vertex(
            position=cls.base_positions[index[0]],
            normal=normal,
            tex_coord=cgm.vec3(0.5, 1, 0),
        )
        vertex2 = Vertex(
            position=cls.base_positions[index[1]],
            normal=normal,
            tex_coord=cgm.vec3(0.5 - sqrt_3 / 4, 0.25, 0),
        )
        vertex3 = Vertex(
            position=cls.base_positions[index[2]],
            normal=normal,
            tex_coord=cgm.vec3(0.5 + sqrt_3 / 4, 0.25, 0),
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
        color: Union[cgm.vec3, cgm.vec4] = cgm.vec4(0.396, 0.74151, 0.69102, 1),
        back_color: Union[cgm.vec3, cgm.vec4, None] = None,
        normalize_st:bool=False,
        st_per_unit:float=1,
        name: str = "",
    ):
        Mesh.__init__(self, color=color, back_color=back_color, name=name, block=True)
        self.__radius = radius

    def build(self):
        self.is_closed = True
        vertices = self._vertices
        indices = self._indices
        radius = self.__radius

        for i, fix_vert in enumerate(Tetrahedron.fixed_vertices):
            tex_coord = fix_vert.tex_coord
            if not self.normalize_st:
                tex_coord = 2 * self.str_per_unit * radius * (
                    tex_coord - cgm.vec3(0.5, 0.5, 0)
                ) * Tetrahedron.edge_length / math.sqrt(3) + cgm.vec3(0.5, 0.5, 0)

            vertices[i] = Vertex(
                position=radius * fix_vert.position,
                normal=fix_vert.normal,
                tex_coord=tex_coord,
            )

        for i in range(0, len(Tetrahedron.fixed_vertices), 3):
            indices[int(i / 3)] = cgm.uvec3(i, i + 1, i + 2)
            self.generate_temp_TBN(vertices[i], vertices[i + 1], vertices[i + 2])

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    @Mesh.param_setter
    def radius(self, radius: float):
        self.__radius = radius
