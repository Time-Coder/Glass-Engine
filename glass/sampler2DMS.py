from OpenGL import GL
import OpenGL.GL.ARB.bindless_texture as bt

from .FBOAttachment import FBOAttachment
from .GLInfo import GLInfo
from .utils import checktype
from .helper import get_dtype


class sampler2DMS(FBOAttachment):

    _basic_info = {
        "gen_func": GL.glGenTextures,
        "bind_func": GL.glBindTexture,
        "del_func": GL.glDeleteTextures,
        "target_type": GL.GL_TEXTURE_2D_MULTISAMPLE,
        "binding_type": GL.GL_TEXTURE_BINDING_2D_MULTISAMPLE,
        "need_number": True,
    }

    def __init__(
        self,
        width: int = 0,
        height: int = 0,
        samples: int = 4,
        internal_format: GLInfo.internal_formats = GL.GL_RGBA32F,
    ):
        FBOAttachment.__init__(self)

        self._handle = 0
        self._samples = samples
        self._width = width
        self._height = height
        self._internal_format = internal_format
        self._param_changed = True

    def __del__(self):
        if self._handle != 0:
            self._handle = 0

        FBOAttachment.__del__(self)

    def __deepcopy__(self, memo):
        result = sampler2DMS()
        result._samples = self._samples
        result._width = self._width
        result._height = self._height
        result._internal_format = self._internal_format

        return result

    def bind(self, update_fbo: bool = False, force_update_image: bool = False):
        FBOAttachment.bind(self, update_fbo, force_update_image)
        if force_update_image or self._param_changed:
            GL.glTexImage2DMultisample(
                GL.GL_TEXTURE_2D_MULTISAMPLE,
                self._samples,
                self._internal_format,
                self._width,
                self._height,
                GL.GL_TRUE,
            )
            self._param_changed = False

    @property
    def handle(self):
        if not bt.glGetTextureHandleARB:
            return 0

        if self._id == 0:
            return 0

        if self._handle == 0:
            self._handle = bt.glGetTextureHandleARB(self._id)
            if self._handle == 0:
                raise RuntimeError(f"failed to create sampler2D {self._id}'s handle")
            self._dynamic = False
            bt.glMakeTextureHandleResidentARB(self._handle)

        return self._handle

    @property
    def samples(self):
        return self._samples

    @samples.setter
    @FBOAttachment.param_setter
    def samples(self, samples: int):
        self._samples = samples
        self._param_changed = True

    @property
    def width(self):
        return self._width

    @width.setter
    @FBOAttachment.param_setter
    def width(self, width: int):
        self._width = width
        self._param_changed = True

    @property
    def height(self):
        return self._height

    @height.setter
    @FBOAttachment.param_setter
    def height(self, height: int):
        self._height = height
        self._param_changed = True

    @property
    def dtype(self):
        return get_dtype(self._internal_format)

    @property
    def internal_format(self):
        return self._internal_format

    @internal_format.setter
    @FBOAttachment.param_setter
    def internal_format(self, format: GLInfo.internal_formats):
        self._internal_format = format
        self._param_changed = True

    def update(self):
        self._param_changed = True

    @checktype
    def malloc(
        self,
        width: int,
        height: int,
        samples: int = 4,
        layers: int = None,
        internal_format: GLInfo.internal_formats = None,
    ):
        self.width = width
        self.height = height
        self.samples = samples

        if internal_format is None:
            internal_format = self.internal_format

        if internal_format is None:
            internal_format = GL.GL_RGBA32F

        self.internal_format = internal_format

    @property
    def is_completed(self):
        return self._width > 0 and self._height > 0
