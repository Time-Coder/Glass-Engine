from ..Mesh import Mesh
from ..ColorMap import ColorMap
from .Surf import Surf

from glass.utils import checktype

import numpy as np
import glm

class FSurf(Mesh):

    @checktype
    def __init__(self, func, x_range=[-3,3], y_range=[-3,3], z_range=[-3,3], dep_var="Z",
                 color_map:ColorMap=None, back_color_map:ColorMap=None,
                 color:(glm.vec3,glm.vec4)=None, back_color:(glm.vec3,glm.vec4)=None,
                 surf_type:Mesh.SurfType=Mesh.SurfType.Smooth,
                 name:str=""):
        Mesh.__init__(self, name=name, surf_type=surf_type)
        self._func = func
        self._x_range = x_range
        self._y_range = y_range
        self._z_range = z_range
        self._dep_var = dep_var.upper()
        
        Surf._set_colors(self, color, back_color, color_map, back_color_map)
        self.start_building()
            
    def build(self):
        func = self._func
        x_range = self._x_range
        y_range = self._y_range
        z_range = self._z_range
        dep_var = self._dep_var
        
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

        Surf._build(self, X, Y, Z, C, C)

    @property
    def func(self):
        return self._func
    
    @func.setter
    @Mesh.param_setter
    def func(self, func):
        self._func = func

    @property
    def x_range(self):
        return self._x_range
    
    @x_range.setter
    @Mesh.param_setter
    def x_range(self, range):
        self._x_range = range

    @property
    def y_range(self):
        return self._y_range
    
    @y_range.setter
    @Mesh.param_setter
    def y_range(self, range):
        self._y_range = range

    @property
    def z_range(self):
        return self._z_range
    
    @z_range.setter
    @Mesh.param_setter
    def z_range(self, range):
        self._z_range = range

    @property
    def color_map(self):
        return self._color_map
    
    @color_map.setter
    @Mesh.param_setter
    def color_map(self, color_map:ColorMap):
        self._color_map = color_map
        self._use_color_map = True
        if not self._back_color_map_user_set:
            self._back_color_map = color_map
            self._back_use_color_map = True

    @property
    def back_color_map(self):
        return self._back_color_map
    
    @back_color_map.setter
    @Mesh.param_setter
    def back_color_map(self, color_map:ColorMap):
        self._back_color_map = color_map
        self._back_use_color_map = True
        self._back_color_map_user_set = True
