from ..Mesh import Mesh

from glass import Vertex
from glass.utils import checktype

import glm
from OpenGL import GL

class Point(Mesh):
    def __init__(self, position:glm.vec3=glm.vec3(0,0,0), color:(glm.vec3,glm.vec4)=glm.vec4(0,120,211,255)/255, point_size:int=3,
                 name:str=""):
        Mesh.__init__(self, element_type=GL.GL_POINTS, color=color, name=name)
        self.render_hint.point_size = point_size
        self.__position = position
        self.start_building()

    def build(self):
        position = self.__position
        vertices = self.vertices

        vertices[0] = Vertex(position=position, tex_coord=glm.vec3(0.5, 0.5, 0))
        del vertices[1:]

    @property
    def position(self):
        return self.__position
    
    @position.setter
    @Mesh.param_setter
    def position(self, position:glm.vec3):
        self.__position = position

    @property
    def point_size(self):
        return self.render_hint.point_size
    
    @point_size.setter
    @checktype
    def point_size(self, point_size:int):
        self.render_hint.point_size = point_size