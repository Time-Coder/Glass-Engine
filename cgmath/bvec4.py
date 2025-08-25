from .genVec4 import genVec4

import ctypes


class bvec4(genVec4):
    
    @property
    def dtype(self)->type:
        return ctypes.c_bool