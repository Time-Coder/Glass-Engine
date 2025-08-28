from .genMat2x3 import genMat2x3

import ctypes


class bmat2x3(genMat2x3):

    @property
    def dtype(self)->type:
        return ctypes.c_bool