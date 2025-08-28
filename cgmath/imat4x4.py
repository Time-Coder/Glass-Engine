from .genMat4x4 import genMat4x4

import ctypes


class imat4x4(genMat4x4):

    @property
    def dtype(self)->type:
        return ctypes.c_int
    
imat4 = imat4x4