from .genMat4x2 import genMat4x2

import ctypes


class bmat4x2(genMat4x2):

    @property
    def dtype(self)->type:
        return ctypes.c_bool