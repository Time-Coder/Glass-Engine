from .genVec3 import genVec3

import ctypes


class uvec3(genVec3):
    
    dtype:type = ctypes.c_uint32