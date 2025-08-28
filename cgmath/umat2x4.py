from .genMat2x4 import genMat2x4

import ctypes


class umat2x4(genMat2x4):

    @property
    def dtype(self)->type:
        return ctypes.c_uint