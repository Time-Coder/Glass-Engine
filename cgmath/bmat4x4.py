from .genMat4x4 import genMat4x4

import ctypes


class bmat4x4(genMat4x4):

    @property
    def dtype(self)->type:
        return ctypes.c_bool
    
bmat4 = bmat4x4