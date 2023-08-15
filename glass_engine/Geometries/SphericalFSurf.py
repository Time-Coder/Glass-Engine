from ..Mesh import Mesh
from ..ColorMap import ColorMap
from .Surf import Surf

from glass.utils import checktype

import numpy as np
import glm
import math

class SphericalFSurf(Mesh):

    @checktype
    def __init__(self, func, lon_range=[0,2*math.pi], lat_range=[-math.pi/2,math.pi/2],
                 color_map:ColorMap=None, back_color_map:ColorMap=None,
                 color:(glm.vec3,glm.vec4)=None, back_color:(glm.vec3,glm.vec4)=None,
                 surf_type:Mesh.SurfType=Mesh.SurfType.Smooth,
                 name:str=""):
        Mesh.__init__(self, name=name, surf_type=surf_type)
        self._func = func
        self._lon_range = lon_range
        self._lat_range = lat_range

        Surf._set_colors(self, color, back_color, color_map, back_color_map)
        self.start_building()
            
    def build(self):
        self.should_add_color = False

        func = self._func
        lon_range = self._lon_range
        lat_range = self._lat_range

        lon = np.linspace(lon_range[0], lon_range[1]) if len(lon_range) == 2 else lon_range
        lat = np.linspace(lat_range[0], lat_range[1]) if len(lat_range) == 2 else lat_range
        lon, lat = np.meshgrid(lon, lat)

        try:
            r = func(lon, lat)
            if r.shape != lon.shape:
                raise Exception()
        except:
            func = np.vectorize(func)
            r = func(lon, lat)

        X = r*np.cos(lat)*np.cos(lon)
        Y = r*np.cos(lat)*np.sin(lon)
        Z = r*np.sin(lat)
        C = r
        
        Surf._build(self, X, Y, Z, C, C)

    @property
    def func(self):
        return self._func
    
    @func.setter
    @Mesh.param_setter
    def func(self, func):
        self._func = func

    @property
    def lon_range(self):
        return self._lon_range
    
    @lon_range.setter
    @Mesh.param_setter
    def lon_range(self, range):
        self._lon_range = range

    @property
    def lat_range(self):
        return self._lat_range
    
    @lat_range.setter
    @Mesh.param_setter
    def lat_range(self, range):
        self._lat_range = range

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
