from .genVec4 import genVec4

import ctypes


class bvec4(genVec4):
    
    dtype:type = ctypes.c_bool
    prefix:str = "b"