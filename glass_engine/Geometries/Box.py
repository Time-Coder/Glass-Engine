from ..Mesh import Mesh

from glass.utils import checktype
from glass import Vertex

import glm
from typing import Union


class Box(Mesh):

    @checktype
    def __init__(
        self,
        Lx: float = 1,
        Ly: Union[float, None] = None,
        Lz: Union[float, None] = None,
        color: Union[glm.vec3, glm.vec4] = glm.vec4(0.396, 0.74151, 0.69102, 1),
        back_color: Union[glm.vec3, glm.vec4, None] = None,
        normalize_st: bool = False,
        st_per_unit: float = 1,
        name: str = "",
    ):
        Mesh.__init__(
            self, color=color, back_color=back_color,
            st_per_unit = st_per_unit,
            normalize_st = normalize_st,
            name=name, block=True
        )

        if Ly is None:
            Ly = Lx

        if Lz is None:
            Lz = Lx

        self.__Lx:float = Lx
        self.__Ly:float = Ly
        self.__Lz:float = Lz

    def build(self):
        self.is_closed = True
        self.self_calculated_normal = True

        vertices = self._vertices
        indices = self._indices

        Lx = self.__Lx
        Ly = self.__Ly
        Lz = self.__Lz

        # 左面
        position = glm.vec3(-Lx / 2, Ly / 2, -Lz / 2)
        tex_coord = (
            glm.vec3(0)
            if self.normalize_st
            else glm.vec3(0.5 - self.s_per_unit*position.y, 0.5 + self.t_per_unit*position.z, 0)
        )
        vertices[0] = Vertex(
            position=position, normal=glm.vec3(-1, 0, 0), tex_coord=tex_coord
        )

        position = glm.vec3(-Lx / 2, -Ly / 2, -Lz / 2)
        tex_coord = (
            glm.vec3(1, 0, 0)
            if self.normalize_st
            else glm.vec3(0.5 - self.s_per_unit*position.y, 0.5 + self.t_per_unit*position.z, 0)
        )
        vertices[1] = Vertex(
            position=position, normal=glm.vec3(-1, 0, 0), tex_coord=tex_coord
        )

        position = glm.vec3(-Lx / 2, -Ly / 2, Lz / 2)
        tex_coord = (
            glm.vec3(1, 1, 0)
            if self.normalize_st
            else glm.vec3(0.5 - self.s_per_unit*position.y, 0.5 + self.t_per_unit*position.z, 0)
        )
        vertices[2] = Vertex(
            position=position, normal=glm.vec3(-1, 0, 0), tex_coord=tex_coord
        )

        position = glm.vec3(-Lx / 2, Ly / 2, Lz / 2)
        tex_coord = (
            glm.vec3(0, 1, 0)
            if self.normalize_st
            else glm.vec3(0.5 - self.s_per_unit*position.y, 0.5 + self.t_per_unit*position.z, 0)
        )
        vertices[3] = Vertex(
            position=position, normal=glm.vec3(-1, 0, 0), tex_coord=tex_coord
        )

        # 右面
        position = glm.vec3(Lx / 2, -Ly / 2, -Lz / 2)
        tex_coord = (
            glm.vec3(0)
            if self.normalize_st
            else glm.vec3(0.5 + self.s_per_unit*position.y, 0.5 + self.t_per_unit*position.z, 0)
        )
        vertices[4] = Vertex(
            position=position, normal=glm.vec3(1, 0, 0), tex_coord=tex_coord
        )

        position = glm.vec3(Lx / 2, Ly / 2, -Lz / 2)
        tex_coord = (
            glm.vec3(1, 0, 0)
            if self.normalize_st
            else glm.vec3(0.5 + self.s_per_unit*position.y, 0.5 + self.t_per_unit*position.z, 0)
        )
        vertices[5] = Vertex(
            position=position, normal=glm.vec3(1, 0, 0), tex_coord=tex_coord
        )

        position = glm.vec3(Lx / 2, Ly / 2, Lz / 2)
        tex_coord = (
            glm.vec3(1, 1, 0)
            if self.normalize_st
            else glm.vec3(0.5 + self.s_per_unit*position.y, 0.5 + self.t_per_unit*position.z, 0)
        )
        vertices[6] = Vertex(
            position=position, normal=glm.vec3(1, 0, 0), tex_coord=tex_coord
        )

        position = glm.vec3(Lx / 2, -Ly / 2, Lz / 2)
        tex_coord = (
            glm.vec3(0, 1, 0)
            if self.normalize_st
            else glm.vec3(0.5 + self.s_per_unit*position.y, 0.5 + self.t_per_unit*position.z, 0)
        )
        vertices[7] = Vertex(
            position=position, normal=glm.vec3(1, 0, 0), tex_coord=tex_coord
        )

        # 后面
        position = glm.vec3(-Lx / 2, -Ly / 2, -Lz / 2)
        tex_coord = (
            glm.vec3(0)
            if self.normalize_st
            else glm.vec3(0.5 + self.s_per_unit*position.x, 0.5 + self.t_per_unit*position.z, 0)
        )
        vertices[8] = Vertex(
            position=position, normal=glm.vec3(0, -1, 0), tex_coord=tex_coord
        )

        position = glm.vec3(Lx / 2, -Ly / 2, -Lz / 2)
        tex_coord = (
            glm.vec3(1, 0, 0)
            if self.normalize_st
            else glm.vec3(0.5 + self.s_per_unit*position.x, 0.5 + self.t_per_unit*position.z, 0)
        )
        vertices[9] = Vertex(
            position=position, normal=glm.vec3(0, -1, 0), tex_coord=tex_coord
        )

        position = glm.vec3(Lx / 2, -Ly / 2, Lz / 2)
        tex_coord = (
            glm.vec3(1, 1, 0)
            if self.normalize_st
            else glm.vec3(0.5 + self.s_per_unit*position.x, 0.5 + self.t_per_unit*position.z, 0)
        )
        vertices[10] = Vertex(
            position=position, normal=glm.vec3(0, -1, 0), tex_coord=tex_coord
        )

        position = glm.vec3(-Lx / 2, -Ly / 2, Lz / 2)
        tex_coord = (
            glm.vec3(0, 1, 0)
            if self.normalize_st
            else glm.vec3(0.5 + self.s_per_unit*position.x, 0.5 + self.t_per_unit*position.z, 0)
        )
        vertices[11] = Vertex(
            position=position, normal=glm.vec3(0, -1, 0), tex_coord=tex_coord
        )

        # 前面
        position = glm.vec3(Lx / 2, Ly / 2, -Lz / 2)
        tex_coord = (
            glm.vec3(0)
            if self.normalize_st
            else glm.vec3(0.5 - self.s_per_unit*position.x, 0.5 + self.t_per_unit*position.z, 0)
        )
        vertices[12] = Vertex(
            position=position, normal=glm.vec3(0, 1, 0), tex_coord=tex_coord
        )

        position = glm.vec3(-Lx / 2, Ly / 2, -Lz / 2)
        tex_coord = (
            glm.vec3(1, 0, 0)
            if self.normalize_st
            else glm.vec3(0.5 - self.s_per_unit*position.x, 0.5 + self.t_per_unit*position.z, 0)
        )
        vertices[13] = Vertex(
            position=position, normal=glm.vec3(0, 1, 0), tex_coord=tex_coord
        )

        position = glm.vec3(-Lx / 2, Ly / 2, Lz / 2)
        tex_coord = (
            glm.vec3(1, 1, 0)
            if self.normalize_st
            else glm.vec3(0.5 - self.s_per_unit*position.x, 0.5 + self.t_per_unit*position.z)
        )
        vertices[14] = Vertex(
            position=position, normal=glm.vec3(0, 1, 0), tex_coord=tex_coord
        )

        position = glm.vec3(Lx / 2, Ly / 2, Lz / 2)
        tex_coord = (
            glm.vec3(0, 1, 0)
            if self.normalize_st
            else glm.vec3(0.5 - self.s_per_unit*position.x, 0.5 + self.t_per_unit*position.z)
        )
        vertices[15] = Vertex(
            position=position, normal=glm.vec3(0, 1, 0), tex_coord=tex_coord
        )

        # 下面
        position = glm.vec3(-Lx / 2, Ly / 2, -Lz / 2)
        tex_coord = (
            glm.vec3(0)
            if self.normalize_st
            else glm.vec3(0.5 + self.s_per_unit*position.x, 0.5 - self.t_per_unit*position.y)
        )
        vertices[16] = Vertex(
            position=position, normal=glm.vec3(0, 0, -1), tex_coord=tex_coord
        )

        position = glm.vec3(Lx / 2, Ly / 2, -Lz / 2)
        tex_coord = (
            glm.vec3(1, 0, 0)
            if self.normalize_st
            else glm.vec3(0.5 + self.s_per_unit*position.x, 0.5 - self.t_per_unit*position.y)
        )
        vertices[17] = Vertex(
            position=position, normal=glm.vec3(0, 0, -1), tex_coord=tex_coord
        )

        position = glm.vec3(Lx / 2, -Ly / 2, -Lz / 2)
        tex_coord = (
            glm.vec3(1, 1, 0)
            if self.normalize_st
            else glm.vec3(0.5 + self.s_per_unit*position.x, 0.5 - self.t_per_unit*position.y)
        )
        vertices[18] = Vertex(
            position=position, normal=glm.vec3(0, 0, -1), tex_coord=tex_coord
        )

        position = glm.vec3(-Lx / 2, -Ly / 2, -Lz / 2)
        tex_coord = (
            glm.vec3(0, 1, 0)
            if self.normalize_st
            else glm.vec3(0.5 + self.s_per_unit*position.x, 0.5 - self.t_per_unit*position.y)
        )
        vertices[19] = Vertex(
            position=position, normal=glm.vec3(0, 0, -1), tex_coord=tex_coord
        )

        # 上面
        position = glm.vec3(-Lx / 2, -Ly / 2, Lz / 2)
        tex_coord = (
            glm.vec3(0)
            if self.normalize_st
            else glm.vec3(0.5 + self.s_per_unit*position.x, 0.5 + self.t_per_unit*position.y)
        )
        vertices[20] = Vertex(
            position=position, normal=glm.vec3(0, 0, 1), tex_coord=tex_coord
        )

        position = glm.vec3(Lx / 2, -Ly / 2, Lz / 2)
        tex_coord = (
            glm.vec3(1, 0, 0)
            if self.normalize_st
            else glm.vec3(0.5 + self.s_per_unit*position.x, 0.5 + self.t_per_unit*position.y, 0)
        )
        vertices[21] = Vertex(
            position=position, normal=glm.vec3(0, 0, 1), tex_coord=tex_coord
        )

        position = glm.vec3(Lx / 2, Ly / 2, Lz / 2)
        tex_coord = (
            glm.vec3(1, 1, 0)
            if self.normalize_st
            else glm.vec3(0.5 + self.s_per_unit*position.x, 0.5 + self.t_per_unit*position.y, 0)
        )
        vertices[22] = Vertex(
            position=position, normal=glm.vec3(0, 0, 1), tex_coord=tex_coord
        )

        position = glm.vec3(-Lx / 2, Ly / 2, Lz / 2)
        tex_coord = (
            glm.vec3(0, 1, 0)
            if self.normalize_st
            else glm.vec3(0.5 + self.s_per_unit*position.x, 0.5 + self.t_per_unit*position.y, 0)
        )
        vertices[23] = Vertex(
            position=position, normal=glm.vec3(0, 0, 1), tex_coord=tex_coord
        )

        # 左面
        indices[0] = glm.uvec3(0, 1, 2)
        indices[1] = glm.uvec3(0, 2, 3)

        # 右面
        indices[2] = 4 + glm.uvec3(0, 1, 2)
        indices[3] = 4 + glm.uvec3(0, 2, 3)

        # 后面
        indices[4] = 8 + glm.uvec3(0, 1, 2)
        indices[5] = 8 + glm.uvec3(0, 2, 3)

        # 前面
        indices[6] = 12 + glm.uvec3(0, 1, 2)
        indices[7] = 12 + glm.uvec3(0, 2, 3)

        # 下面
        indices[8] = 16 + glm.uvec3(0, 1, 2)
        indices[9] = 16 + glm.uvec3(0, 2, 3)

        # 上面
        indices[10] = 20 + glm.uvec3(0, 1, 2)
        indices[11] = 20 + glm.uvec3(0, 2, 3)

        del vertices[24:]
        del indices[12:]

        for index in indices:
            self.generate_temp_TBN(
                vertices[index[0]], vertices[index[1]], vertices[index[2]]
            )

    @property
    def Lx(self):
        return self.__Lx

    @Lx.setter
    @Mesh.param_setter
    def Lx(self, Lx: int):
        self.__Lx = Lx

    @property
    def Ly(self):
        return self.__Ly

    @Ly.setter
    @Mesh.param_setter
    def Ly(self, Ly: int):
        self.__Ly = Ly

    @property
    def Lz(self):
        return self.__Lz

    @Lz.setter
    @Mesh.param_setter
    def Lz(self, Lz: int):
        self.__Lz = Lz
