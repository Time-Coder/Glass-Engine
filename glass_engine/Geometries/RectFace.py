from ..Mesh import Mesh

from glass.utils import checktype
from glass import Vertex

import glm


class RectFace(Mesh):

    @checktype
    def __init__(
        self,
        width: float = 2,
        height: float = 1,
        color: (glm.vec3, glm.vec4) = glm.vec4(0.396, 0.74151, 0.69102, 1),
        back_color: (glm.vec3, glm.vec4) = None,
        vertical: bool = False,
        normalize_tex_coord: bool = False,
        name: str = "",
    ):
        Mesh.__init__(self, color=color, back_color=back_color, name=name, block=True)
        self.__width = width
        self.__height = height
        self.__vertical = vertical
        self.__normalize_tex_coord = normalize_tex_coord
        self.start_building()

    def build(self):
        self.is_closed = False
        self.self_calculated_normal = True

        vertices = self.vertices
        indices = self.indices
        width = self.__width
        height = self.__height
        vertical = self.__vertical
        normalize_tex_coord = self.__normalize_tex_coord

        normal = glm.vec3(0, 0, 1)
        if vertical:
            normal = glm.vec3(0, -1, 0)

        # 左下
        vertex0 = Vertex()
        vertex0.position = glm.vec3(-width / 2, -height / 2, 0)
        if vertical:
            vertex0.position = glm.vec3(-width / 2, 0, -height / 2)
        vertex0.normal = normal
        vertex0.tex_coord = glm.vec3(0, 1 - height, 0)
        if normalize_tex_coord:
            vertex0.tex_coord = glm.vec3(0, 1 - height / width, 0)

        # 右下
        vertex1 = Vertex()
        vertex1.position = glm.vec3(width / 2, -height / 2, 0)
        if vertical:
            vertex1.position = glm.vec3(width / 2, 0, -height / 2)
        vertex1.normal = normal
        vertex1.tex_coord = glm.vec3(width, 1 - height, 0)
        if normalize_tex_coord:
            vertex1.tex_coord = glm.vec3(1, 1 - height / width, 0)

        # 右上
        vertex2 = Vertex()
        vertex2.position = glm.vec3(width / 2, height / 2, 0)
        if vertical:
            vertex2.position = glm.vec3(width / 2, 0, height / 2)
        vertex2.normal = normal
        vertex2.tex_coord = glm.vec3(width, 1, 0)
        if normalize_tex_coord:
            vertex2.tex_coord = glm.vec3(1, 1, 0)

        # 左上
        vertex3 = Vertex()
        vertex3.position = glm.vec3(-width / 2, height / 2, 0)
        if vertical:
            vertex3.position = glm.vec3(-width / 2, 0, height / 2)
        vertex3.normal = normal
        vertex3.tex_coord = glm.vec3(0, 1, 0)

        vertices[0] = vertex0
        vertices[1] = vertex1
        vertices[2] = vertex2
        vertices[3] = vertex3

        indices[0] = glm.uvec3(0, 1, 2)
        indices[1] = glm.uvec3(0, 2, 3)

        self.generate_temp_TBN(vertices[0], vertices[1], vertices[2])
        self.generate_temp_TBN(vertices[0], vertices[2], vertices[3])

        del vertices[4:]
        del indices[2:]

    @property
    def vertical(self):
        return self.__vertical

    @vertical.setter
    @Mesh.param_setter
    def vertical(self, flag: bool):
        self.__vertical = flag

    @property
    def width(self):
        return self.__width

    @width.setter
    @Mesh.param_setter
    def width(self, width: float):
        self.__width = width

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
