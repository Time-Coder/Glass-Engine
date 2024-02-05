from .BO import BO
from .utils import capacity_of

from OpenGL import GL
import numpy as np


class ACBO(BO):

    _basic_info = {
        "gen_func": GL.glGenBuffers,
        "bind_func": GL.glBindBuffer,
        "del_func": GL.glDeleteBuffers,
        "target_type": GL.GL_ATOMIC_COUNTER_BUFFER,
        "binding_type": GL.GL_ATOMIC_COUNTER_BUFFER_BINDING,
        "need_number": True,
    }

    _binding_points_pool = None

    _ACBO_map = {}

    def __init__(self) -> None:
        BO.__init__(self)

    @staticmethod
    def set(binding: int, offset: int, value: int) -> None:
        acbo = None
        if binding not in ACBO._ACBO_map:
            acbo = ACBO()
            acbo.malloc(4 * capacity_of(offset / 4), GL.GL_DYNAMIC_COPY)
            ACBO._ACBO_map[binding] = acbo
        else:
            acbo = ACBO._ACBO_map[binding]
            if offset + 4 > acbo.nbytes:
                temp_bo = ACBO()
                temp_bo.malloc(4 * capacity_of(offset / 4), GL.GL_DYNAMIC_COPY)
                acbo.copy_to(0, acbo.nbytes, temp_bo, 0)
                acbo.delete()
                acbo = temp_bo
                ACBO._ACBO_map[binding] = acbo

        acbo.bind_to_point(binding)
        acbo.bufferSubData(offset, 4, np.array([int(value)], dtype=np.uint32))

    @staticmethod
    def get(binding: int, offset: int) -> int:
        if binding not in ACBO._ACBO_map:
            return 0

        acbo = ACBO._ACBO_map[binding]
        acbo.bind()
        data = np.array([0], np.uint32)
        GL.glGetBufferSubData(GL.GL_ATOMIC_COUNTER_BUFFER, offset, 4, data)
        return int(data[0])

    def bind_to_point(self, binding_point: int) -> None:
        self.bind()
        GL.glBindBufferBase(GL.GL_ATOMIC_COUNTER_BUFFER, binding_point, self._id)
