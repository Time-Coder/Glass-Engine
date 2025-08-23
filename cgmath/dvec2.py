from .genVec2 import genVec2

import ctypes


class dvec2(genVec2):
    
    dtype:type = ctypes.c_double
    prefix:str = "d"