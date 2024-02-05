from .GLInfo import GLInfo
from .GLObject import GLObject
from .TextureUnits import TextureUnits
from .GLConfig import GLConfig
from .utils import checktype

import random
from functools import wraps


class FBOAttachment(GLObject):

    def __init__(self):
        GLObject.__init__(self)

        self._fbo = None
        self._fbo_attach_point = None
        self._fbo_image_changed = False
        self._fbo_image_generated_mipmap = True
        self._can_resize = True
        self._dynamic = True

    @property
    def dynamic(self):
        return self._dynamic

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
                raise RuntimeError(
                    f"none dynamic {self.__class__.__name__} cannot change any parameters"
                )

            safe_func = checktype(func)
            return_value = safe_func(*args, **kwargs)

            return return_value

        return wrapper

    def malloc(
        self,
        width: int,
        height: int,
        samples: int = None,
        layers: int = None,
        internal_format: GLInfo.internal_formats = None,
    ):
        pass

    def resize(self, width: int, height: int, samples: int = None, layers: int = None):
        if not self._can_resize:
            return

        self._can_resize = False

        self.malloc(width, height, samples, layers, internal_format=None)
        if self._fbo is not None:
            self._fbo.resize(width, height, samples, layers)

        self._can_resize = True

    def clear_buffer(self):
        self.bind(force_update_image=True)

    @property
    def fbo(self):
        return self._fbo

    def bind(self, update_fbo: bool = False, force_update_image: bool = False):
        cls_name = self.__class__.__name__
        target_type = self.__class__._basic_info["target_type"]
        if "sampler" in cls_name:
            texture_unit = None
            if self._id == 0:
                texture_unit = TextureUnits.available_unit
            else:
                texture_unit = TextureUnits.unit_of_texture((target_type, self._id))
                if texture_unit is None:
                    texture_unit = TextureUnits.available_unit

            if texture_unit is None:
                texture_unit = random.randint(0, GLConfig.max_texture_units - 1)

            GLConfig.active_texture_unit = texture_unit

        GLObject.bind(self)
        if update_fbo:
            self._fbo_image_changed = True
            self._fbo_image_generated_mipmap = False

        if "sampler" in cls_name:
            TextureUnits[texture_unit] = (target_type, self._id)

    def unbind(self):
        success = GLObject.unbind(self)
        cls_name = self.__class__.__name__
        if success and "sampler" in cls_name:
            target_type = self.__class__._basic_info["target_type"]
            assert TextureUnits.current_texture == (target_type, self._id)
            TextureUnits.current_texture = (target_type, 0)

        return success

    def __del__(self):
        self.unbind()
        GLObject.__del__(self)
