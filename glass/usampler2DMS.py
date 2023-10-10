from .sampler2DMS import sampler2DMS
from .GLInfo import GLInfo
from .utils import checktype

from OpenGL import GL
import OpenGL.GL.ARB.bindless_texture as bt

class usampler2DMS(sampler2DMS):

    @checktype
    def __init__(self, width:int=0, height:int=0, samples:int=4, internal_format:GLInfo.usampler_internal_formats=None):
        if internal_format is None:
            internal_format = GL.GL_RGBA32UI

        sampler2DMS.__init__(self, width, height, samples, internal_format)

    @property
    def internal_format(self):
        return self._internal_format

    @internal_format.setter
    @checktype
    def internal_format(self, format:GLInfo.usampler_internal_formats):
        if self._internal_format != format:
            self._internal_format = format
            self._param_changed = True

    @property
    def handle(self):
        if not bt.glGetTextureHandleARB:
            return 0
        
        self.bind()
        if self._handle == 0:
            self._handle = bt.glGetTextureHandleARB(self._id)
            if self._handle == 0:
                raise RuntimeError(f"failed to create isampler2D {self._id}'s handle")
            bt.glMakeTextureHandleResidentARB(self._handle)
            self._dynamic = False

        return self._handle