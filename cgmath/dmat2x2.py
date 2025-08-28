from .genMat2x2 import genMat2x2

import ctypes


class dmat2x2(genMat2x2):

    @property
    def dtype(self)->type:
        return ctypes.c_double
    
dmat2 = dmat2x2