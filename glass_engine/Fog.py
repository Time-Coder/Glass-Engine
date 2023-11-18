import glm
import math
from enum import Enum
from OpenGL import GL

from glass.utils import checktype
from glass.MetaInstancesRecorder import MetaInstancesRecorder
from glass import GLInfo
from .GlassEngineConfig import GlassEngineConfig

class Fog(metaclass=MetaInstancesRecorder):

    class Mode(Enum):
        Linear = GL.GL_LINEAR
        Exp = GL.GL_EXP
        Exp2 = GL.GL_EXP2

    @MetaInstancesRecorder.init
    def __init__(self):
        self._mode = Fog.Mode.Exp
        self._color = glm.vec3(1, 1, 1)
        self._extinction_density = 0
        self._inscattering_density = 0

    @MetaInstancesRecorder.delete
    def __del__(self):
        pass

    def apply(self, color:(glm.vec3, glm.vec4), camera_pos:glm.vec3, frag_pos:glm.vec3):
        if self.extinction_density < 1E-6 and \
           self.inscattering_density < 1E-6:
            return color

        d = glm.length(frag_pos - camera_pos)
        extinction = 1
        inscattering = 1
        if self.mode == Fog.Mode.Linear:
            extinction = max(0, 1 - self.extinction_density*d)
            inscattering = max(0, 1 - self.inscattering_density*d)
        elif self.mode == Fog.Mode.Exp:
            extinction = math.exp(-self.extinction_density*d)
            inscattering = math.exp(-self.inscattering_density*d)
        elif self.mode == Fog.Mode.Exp2:
            extinction = math.exp(-self.extinction_density*d*d)
            inscattering = math.exp(-self.inscattering_density*d*d)

        self_color = self.color
        if isinstance(color, glm.vec4):
            self_color = glm.vec4(self_color, 1)

        return color * extinction + self_color * (1 - inscattering)

    @property
    def mode(self)->Mode:
        return self._mode
    
    @mode.setter
    @checktype
    def mode(self, mode:[Mode.Linear, Mode.Exp, Mode.Exp2, *GLInfo.fog_modes]):
        if mode in GLInfo.fog_modes:
            mode = Fog.Mode(mode)

        self._mode = mode

    @property
    def color(self)->glm.vec3:
        return self._color
    
    @color.setter
    @checktype
    def color(self, color:glm.vec3):
        self._color = color

    @property
    def density(self)->float:
        return self._extinction_density
    
    @density.setter
    @checktype
    def density(self, density:float):
        self._extinction_density = density
        self._inscattering_density = density
        GlassEngineConfig._update_fog()

    @property
    def extinction_density(self)->float:
        return self._extinction_density
    
    @extinction_density.setter
    @checktype
    def extinction_density(self, density:float):
        self._extinction_density = density
        GlassEngineConfig._update_fog()

    @property
    def inscattering_density(self)->float:
        return self._inscattering_density
    
    @inscattering_density.setter
    @checktype
    def inscattering_density(self, density:float):
        self._inscattering_density = density
        GlassEngineConfig._update_fog()
        