from .genVec4 import genVec4

import ctypes


class ivec4(genVec4):
    
    dtype:type = ctypes.c_int32