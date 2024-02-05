from OpenGL import GL
import numpy as np

from .GLInfo import GLInfo
from .GLObject import GLObject
from .GlassConfig import GlassConfig


class BO(GLObject):

    def __init__(self, context_shared=True) -> None:
        GLObject.__init__(self, context_shared=context_shared)
        self._nbytes: int = 0
        self._draw_type: GLInfo.draw_types = GL.GL_STATIC_DRAW

    def delete(self) -> None:
        GLObject.delete(self)
        self._nbytes = 0

    def bufferData(
        self, value_array, draw_type: GLInfo.draw_types = GL.GL_STATIC_DRAW
    ) -> None:
        if GlassConfig.debug and self.__class__.__name__ in ["FBO", "RBO"]:
            raise AttributeError(
                "'" + self.__class__.__name__ + "' object has no attribute 'bufferData'"
            )

        array_bytes = 0
        if isinstance(value_array, np.ndarray):
            array_bytes = value_array.nbytes
        elif isinstance(value_array, bytes):
            array_bytes = len(value_array)
        elif isinstance(value_array, bytearray):
            array_bytes = len(value_array)
            value_array = bytes(value_array)
        else:
            value_array = np.array(value_array)
            array_bytes = value_array.nbytes

        self.bind()
        GL.glBufferData(
            self.__class__._basic_info["target_type"],
            array_bytes,
            value_array,
            draw_type,
        )
        self._nbytes = array_bytes
        self._draw_type = draw_type

    def malloc(
        self, nbytes: int, draw_type: GLInfo.draw_types = GL.GL_STATIC_DRAW
    ) -> None:
        if GlassConfig.debug:
            if self.__class__.__name__ in ["FBO", "RBO"]:
                raise AttributeError(
                    "'" + self.__class__.__name__ + "' object has no attribute 'malloc'"
                )

        self.bind()
        GL.glBufferData(
            self.__class__._basic_info["target_type"], nbytes, None, draw_type
        )
        self._nbytes = nbytes
        self._draw_type = draw_type

    def memmove(self, old_start: int, nbytes: int, new_start: int) -> None:
        if GlassConfig.debug:
            if old_start < 0:
                raise ValueError(
                    "source start position should be positive, "
                    + str(old_start)
                    + " is passed"
                )
            elif old_start >= self.nbytes:
                raise ValueError(
                    "source start position is out of range, max position is "
                    + str(self._nbytes - 1),
                    ", " + str(old_start) + " is passed",
                )

            if new_start < 0:
                raise ValueError(
                    "dest start position should be positive, "
                    + str(new_start)
                    + " is passed"
                )
            elif new_start >= self.nbytes:
                raise ValueError(
                    "dest start position is out of range, max position is "
                    + str(self._nbytes - 1),
                    ", " + str(new_start) + " is passed",
                )

            if nbytes < 0:
                raise ValueError(
                    "'nbytes' should be positive, " + str(nbytes) + " is passed"
                )

            if old_start + nbytes > self._nbytes:
                raise ValueError(
                    "source buffer end position is out of range, max position is "
                    + str(self._nbytes)
                    + ", "
                    + str(old_start + nbytes)
                    + " is applied."
                )

        if self._nbytes == 0 or nbytes == 0 or old_start == new_start:
            return

        temp_bo_id = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_COPY_WRITE_BUFFER, temp_bo_id)
        GL.glBufferData(GL.GL_COPY_WRITE_BUFFER, nbytes, None, self.draw_type)

        GL.glBindBuffer(GL.GL_COPY_READ_BUFFER, self._id)
        GL.glCopyBufferSubData(
            GL.GL_COPY_READ_BUFFER, GL.GL_COPY_WRITE_BUFFER, old_start, 0, nbytes
        )

        GL.glBindBuffer(GL.GL_COPY_WRITE_BUFFER, 0)
        GL.glBindBuffer(GL.GL_COPY_READ_BUFFER, 0)

        self.bufferSubData(old_start, nbytes, bytes(nbytes))
        real_delta = 0
        if old_start - new_start > 0:
            real_delta = old_start - new_start
            self.copy_to(new_start, real_delta, self, new_start + nbytes)
        else:
            real_delta = min(new_start + nbytes, self._nbytes) - (old_start + nbytes)
            self.copy_to(old_start + nbytes, real_delta, self, old_start)

        GL.glBindBuffer(GL.GL_COPY_WRITE_BUFFER, self._id)
        GL.glBindBuffer(GL.GL_COPY_READ_BUFFER, temp_bo_id)
        GL.glCopyBufferSubData(
            GL.GL_COPY_READ_BUFFER, GL.GL_COPY_WRITE_BUFFER, 0, new_start, nbytes
        )
        GL.glBindBuffer(GL.GL_COPY_WRITE_BUFFER, 0)
        GL.glBindBuffer(GL.GL_COPY_READ_BUFFER, 0)
        GL.glDeleteBuffers(1, np.array([temp_bo_id]))
        temp_bo_id = 0

    def bufferSubData(self, start: int, nbytes: int, value_array) -> None:
        if GlassConfig.debug:
            if self.__class__.__name__ in ["FBO", "RBO"]:
                raise AttributeError(
                    "'"
                    + self.__class__.__name__
                    + "' object has no attribute 'bufferSubData'"
                )

        array_nbytes = 0
        if isinstance(value_array, np.ndarray):
            array_nbytes = value_array.nbytes
            value_array = value_array.tobytes()
        elif isinstance(value_array, bytes):
            array_nbytes = len(value_array)
        elif isinstance(value_array, bytearray):
            array_nbytes = len(value_array)
            value_array = bytes(value_array)
        else:
            value_array = np.array(value_array)
            array_nbytes = value_array.nbytes
            value_array = value_array.tobytes()

        if GlassConfig.debug:
            if start < 0:
                raise ValueError(
                    "Memory start position should be positive, "
                    + str(start)
                    + " is passed"
                )

            if nbytes < 0:
                raise ValueError(
                    "'nbytes' should be positive, " + str(nbytes) + " is passed"
                )

            if start >= self._nbytes:
                raise ValueError(
                    "Memory start position is out of range, max position is "
                    + str(self._nbytes - 1)
                    + ", "
                    + str(start)
                    + " is passed."
                )

            if start + nbytes > self._nbytes:
                raise ValueError(
                    "Memory end position is out of range, max position is "
                    + str(self._nbytes)
                    + ", "
                    + str(start + nbytes)
                    + " is applied."
                )

            if nbytes > array_nbytes:
                raise ValueError(
                    "Need copy data is over value_array's size. Max data size is "
                    + str(value_array.nbytes)
                    + " bytes, "
                    + str(nbytes)
                    + " bytes is needed."
                )

        if nbytes == 0:
            return

        self.bind()
        GL.glBufferSubData(
            self.__class__._basic_info["target_type"], start, nbytes, value_array
        )

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
