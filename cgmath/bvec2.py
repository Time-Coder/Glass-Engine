from .genVec2 import genVec2

import ctypes


class bvec2(genVec2):
    
    dtype:type = ctypes.c_bool