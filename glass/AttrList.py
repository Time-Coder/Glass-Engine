from .SameTypeList import SameTypeList
from .GLInfo import GLInfo
from .helper import sizeof
from .VBO import VBO

from OpenGL import GL
import numpy as np
import glm
from typing import Union, Any


class AttrList:

    def __init__(
        self,
        _list: Union[list[Any], np.ndarray] = None,
        draw_type: GLInfo.draw_types = GL.GL_STATIC_DRAW,
        dtype: GLInfo.attr_types = None,
    ):
        SameTypeList.__init__(self, _list, dtype)
        self._vbo = VBO(draw_type=draw_type)
        if _list:
            if self._dtype is None:
                ndarray = np.array(_list)
            else:
                np_dtype = self._dtype
                if np_dtype in GLInfo.np_dtype_map:
                    np_dtype = GLInfo.np_dtype_map[np_dtype]
                ndarray = np.array(_list, dtype=np_dtype)
            self._vbo.assign(ndarray)

        self.stride = sizeof(dtype)
        self.is_new_vbo = False

    @property
    def dtype(self) -> GLInfo.attr_types:
        if self._dtype is not None:
            return self._dtype

        if self:
            return type(self._list[0])

        return None

    @dtype.setter
    def dtype(self, dtype: GLInfo.attr_types):
        str_dtype = str(dtype)
        if str_dtype == "callback_vec3":
            dtype = glm.vec3
        elif str_dtype == "callback_vec4":
            dtype = glm.vec4
        elif str_dtype == "callback_quat":
            dtype = glm.quat

        if self._dtype == dtype:
            return

        self._dtype = dtype
        self.stride = sizeof(dtype)
