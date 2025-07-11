from .ShaderEffect import ShaderEffect
from .PostProcessEffect import PostProcessEffect
from .GaussBlur import GaussBlur
from .MulFilter import MulFilter
from glass import sampler2D

from OpenGL import GL
import os


class SSAOVisibility(ShaderEffect):

    def __init__(self):
        self_folder = os.path.dirname(os.path.abspath(__file__))
        ShaderEffect.__init__(
            self,
            self_folder + "/../glsl/PostProcessEffects/SSAO_visibility.glsl",
            GL.GL_R32F,
        )


class SSAOEffect(PostProcessEffect):

    def __init__(self):
        PostProcessEffect.__init__(self)

        self._ssao_visibility = SSAOVisibility()
        self._gauss_blur = GaussBlur(kernel_shape=16, internal_format=GL.GL_R32F)
        self._mul_filter = MulFilter()

        self.__radius: float = 0.2
        self.__samples: int = 64
        self.__power: float = 2.2

    def apply(self, screen_image: sampler2D) -> sampler2D:
        self._ssao_visibility.camera = self.camera
        self._ssao_visibility.world_pos_map = self.world_pos_map
        self._ssao_visibility.world_normal_map = self.world_normal_map
        self._ssao_visibility.depth_map = self.depth_map
        self._ssao_visibility["radius"] = self.radius
        self._ssao_visibility["samples"] = self.samples
        self._ssao_visibility["power"] = self.power

        ssao_image = self._ssao_visibility.apply(screen_image)
        ssao_image = self._gauss_blur.apply(ssao_image)

        self._mul_filter["filter_image"] = ssao_image
        self._mul_filter["filter_channels"] = 1
        return self._mul_filter.apply(screen_image)

    def need_pos_info(self) -> bool:
        return True

    def draw_to_active(self, screen_image: sampler2D):
        self._ssao_visibility.camera = self.camera
        self._ssao_visibility.world_pos_map = self.world_pos_map
        self._ssao_visibility.world_normal_map = self.world_normal_map
        self._ssao_visibility.depth_map = self.depth_map
        self._ssao_visibility["radius"] = self.radius
        self._ssao_visibility["samples"] = self.samples
        self._ssao_visibility["power"] = self.power

        ssao_image = self._ssao_visibility.apply(screen_image)
        ssao_image = self._gauss_blur.apply(ssao_image)

        self._mul_filter["filter_image"] = ssao_image
        self._mul_filter["filter_channels"] = 1
        self._mul_filter.draw_to_active(screen_image)

    @property
    def radius(self)->float:
        return self.__radius

    @radius.setter
    @PostProcessEffect.param_setter
    def radius(self, value: float):
        self.__radius = value

    @property
    def samples(self)->int:
        return self.__samples
    
    @samples.setter
    @PostProcessEffect.param_setter
    def samples(self, samples:int):
        self.__samples = samples

    @property
    def power(self)->float:
        return self.__power
    
    @power.setter
    @PostProcessEffect.param_setter
    def power(self, power:float):
        self.__power = power
