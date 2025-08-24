from .genVec3 import genVec3

import ctypes


class vec3(genVec3):
    
    dtype:type = ctypes.c_float