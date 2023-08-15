import os

import cv2
import numpy as np
from OpenGL import GL
from functools import wraps
import random

from .GLObject import GLObject
from .GLConfig import GLConfig
from .GLInfo import GLInfo
from .utils import checktype
from .ImageLoader import ImageLoader
from .TextureUnits import TextureUnits
from .helper import get_external_format, get_dtype, width_adapt, get_channels

class image2D(GLObject):

    _basic_info = \
    {
        "gen_func": GL.glGenTextures,
        "bind_func": GL.glBindTexture,
        "del_func": GL.glDeleteTextures,
        "target_type": GL.GL_TEXTURE_2D,
        "binding_type": GL.GL_TEXTURE_BINDING_2D,
        "need_number": True,
    }

    _image2D_map = {}

    @checktype
    def __init__(self, image:(str,np.ndarray)=None, width:int=None, height:int=None, internal_format:GLInfo.internal_formats=None):
        GLObject.__init__(self)
        
        self._handle = 0
        self._image = None
        self._width = 0
        self._height = 0
        self._internal_format = GL.GL_RGBA32F

        self._image_changed = True
        self._dynamic = True

        if image is not None:
            self.image = image

        if width is not None:
            self.width = width

        if height is not None:
            self.height = height

        if internal_format is not None:
            self.internal_format = internal_format

    def __hash__(self):
        return id(self)

    def __deepcopy__(self, memo):
        result = self.__class__()
        result._image = self._image
        result._width = self._width
        result._height = self._height
        result._internal_format = self._internal_format
        result._dynamic = self._dynamic

        return result

    @classmethod
    def load(cls, file_name:str, internal_format:GLInfo.internal_formats=None):
        if not os.path.isfile(file_name):
            raise FileNotFoundError("not a valid image file: " + file_name)
        
        file_name = os.path.abspath(file_name).replace("\\", "/")
        if file_name not in image2D._image2D_map:
            image = cls(file_name, internal_format=internal_format)
            image._dynamic = False
            image2D._image2D_map[file_name] = image

        return image2D._image2D_map[file_name]

    def clear(self):
        if self._id == 0:
            return

        self.bind()
        external_format = get_external_format(self._internal_format)
        dtype = get_dtype(self._internal_format)
        GL.glClearTexImage(self._id, 0, external_format, dtype, None)

    def bind(self, force_update_image:bool=False):
        target_type = self.__class__._basic_info["target_type"]
        texture_unit = None
        if self._id == 0:
            texture_unit = TextureUnits.available_unit
        else:
            texture_unit = TextureUnits.unit_of_texture((target_type, self._id))
            if texture_unit is None:
                texture_unit = TextureUnits.available_unit

        if texture_unit is None:
            texture_unit = random.randint(0, GLConfig.max_texture_units-1)

        GLConfig.active_texture_unit = texture_unit
        GLObject.bind(self)
        TextureUnits[texture_unit] = (target_type, self._id)

        if force_update_image or self._image_changed:
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)
            external_format = get_external_format(self._internal_format)
            width_adapt(self._width)
            GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, self._internal_format,
                            self._width, self._height, 0, external_format, self.dtype, self._image)

            self._image_changed = False

    def unbind(self):
        success = GLObject.unbind(self)
        target_type = self.__class__._basic_info["target_type"]
        assert TextureUnits.current_texture == (target_type, self._id)
        TextureUnits.current_texture = (target_type, 0)

        return success

    @staticmethod
    def param_setter(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            value = args[1]

            equal = False
            try:
                lvalue = getattr(self, func.__name__)
                if type(lvalue) != type(value):
                    equal = False
                else:
                    equal = bool(getattr(self, func.__name__) == value)
            except:
                equal = False

            if equal:
                return

            if not self.dynamic:
                raise RuntimeError("none dynamic image2D cannot change any parameters")

            safe_func = checktype(func)
            return_value = safe_func(*args, **kwargs)

            return return_value

        return wrapper

    @property
    def dynamic(self):
        return self._dynamic

    @property
    def width(self):
        return self._width

    @width.setter
    @param_setter
    def width(self, width:int):
        self._width = width
        if self._image is not None:
            if len(self._image.shape) > 2:
                cv2.resize(self._image, (width, self._image.shape[0], self._image.shape[2]))
            else:
                cv2.resize(self._image, (width, self._image.shape[0]))

        self._image_changed = True

    @property
    def height(self):
        return self._height

    @height.setter
    @param_setter
    def height(self, height:int):
        self._height = height
        if self._image is not None:
            if len(self._image.shape) > 2:
                cv2.resize(self._image, (self._image.shape[1], height, self._image.shape[2]))
            else:
                cv2.resize(self._image, (self._image.shape[1], height))

        self._image_changed = True

    @property
    def dtype(self):
        return get_dtype(self._internal_format)

    @property
    def internal_format(self):
        return self._internal_format

    def _set_internal_format(self, internal_format):
        self._internal_format = internal_format

        if self._image is not None:
            old_channels = self._image.shape[2] if len(self._image.shape) > 2 else 1
            new_channels = get_channels(internal_format)
            convert_map = \
            {
                (1,3): cv2.COLOR_GRAY2RGB,
                (1,4): cv2.COLOR_GRAY2RGBA,
                (3,1): cv2.COLOR_RGB2GRAY,
                (3,4): cv2.COLOR_RGB2RGBA,
                (4,1): cv2.COLOR_RGBA2GRAY,
                (4,3): cv2.COLOR_RGBA2RGB
            }
            if (old_channels,new_channels) in convert_map:
                conversion = convert_map[(old_channels,new_channels)]
                self._image = cv2.cvtColor(self._image, conversion)
            elif old_channels == 1:
                if len(self._image.shape) == 2:
                    self._image = np.expand_dims(self._image, axis=2)
                self._image = self._image.repeat(new_channels, axis=2)
            elif new_channels > old_channels:
                self._image = np.append(self._image, np.zeros((self._image.shape[0], self._image.shape[1], new_channels-old_channels), dtype=self._image.dtype), axis=2)
            elif new_channels < old_channels:
                self._image = self._image[:, :, :new_channels]

        if self._image is not None:
            old_np_dtype = self._image.dtype
            new_np_dtype = GLInfo.dtype_map[get_dtype(self._internal_format)]
            if old_np_dtype != new_np_dtype:
                if "int" in str(old_np_dtype) and "float" in str(new_np_dtype):
                    self._image = (self._image / 255).astype(new_np_dtype)
                elif "float" in str(old_np_dtype) and "int" in str(new_np_dtype):
                    self._image = (self._image * 255).astype(new_np_dtype)
                else:
                    self._image = self._image.astype(new_np_dtype)

        self._image_changed = True

    @internal_format.setter
    @param_setter
    def internal_format(self, internal_format:GLInfo.internal_formats):
        self._set_internal_format(internal_format)

    @property
    def image(self):
        return self._image

    @image.setter
    @param_setter
    def image(self, image:(np.ndarray,str)):
        if isinstance(image, str):
            image = ImageLoader.load(image)

        self._image = image
        self._width = self._image.shape[1]
        self._height = self._image.shape[0]

        channels = self._image.shape[2] if len(self._image.shape) > 2 else 1
        self._internal_format = GLInfo.internal_formats_map[self._image.dtype][channels]
        self._image_changed = True
        
    @checktype
    def malloc(self, width:int, height:int, internal_format:GLInfo.internal_formats=None):
        self.width = width
        self.height = height

        if internal_format is None:
            internal_format = self.internal_format

        if internal_format is None:
            internal_format = GL.GL_RGBA32F

        self.internal_format = internal_format

    @checktype
    def resize(self, width:int, height:int):
        self.width = width
        self.height = height

    @property
    def is_completed(self):
        return (self._width > 0 and self._height > 0)
