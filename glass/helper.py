from OpenGL import GL, constant
import numpy as np
import glm
import struct

from .GLInfo import GLInfo


def glGetInt(gl_constant: constant.IntConstant) -> int:
    value = GL.glGetIntegerv(gl_constant)
    try:
        value = value[0]
    except:
        pass

    value = int(value)
    return value


def glGetEnum(gl_constant: constant.IntConstant):
    value = glGetInt(gl_constant)
    if value in GLInfo.enum_map:
        return GLInfo.enum_map[value]
    else:
        return value


def glGetEnumi(gl_constant: constant.IntConstant, index: int):
    value = int(GL.glGetIntegeri_v(gl_constant, index))
    if value in GLInfo.enum_map:
        return GLInfo.enum_map[value]
    else:
        return value


def width_adapt(width):
    if width % 4 != 0:
        if width % 2 == 0:
            GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 2)
        else:
            GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)


def sizeof(type_var):
    if not isinstance(type_var, type):
        type_var = type(type_var)

    if "sampler" in str(type_var):
        return 8

    size = 0

    try:
        size = glm.sizeof(type_var)
    except:
        pass

    if size != 0:
        return size

    if type_var == bool:
        return 1
    elif type_var in [int, float]:
        return 4

    return np.dtype(type_var).itemsize


def nitems(element_type):
    str_element_type = str(element_type)
    if "vec2" in str_element_type:
        return 2
    elif "vec3" in str_element_type:
        return 3
    elif "vec4" in str_element_type or "mat2x2" in str_element_type:
        return 4
    elif "mat2x3" in str_element_type or "mat3x2" in str_element_type:
        return 6
    elif "mat3x3" in str_element_type:
        return 9
    elif "mat2x4" in str_element_type or "mat4x2" in str_element_type:
        return 8
    elif "mat3x4" in str_element_type or "mat4x3" in str_element_type:
        return 12
    elif "mat4x4" in str_element_type:
        return 16
    else:
        return 1


def to_bytes(value):
    if isinstance(value, bool):
        return int(value).to_bytes(4, byteorder="little")
    elif isinstance(value, int):
        return value.to_bytes(4, byteorder="little")
    elif isinstance(value, float):
        return struct.pack("<f", value)
    else:
        return value.to_bytes()


def type_from_str(type_str):
    if type_str in GLInfo.atom_type_map:
        return GLInfo.atom_type_map[type_str][0]

    if type_str == "sampler2D":
        from .sampler2D import sampler2D

        return sampler2D
    elif type_str == "isampler2D":
        from .isampler2D import isampler2D

        return isampler2D
    elif type_str == "usampler2D":
        from .usampler2D import usampler2D

        return usampler2D
    elif type_str == "samplerCube":
        from .samplerCube import samplerCube

        return samplerCube
    elif type_str == "sampler2DMS":
        from .sampler2DMS import sampler2DMS

        return sampler2DMS
    elif type_str == "isampler2DMS":
        from .isampler2DMS import isampler2DMS

        return isampler2DMS
    elif type_str == "usampler2DMS":
        from .usampler2DMS import usampler2DMS

        return usampler2DMS
    else:
        raise TypeError(f"not support type {type_str}")


def get_external_format(internal_format):
    return GLInfo.format_info_map[internal_format][0]


def get_channels(internal_format):
    external_format = get_external_format(internal_format)
    if external_format == GL.GL_RED:
        return 1
    elif external_format == GL.GL_RG:
        return 2
    elif external_format == GL.GL_RGB:
        return 3
    elif external_format == GL.GL_RGBA:
        return 4
    elif external_format == GL.GL_STENCIL_INDEX:
        return 1
    elif external_format == GL.GL_DEPTH_COMPONENT:
        return 1
    elif external_format == GL.GL_DEPTH_STENCIL:
        return 2
    else:
        raise ValueError(f"not support format {external_format}")


def get_dtype(internal_format):
    return GLInfo.format_info_map[internal_format][1]


