from .genMat3x3 import genMat3x3

import ctypes


class bmat3x3(genMat3x3):

    @property
    def dtype(self)->type:
        return ctypes.c_bool
    
bmat3 = bmat3x3