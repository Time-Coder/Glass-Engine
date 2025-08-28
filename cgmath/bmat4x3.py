from .genMat4x3 import genMat4x3

import ctypes


class bmat4x3(genMat4x3):

    @property
    def dtype(self)->type:
        return ctypes.c_bool