def type_distance(type1: str, type2: str):
    if type1 == type2:
        return 0

    if type1 == "" or type2 == "":
        return "unknown"

    def type_index(type_, types):
        for i, target_type in enumerate(types):
            if isinstance(target_type, tuple):
                if type_ in target_type:
                    return i
            else:
                if type_ == target_type:
                    return i
        return -1

    all_types = [
        GLInfo.basic_types,
        GLInfo.gvec2_types,
        GLInfo.gvec3_types,
        GLInfo.gvec4_types,
        GLInfo.gmat2x2_types,
        GLInfo.gmat3x2_types,
        GLInfo.gmat3x3_types,
        GLInfo.gmat3x4_types,
        GLInfo.gmat4x2_types,
        GLInfo.gmat4x3_types,
        GLInfo.gmat4x4_types,
    ]

    for target_types in all_types:
        type1_index = type_index(type1, target_types)
        type2_index = type_index(type2, target_types)
        if type1_index != -1 and type2_index != -1:
            return abs(type1_index - type2_index)

    return "inf"


def type_list_distance(type_list1, type_list2):
    for type1, type2 in zip(type_list1, type_list2):
        current_distance = type_distance(type1, type2)
        if current_distance == "inf":
            return "inf"

    full_distance = 0
    for type1, type2 in zip(type_list1, type_list2):
        current_distance = type_distance(type1, type2)
        if current_distance == "unknown":
            return "unknown"
        full_distance += current_distance

    return full_distance


def greater_type(type1: str, type2: str):
    if type1 == "":
        return type2

    if type2 == "":
        return type1

    if type1 == type2:
        return type1

    type1_struct = GLInfo.atom_type_map[type1][2]
    type1_dtype = GLInfo.atom_type_map[type1][1]
    type1_index = GLInfo.basic_types.index(type1_dtype)
    type1_nitems = nitems(type1)

    type2_struct = GLInfo.atom_type_map[type2][2]
    type2_dtype = GLInfo.atom_type_map[type2][1]
    type2_index = GLInfo.basic_types.index(type2_dtype)
    type2_nitems = nitems(type2)

    result_dtype = type1_dtype if type1_index >= type2_index else type2_dtype
    result_struct = type1_struct if type1_nitems >= type2_nitems else type2_struct
    if not result_struct:
        return result_dtype

    if result_dtype == "bool":
        return "b" + result_struct
    elif result_dtype == "int":
        return "i" + result_struct
    elif result_dtype == "uint":
        return "u" + result_struct
    elif result_dtype == "float":
        return result_struct
    elif result_dtype == "double":
        return "d" + result_struct


def subscript_type(type_str: str):
    pos_bracket = type_str.rfind("[")
    if pos_bracket != -1:
        return type_str[:pos_bracket]

    if type_str in ["bvec2", "bvec3", "bvec4"]:
        return "bool"

    if type_str in ["ivec2", "ivec3", "ivec4"]:
        return "int"

    if type_str in ["uvec2", "uvec3", "uvec4"]:
        return "uint"

    if type_str in ["vec2", "vec3", "vec4"]:
        return "float"

    if type_str in ["dvec2", "dvec3", "dvec4"]:
        return "double"

    if type_str in ["mat2", "mat2x2", "mat2x3", "mat2x4"]:
        return "vec2"

    if type_str in ["mat3", "mat3x2", "mat3x3", "mat3x4"]:
        return "vec3"

    if type_str in ["mat4", "mat4x2", "mat4x3", "mat4x4"]:
        return "vec4"

    if type_str in ["dmat2", "dmat2x2", "dmat2x3", "dmat2x4"]:
        return "dvec2"

    if type_str in ["dmat3", "dmat3x2", "dmat3x3", "dmat3x4"]:
        return "dvec3"

    if type_str in ["dmat4", "dmat4x2", "dmat4x3", "dmat4x4"]:
        return "dvec4"

    return ""
