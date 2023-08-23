from ..SceneNode import SceneNode
from glass.utils import checktype

import glm

class Light(SceneNode):

    def __init__(self, name:str=""):
        SceneNode.__init__(self, name)
        self._color = SceneNode.dvec3(1, 1, 1, callback=self._update_color)
        self._brightness = 1.0
        self._ambient = SceneNode.dvec3(1, 1, 1, callback=self._update_ambient)
        self._diffuse = SceneNode.dvec3(1, 1, 1, callback=self._update_diffuse)
        self._specular = SceneNode.dvec3(1, 1, 1, callback=self._update_specular)
        self._generate_shadows = True
        self._flats = set()

    def _set_transform_dirty(self, scenes):
        self._transform_dirty.update(scenes)
        return True

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

    @property
    def ambient(self):
        return self._ambient
    
    @ambient.setter
    @checktype
    def ambient(self, ambient:glm.vec3):
        if self._ambient == ambient:
            return
        
        self._ambient.r = ambient.r
        self._ambient.g = ambient.g
        self._ambient.b = ambient.b

    @property
    def diffuse(self):
        return self._diffuse
    
    @diffuse.setter
    @checktype
    def diffuse(self, diffuse:glm.vec3):
        if self._diffuse == diffuse:
            return
        
        self._diffuse.r = diffuse.r
        self._diffuse.g = diffuse.g
        self._diffuse.b = diffuse.b

    @property
    def specular(self):
        return self._specular
    
    @specular.setter
    @checktype
    def specular(self, specular:glm.vec3):
        if self._specular == specular:
            return
        
        self._specular.r = specular.r
        self._specular.g = specular.g
        self._specular.b = specular.b

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
            flat.brightness = brightness

        self._update_scene_lights()

    @property
    def generate_shadows(self):
        return self._generate_shadows
    
    @generate_shadows.setter
    @checktype
    def generate_shadows(self, flag:bool):
        self._generate_shadows = flag
        self._update_generate_shadows()

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

    def _update_diffuse(self):
        for flat in self._flats:
            flat.diffuse = self._diffuse

        self._update_scene_lights()

    def _update_specular(self):
        for flat in self._flats:
            flat.specular = self._specular

        self._update_scene_lights()

    def _update_ambient(self):
        for flat in self._flats:
            flat.ambient = self._ambient

        self._update_scene_lights()

    def _update_generate_shadows(self):
        for flat in self._flats:
            flat.generate_shadows = self._generate_shadows

        self._update_scene_lights()
