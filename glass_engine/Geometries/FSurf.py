from ..Mesh import Mesh
from ..ColorMap import ColorMap

from glass.utils import checktype
from glass import Vertex

import numpy as np
import glm

class FSurf(Mesh):

    @checktype
    def __init__(self, func, x_range=[-3,3], y_range=[-3,3], z_range=[-3,3], dep_var="Z",
                 color_map:ColorMap=None, back_color_map:ColorMap=None,
                 color:(glm.vec3,glm.vec4)=None, back_color:(glm.vec3,glm.vec4)=None,
                 surf_type:Mesh.SurfType=Mesh.SurfType.Smooth,
                 name:str="", block:bool=True):
        Mesh.__init__(self, name=name, block=block, surf_type=surf_type)
        self.__func = func
        self.__x_range = x_range
        self.__y_range = y_range
        self.__z_range = z_range
        self.__dep_var = dep_var.upper()

        self.__use_color_map = (color is None)
        if color_map is None:
            color_map = ColorMap.parula()

        if color is not None:
            self.color = color

        self.__color_map = color_map

        self.__back_color_map_user_set = (back_color_map is not None)
        self.__back_use_color_map = (back_color is None)
        if back_color_map is None:
            back_color_map = color_map

        if back_color is not None:
            self.back_color = back_color

        self.__back_color_map = back_color_map

        self.start_building()
            
    def build(self):
        func = self.__func
        x_range = self.__x_range
        y_range = self.__y_range
        z_range = self.__z_range
        dep_var = self.__dep_var
        color_map = self.__color_map
        use_color_map = self.__use_color_map
        back_color_map = self.__back_color_map
        back_use_color_map = self.__back_use_color_map

        vertices = self.vertices
        indices = self.indices
        
        X, Y, Z = None, None, None
        if dep_var == "X":
            Y = np.linspace(y_range[0], y_range[1]) if len(y_range) == 2 else y_range
            Z = np.linspace(z_range[0], z_range[1]) if len(z_range) == 2 else z_range
            Y, Z = np.meshgrid(Y, Z)
            try:
                X = func(Y, Z)
            except:
                func = np.vectorize(func)
                X = func(Y, Z)
        elif dep_var == "Y":
            X = np.linspace(x_range[0], x_range[1]) if len(x_range) == 2 else x_range
            Z = np.linspace(z_range[0], z_range[1]) if len(z_range) == 2 else z_range
            X, Z = np.meshgrid(X, Z)
            try:
                Y = func(X, Z)
            except:
                func = np.vectorize(func)
                Y = func(X, Z)
        elif dep_var == "Z":
            X = np.linspace(x_range[0], x_range[1]) if len(x_range) == 2 else x_range
            Y = np.linspace(y_range[0], y_range[1]) if len(y_range) == 2 else y_range
            X, Y = np.meshgrid(X, Y)
            try:
                Z = func(X, Y)
            except:
                func = np.vectorize(func)
                Z = func(X, Y)
        C = eval(dep_var)
        C_min, C_max = C.min(), C.max()
        color_map.range = (C_min, C_max)
        back_color_map.range =  (C_min, C_max)
        rows = X.shape[0]
        cols = X.shape[1]

        i_vertex = 0
        i_index = 0

        for i in range(rows):
            t = 1 - i/(rows-1)
            for j in range(cols):
                s = j/(cols-1)
                vertex = Vertex()
                vertex.position = glm.vec3(X[i,j], Y[i,j], Z[i,j])
                vertex.normal = glm.vec3(0, 0, 0)
                if use_color_map:
                    vertex.color = glm.vec4(color_map(C[i,j]), 1)

                if back_use_color_map:
                    vertex.back_color = glm.vec4(back_color_map(C[i,j]), 1)

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
    def func(self):
        return self.__func
    
    @func.setter
    @Mesh.param_setter
    def func(self, func):
        self.__func = func

    @property
    def x_range(self):
        return self.__x_range
    
    @x_range.setter
    @Mesh.param_setter
    def x_range(self, range):
        self.__x_range = range

    @property
    def y_range(self):
        return self.__y_range
    
    @y_range.setter
    @Mesh.param_setter
    def y_range(self, range):
        self.__y_range = range

    @property
    def z_range(self):
        return self.__z_range
    
    @z_range.setter
    @Mesh.param_setter
    def z_range(self, range):
        self.__z_range = range

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
