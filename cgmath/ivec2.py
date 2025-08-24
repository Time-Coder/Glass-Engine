from .genVec2 import genVec2

import ctypes


class ivec2(genVec2):
    
    dtype:type = ctypes.c_int32