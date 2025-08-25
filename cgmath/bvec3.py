from .genVec3 import genVec3

import ctypes


class bvec3(genVec3):
    
    @property
    def dtype(self)->type:
        return ctypes.c_bool