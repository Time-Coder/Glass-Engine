from OpenGL import GL
import numpy as np

from .FBOAttachment import FBOAttachment
from .GLInfo import GLInfo
from .utils import checktype
from .sampler2D import sampler2D


class image2D(sampler2D):

    _default_internal_format = GL.GL_RGBA32F
    _default_filter_min = GL.GL_NEAREST
    _default_filter_mag = GL.GL_NEAREST
    _default_filter_mipmap = None

    @checktype
    def __init__(
        self,
        image: (str, np.ndarray) = None,
        width: int = None,
        height: int = None,
        internal_format: GLInfo.image_internal_formats = None,
    ):
        sampler2D.__init__(self, image, width, height, internal_format)

    @property
    def internal_format(self):
        return self._internal_format

    @internal_format.setter
    @FBOAttachment.param_setter
    def internal_format(self, internal_format: GLInfo.image_internal_formats):
        self._set_internal_format(internal_format)

    @property
    def filter_min(self):
        return GL.GL_NEAREST

    @filter_min.setter
    def filter_min(self, filter_type: GLInfo.filter_types):
        raise RuntimeError("cannot set filter for image2D")

    @property
    def filter_mag(self):
        return GL.GL_NEAREST

    @filter_mag.setter
    def filter_mag(self, filter_type: GLInfo.filter_types):
        raise RuntimeError("cannot set filter for image2D")

    @property
    def filter_mipmap(self):
        return GL.GL_NONE

    @filter_mipmap.setter
    def filter_mipmap(self, filter_type: GLInfo.filter_types):
        raise RuntimeError("cannot set filter for image2D")

    @property
    def filter(self):
        return GL.GL_NEAREST, GL.GL_NEAREST, None

    @filter.setter
    def filter(self, filter_type):
        raise RuntimeError("cannot set filter for image2D")
