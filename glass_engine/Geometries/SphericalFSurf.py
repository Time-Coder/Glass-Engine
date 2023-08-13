from ..Mesh import Mesh
from ..ColorMap import ColorMap

from glass.utils import checktype
from glass import Vertex

import numpy as np
import glm
import math
import copy

class SphericalFSurf(Mesh):

    @checktype
    def __init__(self, func, theta_range=[0,2*math.pi], phi_range=[-math.pi/2,math.pi/2],
                 color_map:ColorMap=None, back_color_map:ColorMap=None,
                 color:(glm.vec3,glm.vec4)=None, back_color:(glm.vec3,glm.vec4)=None,
                 surf_type:Mesh.SurfType=Mesh.SurfType.Smooth,
                 name:str="", block:bool=True):
        Mesh.__init__(self, name=name, block=block, surf_type=surf_type)
        self.__func = func
        self.__theta_range = theta_range
        self.__phi_range = phi_range

        self.__use_color_map = (color is None)
        if color_map is None:
            color_map = ColorMap.parula()

        if color is not None:
            self.color = color

        if back_color is None:
            back_color = color

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
        self.should_add_color = False

        func = self.__func
        theta_range = self.__theta_range
        phi_range = self.__phi_range
        color_map = self.__color_map
        back_color_map = self.__back_color_map
        use_color_map = self.__use_color_map
        back_use_color_map = self.__back_use_color_map
        color = self._color
        back_color = self._back_color

        vertices = self.vertices
        indices = self.indices

        theta = np.linspace(theta_range[0], theta_range[1]) if len(theta_range) == 2 else theta_range
        phi = np.linspace(phi_range[0], phi_range[1]) if len(phi_range) == 2 else phi_range
        theta, phi = np.meshgrid(theta, phi)

        try:
            r = func(theta, phi)
            if r.shape != theta.shape:
                raise Exception()
        except:
            func = np.vectorize(func)
            r = func(theta, phi)

        X = r*np.cos(phi)*np.cos(theta)
        Y = r*np.cos(phi)*np.sin(theta)
        Z = r*np.sin(phi)

        C = r
        C_min, C_max = C.min(), C.max()
        color_map.range = (C_min, C_max)
        back_color_map.range = (C_min, C_max)
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
                if use_color_map:
                    vertex.color = glm.vec4(color_map(C[i,j]), 1)
                else:
                    vertex.color = color

                if back_use_color_map:
                    vertex.back_color = glm.vec4(back_color_map(C[i,j]), 1)
                else:
                    vertex.back_color = back_color

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
    def theta_range(self):
        return self.__theta_range
    
    @theta_range.setter
    @Mesh.param_setter
    def theta_range(self, range):
        self.__theta_range = range

    @property
    def phi_range(self):
        return self.__phi_range
    
    @phi_range.setter
    @Mesh.param_setter
    def phi_range(self, range):
        self.__phi_range = range

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
