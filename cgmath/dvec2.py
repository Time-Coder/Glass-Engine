from .genVec2 import genVec2

import ctypes


class dvec2(genVec2):
    
    @property
    def dtype(self)->type:
        return ctypes.c_double