from .sampler2D import sampler2D
from .GLInfo import GLInfo
from .utils import checktype
from .isampler2D import isampler2D

import numpy as np
from OpenGL import GL

class iimage2D(isampler2D):

    _default_internal_format = GL.GL_RGBA32I
    _default_filter_min = GL.GL_NEAREST
    _default_filter_mag = GL.GL_NEAREST
    _default_filter_mipmap = None

    @checktype
    def __init__(self, image:(str,np.ndarray)=None, width:int=None, height:int=None, internal_format:GLInfo.iimage_internal_formats=None):
        isampler2D.__init__(self, image, width, height, internal_format)

    @property
    def internal_format(self):
        return self._internal_format

    @internal_format.setter
    @sampler2D.param_setter
    def internal_format(self, internal_format:GLInfo.iimage_internal_formats):
        self._set_internal_format(internal_format)

    @property
    def filter_min(self):
        return GL.GL_NEAREST

    @filter_min.setter
    def filter_min(self, filter_type:GLInfo.filter_types):
        raise RuntimeError("cannot set filter for iimage2D")

    @property
    def filter_mag(self):
        return GL.GL_NEAREST

    @filter_mag.setter
    def filter_mag(self, filter_type:GLInfo.filter_types):
        raise RuntimeError("cannot set filter for iimage2D")

    @property
    def filter_mipmap(self):
        return GL.GL_NONE

    @filter_mipmap.setter
    def filter_mipmap(self, filter_type:GLInfo.filter_types):
        raise RuntimeError("cannot set filter for iimage2D")
        
    @property
    def filter(self):
        return GL.GL_NEAREST, GL.GL_NEAREST, None

    @filter.setter
    def filter(self, filter_type):
        raise RuntimeError("cannot set filter for iimage2D")