from ..Mesh import Mesh

from glass.utils import checktype
from glass import Vertex

import glm
import numpy as np

class Floor(Mesh):

    __default_image = None

    @checktype
    def __init__(self, color:(glm.vec3,glm.vec4)=glm.vec4(0.396, 0.74151, 0.69102, 1), back_color:(glm.vec3,glm.vec4)=None,
                 length:float=1000, repeat_per_meter:float=1, name:str=""):
        Mesh.__init__(self, color=color, back_color=back_color, name=name, block=True)
        self.__length = length
        self.__repeat_per_meter = repeat_per_meter

        if Floor.__default_image is None:
            Floor.__default_image = np.zeros((100, 100, 3), dtype=np.uint8)
            Floor.__default_image[:50, :50, :] = 140
            Floor.__default_image[50:, 50:, :] = 140
            Floor.__default_image[:50, 50:, :] = 127
            Floor.__default_image[50:, :50, :] = 127

        self.material.diffuse_map = Floor.__default_image
        self.material.cast_shadows = False
        self.start_building()

    def build(self):
        self.is_closed = False
        self.self_calculated_normal = True

        vertices = self.vertices
        indices = self.indices
        length = self.__length
        repeat_per_meter = self.__repeat_per_meter
        vertices = self.vertices
        indices = self.indices

        vertices[0] = Vertex(
            position=glm.vec3(-length/2, -length/2, -0.001),
            tangent=glm.vec3(1/repeat_per_meter, 0, 0),
            bitangent=glm.vec3(0, 1/repeat_per_meter, 0),
            normal=glm.vec3(0, 0, 1),
            tex_coord=glm.vec3(0))
        vertices[1] = Vertex(
            position=glm.vec3( length/2, -length/2, -0.001),
            tangent=glm.vec3(1/repeat_per_meter, 0, 0),
            bitangent=glm.vec3(0, 1/repeat_per_meter, 0),
            normal=glm.vec3(0, 0, 1),
            tex_coord=repeat_per_meter*glm.vec3(length/2, 0, 0))
        vertices[2] = Vertex(
            position=glm.vec3( length/2,  length/2, -0.001),
            tangent=glm.vec3(1/repeat_per_meter, 0, 0),
            bitangent=glm.vec3(0, 1/repeat_per_meter, 0),
            normal=glm.vec3(0, 0, 1),
            tex_coord=repeat_per_meter*glm.vec3(length/2, length/2, 0))
        vertices[3] = Vertex(
            position=glm.vec3(-length/2,  length/2, -0.001),
            tangent=glm.vec3(1/repeat_per_meter, 0, 0),
            bitangent=glm.vec3(0, 1/repeat_per_meter, 0),
            normal=glm.vec3(0, 0, 1),
            tex_coord=repeat_per_meter*glm.vec3(0, length/2, 0))

        indices[0] = glm.uvec3(0, 1, 2)
        indices[1] = glm.uvec3(0, 2, 3)

        del vertices[4:]
        del indices[2:]

    @property
    def length(self):
        return self.__length
    
    @length.setter
    @Mesh.param_setter
    def length(self, length:glm.vec3):
        self.__length = length

    @property
    def repeat_per_meter(self):
        return self.__repeat_per_meter
    
    @repeat_per_meter.setter
    @Mesh.param_setter
    def repeat_per_meter(self, repeat_per_meter:int):
        self.__repeat_per_meter = repeat_per_meter
