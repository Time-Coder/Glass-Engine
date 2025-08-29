from ..Mesh import Mesh

from glass.utils import checktype
from glass import Vertex

import cgmath as cgm
import numpy as np
from typing import Union


class Floor(Mesh):

    __default_image = None

    @checktype
    def __init__(
        self,
        color: Union[cgm.vec3, cgm.vec4] = cgm.vec4(0.396, 0.74151, 0.69102, 1),
        back_color: Union[cgm.vec3, cgm.vec4, None] = None,
        length: float = 1000,
        st_per_units: float = 1,
        name: str = "",
    ):
        Mesh.__init__(
            self, color=color, back_color=back_color,
            normalize_st=False,
            st_per_unit=st_per_units,
            name=name, block=True
        )
        self.__length = length

        if Floor.__default_image is None:
            Floor.__default_image = np.zeros((100, 100, 3), dtype=np.uint8)
            Floor.__default_image[:50, :50, :] = 140
            Floor.__default_image[50:, 50:, :] = 140
            Floor.__default_image[:50, 50:, :] = 127
            Floor.__default_image[50:, :50, :] = 127

        self.material.diffuse_map = Floor.__default_image
        self.material.cast_shadows = False

    def build(self):
        self.is_closed = False
        self.self_calculated_normal = True

        vertices = self._vertices
        indices = self._indices
        length = self.__length
        vertices = self._vertices
        indices = self._indices

        vertices[0] = Vertex(
            position=cgm.vec3(-length / 2, -length / 2, -0.001),
            tangent=cgm.vec3(1 / self.s_per_unit, 0, 0),
            bitangent=cgm.vec3(0, 1 / self.t_per_unit, 0),
            normal=cgm.vec3(0, 0, 1),
            tex_coord=cgm.vec3(0),
        )
        vertices[1] = Vertex(
            position=cgm.vec3(length / 2, -length / 2, -0.001),
            tangent=cgm.vec3(1 / self.s_per_unit, 0, 0),
            bitangent=cgm.vec3(0, 1 / self.t_per_unit, 0),
            normal=cgm.vec3(0, 0, 1),
            tex_coord=self.str_per_unit * cgm.vec3(length / 2, 0, 0),
        )
        vertices[2] = Vertex(
            position=cgm.vec3(length / 2, length / 2, -0.001),
            tangent=cgm.vec3(1 / self.s_per_unit, 0, 0),
            bitangent=cgm.vec3(0, 1 / self.t_per_unit, 0),
            normal=cgm.vec3(0, 0, 1),
            tex_coord=self.str_per_unit * cgm.vec3(length / 2, length / 2, 0),
        )
        vertices[3] = Vertex(
            position=cgm.vec3(-length / 2, length / 2, -0.001),
            tangent=cgm.vec3(1 / self.s_per_unit, 0, 0),
            bitangent=cgm.vec3(0, 1 / self.t_per_unit, 0),
            normal=cgm.vec3(0, 0, 1),
            tex_coord=self.str_per_unit * cgm.vec3(0, length / 2, 0),
        )

        indices[0] = cgm.uvec3(0, 1, 2)
        indices[1] = cgm.uvec3(0, 2, 3)

        del vertices[4:]
        del indices[2:]

    @property
    def length(self):
        return self.__length

    @length.setter
    @Mesh.param_setter
    def length(self, length: cgm.vec3):
        self.__length = length
