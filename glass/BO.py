from OpenGL import GL
import numpy as np

from .GLInfo import GLInfo
from .GLObject import GLObject
from .GlassConfig import GlassConfig
from .Increment import Increment

from typing import Union

class BO(GLObject, Increment):

    def __init__(self, byte_array:Union[bytes,bytearray]=b'', context_shared:bool=True, redundant:bool=False) -> None:
        GLObject.__init__(self, context_shared=context_shared)
        Increment.__init__(self, byte_array)
        self._nbytes: int = 0
        self._draw_type: GLInfo.draw_types = GL.GL_STATIC_DRAW
        self._redundant = redundant

    def bind(self):
        GLObject.bind(self)
        self.__apply_increment()

    def __apply_move(self, move):
        new_start = move["new_start"]
        old_start = move["old_start"]
        nbytes = move["size"]

        temp_bo_id = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_COPY_WRITE_BUFFER, temp_bo_id)
        GL.glBufferData(GL.GL_COPY_WRITE_BUFFER, nbytes, None, self.draw_type)

        target_type = self.__class__._basic_info["target_type"]
        GL.glCopyBufferSubData(
            target_type, GL.GL_COPY_WRITE_BUFFER, old_start, 0, nbytes
        )
        GL.glCopyBufferSubData(
            GL.GL_COPY_WRITE_BUFFER, target_type, new_start, 0, nbytes
        )

        GL.glDeleteBuffers(1, [temp_bo_id])
        move["is_moved"] = True
        move["current_start"] = new_start

    def __apply_increment(self):
        if not self.is_changed:
            return
        
        patch = self.patch()
        if self._redundant:
            old_capacity = patch["old_capacity"]
            new_capacity = patch["new_capacity"]
        else:
            old_capacity = patch["old_size"]
            new_capacity = patch["new_size"]

        target_type = self.__class__._basic_info["target_type"]

        if old_capacity != new_capacity:
            GL.glBufferData(target_type, len(self), self, self.draw_type)
            return

        len_move = len(patch["move"])
        has_moved = True
        while has_moved:
            has_moved = False
            for i, move in enumerate(patch["move"]):
                if move["is_moved"]:
                    continue

                new_start = move["new_start"]
                old_start = move["old_start"]
                nbytes = move["size"]
                if new_start > old_start:
                    if i + 1 < len_move:
                        if new_start + nbytes <= patch["move"][i + 1]["current_start"]:
                            self.__apply_move(move)
                            has_moved = True
                    else:
                        self.__apply_move(move)
                        has_moved = True
                else:
                    if i - 1 >= 0:
                        if new_start >= patch["move"][i - 1]["current_start"] + patch["move"][i - 1]["size"]:
                            self.__apply_move(move)
                            has_moved = True
                    else:
                        self.__apply_move(move)
                        has_moved = True

        if patch["old_size"] > patch["new_size"]:
            del self[patch["new_size"]:]

        new_data = patch["new_data"]
        patch_update = patch["update"]

        if new_data and patch_update:
            if len(patch_update) > 1:
                temp_bo_id = GL.glGenBuffers(1)
                GL.glBindBuffer(GL.GL_COPY_READ_BUFFER, temp_bo_id)
                GL.glBufferData(GL.GL_COPY_READ_BUFFER, nbytes, new_data, self.draw_type)
                for update in patch_update:
                    dest_start = update["dest_start"]
                    size = update["size"]
                    src_start = update["src_start"]
                    GL.glCopyBufferSubData(GL.GL_COPY_READ_BUFFER, target_type, src_start, dest_start, size)

                GL.glDeleteBuffers(1, [temp_bo_id])
            else:
                update = patch_update[0]
                dest_start = update["dest_start"]
                size = update["size"]
                GL.glBufferSubData(target_type, dest_start, size, new_data)

        self._nbytes = len(self)
        
    def delete(self) -> None:
        GLObject.delete(self)
        self._nbytes = 0

    def copy_to(self, src_start: int, nbytes: int, dest_bo, dest_start: int) -> None:
        if GlassConfig.debug:
            if self.__class__.__name__ in ["FBO", "RBO"]:
                raise AttributeError(
                    "'"
                    + self.__class__.__name__
                    + "' object has no attribute 'copy_to'"
                )

            if src_start < 0:
                raise ValueError(
                    "source start position should be positive, "
                    + str(src_start)
                    + " is passed"
                )
            elif src_start >= self.nbytes:
                raise ValueError(
                    "source start position is out of range, max position is "
                    + str(self._nbytes - 1)
                    + ", "
                    + str(src_start)
                    + " is passed"
                )

            if dest_start < 0:
                raise ValueError(
                    "dest start position should be positive, "
                    + str(dest_start)
                    + " is passed"
                )
            elif dest_start >= dest_bo.nbytes:
                raise ValueError(
                    "dest start position is out of range, max position is "
                    + str(dest_bo._nbytes - 1)
                    + ", "
                    + str(dest_start)
                    + " is passed"
                )

            if nbytes < 0:
                raise ValueError(
                    "'nbytes' should be positive, " + str(nbytes) + " is passed"
                )

            if src_start + nbytes > self._nbytes:
                raise ValueError(
                    "source buffer end position is out of range, max position is "
                    + str(self._nbytes)
                    + ", "
                    + str(src_start + nbytes)
                    + " is applied."
                )

        if self._nbytes == 0 or nbytes == 0:
            return

        real_nbytes = min(nbytes, dest_bo._nbytes - dest_start)
        if self._id != dest_bo._id:
            GL.glBindBuffer(GL.GL_COPY_READ_BUFFER, self._id)
            GL.glBindBuffer(GL.GL_COPY_WRITE_BUFFER, dest_bo._id)
            GL.glCopyBufferSubData(
                GL.GL_COPY_READ_BUFFER,
                GL.GL_COPY_WRITE_BUFFER,
                src_start,
                dest_start,
                real_nbytes,
            )
            GL.glBindBuffer(GL.GL_COPY_READ_BUFFER, 0)
            GL.glBindBuffer(GL.GL_COPY_WRITE_BUFFER, 0)
        else:
            temp_bo_id = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_COPY_WRITE_BUFFER, temp_bo_id)
            GL.glBufferData(GL.GL_COPY_WRITE_BUFFER, real_nbytes, None, self.draw_type)

            GL.glBindBuffer(GL.GL_COPY_READ_BUFFER, self._id)
            GL.glCopyBufferSubData(
                GL.GL_COPY_READ_BUFFER,
                GL.GL_COPY_WRITE_BUFFER,
                src_start,
                0,
                real_nbytes,
            )

            GL.glBindBuffer(GL.GL_COPY_READ_BUFFER, temp_bo_id)
            GL.glBindBuffer(GL.GL_COPY_WRITE_BUFFER, self._id)
            GL.glCopyBufferSubData(
                GL.GL_COPY_READ_BUFFER,
                GL.GL_COPY_WRITE_BUFFER,
                0,
                dest_start,
                real_nbytes,
            )

            GL.glBindBuffer(GL.GL_COPY_READ_BUFFER, 0)
            GL.glBindBuffer(GL.GL_COPY_WRITE_BUFFER, 0)

            GL.glDeleteBuffers(1, np.array([temp_bo_id]))
            temp_bo_id = 0

    def shallow_copy_to(self, dest_bo) -> None:
        self_members = dir(self)
        dest_members = dir(dest_bo)
        for key in self_members:
            if (
                key in dest_members
                and not (key.startswith("__") and key.endswith("__"))
                and not callable(getattr(self, key))
            ):
                setattr(dest_bo, key, getattr(self, key))

    @property
    def nbytes(self) -> int:
        if GlassConfig.debug:
            if self.__class__.__name__ in ["FBO", "RBO"]:
                raise AttributeError(
                    "'" + self.__class__.__name__ + "' object has no attribute 'nbytes'"
                )

        return self._nbytes

    @property
    def empty(self) -> bool:
        return self._nbytes == 0

    @property
    def draw_type(self) -> GLInfo.draw_types:
        if GlassConfig.debug:
            if self.__class__.__name__ in ["FBO", "RBO"]:
                raise AttributeError(
                    "'"
                    + self.__class__.__name__
                    + "' object has no attribute 'draw_type'"
                )

        return self._draw_type
