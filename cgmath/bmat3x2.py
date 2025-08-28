from .genMat3x2 import genMat3x2

import ctypes


class bmat3x2(genMat3x2):

    @property
    def dtype(self)->type:
        return ctypes.c_bool