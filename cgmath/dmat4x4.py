from .genMat4x4 import genMat4x4

import ctypes


class dmat4x4(genMat4x4):

    @property
    def dtype(self)->type:
        return ctypes.c_double
    
dmat4 = dmat4x4