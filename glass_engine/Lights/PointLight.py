from .Light import Light
from ..algorithm import fzero

from glass.utils import checktype
from glass.DictList import DictList
from glass.ShaderStorageBlock import ShaderStorageBlock

import glm
import math

class PointLight(Light):

    @checktype
    def __init__(self, name:str=""):
        Light.__init__(self, name)
        
        self._K1 = 0.045
        self._K2 = 0.0075

        self._luminance = 0
        self._coverage = 0
        self.__update_luminance()
        self.__update_coverage()

    def __update_luminance(self):
        self._luminance = self._brightness * glm.dot(self._color, glm.vec3(0.2126, 0.7152, 0.0722))
        for flat in self._flats:
            flat.luminance = self._luminance

        self._update_scene_lights()

    def __update_coverage(self):
        epsilon = 0.01
        self._coverage = (-self._K1 + math.sqrt(self._K1**2 - 4*self._K2*(1-self.luminance/epsilon)))/(2*self._K2)
        for flat in self._flats:
            flat.coverage = self._coverage

        self._update_scene_lights()

    @property
    def color(self):
        return self._color

    @color.setter
    @checktype
    def color(self, color:glm.vec3):
        if self._color == color:
            return
        
        self._color.r = color.r
        self._color.g = color.g
        self._color.b = color.b

        for flat in self._flats:
            flat.color = self._color

        self.__update_luminance()
        self.__update_coverage()

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    @checktype
    def brightness(self, brightness:float):
        if self._brightness == brightness:
            return
        
        self._brightness = brightness
        for flat in self._flats:
            flat.brightness = self._brightness

        self.__update_luminance()
        self.__update_coverage()

    @property
    def luminance(self):
        return self._luminance
    
    @luminance.setter
    @checktype
    def luminance(self, lumninance:float):
        if self._luminance == lumninance:
            return
        
        self._luminance = lumninance
        self._brightness = lumninance / glm.dot(self._color, glm.vec3(0.2126, 0.7152, 0.0722))

        for flat in self._flats:
            flat.luminance = self._luminance
            flat.brightness = self._brightness

        self._update_scene_lights()

    @property
    def coverage(self):
        return self._coverage
    
    @coverage.setter
    def coverage(self, coverage:float):
        def func(t):
            K1 = 3.651720188286232 / math.pow(t - 1.379181323137789, 0.956790970458513)
            K2 = 27.101525310782399 / math.pow(t - 2.191989674193149, 1.727016118197271)
            epsilon = 0.01
            return (-K1 + math.sqrt(K1**2 - 4*K2*(1-self._luminance/epsilon)))/(2*K2) - coverage
        
        t = fzero(func, [2.2, 100])
        if t is None:
            t = 2.2

        self._K1 = 3.651720188286232 / math.pow(t - 1.379181323137789, 0.956790970458513)
        self._K2 = 27.101525310782399 / math.pow(t - 2.191989674193149, 1.727016118197271)
        for flat in self._flats:
            flat.K1 = self._K1
            flat.K2 = self._K2

        self.__update_coverage()

    @property
    def K1(self):
        return self._K1
    
    @K1.setter
    @checktype
    def K1(self, K1:float):
        if self._K1 == K1:
            return
        
        self._K1 = K1
        for flat in self._flats:
            flat.K1 = self._K1
            
        self.__update_coverage()

    @property
    def K2(self):
        return self._K2
    
    @K2.setter
    @checktype
    def K2(self, K2:float):
        if self._K2 == K2:
            return
        
        self._K2 = K2
        for flat in self._flats:
            flat.K2 = self._K2

        self.__update_coverage()

class FlatPointLight:

    def __init__(self, point_light:PointLight):
        self.color = point_light._color.flat
        self.brightness = point_light._brightness
        self.ambient = point_light._ambient.flat
        self.diffuse = point_light._diffuse.flat
        self.specular = point_light._specular.flat
        self.K1 = point_light._K1
        self.K2 = point_light._K2
        self.coverage = point_light._coverage
        self.abs_position = glm.vec3(0, 0, 0)

        self._source = point_light
        point_light._flats.add(self)

class PointLights(ShaderStorageBlock.HostClass):

    def __init__(self):
        ShaderStorageBlock.HostClass.__init__(self)
        self.point_lights = DictList()

    def __getitem__(self, path_str:str):
        return self.point_lights[path_str]
    
    @ShaderStorageBlock.HostClass.not_const
    def __setitem__(self, path_str:str, point_light:FlatPointLight):
        self.point_lights[path_str] = point_light

    @ShaderStorageBlock.HostClass.not_const
    def __delitem__(self, path_str:str):
        del self.point_lights[path_str]

    def __contains__(self, path_str:str):
        return (path_str in self.point_lights)
    
    def __len__(self):
        return len(self.point_lights)
    
    def keys(self):
        return self.point_lights.keys()

    @property
    def n_point_lights(self):
        return len(self.point_lights)
    
    