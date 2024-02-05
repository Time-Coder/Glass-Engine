import os

os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
import cv2
import numpy as np
import glm
from OpenGL import GL
import OpenGL.GL.ARB.bindless_texture as bt

from .FBOAttachment import FBOAttachment
from .GLInfo import GLInfo
from .utils import checktype
from .helper import get_dtype, get_channels, width_adapt, get_external_format
from .ImageLoader import ImageLoader
from .DictList import DictList


class samplerCube(FBOAttachment):

    _basic_info = {
        "gen_func": GL.glGenTextures,
        "bind_func": GL.glBindTexture,
        "del_func": GL.glDeleteTextures,
        "target_type": GL.GL_TEXTURE_CUBE_MAP,
        "binding_type": GL.GL_TEXTURE_BINDING_CUBE_MAP,
        "need_number": True,
    }

    class Face:
        def __init__(
            self,
            sampler_cube,
            texture_target,
            width: int = 0,
            height: int = 0,
            internal_format: GLInfo.internal_formats = GL.GL_RGBA32F,
        ):
            self._texture_target = texture_target
            self._sampler_cube = sampler_cube
            self._dynamic = sampler_cube.dynamic

            self._image = None
            self._width = width
            self._height = height
            self._internal_format = internal_format
            self._dtype = None

            self._image_changed = True

        @property
        def dynamic(self):
            return self._dynamic

        @property
        def width(self):
            return self._width

        @width.setter
        @FBOAttachment.param_setter
        def width(self, width: int):
            self._width = width
            if self._image is not None:
                if len(self._image.shape) > 2:
                    cv2.resize(
                        self._image, (self._image.shape[0], width, self._image.shape[2])
                    )
                else:
                    cv2.resize(self._image, (self._image.shape[0], width))

            self._image_changed = True

        @property
        def height(self):
            return self._height

        @height.setter
        @FBOAttachment.param_setter
        def height(self, height: int):
            self._height = height
            if self._image is not None:
                if len(self._image.shape) > 2:
                    cv2.resize(
                        self._image,
                        (height, self._image.shape[1], self._image.shape[2]),
                    )
                else:
                    cv2.resize(self._image, (height, self._image.shape[1]))

            self._image_changed = True

        @property
        def dtype(self):
            return get_dtype(self._internal_format)

        @property
        def internal_format(self):
            return self._internal_format

        @internal_format.setter
        @FBOAttachment.param_setter
        def internal_format(self, format: GLInfo.internal_formats):
            if self._internal_format == format:
                return

            self._internal_format = format
            if self._image is not None:
                old_channels = self._image.shape[2] if len(self._image.shape) > 2 else 1
                new_channels = get_channels(format)
                if old_channels == 3 and new_channels == 4:
                    self._image = cv2.cvtColor(self._image, cv2.COLOR_RGB2RGBA)
                elif old_channels == 4 and new_channels == 3:
                    self._image = cv2.cvtColor(self._image, cv2.COLOR_RGBA2RGB)
                elif old_channels != new_channels:
                    self._image = None
            if self._image is not None:
                old_np_dtype = self._image.dtype
                new_np_dtype = GLInfo.dtype_map[get_dtype(self._internal_format)]
                if old_np_dtype != new_np_dtype:
                    self._image = self._image.astype(new_np_dtype)
            self._image_changed = True

        @property
        def image(self):
            return self._image

        @image.setter
        @FBOAttachment.param_setter
        def image(self, image: (np.ndarray, str)):
            if isinstance(image, str):
                image = ImageLoader.load(image)

            self._image = image

            self._width = self._image.shape[1]
            self._height = self._image.shape[0]
            channels = self._image.shape[2] if len(self._image.shape) > 2 else 1
            self._internal_format = GLInfo.internal_formats_map[self._image.dtype][
                channels
            ]
            self._dtype = GLInfo.dtype_inverse_map[self._image.dtype]

            self._image_changed = True

        @property
        def target(self):
            return self._texture_target

        def _apply(self, force_update_image: bool = False):
            if not self._image_changed and not force_update_image:
                return False

            width_adapt(self._width)
            external_format = get_external_format(self._internal_format)
            GL.glTexImage2D(
                self._texture_target,
                0,
                self._internal_format,
                self._width,
                self._height,
                0,
                external_format,
                self.dtype,
                self._image,
            )
            self._image_changed = False

            return True

        @checktype
        def malloc(
            self,
            width: int,
            height: int,
            internal_format: GLInfo.internal_formats = None,
        ):
            self.width = width
            self.height = height

            if internal_format is None:
                internal_format = self.internal_format

            if internal_format is None:
                internal_format = GL.GL_RGBA32F

            self.internal_format = internal_format

    def __init__(
        self,
        width: int = 0,
        height: int = 0,
        internal_format: GLInfo.internal_formats = GL.GL_RGBA32F,
    ):
        FBOAttachment.__init__(self)

        self._handle = 0
        self._dynamic = True

        self._faces = DictList()
        self._faces["right"] = samplerCube.Face(
            self, GL.GL_TEXTURE_CUBE_MAP_POSITIVE_X, width, height, internal_format
        )
        self._faces["left"] = samplerCube.Face(
            self, GL.GL_TEXTURE_CUBE_MAP_NEGATIVE_X, width, height, internal_format
        )
        self._faces["bottom"] = samplerCube.Face(
            self, GL.GL_TEXTURE_CUBE_MAP_POSITIVE_Y, width, height, internal_format
        )
        self._faces["top"] = samplerCube.Face(
            self, GL.GL_TEXTURE_CUBE_MAP_NEGATIVE_Y, width, height, internal_format
        )
        self._faces["front"] = samplerCube.Face(
            self, GL.GL_TEXTURE_CUBE_MAP_POSITIVE_Z, width, height, internal_format
        )
        self._faces["back"] = samplerCube.Face(
            self, GL.GL_TEXTURE_CUBE_MAP_NEGATIVE_Z, width, height, internal_format
        )

        self._wrap_s = GL.GL_CLAMP_TO_EDGE
        self._wrap_t = GL.GL_CLAMP_TO_EDGE
        self._wrap_r = GL.GL_CLAMP_TO_EDGE
        self._filter_min = GL.GL_LINEAR
        self._filter_mag = GL.GL_LINEAR
        self._filter_mipmap = GL.GL_LINEAR
        self._border_color = glm.vec4(0, 0, 0, 1)

        self._wrap_s_changed = True
        self._wrap_t_changed = True
        self._wrap_r_changed = True
        self._filter_min_changed = True
        self._filter_mag_changed = True
        self._border_color_changed = False

    def __del__(self):
        if self._handle != 0:
            self._handle = 0

        FBOAttachment.__del__(self)

    def __getitem__(self, key: (str, int)):
        if key == "up":
            key = "top"
        elif key == "down":
            key = "bottom"

        return self._faces[key]

    @checktype
    def __setitem__(self, key: str, value: (np.ndarray, str)):
        if key == "up":
            key = "top"
        elif key == "down":
            key = "bottom"

        self._faces[key].image = value

    def __getattr__(self, key):
        if key not in ["right", "left", "top", "bottom", "back", "front", "up", "down"]:
            return super().__getattribute__(key)

        return self[key]

    def __setattr__(self, key, value):
        if key not in ["right", "left", "top", "bottom", "back", "front", "up", "down"]:
            return super().__setattr__(key, value)

        self[key] = value

    @property
    def handle(self):
        if not bt.glGetTextureHandleARB:
            return 0

        if self._id == 0:
            return 0

        if self._handle == 0:
            self._handle = bt.glGetTextureHandleARB(self._id)
            if self._handle == 0:
                raise RuntimeError("failed to create samplerCube {self._id}'s handle")
            bt.glMakeTextureHandleResidentARB(self._handle)
            self._dynamic = False

        return self._handle

    @property
    def is_completed(self):
        for face in self._faces:
            if face.width <= 0 or face.height <= 0:
                return False

        return True

    def bind(self, update_fbo: bool = False, force_update_image: bool = False):
        FBOAttachment.bind(self, update_fbo, force_update_image)
        GL.glEnable(GL.GL_TEXTURE_CUBE_MAP_SEAMLESS)

        if self._wrap_s_changed:
            GL.glTexParameteri(
                GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_WRAP_S, self._wrap_s
            )
            self._wrap_s_changed = False
        if self._wrap_t_changed:
            GL.glTexParameteri(
                GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_WRAP_T, self._wrap_t
            )
            self._wrap_t_changed = False
        if self._wrap_r_changed:
            GL.glTexParameteri(
                GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_WRAP_R, self._wrap_r
            )
            self._wrap_r_changed = False
        if self._border_color_changed:
            GL.glTexParameterfv(
                GL.GL_TEXTURE_CUBE_MAP,
                GL.GL_TEXTURE_BORDER_COLOR,
                glm.value_ptr(self._border_color),
            )
            self._border_color_changed = False

        if self._filter_min_changed:
            GL.glTexParameteri(
                GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_MIN_FILTER, self._get_filter_min()
            )
            self._filter_min_changed = False
        if self._filter_mag_changed:
            GL.glTexParameteri(
                GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_MAG_FILTER, self._filter_mag
            )
            self._filter_mag_changed = False

        image_changed = False
        for face in self._faces:
            image_changed = face._apply(force_update_image) or image_changed

        if not update_fbo and self._filter_mipmap is not None:
            generated_mipmap = False
            if image_changed:
                self.generate_mipmap()
                generated_mipmap = True

            if not generated_mipmap and not self._fbo_image_generated_mipmap:
                self.generate_mipmap()

    def generate_mipmap(self):
        FBOAttachment.bind(self)
        GL.glGenerateMipmap(GL.GL_TEXTURE_CUBE_MAP)
        self._fbo_image_generated_mipmap = True

    @property
    def internal_format(self):
        return self._faces[0].internal_format

    @internal_format.setter
    @FBOAttachment.param_setter
    def internal_format(self, internal_format: GLInfo.internal_formats):
        for i in range(6):
            self._faces[i].internal_format = internal_format

    @property
    def wrap_s(self):
        return self._wrap_s

    @wrap_s.setter
    @FBOAttachment.param_setter
    def wrap_s(self, wrap_type: GLInfo.wrap_types):
        self._wrap_s = wrap_type
        self._wrap_s_changed = True

    @property
    def wrap_t(self):
        return self._wrap_t

    @wrap_t.setter
    @FBOAttachment.param_setter
    def wrap_t(self, wrap_type: GLInfo.wrap_types):
        self._wrap_t = wrap_type
        self._wrap_t_changed = True

    @property
    def wrap_r(self):
        return self._wrap_r

    @wrap_r.setter
    @FBOAttachment.param_setter
    def wrap_r(self, wrap_type: GLInfo.wrap_types):
        self._wrap_r = wrap_type
        self._wrap_r_changed = True

    @property
    def wrap(self):
        return self._wrap_s, self._wrap_t, self._wrap_r

    @wrap.setter
    @FBOAttachment.param_setter
    def wrap(self, wrap_type):
        if wrap_type in GLInfo.wrap_types:
            self.wrap_s = wrap_type
            self.wrap_t = wrap_type
            self.wrap_r = wrap_type
        else:
            self.wrap_s = wrap_type[0]
            self.wrap_t = wrap_type[1]
            self.wrap_r = wrap_type[2]

    @property
    def filter_min(self):
        return self._filter_min

    @filter_min.setter
    @FBOAttachment.param_setter
    def filter_min(self, filter_type: GLInfo.filter_types):
        self._filter_min = filter_type
        self._filter_min_changed = True

    @property
    def filter_mag(self):
        return self._filter_mag

    @filter_mag.setter
    @FBOAttachment.param_setter
    def filter_mag(self, filter_type: GLInfo.filter_types):
        self._filter_mag = filter_type
        self._filter_mag_changed = True

    @property
    def filter_mipmap(self):
        return self._filter_mipmap

    @filter_mipmap.setter
    @FBOAttachment.param_setter
    def filter_mipmap(self, filter_type: GLInfo.filter_types):
        self._filter_mipmap = filter_type
        self._filter_min_changed = True
        self._filter_mag_changed = True

    def _get_filter_min(self):
        if self._filter_mipmap is None:
            return self._filter_min
        else:
            return GLInfo.mipmap_filter_map[(self._filter_min, self._filter_mipmap)]

    @property
    def filter(self):
        return self._filter_min, self._filter_mag, self._filter_mipmap

    @filter.setter
    @FBOAttachment.param_setter
    def filter(self, filter_type):
        if filter_type in GLInfo.filter_types:
            self.filter_min = filter_type
            self.filter_mag = filter_type
        else:
            self.filter_min = filter_type[0]
            self.filter_mag = filter_type[1]

    @property
    def border_color(self):
        return self._border_color

    @border_color.setter
    @FBOAttachment.param_setter
    def border_color(self, color: (glm.vec3, glm.vec4)):
        if isinstance(color, glm.vec3):
            color = glm.vec4(color, 1)

        self._border_color = color
        self._border_color_changed = True

    @checktype
    def malloc(
        self,
        width: int,
        height: int,
        samples: int = None,
        layers: int = None,
        internal_format: GLInfo.internal_formats = None,
    ):
        for face in self._faces:
            face.malloc(width, height, internal_format)

    @property
    def width(self):
        return self.faces[0].width

    @property
    def height(self):
        return self.faces[0].height

    @property
    def layers(self):
        return 6

    @property
    def faces(self):
        return self._faces

    @property
    def samples(self):
        return None

    @samples.setter
    def samples(self, samples: int):
        pass
