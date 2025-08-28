from .genMat4x4 import genMat4x4

import ctypes


class mat4x4(genMat4x4):

    @property
    def dtype(self)->type:
        return ctypes.c_float
    
mat4 = mat4x4