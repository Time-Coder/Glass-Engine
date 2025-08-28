from .genMat3x3 import genMat3x3

import ctypes


class umat3x3(genMat3x3):

    @property
    def dtype(self)->type:
        return ctypes.c_uint
    
umat3 = umat3x3