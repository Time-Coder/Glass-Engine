from ..SceneNode import SceneNode
from ..callback_vec import callback_vec3

from glass.utils import checktype, di
from glass import GLConfig
from ..GlassEngineConfig import GlassEngineConfig

import glm


class Light(SceneNode):

    def __init__(self, name: str = ""):
        SceneNode.__init__(self, name)
        self._color: callback_vec3 = callback_vec3(1, 1, 1, callback=self._update_color)
        self._intensity: float = 1.0
        self._generate_shadows: bool = True
        self._rim_power: float = 0.3
        self._flats: set = set()

        cls_name = self.__class__.__name__
        if cls_name == "DirLight":
            GlassEngineConfig._update_dir_lights()
            GlassEngineConfig._update_dir_lights_generate_shadows(
                self._generate_shadows
            )
        elif cls_name == "PointLight":
            GlassEngineConfig._update_point_lights()
            GlassEngineConfig._update_point_lights_generate_shadows(
                self._generate_shadows
            )
        elif cls_name == "SpotLight":
            GlassEngineConfig._update_spot_lights()
            GlassEngineConfig._update_spot_lights_generate_shadows(
                self._generate_shadows
            )

    def __del__(self):
        cls_name = self.__class__.__name__
        if cls_name == "DirLight":
            GlassEngineConfig._update_dir_lights()
        elif cls_name == "PointLight":
            GlassEngineConfig._update_point_lights()
        elif cls_name == "SpotLight":
            GlassEngineConfig._update_spot_lights()

    @property
    def color(self):
        return self._color

    @color.setter
    @checktype
    def color(self, color: glm.vec3):
        if self._color == color:
            return

        self._color.r = color.r
        self._color.g = color.g
        self._color.b = color.b

    @property
    def intensity(self):
        return self._intensity

    @intensity.setter
    @checktype
    def intensity(self, intensity: float):
        if self._intensity == intensity:
            return

        self._intensity = intensity
        for flat in self._flats:
            flat.intensity = intensity

        self._update_scene_lights()

    @property
    def generate_shadows(self):
        return self._generate_shadows

    @generate_shadows.setter
    @checktype
    def generate_shadows(self, flag: bool):
        self._generate_shadows = flag
        self._update_generate_shadows()

        cls_name = self.__class__.__name__
        if cls_name == "DirLight":
            GlassEngineConfig._update_dir_lights_generate_shadows(
                self._generate_shadows
            )
        elif cls_name == "PointLight":
            GlassEngineConfig._update_point_lights_generate_shadows(
                self._generate_shadows
            )
        elif cls_name == "SpotLight":
            GlassEngineConfig._update_spot_lights_generate_shadows(
                self._generate_shadows
            )

    @property
    def rim_power(self):
        return self._rim_power

    @rim_power.setter
    @checktype
    def rim_power(self, rim_power: float):
        if self._rim_power == rim_power:
            return

        self._rim_power = rim_power
        for flat in self._flats:
            flat.rim_power = rim_power

        self._update_scene_lights()

    def _update_scene_lights(self):
        for scene in self.scenes:
            if self.__class__.__name__ == "PointLight":
                scene._point_lights.dirty = True
            elif self.__class__.__name__ == "DirLight":
                scene._dir_lights.dirty = True
            elif self.__class__.__name__ == "SpotLight":
                scene._spot_lights.dirty = True

    def _update_color(self):
        for flat in self._flats:
            flat.color = self._color

        self._update_scene_lights()

    def _update_generate_shadows(self):
        for flat in self._flats:
            flat.generate_shadows = self._generate_shadows

        self._update_scene_lights()


class FlatLight:

    def __init__(self, light: Light):
        self.depth_fbo_map = {}
        self.depth_map_handle = 0
        self._source_id = 0
        self.update(light)

    @property
    def depth_fbo(self):
        return self.depth_fbo_map.get(GLConfig.buffered_current_context, None)

    @depth_fbo.setter
    def depth_fbo(self, fbo):
        self.depth_fbo_map[GLConfig.buffered_current_context] = fbo

    def update(self, light: Light):
        self.color = light._intensity * light._color.flat
        self.generate_shadows = light._generate_shadows
        self.rim_power = light._rim_power

        self._source_id = id(light)
        light._flats.add(self)

    def before_del(self):
        if self._source_id == 0:
            return

        light = di(self._source_id)
        light._flats.remove(self)
