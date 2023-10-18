from OpenGL import GL, constant
import numpy as np
import glm
import struct

from .GLInfo import GLInfo

def glGetInt(gl_constant:constant.IntConstant)->int:
	value = GL.glGetIntegerv(gl_constant)
	try:
		value = value[0]
	except:
		pass

	value = int(value)
	return value

def glGetEnum(gl_constant:constant.IntConstant):
	value = glGetInt(gl_constant)
	if value in GLInfo.enum_map:
		return GLInfo.enum_map[value]
	else:
		return value
	
def glGetEnumi(gl_constant:constant.IntConstant, index:int):
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
	if 'vec2' in str_element_type:
		return 2
	elif 'vec3' in str_element_type:
		return 3
	elif 'vec4' in str_element_type or 'mat2x2' in str_element_type:
		return 4
	elif 'mat2x3' in str_element_type or 'mat3x2' in str_element_type:
		return 6
	elif 'mat3x3' in str_element_type:
		return 9
	elif 'mat2x4' in str_element_type or 'mat4x2' in str_element_type:
		return 8
	elif 'mat3x4' in str_element_type or 'mat4x3' in str_element_type:
		return 12
	elif 'mat4x4' in str_element_type:
		return 16
	else:
		return 1

def to_bytes(value):
	if isinstance(value, bool):
		return int(value).to_bytes(4, byteorder="little")
	elif isinstance(value, int):
		return value.to_bytes(4, byteorder="little")
	elif isinstance(value, float):
		return struct.pack('<f', value)
	else:
		return value.to_bytes()

def type_from_str(type_str):
	if type_str in GLInfo.atom_type_map:
		return GLInfo.atom_type_map[type_str]
	
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
	if internal_format not in GLInfo.format_info_map:
		return GL.GL_RGB
	else:
		return GLInfo.format_info_map[internal_format][0]

def get_channels(internal_format):
	external_format = get_external_format(internal_format)
	if external_format == GL.GL_RED: return 1
	elif external_format == GL.GL_RG: return 2
	elif external_format == GL.GL_RGB: return 3
	elif external_format == GL.GL_RGBA: return 4
	elif external_format == GL.GL_STENCIL_INDEX: return 1
	elif external_format == GL.GL_DEPTH_COMPONENT: return 1
	elif external_format == GL.GL_DEPTH_STENCIL: return 2
	else: return 3

def get_dtype(internal_format):
	if internal_format not in GLInfo.format_info_map:
		return GL.GL_UNSIGNED_BYTE
	else:
		return GLInfo.format_info_map[internal_format][1]
