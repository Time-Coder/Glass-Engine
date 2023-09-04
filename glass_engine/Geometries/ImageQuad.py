from ..Mesh import Mesh

from glass.utils import checktype
from glass import Vertex
from glass.ImageLoader import ImageLoader

import glm
import numpy as np
from enum import Enum

class ImageQuad(Mesh):

    class AlignCenter(Enum):
        Center = (0, 0)
        LeftCenter = (-0.5, 0)
        RightCenter = (0.5, 0)
        TopCenter = (0, 0.5)
        BottomCenter = (0, -0.5)
        LeftTop = (-0.5, 0.5)
        RightTop = (0.5, 0.5)
        LeftBottom = (-0.5, -0.5)
        RightBottom = (0.5, -0.5)

    @checktype
    def __init__(self, image:(str,np.ndarray), align_center:AlignCenter=AlignCenter.BottomCenter,
                 width:float=None, height:float=None,
                 vertical:bool=True, name:str=""):
        Mesh.__init__(self, color=glm.vec4(0), back_color=glm.vec4(0), name=name, block=True)
        self.__align_center = align_center

        _image = image
        aspect = 1
        if isinstance(image, str):
            try:
                _image = ImageLoader.load(image)
                aspect = _image.shape[1] / _image.shape[0]
            except:
                pass
        elif isinstance(image, np.ndarray):
            aspect = _image.shape[1] / _image.shape[0]

        if width is None and height is None:
            width = 1

        if width is None:
            width = height * aspect

        if height is None:
            height = width / aspect

        self.__width = width
        self.__height = height
        self.__vertical = vertical
        
        self.material.diffuse_map = image
        self.start_building()

    def build(self):
        self.is_closed = False
        self.self_calculated_normal = True

        vertices = self.vertices
        indices = self.indices        
        width = self.__width
        height = self.__height
        vertical = self.__vertical
        align0 = self.__align_center.value[0]*width
        align1 = self.__align_center.value[1]*height

        normal = glm.vec3(0, 0, 1)
        if vertical:
            normal = glm.vec3(0, -1, 0)

        # 左下
        vertex0 = Vertex()
        vertex0.position = glm.vec3(-width/2-align0, -height/2-align1, 0)
        if vertical:
            vertex0.position = glm.vec3(-width/2-align0, 0, -height/2-align1)
        vertex0.normal = normal
        vertex0.tex_coord = glm.vec3(0)

        # 右下
        vertex1 = Vertex()
        vertex1.position = glm.vec3(width/2-align0, -height/2-align1, 0)
        if vertical:
            vertex1.position = glm.vec3(width/2-align0, 0, -height/2-align1)
        vertex1.normal = normal
        vertex1.tex_coord = glm.vec3(1, 0, 0)

        # 右上
        vertex2 = Vertex()
        vertex2.position = glm.vec3(width/2-align0, height/2-align1, 0)
        if vertical:
            vertex2.position = glm.vec3(width/2-align0, 0, height/2-align1)
        vertex2.normal = normal
        vertex2.tex_coord = glm.vec3(1, 1, 0)

        # 左上
        vertex3 = Vertex()
        vertex3.position = glm.vec3(-width/2-align0, height/2-align1, 0)
        if vertical:
            vertex3.position = glm.vec3(-width/2-align0, 0, height/2-align1)
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
    def vertical(self, flag:bool):
        self.__vertical = flag

    @property
    def align_center(self):
        return self.__align_center
    
    @align_center.setter
    @Mesh.param_setter
    def align_center(self, align_center:AlignCenter):
        self.__align_center = align_center

    @property
    def width(self):
        return self.__width
    
    @width.setter
    @Mesh.param_setter
    def width(self, width:float):
        self.__width = width

    @property
    def height(self):
        return self.__height
    
    @height.setter
    @Mesh.param_setter
    def height(self, height:float):
        self.__height = height
