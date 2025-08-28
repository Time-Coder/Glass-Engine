from .genMat2x2 import genMat2x2

import ctypes


class umat2x2(genMat2x2):

    @property
    def dtype(self)->type:
        return ctypes.c_uint
    
umat2 = umat2x2