from .SingleShaderFilter import SingleShaderFilter
from glass.utils import checktype

import glm

class GrayscaleFilter(SingleShaderFilter):

    @checktype
    def __init__(self, weight:glm.vec3=glm.vec3(0.2126, 0.7152, 0.0722)):
        SingleShaderFilter.__init__(self, "../glsl/Filters/gray_scale_filter.glsl")
        self._weight = weight
        self["weight"].bind(self._weight)

    @property
    def weight(self):
        return self.__weight
    
    @weight.setter
    @checktype
    def weight(self, weight:glm.vec3):
        self.__weight.x = weight.x
        self.__weight.y = weight.y
        self.__weight.z = weight.z
