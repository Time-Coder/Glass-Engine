from .genMat3x3 import genMat3x3

import ctypes


class mat3x3(genMat3x3):

    @property
    def dtype(self)->type:
        return ctypes.c_float
    
mat3 = mat3x3