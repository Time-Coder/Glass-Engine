from .genVec4 import genVec4

import ctypes


class vec4(genVec4):
    
    dtype:type = ctypes.c_float