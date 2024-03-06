from .BO import BO

import platform

if platform.machine() == "aarch64":
    from OpenGL import GLES2 as GL
else:
    from OpenGL import GL


class VBO(BO):

    _basic_info = {
        "gen_func": GL.glGenBuffers,
        "bind_func": GL.glBindBuffer,
        "del_func": GL.glDeleteBuffers,
        "target_type": GL.GL_ARRAY_BUFFER,
        "binding_type": GL.GL_ARRAY_BUFFER_BINDING,
        "need_number": True,
    }

    def __init__(self):
        BO.__init__(self)
        self._location = -1
