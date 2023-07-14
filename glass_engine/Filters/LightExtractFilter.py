from .SingleShaderFilter import SingleShaderFilter

from glass.utils import checktype

class LightExtractFilter(SingleShaderFilter):

    def __init__(self, threshold:float=1):
        SingleShaderFilter.__init__(self, "../glsl/Filters/light_extract_filter.glsl")
        self.__threshold = threshold
        self.program["threshold"] = threshold

    @property
    def threshold(self):
        return self.__threshold
    
    @threshold.setter
    @checktype
    def threshold(self, threshold:float):
        self.__threshold = threshold
        self.program["threshold"] = threshold