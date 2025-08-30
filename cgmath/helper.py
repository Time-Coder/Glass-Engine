import itertools
from typing import List, Set, Dict, Any
from types import ModuleType
import importlib
import os
import ctypes
from decimal import Decimal


_module_map:Dict[str, ModuleType] = {}

def from_import(module_name:str, attr_name:str)->type:
    if module_name not in _module_map:
        module = None
        if module_name.startswith("."):
            module = importlib.import_module(module_name, package=__package__)
        else:
            module = importlib.import_module(module_name)
        _module_map[module_name] = module
    
    return getattr(_module_map[module_name], attr_name)

def is_number(value:Any)->bool:
    return isinstance(value, (
        float, bool, int, Decimal,
        ctypes.c_bool, ctypes.c_int8, ctypes.c_uint8,
        ctypes.c_int16, ctypes.c_uint16,
        ctypes.c_int32, ctypes.c_uint32,
        ctypes.c_int64, ctypes.c_uint64,
        ctypes.c_float, ctypes.c_double, ctypes.c_longdouble
    )) or value.__class__.__name__ in (
        'int8', 'int16', 'int32', 'int64',
        'uint8', 'uint16', 'uint32', 'uint64',
        'float16', 'float32', 'float64', 'float128',
        'bool'
    )

def generate_getter_swizzles(char_sets:List[str])->Set[str]:
    result:List[str] = []
    
    for char_set in char_sets:
        for length in range(1, 4 + 1):
            for combo in itertools.product(char_set, repeat=length):
                swizzle = ''.join(combo)
                result.append(swizzle)
    
    return result

def generate_setter_swizzles(char_sets:List[str])->Set[str]:
    result:List[str] = []
    
    for char_set in char_sets:
        for length in range(1, len(char_set) + 1):
            for combo in itertools.permutations(char_set, length):
                swizzle = ''.join(combo)
                result.append(swizzle)
    
    return result

def generate_swizzle_defines(type_name:str, dtype_name:str, char_sets:List[str])->str:
    result:str = ""
    vec_basename = type_name[:-1]
    getter_swizzles:Set[str] = generate_getter_swizzles(char_sets)
    setter_swizzles:Set[str] = generate_setter_swizzles(char_sets)
    for swizzle in getter_swizzles:
        return_type_name:str = dtype_name
        input_type_name:str = "Union[bool, int, float]"

        n_swizzle = len(swizzle)
        if n_swizzle > 1:
            return_type_name:str = vec_basename + str(n_swizzle)
            input_type_name:str = f"Union[bool, int, float, genVec{n_swizzle}]"

        result += f"""
    @property
    def {swizzle}(self)->{return_type_name}: ...
"""
        
        if swizzle in setter_swizzles:
            result += f"""
    @{swizzle}.setter
    def {swizzle}(self, value:{input_type_name})->None: ...
"""
            
    return result


if __name__ == "__main__":
    self_folder = os.path.dirname(os.path.abspath(__file__))
    vec_infos = [
        ('bvec2', 'bool', ['xy', 'rg', 'st']),
        ('bvec3', 'bool', ['xyz', 'rgb', 'stp']),
        ('bvec4', 'bool', ['xyzw', 'rgba', 'stpq']),
        ('ivec2', 'int', ['xy', 'rg', 'st']),
        ('ivec3', 'int', ['xyz', 'rgb', 'stp']),
        ('ivec4', 'int', ['xyzw', 'rgba', 'stpq']),
        ('uvec2', 'int', ['xy', 'rg', 'st']),
        ('uvec3', 'int', ['xyz', 'rgb', 'stp']),
        ('uvec4', 'int', ['xyzw', 'rgba', 'stpq']),
        ('vec2', 'float', ['xy', 'rg', 'st']),
        ('vec3', 'float', ['xyz', 'rgb', 'stp']),
        ('vec4', 'float', ['xyzw', 'rgba', 'stpq']),
        ('dvec2', 'float', ['xy', 'rg', 'st']),
        ('dvec3', 'float', ['xyz', 'rgb', 'stp']),
        ('dvec4', 'float', ['xyzw', 'rgba', 'stpq'])
    ]

    pyi_in_contents:Dict[str, str] = {}

    for vec_inf in vec_infos:
        basename:str = vec_inf[0][:-1]
        num:str = vec_inf[0][-1]
        in_file_name:str = f"{self_folder}/genVec{num}.pyi.in"
        if in_file_name not in pyi_in_contents:
            pyi_in_contents[in_file_name] = open(in_file_name).read()

        with open(f"{self_folder}/{vec_inf[0]}.pyi", "w") as out_file:
            swizzle_defines:str = generate_swizzle_defines(*vec_inf)
            pyi_in_content = pyi_in_contents[in_file_name].format(basename=basename)
            out_file.write(pyi_in_content + swizzle_defines)