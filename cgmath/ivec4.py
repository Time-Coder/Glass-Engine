from .genVec4 import genVec4

import ctypes


class ivec4(genVec4):
    
    @property
    def dtype(self)->type:
        return ctypes.c_int