from .genVec3 import genVec3

import ctypes


class ivec3(genVec3):
    
    dtype:type = ctypes.c_int32