from .genVec4 import genVec4

import ctypes


class dvec4(genVec4):
    
    dtype:type = ctypes.c_double