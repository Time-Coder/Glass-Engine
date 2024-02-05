from .Icosahedron import Icosahedron

from ..Mesh import Mesh

from glass.utils import checktype
from glass import Vertex

import glm
import math
import copy


class Icosphere(Mesh):

    __base_vertices = []
    __base_indices = []

    @checktype
    def __init__(
        self,
        radius: float = 1,
        color: (glm.vec3, glm.vec4) = glm.vec4(0.396, 0.74151, 0.69102, 1),
        back_color: (glm.vec3, glm.vec4) = None,
        n_levels: int = 4,
        name: str = "",
        block=True,
    ):
        Mesh.__init__(self, color=color, back_color=back_color, name=name, block=block)
        self.__radius = radius
        self.__n_levels = n_levels
        self.start_building()

    def __generate_base_data(self):
        if Icosphere.__base_indices:
            return

        Icosphere.__base_indices = copy.deepcopy(Icosahedron.base_indices)
        Icosphere.__base_vertices = []

        half_theta = math.atan(2) / 4
        cos_half_theta = math.cos(half_theta)
        sin_half_theta = math.sin(half_theta)
        q = glm.quat(cos_half_theta, 0, sin_half_theta, 0)
        for base_pos in Icosahedron.base_positions:
            pos = q * base_pos
            if glm.length(pos - glm.vec3(0, 0, 1)) < 1e-6:
                pos = glm.vec3(0, 0, 1)
            elif glm.length(pos - glm.vec3(0, 0, -1)) < 1e-6:
                pos = glm.vec3(0, 0, -1)
            Icosphere.__base_vertices.append(Icosphere.__create_vertex(pos))

        for index in Icosphere.__base_indices:
            vertex0 = Icosphere.__base_vertices[index[0]]
            vertex1 = Icosphere.__base_vertices[index[1]]
            vertex2 = Icosphere.__base_vertices[index[2]]

            v1 = vertex1.position - vertex0.position
            v2 = vertex2.position - vertex0.position
            normal = glm.cross(v1, v2)

            for i in range(3):
                vertex = Icosphere.__base_vertices[index[i]]
                if vertex.tex_coord.t == 0 or vertex.tex_coord.t == 1:
                    new_vertex = Icosphere.__create_vertex(vertex.position, normal)
                    new_index = len(Icosphere.__base_vertices)
                    Icosphere.__base_vertices.append(new_vertex)
                    index[i] = new_index

    def build(self):
        self.is_closed = True
        vertices = self.vertices
        indices = self.indices
        self.__generate_base_data()

        radius = self.__radius
        n_levels = self.__n_levels

        _indices = Icosphere.__base_indices

        i_vertex = 0
        i_index = 0
        for vertex in Icosphere.__base_vertices:
            new_vertex = copy.deepcopy(vertex)
            new_vertex.position = radius * new_vertex.position
            new_vertex.tangent = radius * new_vertex.tangent
            new_vertex.bitangent = radius * new_vertex.bitangent
            vertices[i_vertex] = new_vertex
            i_vertex += 1

        for _ in range(n_levels):
            i_index = 0
            for index in _indices:
                vertex0 = vertices[index[0]]
                vertex1 = vertices[index[1]]
                vertex2 = vertices[index[2]]

                new_pos0 = glm.normalize(vertex1.position + vertex2.position)
                new_pos1 = glm.normalize(vertex0.position + vertex2.position)
                new_pos2 = glm.normalize(vertex0.position + vertex1.position)

                new_vertex0 = Icosphere.__create_vertex(new_pos0, radius=radius)
                new_vertex1 = Icosphere.__create_vertex(new_pos1, radius=radius)
                new_vertex2 = Icosphere.__create_vertex(new_pos2, radius=radius)

                start_index = i_vertex
                vertices[i_vertex] = new_vertex0
                i_vertex += 1

                vertices[i_vertex] = new_vertex1
                i_vertex += 1

                vertices[i_vertex] = new_vertex2
                i_vertex += 1

                indices[i_index] = glm.uvec3(index[0], start_index + 2, start_index + 1)
                i_index += 1

                indices[i_index] = glm.uvec3(index[1], start_index, start_index + 2)
                i_index += 1

                indices[i_index] = glm.uvec3(index[2], start_index + 1, start_index)
                i_index += 1

                indices[i_index] = glm.uvec3(
                    start_index, start_index + 1, start_index + 2
                )
                i_index += 1

                yield

            _indices = list(indices)

        del vertices[i_vertex:]
        del indices[i_index:]

        for index in indices:
            vertex0 = vertices[index[0]]
            vertex1 = vertices[index[1]]
            vertex2 = vertices[index[2]]
            s0 = vertex0.tex_coord.s
            s1 = vertex1.tex_coord.s
            s2 = vertex2.tex_coord.s

            if abs(s0 - s1) > 0.5 and abs(s0 - s2) > 0.5:
                new_vertex = copy.deepcopy(vertex0)
                new_vertex.tex_coord.s += 1 if s1 + s2 > 1 else -1
                new_index = len(vertices)
                vertices.append(new_vertex)
                index[0] = new_index

            if abs(s1 - s0) > 0.5 and abs(s1 - s2) > 0.5:
                new_vertex = copy.deepcopy(vertex1)
                new_vertex.tex_coord.s += 1 if s0 + s2 > 1 else -1
                new_index = len(vertices)
                vertices.append(new_vertex)
                index[1] = new_index

            if abs(s2 - s0) > 0.5 and abs(s2 - s1) > 0.5:
                new_vertex = copy.deepcopy(vertex2)
                new_vertex.tex_coord.s += 1 if s0 + s1 > 1 else -1
                new_index = len(vertices)
                vertices.append(new_vertex)
                index[2] = new_index

            yield

    def __get_info(position, normal=None):
        dem = math.sqrt(position.x * position.x + position.y * position.y)
        if dem == 0:
            s = 0
            tangent = glm.vec3(0, 2 * math.pi, 0)
            bitangent = glm.vec3(-math.pi, 0, 0)
            if normal is not None:
                theta = math.atan2(normal.y, normal.x)
                phi = math.pi / 2 if normal.z > 0 else -math.pi / 2
                sin_theta = math.sin(theta)
                cos_theta = math.cos(theta)
                sin_phi = math.sin(phi)
                cos_phi = math.cos(phi)
                s = theta / (2 * math.pi) + 0.5
                tangent = 2 * math.pi * cos_phi * glm.vec3(-sin_theta, cos_theta, 0)
                bitangent = math.pi * glm.vec3(
                    -sin_phi * cos_theta, -sin_phi * sin_theta, cos_phi
                )
            t = int((position.z + 1) / 2)

            return glm.vec3(s, t, 0), tangent, bitangent

        theta = math.atan2(position.y, position.x)
        phi = math.atan(position.z / dem)
        sin_theta = math.sin(theta)
        cos_theta = math.cos(theta)
        sin_phi = math.sin(phi)
        cos_phi = math.cos(phi)

        s = theta / (2 * math.pi) + 0.5
        t = phi / math.pi + 0.5

        tex_coord = glm.vec3(s, t, 0)
        tangent = 2 * math.pi * cos_phi * glm.vec3(-sin_theta, cos_theta, 0)
        bitangent = math.pi * glm.vec3(
            -sin_phi * cos_theta, -sin_phi * sin_theta, cos_phi
        )
        return tex_coord, tangent, bitangent

    @staticmethod
    def __create_vertex(position, normal=None, radius=1, **kwargs):
        tex_coord, tangent, bitangent = Icosphere.__get_info(position, normal)
        return Vertex(
            position=radius * position,
            tangent=radius * tangent,
            bitangent=radius * bitangent,
            normal=position,
            tex_coord=tex_coord,
            **kwargs
        )

    @property
    def n_levels(self):
        return self.__n_levels

    @n_levels.setter
    @Mesh.param_setter
    def n_levels(self, n_levels: int):
        self.__n_levels = n_levels

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    @Mesh.param_setter
    def radius(self, radius: float):
        self.__radius = radius
