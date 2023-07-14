from .sampler2D import sampler2D
from .GLInfo import GLInfo
from .utils import checktype
from .ShaderStorageBlock import ShaderStorageBlock

import numpy as np
from OpenGL import GL
import OpenGL.GL.ARB.bindless_texture as bt

class usampler2D(sampler2D):

    class BindlessUSampler2Ds(ShaderStorageBlock.HostClass):
        def __init__(self):
            ShaderStorageBlock.HostClass.__init__(self)
            self.bindless_usampler2Ds = [0]

        @property
        def n_bindless_usampler2Ds(self):
            return len(self.bindless_usampler2Ds)

        @ShaderStorageBlock.HostClass.not_const
        def append(self, handle:int)->int:
            index = len(self.bindless_usampler2Ds)
            self.bindless_usampler2Ds.append(handle)
            return index
        
    BindlessUSampler2Ds = BindlessUSampler2Ds()

    _default_internal_format = GL.GL_RGBA32UI
    _default_filter_min = GL.GL_NEAREST
    _default_filter_mag = GL.GL_NEAREST
    _default_filter_mipmap = None

    @checktype
    def __init__(self, image:(str,np.ndarray)=None, width:int=None, height:int=None, internal_format:GLInfo.uimage_internal_formats=None):
        if internal_format is None:
            internal_format = GL.GL_RGBA32UI

        sampler2D.__init__(self, image, width, height, internal_format)

    @property
    def internal_format(self):
        return self._internal_format

    @internal_format.setter
    @sampler2D.param_setter
    def internal_format(self, internal_format:GLInfo.uimage_internal_formats):
        self._set_internal_format(internal_format)

    @property
    def handle(self):
        self.bind()
        if self._handle == 0:
            self._handle = bt.glGetTextureHandleARB(self._id)
            if self._handle == 0:
                raise RuntimeError(f"failed to create usampler2D {self._id}'s handle")
            bt.glMakeTextureHandleResidentARB(self._handle)
            self._index = usampler2D.BindlessUSampler2Ds.append(self._handle)
            
            self._dynamic = False

        return self._handle
    
    @property
    def index(self):
        self.bind()
        if self._handle == 0:
            self._handle = bt.glGetTextureHandleARB(self._id)
            if self._handle == 0:
                raise RuntimeError(f"failed to create usampler2D {self._id}'s handle")
            bt.glMakeTextureHandleResidentARB(self._handle)
            self._index = usampler2D.BindlessUSampler2Ds.append(self._handle)
            
            self._dynamic = False

        return self._index
    
uimage2D = usampler2D