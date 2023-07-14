from .sampler2D import sampler2D
from .GLInfo import GLInfo
from .utils import checktype

import numpy as np

class image2D(sampler2D):
    @checktype
    def __init__(self, image:(str,np.ndarray)=None, width:int=None, height:int=None, internal_format:GLInfo.image_internal_formats=None):
        sampler2D.__init__(self, image, width, height, internal_format)
        if self._internal_format not in GLInfo.image_internal_formats:
            raise ValueError(f"image2D internal format must be in {GLInfo.image_internal_formats}, {self._internal_format} is given")

    @property
    def internal_format(self):
        return self._internal_format

    @internal_format.setter
    @sampler2D.param_setter
    def internal_format(self, internal_format:GLInfo.image_internal_formats):
        self._set_internal_format(internal_format)