from .sampler2DMS import sampler2DMS
from .GLInfo import GLInfo
from .utils import checktype
from .ShaderStorageBlock import ShaderStorageBlock

from OpenGL import GL
import OpenGL.GL.ARB.bindless_texture as bt

class isampler2DMS(sampler2DMS):

    class BindlessISampler2DMSs(ShaderStorageBlock.HostClass):
        def __init__(self):
            ShaderStorageBlock.HostClass.__init__(self)
            self.bindless_isampler2DMSs = [0]

        @property
        def n_bindless_isampler2DMSs(self):
            return len(self.bindless_isampler2DMSs)

        @ShaderStorageBlock.HostClass.not_const
        def append(self, handle:int)->int:
            index = len(self.bindless_isampler2DMSs)
            self.bindless_isampler2DMSs.append(handle)
            return index
        
    BindlessISampler2DMSs = BindlessISampler2DMSs()

    @checktype
    def __init__(self, width:int=0, height:int=0, samples:int=4, internal_format:GLInfo.iimage_internal_formats=None):
        if internal_format is None:
            internal_format = GL.GL_RGBA32I

        sampler2DMS.__init__(self, width, height, samples, internal_format)

    @property
    def internal_format(self):
        return self._internal_format

    @internal_format.setter
    @checktype
    def internal_format(self, format:GLInfo.iimage_internal_formats):
        if self._internal_format != format:
            self._internal_format = format
            self._param_changed = True

    @property
    def handle(self):
        self.bind()
        if self._handle == 0:
            self._handle = bt.glGetTextureHandleARB(self._id)
            if self._handle == 0:
                raise RuntimeError(f"failed to create isampler2D {self._id}'s handle")
            bt.glMakeTextureHandleResidentARB(self._handle)
            self._index = isampler2DMS.BindlessISampler2DMSs.append(self._handle)
            
            self._dynamic = False

        return self._handle
    
    @property
    def index(self):
        self.bind()
        if self._handle == 0:
            self._handle = bt.glGetTextureHandleARB(self._id)
            if self._handle == 0:
                raise RuntimeError(f"failed to create sampler2D {self._id}'s handle")
            bt.glMakeTextureHandleResidentARB(self._handle)
            self._index = isampler2DMS.BindlessISampler2DMSs.append(self._handle)
            
            self._dynamic = False

        return self._index
    