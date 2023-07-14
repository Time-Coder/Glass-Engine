from ..Mesh import Mesh
from ..ColorMap import ColorMap

from glass.utils import checktype
from glass import Vertex

import glm
import numpy as np
import copy

class Surf(Mesh):
    @checktype
    def __init__(self, X:np.ndarray, Y:np.ndarray, Z:np.ndarray,
                 C:np.ndarray=None, back_C:np.ndarray=None,
                 color_map:ColorMap=None, back_color_map:ColorMap=None, 
                 color:(glm.vec3,glm.vec4)=None, back_color:(glm.vec3,glm.vec4)=None,
                 surf_type:Mesh.SurfType=Mesh.SurfType.Smooth, name="", block=True):
        Mesh.__init__(self, name=name, block=block, surf_type=surf_type)
        self.__XData = X
        self.__YData = Y
        self.__ZData = Z
        self.__CData = C if C is not None else Z

        self.__back_CData_user_set = (back_C is not None)
        self.__back_CData = back_C if self.__back_CData_user_set else self.__CData

        self.__use_color_map = (color is None)
        if color_map is None:
            color_map = ColorMap.parula()

        if color is not None:
            self.color = color

        self.__color_map = color_map

        self.__back_color_map_user_set = (back_color_map is not None)
        self.__back_use_color_map = (back_color is None)
        if back_color_map is None:
            back_color_map = copy.deepcopy(color_map)

        if back_color is not None:
            self.back_color = back_color

        self.__back_color_map = back_color_map

        self.start_building()

    def build(self):
        vertices = self.vertices
        indices = self.indices
        X = self.__XData
        Y = self.__YData
        Z = self.__ZData
        C = self.__CData if self.__CData is not None else Z
        back_C = self.__back_CData if self.__back_CData is not None else C
        rows = X.shape[0]
        cols = X.shape[1]
        color_map = self.__color_map
        back_color_map = self.__back_color_map
        use_color_map = self.__use_color_map
        back_use_color_map = self.__back_use_color_map

        use_cmap = False
        if len(C.shape) == 2 or C.shape[2] == 1:
            use_cmap = True
            color_map.range = (C.min(), C.max())

        back_use_cmap = False
        if len(back_C.shape) == 2 or back_C.shape[2] == 1:
            back_use_cmap = True
            back_color_map.range = (back_C.min(), back_C.max())

        i_vertex = 0
        i_index = 0

        for i in range(rows):
            t = 1 - i/(rows-1)
            for j in range(cols):
                s = j/(cols-1)
                vertex = Vertex()
                vertex.position = glm.vec3(X[i,j], Y[i,j], Z[i,j])
                vertex.tangent = glm.vec3(0, 0, 0)
                vertex.bitangent = glm.vec3(0, 0, 0)
                vertex.normal = glm.vec3(0, 0, 0)
                if use_color_map:
                    if use_cmap:
                        vertex.color = glm.vec4(color_map(C[i,j]), 1)
                    elif C.shape[2] == 4:
                        vertex.color = glm.vec4(C[i,j,0], C[i,j,1], C[i,j,2], C[i,j,3])
                    elif C.shape[2] == 3:
                        vertex.color = glm.vec4(C[i,j,0], C[i,j,1], C[i,j,2], 1)

                if back_use_color_map:
                    if back_use_cmap:
                        vertex.back_color = glm.vec4(back_color_map(back_C[i,j]), 1)
                    elif back_C.shape[2] == 4:
                        vertex.back_color = glm.vec4(back_C[i,j,0], back_C[i,j,1], back_C[i,j,2], back_C[i,j,3])
                    elif back_C.shape[3] == 3:
                        vertex.back_color = glm.vec4(back_C[i,j,0], back_C[i,j,1], back_C[i,j,2], 1)

                vertex.tex_coord = glm.vec3(s, t, 0)
                vertices[i_vertex] = vertex
                i_vertex += 1

                if i > 0 and j > 0:
                    triangle = glm.uvec3(0, 0, 0)
                    triangle[0] = i_vertex-1
                    triangle[1] = i_vertex-1-1
                    triangle[2] = i_vertex-1-1-cols
                    indices[i_index] = triangle
                    i_index += 1
                    self.generate_temp_TBN(vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]])

                    triangle = glm.uvec3(0, 0, 0)
                    triangle[0] = i_vertex-1
                    triangle[1] = i_vertex-1-1-cols
                    triangle[2] = i_vertex-1-cols
                    indices[i_index] = triangle
                    i_index += 1
                    self.generate_temp_TBN(vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]])

            yield

        del vertices[i_vertex:]
        del indices[i_index:]

    @property
    def XData(self):
        return self.__XData
    
    @XData.setter
    @Mesh.param_setter
    def XData(self, X:np.ndarray):
        self.__XData = X
    
    @property
    def YData(self):
        return self.__YData
    
    @YData.setter
    @Mesh.param_setter
    def YData(self, Y:np.ndarray):
        self.__YData = Y
    
    @property
    def ZData(self):
        return self.__ZData
    
    @ZData.setter
    @Mesh.param_setter
    def ZData(self, Z:np.ndarray):
        self.__ZData = Z
    
    @property
    def CData(self):
        return self.__CData
    
    @CData.setter
    @Mesh.param_setter
    def CData(self, C:np.ndarray):
        self.__CData = C
        self.__use_color_map = True
        if not self.__back_CData_user_set:
            self.__back_CData = C
            self.__back_use_color_map = True

    @property
    def back_CData(self):
        return self.__back_CData
    
    @back_CData.setter
    @Mesh.param_setter
    def back_CData(self, C:np.ndarray):
        self.__back_CData = C
        self.__back_CData_user_set = True
        self.__back_use_color_map = True
    
    @property
    def color_map(self):
        return self.__color_map
    
    @color_map.setter
    @Mesh.param_setter
    def color_map(self, color_map:ColorMap):
        self.__color_map = color_map
        self.__use_color_map = True
        if not self.__back_color_map_user_set:
            self.__back_color_map = color_map
            self.__back_use_color_map = True

    @property
    def back_color_map(self):
        return self.__back_color_map
    
    @back_color_map.setter
    @Mesh.param_setter
    def back_color_map(self, color_map:ColorMap):
        self.__back_color_map = color_map
        self.__back_use_color_map = True
        self.__back_color_map_user_set = True
