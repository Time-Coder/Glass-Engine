from .genMat3x4 import genMat3x4

import ctypes


class umat3x4(genMat3x4):

    @property
    def dtype(self)->type:
        return ctypes.c_uint