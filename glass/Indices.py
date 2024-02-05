import glm
from OpenGL import GL
import numpy as np

from .GLInfo import GLInfo
from .EBO import EBO
from .SameTypeList import SameTypeList
from .utils import checktype
from .helper import sizeof
from .Increment import Increment


class Indices(SameTypeList):
    @checktype
    def __init__(
        self,
        _list: (list, np.ndarray) = None,
        draw_type: GLInfo.draw_types = GL.GL_STATIC_DRAW,
        dtype=None,
    ):
        SameTypeList.__init__(self, _list, glm.uvec3)

        self.stride = sizeof(glm.uvec3)
        self._ebo = EBO()
        self._draw_type = draw_type

        self._temp_buffer = None
        self._temp_buffer_changed = False
        self._temp_ebo = EBO()

    def _check_type(self, triangle):
        if not isinstance(triangle, glm.uvec3):
            raise TypeError("indices should be in type uvec3")

    @property
    def ebo(self):
        if self._temp_buffer is None:
            return self._ebo
        else:
            return self._temp_ebo

    @property
    def draw_type(self):
        return self._draw_type

    @draw_type.setter
    def draw_type(self, value):
        self._draw_type = value

    @property
    def temp_buffer(self):
        return self._temp_buffer

    @temp_buffer.setter
    def temp_buffer(self, temp_buffer: bytes):
        if self._temp_buffer == temp_buffer:
            return

        self._temp_buffer = temp_buffer
        self._temp_buffer_changed = True

    def _temp_apply(self):
        self._temp_ebo.bufferData(self._temp_buffer)
        self._temp_buffer_changed = False

    def _first_apply(self):
        if self._increment is not None or not self:
            return False

        self._increment = Increment(self)

        if self._ebo.nbytes == 0:
            self._ebo.bufferData(self.buffer, draw_type=self._draw_type)

        return True

    def _apply_increment(self):
        if not self._increment.is_changed:
            return

        patch = self._increment.patch()

        if patch["old_capacity"] == patch["new_capacity"]:
            for move in patch["move"]:
                self._ebo.memmove(
                    move["old_start"] * self.stride,
                    move["size"] * self.stride,
                    move["new_start"] * self.stride,
                )
        else:
            temp_ebo = EBO()
            temp_ebo.malloc(patch["new_capacity"] * self.stride, self._draw_type)
            self._ebo.copy_to(
                0, min(patch["old_size"], patch["new_size"]) * self.stride, temp_ebo, 0
            )
            for move in patch["move"]:
                self._ebo.copy_to(
                    move["old_start"] * self.stride,
                    move["size"] * self.stride,
                    temp_ebo,
                    move["new_start"] * self.stride,
                )

            self._ebo.delete()
            self._ebo = temp_ebo

        new_data = patch["new_data"]
        patch_update = patch["update"]
        len_patch_update = len(patch_update)

        if new_data and patch_update:
            temp_buffer = np.array(new_data).tobytes()
            if len_patch_update > 1:
                temp_ebo = EBO()
                temp_ebo.bufferData(temp_buffer, self._draw_type)

                for update in patch_update:
                    dest_start = update["dest_start"]
                    size = update["size"]
                    src_start = update["src_start"]
                    temp_ebo.copy_to(
                        src_start * self.stride,
                        size * self.stride,
                        self._ebo,
                        dest_start * self.stride,
                    )
            else:
                update = patch_update[0]
                dest_start = update["dest_start"]
                size = update["size"]
                self._ebo.bufferSubData(
                    dest_start * self.stride, size * self.stride, temp_buffer
                )

    def _apply(self):
        if self._temp_buffer is not None:
            if self._temp_buffer_changed:
                self._temp_apply()
            return
        else:
            if self._temp_buffer_changed:
                self._temp_ebo.delete()

        self._check_in_items()

        success = False
        if self._increment is None:
            success = self._first_apply()
        else:
            self._apply_increment()
            success = True

        if success:
            self._ebo.bind()

    @property
    def buffer(self):
        return bytearray(self.ndarray.tobytes()) + bytearray(
            (self.capacity - len(self)) * self.stride
        )
