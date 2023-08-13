from .PointLight import PointLight
from glass.utils import checktype, id_to_var
from glass.DictList import DictList
from glass.ShaderStorageBlock import ShaderStorageBlock

import glm
import math

class SpotLight(PointLight):

    def __init__(self, name:str=""):
        PointLight.__init__(self, name)
        self._span_angle = 30
        self._softness = 10
        self.__update_aggregate_coeff()

    def __update_aggregate_coeff(self):
        half_span_angle_rad = self._span_angle/180*math.pi/2
        self._aggregate_coeff = 0.2/(1.1-math.cos(half_span_angle_rad))
        for flat in self._flats:
            flat.aggregate_coeff = self._aggregate_coeff

        self._update_scene_lights()

    @property
    def span_angle(self):
        return self._span_angle

    @span_angle.setter
    @checktype
    def span_angle(self, span_angle:float):
        if self._span_angle == span_angle:
            return

        self._span_angle = span_angle
        for flat in self._flats:
            flat.span_angle = span_angle

        self.__update_aggregate_coeff()

    @property
    def aggregate_coeff(self):
        return self._aggregate_coeff

    @property
    def softness(self):
        return self._softness
    
    @softness.setter
    @checktype
    def softness(self, softness:float):
        if self._softness == softness:
            return

        self._softness = softness
        for flat in self._flats:
            flat.softness = softness

        self._update_scene_lights()

class FlatSpotLight:

    def __init__(self, spot_light:SpotLight):
        self.abs_position = glm.vec3(0, 0, 0)
        self.direction = glm.vec3(0, 1, 0)
        self.depth_fbo = None
        self.depth_map_handle = 0
        self.need_update_depth_map = True
        self.update(spot_light)

    def update(self, spot_light:SpotLight):
        self.color = spot_light._color.flat
        self.brightness = spot_light._brightness
        self.ambient = spot_light._ambient.flat
        self.diffuse = spot_light._diffuse.flat
        self.specular = spot_light._specular.flat
        self.half_span_angle_rad = spot_light._span_angle/180*math.pi/2
        self.half_softness_rad = spot_light._softness/180*math.pi/2
        self.K1 = spot_light._K1
        self.K2 = spot_light._K2
        self.coverage = spot_light._coverage
        self.aggregate_coeff = spot_light.aggregate_coeff
        self.generate_shadows = spot_light.generate_shadows
        self._source_id = id(spot_light)
        spot_light._flats.add(self)

    def before_del(self):
        spot_light = id_to_var(self._source_id)
        spot_light._flats.remove(self)

class SpotLights(ShaderStorageBlock.HostClass):

    def __init__(self):
        ShaderStorageBlock.HostClass.__init__(self)
        self.spot_lights = DictList()

    def __getitem__(self, path_str:str):
        return self.spot_lights[path_str]
    
    @ShaderStorageBlock.HostClass.not_const
    def __setitem__(self, path_str:str, spot_light:FlatSpotLight):
        self.spot_lights[path_str] = spot_light

    @ShaderStorageBlock.HostClass.not_const
    def __delitem__(self, path_str:str):
        del self.spot_lights[path_str]

    def __contains__(self, path_str:str):
        return (path_str in self.spot_lights)
    
    def __len__(self):
        return len(self.spot_lights)
    
    def __iter__(self):
        return iter(self.spot_lights)

    def keys(self):
        return self.spot_lights.keys()

    @property
    def n_spot_lights(self):
        return len(self.spot_lights)