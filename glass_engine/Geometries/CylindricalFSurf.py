from ..Mesh import Mesh
from ..ColorMap import ColorMap
from .Surf import Surf

from glass.utils import checktype

import numpy as np
import glm
import math

class CylindricalFSurf(Mesh):

    @checktype
    def __init__(self, func, r_range=[0,3], theta_range=[0,2*math.pi],
                 color_map:ColorMap=None, back_color_map:ColorMap=None,
                 color:(glm.vec3,glm.vec4)=None, back_color:(glm.vec3,glm.vec4)=None,
                 surf_type:Mesh.SurfType=Mesh.SurfType.Smooth,
                 name:str=""):
        Mesh.__init__(self, name=name, surf_type=surf_type)
        self._func = func
        self._theta_range = theta_range
        self._r_range = r_range

        Surf._set_colors(self, color, back_color, color_map, back_color_map)
        self.start_building()
            
    def build(self):
        func = self._func
        theta_range = self._theta_range
        r_range = self._r_range
    
        theta = np.linspace(theta_range[0], theta_range[1]) if len(theta_range) == 2 else theta_range
        r = np.linspace(r_range[0], r_range[1]) if len(r_range) == 2 else r_range
        theta, r = np.meshgrid(theta, r)

        try:
            Z = func(r, theta)
            if Z.shape != theta.shape:
                raise Exception()
        except:
            func = np.vectorize(func)
            Z = func(r, theta)

        X = r*np.cos(theta)
        Y = r*np.sin(theta)
        C = Z
        
        Surf._build(self, X, Y, Z, C, C)

    @property
    def func(self):
        return self._func
    
    @func.setter
    @Mesh.param_setter
    def func(self, func):
        self._func = func

    @property
    def theta_range(self):
        return self._theta_range
    
    @theta_range.setter
    @Mesh.param_setter
    def theta_range(self, range):
        self._theta_range = range

    @property
    def r_range(self):
        return self._r_range
    
    @r_range.setter
    @Mesh.param_setter
    def r_range(self, range):
        self._r_range = range

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
