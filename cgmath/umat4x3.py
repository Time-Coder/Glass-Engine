from .genMat4x3 import genMat4x3

import ctypes


class umat4x3(genMat4x3):

    @property
    def dtype(self)->type:
        return ctypes.c_uint