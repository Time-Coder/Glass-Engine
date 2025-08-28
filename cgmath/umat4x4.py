from .genMat4x4 import genMat4x4

import ctypes


class umat4x4(genMat4x4):

    @property
    def dtype(self)->type:
        return ctypes.c_uint
    
umat4 = umat4x4