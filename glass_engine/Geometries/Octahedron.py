from ..Mesh import Mesh

from glass.utils import checktype
from glass import Vertex

import glm
import math

def init_Octahedron(cls):
    cls.edge_length = math.sqrt(2)
    cls.base_positions = \
    [
        glm.vec3(-1,  0,  0), # 0
        glm.vec3( 1,  0,  0), # 1

        glm.vec3( 0, -1,  0), # 2
        glm.vec3( 0,  1,  0), # 3

        glm.vec3( 0,  0, -1), # 4
        glm.vec3( 0,  0,  1), # 5
    ]

    cls.base_indices = \
    [
        glm.uvec3(5, 0, 2),
        glm.uvec3(5, 2, 1),
        glm.uvec3(5, 1, 3),
        glm.uvec3(5, 3, 0),

        glm.uvec3(4, 2, 0),
        glm.uvec3(4, 1, 2),
        glm.uvec3(4, 3, 1),
        glm.uvec3(4, 0, 3)
    ]

    cls.fixed_vertices = []
    for index in cls.base_indices:
        pos0 = cls.base_positions[index[0]]
        pos1 = cls.base_positions[index[1]]
        pos2 = cls.base_positions[index[2]]

        v1 = pos1 - pos0
        v2 = pos2 - pos0
        normal = glm.normalize(glm.cross(v1, v2))

        vertex0 = Vertex(
            position=pos0,
            normal=normal,
            tex_coord=glm.vec3(0.5, 1, 0)
        )
        vertex1 = Vertex(
            position=pos1,
            normal=normal,
            tex_coord=glm.vec3(0.5-math.sqrt(3)/4, 0.25, 0)
        )
        vertex2 = Vertex(
            position=pos2,
            normal=normal,
            tex_coord=glm.vec3(0.5+math.sqrt(3)/4, 0.25, 0)
        )
        cls.fixed_vertices.append(vertex0)
        cls.fixed_vertices.append(vertex1)
        cls.fixed_vertices.append(vertex2)

    return cls

@init_Octahedron
class Octahedron(Mesh):

    @checktype
    def __init__(self, radius=1,
                 color:(glm.vec3,glm.vec4)=glm.vec4(0.396, 0.74151, 0.69102, 1), back_color:(glm.vec3,glm.vec4)=None,
                 stable=False, normalize_tex_coord=False,
                 name:str=""):
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
            quat_z = glm.quat(math.cos(math.pi/8), 0, 0, math.sin(math.pi/8))

            theta = math.acos(math.sqrt(3)/3)
            quat_x = glm.quat(math.cos(theta/2), math.sin(theta/2), 0, 0)

            quat = quat_x * quat_z

        for i, fix_vert in enumerate(Octahedron.fixed_vertices):
            tex_coord = fix_vert.tex_coord
            if not normalize_tex_coord:
                tex_coord = 2*radius*(tex_coord - glm.vec3(0.5, 0.5, 0))*Octahedron.edge_length/math.sqrt(3) + glm.vec3(0.5, 0.5, 0)
            
            vertices[i] = Vertex(
                position = radius * (quat * fix_vert.position),
                normal = quat * fix_vert.normal,
                tex_coord = tex_coord
            )

        for i in range(0, len(Octahedron.fixed_vertices), 3):
            indices[int(i/3)] = glm.uvec3(i, i+1, i+2)
            self.generate_temp_TBN(vertices[i], vertices[i+1], vertices[i+2])

    @property
    def radius(self):
        return self.__radius
    
    @radius.setter
    @Mesh.param_setter
    def radius(self, radius:float):
        self.__radius = radius

    @property
    def normalize_tex_coord(self):
        return self.__normalize_tex_coord
    
    @normalize_tex_coord.setter
    @Mesh.param_setter
    def normalize_tex_coord(self, flag:bool):
        self.__normalize_tex_coord = flag

    @property
    def is_stable(self):
        return self.__stable
    
    @is_stable.setter
    @Mesh.param_setter
    def is_stable(self, flag:bool):
        self.__stable = flag