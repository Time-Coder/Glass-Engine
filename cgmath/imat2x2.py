from .genMat2x2 import genMat2x2

import ctypes


class imat2x2(genMat2x2):

    @property
    def dtype(self)->type:
        return ctypes.c_int
    
imat2 = imat2x2