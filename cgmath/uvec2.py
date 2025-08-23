from .genVec2 import genVec2

import ctypes


class uvec2(genVec2):
    
    dtype:type = ctypes.c_uint32
    prefix:str = "u"