from .SameTypeList import SameTypeList
from .GLInfo import GLInfo
from .helper import sizeof
from .VBO import VBO
from .Increment import Increment

from OpenGL import GL
import numpy as np
import glm

class AttrList(SameTypeList):

    def __init__(self, _list:(list,np.ndarray)=None, draw_type:GLInfo.draw_types=GL.GL_STATIC_DRAW, dtype:GLInfo.attr_types=None):
        SameTypeList.__init__(self, _list, dtype)

        self._draw_type = draw_type
        self._vbo = VBO()

        self.stride = 0
        self.is_new_vbo = False
    
    @property
    def draw_type(self)->GLInfo.draw_types:
        return self._draw_type
    
    @draw_type.setter
    def draw_type(self, draw_type:GLInfo.draw_types):
        self._draw_type = draw_type

    @property
    def dtype(self)->GLInfo.attr_types:
        if self._dtype is not None:
            return self._dtype
        
        if self:
            return type(self._list[0])

        return None
    
    @dtype.setter
    def dtype(self, dtype:GLInfo.attr_types):
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
        self._list_dirty = True
        self._should_retest = True
        self.stride = sizeof(dtype)

    def _apply(self)->None:
        self._check_in_items()
        if self._increment is None:
            self.__first_apply()
        elif self._increment.is_changed:
            self.__apply_increment()

    def __first_apply(self)->None:
        if not self:
            return

        assert self._increment is None
        self._increment = Increment(self)

        assert self._vbo.nbytes == 0 and self._vbo.id == 0
        self.stride = sizeof(self.const_get(0))
        self._vbo.malloc(self.capacity*self.stride, self._draw_type)

        value_array = self.ndarray
        self._vbo.bufferSubData(0, value_array.nbytes, value_array)

        self.is_new_vbo = True

    def __apply_increment(self)->None:
        self.is_new_vbo = False

        assert self._increment.is_changed
        patch = self._increment.patch()
        if patch["old_capacity"] == patch["new_capacity"]:
            for move in patch["move"]:
                self._vbo.memmove(move["old_start"]*self.stride, move["size"]*self.stride, move["new_start"]*self.stride)
        else:
            temp_vbo = VBO()
            temp_vbo.malloc(patch["new_capacity"]*self.stride, self._draw_type)
            self._vbo.copy_to(0, min(patch["old_size"], patch["new_size"])*self.stride, temp_vbo, 0)
            for move in patch["move"]:
                self._vbo.copy_to(move["old_start"]*self.stride, move["size"]*self.stride, temp_vbo, move["new_start"]*self.stride)

            self._vbo.delete()
            self._vbo = temp_vbo
            self.is_new_vbo = True

        new_data = patch["new_data"]
        patch_update = patch["update"]

        if new_data and patch_update:
            temp_buffer = np.array(new_data)
            if len(patch_update) > 1:
                temp_vbo = VBO()
                temp_vbo.bufferData(temp_buffer, self._draw_type)
                for update in patch_update:
                    dest_start = update["dest_start"]
                    size = update["size"]
                    src_start = update["src_start"]
                    temp_vbo.copy_to(src_start*self.stride, size*self.stride, self._vbo, dest_start*self.stride)
            else:
                update = patch_update[0]
                dest_start = update["dest_start"]
                size = update["size"]
                self._vbo.bufferSubData(dest_start*self.stride, size*self.stride, temp_buffer)