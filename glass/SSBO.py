from OpenGL import GL

from .SSUBO import SSUBO
from .utils import subscript_set, subscript


class SSBO(SSUBO):

    _basic_info = {
        "gen_func": GL.glGenBuffers,
        "bind_func": GL.glBindBuffer,
        "del_func": GL.glDeleteBuffers,
        "target_type": GL.GL_SHADER_STORAGE_BUFFER,
        "binding_type": GL.GL_SHADER_STORAGE_BUFFER_BINDING,
        "need_number": True,
    }

    _binding_points_pool = None
    _current_context = 0

    def __init__(self):
        SSUBO.__init__(self)

    def read_back(self, start: int, nbytes: int) -> bytearray:
        if start < 0:
            raise ValueError(
                "Memory start position should be positive, " + str(start) + " is passed"
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

        if nbytes == 0:
            return bytearray()

        self.bind()
        ptr_data = GL.glMapBuffer(GL.GL_SHADER_STORAGE_BUFFER, GL.GL_READ_ONLY)
        data = (GL.GLubyte * nbytes).from_address(ptr_data)
        self._buffer[start : start + nbytes] = data[:]
        GL.glUnmapBuffer(GL.GL_SHADER_STORAGE_BUFFER)

        return self._buffer[start : start + nbytes]

    def download(self):
        len_array = None
        for atom_name, atom_info in self._atom_info_map.items():
            atom_type = atom_info["type"]
            get_func = SSUBO._get_atom_func(atom_type)
            atom_offset = atom_info["offset"]
            subscript_chain = atom_info["subscript_chain"]
            if "[{0}]" not in atom_name:
                value = get_func(self, atom_offset)
                subscript_set(self._bound_var, subscript_chain, value)
            else:
                if len_array is None:
                    # pos_array_end = atom_name.find("[{0}]")
                    # len_array = len(eval("self._bound_var." + atom_name[:pos_array_end]))

                    pos_array_end = subscript_chain.index(("getitem", "{0}"))
                    variable_length_array = subscript(
                        self._bound_var, subscript_chain[:pos_array_end]
                    )
                    len_array = len(variable_length_array)

                stride = atom_info["stride"]
                for i in range(len_array):
                    value = get_func(self, atom_offset + i * stride)
                    subscript_set(self._bound_var, subscript_chain, value, i)
