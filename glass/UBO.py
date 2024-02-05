from .SSUBO import SSUBO

from OpenGL import GL


class UBO(SSUBO):

    _basic_info = {
        "gen_func": GL.glGenBuffers,
        "bind_func": GL.glBindBuffer,
        "del_func": GL.glDeleteBuffers,
        "target_type": GL.GL_UNIFORM_BUFFER,
        "binding_type": GL.GL_UNIFORM_BUFFER_BINDING,
        "need_number": True,
    }

    _binding_points_pool = None
    _current_context = 0

    def __init__(self):
        SSUBO.__init__(self)
