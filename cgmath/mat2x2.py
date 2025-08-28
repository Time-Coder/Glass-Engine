from .genMat2x2 import genMat2x2

import ctypes


class mat2x2(genMat2x2):

    @property
    def dtype(self)->type:
        return ctypes.c_float
    
mat2 = mat2x2