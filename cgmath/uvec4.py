from .genVec4 import genVec4

import ctypes


class uvec4(genVec4):
    
    dtype:type = ctypes.c_uint32