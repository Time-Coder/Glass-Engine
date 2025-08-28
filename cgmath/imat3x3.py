from .genMat3x3 import genMat3x3

import ctypes


class imat3x3(genMat3x3):

    @property
    def dtype(self)->type:
        return ctypes.c_int
    
imat3 = imat3x3