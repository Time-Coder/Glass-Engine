from .genVec3 import genVec3

import ctypes


class bvec3(genVec3):
    
    dtype:type = ctypes.c_bool
    prefix:str = "b"