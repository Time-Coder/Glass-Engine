from .SkyBox import SkyBox
from .SkyDome import SkyDome

from glass import samplerCube, sampler2D

import glm

class Background:
    def __init__(self):
        self._skybox:SkyBox = SkyBox()
        self._skydome:SkyDome = SkyDome()
        self._color:glm.vec4 = glm.vec4(0)
        self._distance:float = 100.0

    @property
    def skybox(self):
        return self._skybox
    
    @skybox.setter
    def skybox(self, skybox_map:samplerCube):
        self._skybox.skybox_map = skybox_map
    
    @property
    def skydome(self):
        return self._skydome
    
    @skydome.setter
    def skydome(self, image:str):
        self._skydome.skydome_map = image

    @property
    def skybox_map(self)->samplerCube:
        return self._skybox.skybox_map
    
    @property
    def skydome_map(self)->sampler2D:
        return self._skydome.skydome_map

    @property
    def distance(self)->float:
        return self._distance
    
    @distance.setter
    def distance(self, distance:float)->None:
        self._distance = distance

    @property
    def color(self)->glm.vec4:
        return self._color
    
    @color.setter
    def color(self, color:(glm.vec4,glm.vec3))->None:
        if isinstance(color, glm.vec3):
            color = glm.vec4(color, 1)

        self._color = color