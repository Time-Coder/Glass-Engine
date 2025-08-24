from .genVec3 import genVec3

import ctypes


class dvec3(genVec3):
    
    dtype:type = ctypes.c_double