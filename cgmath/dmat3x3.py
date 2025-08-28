from .genMat3x3 import genMat3x3

import ctypes


class dmat3x3(genMat3x3):

    @property
    def dtype(self)->type:
        return ctypes.c_double
    
dmat3 = dmat3x3