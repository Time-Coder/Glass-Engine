from OpenGL import GL, constant
import OpenGL.GL.ARB.gpu_shader_int64 as gsi64
import numpy as np
import glm
import ctypes

dtype_uint8 = np.array([], dtype=np.uint8).dtype
dtype_int8 = np.array([], dtype=np.int8).dtype
dtype_uint16 = np.array([], dtype=np.uint16).dtype
dtype_int16 = np.array([], dtype=np.int16).dtype
dtype_uint32 = np.array([], dtype=np.uint32).dtype
dtype_uint64 = np.array([], dtype=np.uint64).dtype
dtype_int32 = np.array([], dtype=np.int32).dtype
dtype_int64 = np.array([], dtype=np.int64).dtype
dtype_float16 = np.array([], dtype=np.float16).dtype
dtype_float32 = np.array([], dtype=np.float32).dtype
dtype_float64 = np.array([], dtype=np.float64).dtype

class GLInfo:
	primary_types = \
	[
		int, float, bool,

		np.int8, np.uint8,
		np.int16, np.uint16,
		np.int32, np.uint32,
		np.int64, np.uint64,
		np.float16, np.float32, np.float64,

		dtype_int8, dtype_uint8,
		dtype_int16, dtype_uint16,
		dtype_int32, dtype_uint32,
		dtype_int64, dtype_uint64,
		dtype_float16, dtype_float32, dtype_float64,

		ctypes.c_int8, ctypes.c_uint8,
		ctypes.c_int16, ctypes.c_uint16,
		ctypes.c_int32, ctypes.c_uint32,
		ctypes.c_int64, ctypes.c_uint64,
		ctypes.c_float, ctypes.c_double
	]

	dtype_map = \
	{
		GL.GL_BYTE: np.int8,
		GL.GL_UNSIGNED_BYTE: np.uint8,
		GL.GL_SHORT: np.int16,
		GL.GL_UNSIGNED_SHORT: np.uint16,
		GL.GL_INT: np.int32,
		GL.GL_UNSIGNED_INT: np.uint32,
		gsi64.GL_UNSIGNED_INT64_ARB: np.uint64,
		GL.GL_HALF_FLOAT: np.float16,
		GL.GL_FLOAT: np.float32,
		GL.GL_DOUBLE: np.float64,
	}

	dtype_inverse_map = \
	{
		dtype_int8:GL.GL_BYTE, np.int8:GL.GL_BYTE, ctypes.c_int8:GL.GL_BYTE, bool:GL.GL_BYTE,
		dtype_uint8:GL.GL_UNSIGNED_BYTE, np.uint8:GL.GL_UNSIGNED_BYTE, ctypes.c_uint8:GL.GL_UNSIGNED_BYTE,
		dtype_int16:GL.GL_SHORT, np.int16:GL.GL_SHORT, ctypes.c_int16:GL.GL_SHORT,
		dtype_uint16:GL.GL_UNSIGNED_SHORT, np.uint16:GL.GL_UNSIGNED_SHORT, ctypes.c_uint16:GL.GL_UNSIGNED_SHORT,
		dtype_int32:GL.GL_INT, np.int32:GL.GL_INT, ctypes.c_int32:GL.GL_INT, int:GL.GL_INT,
		dtype_uint32:GL.GL_UNSIGNED_INT, np.uint32:GL.GL_UNSIGNED_INT, ctypes.c_uint32:GL.GL_UNSIGNED_INT,
		dtype_uint64:gsi64.GL_UNSIGNED_INT64_ARB, np.uint64:gsi64.GL_UNSIGNED_INT64_ARB, ctypes.c_uint64:gsi64.GL_UNSIGNED_INT64_ARB,
		dtype_float16:GL.GL_HALF_FLOAT, np.float16:GL.GL_HALF_FLOAT,
		dtype_float32:GL.GL_FLOAT, np.float32:GL.GL_FLOAT, ctypes.c_float:GL.GL_FLOAT, float:GL.GL_FLOAT,
		dtype_float64:GL.GL_DOUBLE, np.float64:GL.GL_DOUBLE, ctypes.c_double:GL.GL_DOUBLE,
		glm.vec2: GL.GL_FLOAT, glm.vec3: GL.GL_FLOAT, glm.vec4: GL.GL_FLOAT,
		glm.bvec2: GL.GL_BYTE, glm.bvec3: GL.GL_BYTE, glm.bvec4: GL.GL_BYTE,
		glm.ivec2: GL.GL_INT, glm.ivec3: GL.GL_INT, glm.ivec4: GL.GL_INT,
		glm.uvec2: GL.GL_UNSIGNED_INT, glm.uvec3: GL.GL_UNSIGNED_INT, glm.uvec4: GL.GL_UNSIGNED_INT,
		glm.dvec2: GL.GL_DOUBLE, glm.dvec3: GL.GL_DOUBLE, glm.dvec4: GL.GL_DOUBLE,
		glm.mat2x2: GL.GL_FLOAT, glm.mat2x3: GL.GL_FLOAT, glm.mat2x4: GL.GL_FLOAT,
		glm.mat3x2: GL.GL_FLOAT, glm.mat3x3: GL.GL_FLOAT, glm.mat3x4: GL.GL_FLOAT,
		glm.mat4x2: GL.GL_FLOAT, glm.mat4x3: GL.GL_FLOAT, glm.mat4x4: GL.GL_FLOAT,
		glm.dmat2x2: GL.GL_DOUBLE, glm.dmat2x3: GL.GL_DOUBLE, glm.dmat2x4: GL.GL_DOUBLE,
		glm.dmat3x2: GL.GL_DOUBLE, glm.dmat3x3: GL.GL_DOUBLE, glm.dmat3x4: GL.GL_DOUBLE,
		glm.dmat4x2: GL.GL_DOUBLE, glm.dmat4x3: GL.GL_DOUBLE, glm.dmat4x4: GL.GL_DOUBLE,
	}

	np_dtype_map = \
	{
		int: np.int32, float: np.float32,
		glm.vec2: np.float32, glm.vec3: np.float32, glm.vec4: np.float32,
		glm.bvec2: np.int8, glm.bvec3: np.int8, glm.bvec4: np.int8,
		glm.ivec2: np.int32, glm.ivec3: np.int32, glm.ivec4: np.int32,
		glm.uvec2: np.uint32, glm.uvec3: np.uint32, glm.uvec4: np.uint32,
		glm.dvec2: np.float64, glm.dvec3: np.float64, glm.dvec4: np.float64,
		glm.mat2x2: np.float32, glm.mat2x3: np.float32, glm.mat2x4: np.float32,
		glm.mat3x2: np.float32, glm.mat3x3: np.float32, glm.mat3x4: np.float32,
		glm.mat4x2: np.float32, glm.mat4x3: np.float32, glm.mat4x4: np.float32,
		glm.dmat2x2: np.float64, glm.dmat2x3: np.float64, glm.dmat2x4: np.float64,
		glm.dmat3x2: np.float64, glm.dmat3x3: np.float64, glm.dmat3x4: np.float64,
		glm.dmat4x2: np.float64, glm.dmat4x3: np.float64, glm.dmat4x4: np.float64,
	}

	blend_equation_map = \
	{
		GL.GL_FUNC_ADD: "+",
		GL.GL_FUNC_SUBTRACT: "-",
		GL.GL_FUNC_REVERSE_SUBTRACT: GL.GL_FUNC_REVERSE_SUBTRACT,

		"+": GL.GL_FUNC_ADD,
		"-": GL.GL_FUNC_SUBTRACT
	}

	depth_func_map = \
	{
		GL.GL_ALWAYS: "always",
		GL.GL_NEVER: "never",
		GL.GL_LESS: "<",
		GL.GL_EQUAL: "==",
		GL.GL_LEQUAL: "<=",
		GL.GL_GREATER: ">",
		GL.GL_NOTEQUAL: "!=",
		GL.GL_GEQUAL: ">=",

		"always": GL.GL_ALWAYS,
		"never": GL.GL_NEVER,
		"<": GL.GL_LESS,
		"==": GL.GL_EQUAL,
		"<=": GL.GL_LEQUAL,
		">": GL.GL_GREATER,
		"!=": GL.GL_NOTEQUAL,
		">=": GL.GL_GEQUAL
	}

	stencil_func_map = \
	{
		GL.GL_ALWAYS: "always",
		GL.GL_NEVER: "never",
		GL.GL_LESS: "<",
		GL.GL_EQUAL: "==",
		GL.GL_LEQUAL: "<=",
		GL.GL_GREATER: ">",
		GL.GL_NOTEQUAL: "!=",
		GL.GL_GEQUAL: ">=",

		"always": GL.GL_ALWAYS,
		"never": GL.GL_NEVER,
		"<": GL.GL_LESS,
		"==": GL.GL_EQUAL,
		"<=": GL.GL_LEQUAL,
		">": GL.GL_GREATER,
		"!=": GL.GL_NOTEQUAL,
		">=": GL.GL_GEQUAL
	}

	internal_formats_map = \
	{
		np.uint8: {1: GL.GL_R8, 2: GL.GL_RG8, 3: GL.GL_RGB8, 4: GL.GL_RGBA8},
		np.int8: {1: GL.GL_R8I, 2: GL.GL_RG8I, 3: GL.GL_RGB8I, 4: GL.GL_RGBA8I},
		np.uint16: {1: GL.GL_R16, 2: GL.GL_RG16, 3: GL.GL_RGB16, 4: GL.GL_RGBA16},
		np.int16: {1: GL.GL_R16I, 2: GL.GL_RG16I, 3: GL.GL_RGB16I, 4: GL.GL_RGBA16I},
		np.uint32: {1: GL.GL_R32UI, 2: GL.GL_RG32UI, 3: GL.GL_RGB32UI, 4: GL.GL_RGBA32UI},
		np.int32: {1: GL.GL_R32I, 2: GL.GL_RG32I, 3: GL.GL_RGB32I, 4: GL.GL_RGBA32I},
		np.float16: {1: GL.GL_R16F, 2: GL.GL_RG16F, 3: GL.GL_RGB16F, 4: GL.GL_RGBA16F},
		np.float32: {1: GL.GL_R32F, 2: GL.GL_RG32F, 3: GL.GL_RGB32F, 4: GL.GL_RGBA32F},
		# np.float64: {1: GL.GL_R64, 2: GL.GL_RG64F, 3: GL.GL_RGB64F, 4: GL.GL_RGBA64F}

		dtype_uint8: {1: GL.GL_R8, 2: GL.GL_RG8, 3: GL.GL_RGB8, 4: GL.GL_RGBA8},
		dtype_int8: {1: GL.GL_R8I, 2: GL.GL_RG8I, 3: GL.GL_RGB8I, 4: GL.GL_RGBA8I},
		dtype_uint16: {1: GL.GL_R16, 2: GL.GL_RG16, 3: GL.GL_RGB16, 4: GL.GL_RGBA16},
		dtype_int16: {1: GL.GL_R16I, 2: GL.GL_RG16I, 3: GL.GL_RGB16I, 4: GL.GL_RGBA16I},
		dtype_uint32: {1: GL.GL_R32UI, 2: GL.GL_RG32UI, 3: GL.GL_RGB32UI, 4: GL.GL_RGBA32UI},
		dtype_int32: {1: GL.GL_R32I, 2: GL.GL_RG32I, 3: GL.GL_RGB32I, 4: GL.GL_RGBA32I},
		dtype_float16: {1: GL.GL_R16F, 2: GL.GL_RG16F, 3: GL.GL_RGB16F, 4: GL.GL_RGBA16F},
		dtype_float32: {1: GL.GL_R32F, 2: GL.GL_RG32F, 3: GL.GL_RGB32F, 4: GL.GL_RGBA32F},
		# dtype_float64: {1: GL.GL_R64, 2: GL.GL_RG64F, 3: GL.GL_RGB64F, 4: GL.GL_RGBA64F}
	}

	format_info_map = \
	{
		GL.GL_RED: [GL.GL_RED, GL.GL_UNSIGNED_BYTE],
		GL.GL_R8: [GL.GL_RED, GL.GL_UNSIGNED_BYTE],
		GL.GL_R8_SNORM: [GL.GL_RED, GL.GL_BYTE],
		GL.GL_R16: [GL.GL_RED, GL.GL_UNSIGNED_SHORT],
		GL.GL_R16_SNORM: [GL.GL_RED, GL.GL_SHORT],
		GL.GL_R16F: [GL.GL_RED, GL.GL_HALF_FLOAT],
		GL.GL_R32F: [GL.GL_RED, GL.GL_FLOAT],
		GL.GL_R8I: [GL.GL_RED_INTEGER, GL.GL_BYTE],
		GL.GL_R8UI: [GL.GL_RED_INTEGER, GL.GL_UNSIGNED_BYTE],
		GL.GL_R16I: [GL.GL_RED_INTEGER, GL.GL_SHORT],
		GL.GL_R16UI: [GL.GL_RED_INTEGER, GL.GL_UNSIGNED_SHORT],
		GL.GL_R32I: [GL.GL_RED_INTEGER, GL.GL_INT],
		GL.GL_R32UI: [GL.GL_RED_INTEGER, GL.GL_UNSIGNED_INT],
		GL.GL_COMPRESSED_RED: [GL.GL_RED, GL.GL_UNSIGNED_BYTE],
		GL.GL_COMPRESSED_RED_RGTC1: [GL.GL_RED, GL.GL_UNSIGNED_BYTE],
		GL.GL_COMPRESSED_SIGNED_RED_RGTC1: [GL.GL_RED, GL.GL_BYTE],
		GL.GL_RG: [GL.GL_RG, GL.GL_UNSIGNED_BYTE],
		GL.GL_RG8: [GL.GL_RG, GL.GL_UNSIGNED_BYTE],
		GL.GL_RG8_SNORM: [GL.GL_RG, GL.GL_BYTE],
		GL.GL_RG16: [GL.GL_RG, GL.GL_UNSIGNED_SHORT],
		GL.GL_RG16_SNORM: [GL.GL_RG, GL.GL_SHORT],
		GL.GL_RG16F: [GL.GL_RG, GL.GL_HALF_FLOAT],
		GL.GL_RG32F: [GL.GL_RG, GL.GL_FLOAT],
		GL.GL_RG8I: [GL.GL_RG_INTEGER, GL.GL_BYTE],
		GL.GL_RG8UI: [GL.GL_RG_INTEGER, GL.GL_UNSIGNED_BYTE],
		GL.GL_RG16I: [GL.GL_RG_INTEGER, GL.GL_SHORT],
		GL.GL_RG16UI: [GL.GL_RG_INTEGER, GL.GL_UNSIGNED_SHORT],
		GL.GL_RG32I: [GL.GL_RG_INTEGER, GL.GL_INT],
		GL.GL_RG32UI: [GL.GL_RG_INTEGER, GL.GL_UNSIGNED_INT],
		GL.GL_COMPRESSED_RG: [GL.GL_RG, GL.GL_UNSIGNED_BYTE],
		GL.GL_COMPRESSED_RG_RGTC2: [GL.GL_RG, GL.GL_UNSIGNED_BYTE],
		GL.GL_COMPRESSED_SIGNED_RG_RGTC2: [GL.GL_RG, GL.GL_BYTE],
		GL.GL_RGB: [GL.GL_RGB, GL.GL_UNSIGNED_BYTE],
		GL.GL_R3_G3_B2: [GL.GL_RGB, GL.GL_UNSIGNED_BYTE],
		GL.GL_RGB4: [GL.GL_RGB, GL.GL_UNSIGNED_BYTE],
		GL.GL_RGB5: [GL.GL_RGB, GL.GL_UNSIGNED_BYTE],
		GL.GL_RGB8: [GL.GL_RGB, GL.GL_UNSIGNED_BYTE],
		GL.GL_RGB8_SNORM: [GL.GL_RGB, GL.GL_BYTE],
		GL.GL_RGB10: [GL.GL_RGB, GL.GL_UNSIGNED_SHORT],
		GL.GL_RGB12: [GL.GL_RGB, GL.GL_UNSIGNED_SHORT],
		GL.GL_RGB16: [GL.GL_RGB, GL.GL_UNSIGNED_SHORT],
		GL.GL_RGB16_SNORM: [GL.GL_RGB, GL.GL_SHORT],
		GL.GL_SRGB8: [GL.GL_RGB, GL.GL_BYTE],
		GL.GL_RGB16F: [GL.GL_RGB, GL.GL_HALF_FLOAT],
		GL.GL_RGB32F: [GL.GL_RGB, GL.GL_FLOAT],
		GL.GL_R11F_G11F_B10F: [GL.GL_RGB, GL.GL_HALF_FLOAT],
		GL.GL_RGB9_E5: [GL.GL_RGB, GL.GL_SHORT],
		GL.GL_RGB8I: [GL.GL_RGB_INTEGER, GL.GL_BYTE],
		GL.GL_RGB8UI: [GL.GL_RGB_INTEGER, GL.GL_UNSIGNED_BYTE],
		GL.GL_RGB16I: [GL.GL_RGB_INTEGER, GL.GL_SHORT],
		GL.GL_RGB16UI: [GL.GL_RGB_INTEGER, GL.GL_UNSIGNED_SHORT],
		GL.GL_RGB32I: [GL.GL_RGB_INTEGER, GL.GL_INT],
		GL.GL_RGB32UI: [GL.GL_RGB_INTEGER, GL.GL_UNSIGNED_INT],
		GL.GL_COMPRESSED_RGB: [GL.GL_RGB, GL.GL_UNSIGNED_BYTE],
		GL.GL_COMPRESSED_SRGB: [GL.GL_RGB, GL.GL_UNSIGNED_BYTE],
		GL.GL_COMPRESSED_RGB_BPTC_SIGNED_FLOAT: [GL.GL_RGB, GL.GL_FLOAT],
		GL.GL_COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT: [GL.GL_RGB, GL.GL_FLOAT],
		GL.GL_RGBA: [GL.GL_RGBA, GL.GL_UNSIGNED_BYTE],
		GL.GL_RGBA2: [GL.GL_RGBA, GL.GL_UNSIGNED_BYTE],
		GL.GL_RGBA4: [GL.GL_RGBA, GL.GL_UNSIGNED_BYTE],
		GL.GL_RGB5_A1: [GL.GL_RGBA, GL.GL_UNSIGNED_BYTE],
		GL.GL_RGBA8: [GL.GL_RGBA, GL.GL_UNSIGNED_BYTE],
		GL.GL_RGBA8_SNORM: [GL.GL_RGBA, GL.GL_BYTE],
		GL.GL_RGB10_A2: [GL.GL_RGBA, GL.GL_UNSIGNED_SHORT],
		GL.GL_RGB10_A2UI: [GL.GL_RGBA, GL.GL_UNSIGNED_SHORT],
		GL.GL_RGBA12: [GL.GL_RGBA, GL.GL_UNSIGNED_SHORT],
		GL.GL_RGBA16: [GL.GL_RGBA, GL.GL_UNSIGNED_SHORT],
		GL.GL_RGBA16_SNORM: [GL.GL_RGBA, GL.GL_UNSIGNED_SHORT],
		GL.GL_SRGB8_ALPHA8: [GL.GL_RGBA, GL.GL_UNSIGNED_BYTE],
		GL.GL_RGBA16F: [GL.GL_RGBA, GL.GL_HALF_FLOAT],
		GL.GL_RGBA32F: [GL.GL_RGBA, GL.GL_FLOAT],
		GL.GL_RGBA8I: [GL.GL_RGBA_INTEGER, GL.GL_BYTE],
		GL.GL_RGBA8UI: [GL.GL_RGBA_INTEGER, GL.GL_UNSIGNED_BYTE],
		GL.GL_RGBA16I: [GL.GL_RGBA_INTEGER, GL.GL_SHORT],
		GL.GL_RGBA16UI: [GL.GL_RGBA_INTEGER, GL.GL_UNSIGNED_SHORT],
		GL.GL_RGBA32I: [GL.GL_RGBA_INTEGER, GL.GL_INT],
		GL.GL_RGBA32UI: [GL.GL_RGBA_INTEGER, GL.GL_UNSIGNED_INT],
		GL.GL_COMPRESSED_RGBA: [GL.GL_RGBA, GL.GL_UNSIGNED_BYTE],
		GL.GL_COMPRESSED_SRGB_ALPHA: [GL.GL_RGBA, GL.GL_UNSIGNED_BYTE],
		GL.GL_COMPRESSED_RGBA_BPTC_UNORM: [GL.GL_RGBA, GL.GL_UNSIGNED_BYTE],
		GL.GL_COMPRESSED_SRGB_ALPHA_BPTC_UNORM: [GL.GL_RGBA, GL.GL_UNSIGNED_BYTE],

		GL.GL_DEPTH_COMPONENT: [GL.GL_DEPTH_COMPONENT, GL.GL_FLOAT],
		GL.GL_DEPTH_COMPONENT16: [GL.GL_DEPTH_COMPONENT, GL.GL_SHORT],
		GL.GL_DEPTH_COMPONENT24: [GL.GL_DEPTH_COMPONENT, GL.GL_INT],
		GL.GL_DEPTH_COMPONENT32: [GL.GL_DEPTH_COMPONENT, GL.GL_INT],
		GL.GL_DEPTH_COMPONENT32F: [GL.GL_DEPTH_COMPONENT, GL.GL_FLOAT],

		GL.GL_STENCIL_INDEX: [GL.GL_STENCIL_INDEX, GL.GL_UNSIGNED_BYTE],
		GL.GL_STENCIL_INDEX1: [GL.GL_STENCIL_INDEX, GL.GL_UNSIGNED_BYTE],
		GL.GL_STENCIL_INDEX4: [GL.GL_STENCIL_INDEX, GL.GL_UNSIGNED_BYTE],
		GL.GL_STENCIL_INDEX8: [GL.GL_STENCIL_INDEX, GL.GL_UNSIGNED_BYTE],
		GL.GL_STENCIL_INDEX16: [GL.GL_STENCIL_INDEX, GL.GL_UNSIGNED_SHORT],

		GL.GL_DEPTH_STENCIL: [GL.GL_DEPTH_STENCIL, GL.GL_FLOAT],
		GL.GL_DEPTH24_STENCIL8: [GL.GL_DEPTH_STENCIL, GL.GL_FLOAT],
		GL.GL_DEPTH32F_STENCIL8: [GL.GL_DEPTH_STENCIL, GL.GL_FLOAT]
	}

	enum_map = {value:value for name, value in vars(GL).items() if name.startswith('GL_') and isinstance(value, constant.IntConstant)}

	internal_formats = \
	[
		GL.GL_RED, GL.GL_R8, GL.GL_R8_SNORM, GL.GL_R16, GL.GL_R16_SNORM,
		GL.GL_R16F, GL.GL_R32F, GL.GL_R8I, GL.GL_R8UI, GL.GL_R16I, GL.GL_R16UI,
		GL.GL_R32I, GL.GL_R32UI, GL.GL_COMPRESSED_RED, GL.GL_COMPRESSED_RED_RGTC1,
		GL.GL_COMPRESSED_SIGNED_RED_RGTC1, GL.GL_RG, GL.GL_RG8, GL.GL_RG8_SNORM, GL.GL_RG16,
		GL.GL_RG16_SNORM, GL.GL_RG16F, GL.GL_RG32F, GL.GL_RG8I, GL.GL_RG8UI, GL.GL_RG16I,
		GL.GL_RG16UI, GL.GL_RG32I, GL.GL_RG32UI, GL.GL_COMPRESSED_RG, GL.GL_COMPRESSED_RG_RGTC2,
		GL.GL_COMPRESSED_SIGNED_RG_RGTC2, GL.GL_RGB, GL.GL_R3_G3_B2, GL.GL_RGB4, GL.GL_RGB5,
		GL.GL_RGB8, GL.GL_RGB8_SNORM, GL.GL_RGB10, GL.GL_RGB12, GL.GL_RGB16, GL.GL_RGB16_SNORM, GL.GL_SRGB8,
		GL.GL_RGB16F, GL.GL_RGB32F, GL.GL_R11F_G11F_B10F, GL.GL_RGB9_E5, GL.GL_RGB8I,
		GL.GL_RGB8UI, GL.GL_RGB16I, GL.GL_RGB16UI, GL.GL_RGB32I, GL.GL_RGB32UI,
		GL.GL_COMPRESSED_RGB, GL.GL_COMPRESSED_SRGB, GL.GL_COMPRESSED_RGB_BPTC_SIGNED_FLOAT,
		GL.GL_COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT, GL.GL_RGBA, GL.GL_RGBA2, GL.GL_RGBA4,
		GL.GL_RGB5_A1, GL.GL_RGBA8, GL.GL_RGBA8_SNORM, GL.GL_RGB10_A2, GL.GL_RGB10_A2UI,
		GL.GL_RGBA12, GL.GL_RGBA16, GL.GL_RGBA16_SNORM, GL.GL_SRGB8_ALPHA8, GL.GL_RGBA16F,
		GL.GL_RGBA32F, GL.GL_RGBA8I, GL.GL_RGBA8UI, GL.GL_RGBA16I, GL.GL_RGBA16UI,
		GL.GL_RGBA32I, GL.GL_RGBA32UI, GL.GL_COMPRESSED_RGBA, GL.GL_COMPRESSED_SRGB_ALPHA,
		GL.GL_COMPRESSED_RGBA_BPTC_UNORM, GL.GL_COMPRESSED_SRGB_ALPHA_BPTC_UNORM,

		GL.GL_DEPTH_COMPONENT, GL.GL_DEPTH_COMPONENT16, GL.GL_DEPTH_COMPONENT24, GL.GL_DEPTH_COMPONENT32, GL.GL_DEPTH_COMPONENT32F,
		GL.GL_STENCIL_INDEX, GL.GL_STENCIL_INDEX1, GL.GL_STENCIL_INDEX4, GL.GL_STENCIL_INDEX8, GL.GL_STENCIL_INDEX16,
		GL.GL_DEPTH_STENCIL, GL.GL_DEPTH24_STENCIL8, GL.GL_DEPTH32F_STENCIL8, None
	]

	color_internal_formats = \
	[
		GL.GL_RED, GL.GL_R8, GL.GL_R8_SNORM, GL.GL_R16, GL.GL_R16_SNORM,
		GL.GL_R16F, GL.GL_R32F, GL.GL_R8I, GL.GL_R8UI, GL.GL_R16I, GL.GL_R16UI,
		GL.GL_R32I, GL.GL_R32UI, GL.GL_COMPRESSED_RED, GL.GL_COMPRESSED_RED_RGTC1,
		GL.GL_COMPRESSED_SIGNED_RED_RGTC1, GL.GL_RG, GL.GL_RG8, GL.GL_RG8_SNORM, GL.GL_RG16,
		GL.GL_RG16_SNORM, GL.GL_RG16F, GL.GL_RG32F, GL.GL_RG8I, GL.GL_RG8UI, GL.GL_RG16I,
		GL.GL_RG16UI, GL.GL_RG32I, GL.GL_RG32UI, GL.GL_COMPRESSED_RG, GL.GL_COMPRESSED_RG_RGTC2,
		GL.GL_COMPRESSED_SIGNED_RG_RGTC2, GL.GL_RGB, GL.GL_R3_G3_B2, GL.GL_RGB4, GL.GL_RGB5,
		GL.GL_RGB8, GL.GL_RGB8_SNORM, GL.GL_RGB10, GL.GL_RGB12, GL.GL_RGB16, GL.GL_RGB16_SNORM, GL.GL_SRGB8,
		GL.GL_RGB16F, GL.GL_RGB32F, GL.GL_R11F_G11F_B10F, GL.GL_RGB9_E5, GL.GL_RGB8I,
		GL.GL_RGB8UI, GL.GL_RGB16I, GL.GL_RGB16UI, GL.GL_RGB32I, GL.GL_RGB32UI,
		GL.GL_COMPRESSED_RGB, GL.GL_COMPRESSED_SRGB, GL.GL_COMPRESSED_RGB_BPTC_SIGNED_FLOAT,
		GL.GL_COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT, GL.GL_RGBA, GL.GL_RGBA2, GL.GL_RGBA4,
		GL.GL_RGB5_A1, GL.GL_RGBA8, GL.GL_RGBA8_SNORM, GL.GL_RGB10_A2, GL.GL_RGB10_A2UI,
		GL.GL_RGBA12, GL.GL_RGBA16, GL.GL_RGBA16_SNORM, GL.GL_SRGB8_ALPHA8, GL.GL_RGBA16F,
		GL.GL_RGBA32F, GL.GL_RGBA8I, GL.GL_RGBA8UI, GL.GL_RGBA16I, GL.GL_RGBA16UI,
		GL.GL_RGBA32I, GL.GL_RGBA32UI, GL.GL_COMPRESSED_RGBA, GL.GL_COMPRESSED_SRGB_ALPHA,
		GL.GL_COMPRESSED_RGBA_BPTC_UNORM, GL.GL_COMPRESSED_SRGB_ALPHA_BPTC_UNORM
	]

	image_internal_formats = \
	[
		GL.GL_RGBA32F, GL.GL_RGBA16F, GL.GL_RG32F, GL.GL_RG16F, GL.GL_R11F_G11F_B10F,
		GL.GL_R32F, GL.GL_R16F, GL.GL_RGBA16, GL.GL_RGB10_A2, GL.GL_RGBA8, GL.GL_RG16,
		GL.GL_RG8, GL.GL_R16, GL.GL_R8, GL.GL_RGBA16_SNORM, GL.GL_RGBA8_SNORM,
		GL.GL_RG16_SNORM, GL.GL_RG8_SNORM, GL.GL_R16_SNORM, None
	]

	isampler_internal_formats = \
	[
		GL.GL_RGBA32I, GL.GL_RGBA16I, GL.GL_RGBA8I,
		GL.GL_RGB32I, GL.GL_RGB16I, GL.GL_RGB8I,
		GL.GL_RG32I, GL.GL_RG16I, GL.GL_RG8I,
		GL.GL_R32I, GL.GL_R16I, GL.GL_R8I, None
	]

	iimage_internal_formats = \
	[
		GL.GL_RGBA32I, GL.GL_RGBA16I, GL.GL_RGBA8I, GL.GL_RG32I, GL.GL_RG16I,
		GL.GL_RG8I, GL.GL_R32I, GL.GL_R16I, GL.GL_R8I, None
	]

	usampler_internal_formats = \
	[
		GL.GL_RGBA32UI, GL.GL_RGBA16UI, GL.GL_RGB10_A2UI, GL.GL_RGBA8UI,
		GL.GL_RGB32UI, GL.GL_RGB16UI, GL.GL_RGB8UI,
		GL.GL_RG32UI, GL.GL_RG16UI, GL.GL_RG8UI,
		GL.GL_R32UI, GL.GL_R16UI, GL.GL_R8UI, None
	]

	uimage_internal_formats = \
	[
		GL.GL_RGBA32UI, GL.GL_RGBA16UI, GL.GL_RGB10_A2UI, GL.GL_RGBA8UI,
		GL.GL_RG32UI, GL.GL_RG16UI, GL.GL_RG8UI, GL.GL_R32UI, GL.GL_R16UI,
		GL.GL_R8UI, None
	]

	depth_internal_formats = \
	[
		GL.GL_DEPTH_COMPONENT, GL.GL_DEPTH_COMPONENT16, GL.GL_DEPTH_COMPONENT24,
		GL.GL_DEPTH_COMPONENT32, GL.GL_DEPTH_COMPONENT32F,
	]

	stencil_internal_formats = \
	[
		GL.GL_STENCIL_INDEX, GL.GL_STENCIL_INDEX1, GL.GL_STENCIL_INDEX4,
		GL.GL_STENCIL_INDEX8, GL.GL_STENCIL_INDEX16,
	]

	depth_stencil_internal_formats = \
	[
		GL.GL_DEPTH_STENCIL, GL.GL_DEPTH24_STENCIL8, GL.GL_DEPTH32F_STENCIL8
	]

	fog_modes = [GL.GL_LINEAR, GL.GL_EXP, GL.GL_EXP2]

	dtypes = \
	[
		GL.GL_BYTE, GL.GL_UNSIGNED_BYTE, GL.GL_SHORT, GL.GL_UNSIGNED_SHORT, GL.GL_INT,
		GL.GL_UNSIGNED_INT, GL.GL_HALF_FLOAT, GL.GL_FLOAT, GL.GL_DOUBLE, None
	]

	operations = \
	[
		GL.GL_KEEP, # 保持模板缓冲区的当前值
		GL.GL_ZERO, # 将模板缓冲区的值设置为 0
		GL.GL_REPLACE, # 将模板缓冲区的值替换为参考值（通过 glStencilFunc() 设置）
		GL.GL_INCR, # 将模板缓冲区的值递增 1（如果结果超出了模板缓冲区的范围，将会回环到 0）
		GL.GL_DECR, # 将模板缓冲区的值递减 1（如果结果小于 0，将会回环到最大值）
		GL.GL_INVERT # 按位取反模板缓冲区的值
	]

	shader_ext_map = \
	{
		".vert": GL.GL_VERTEX_SHADER,
		".tesc": GL.GL_TESS_CONTROL_SHADER,
		".tese": GL.GL_TESS_EVALUATION_SHADER,
		".geom": GL.GL_GEOMETRY_SHADER,
		".frag": GL.GL_FRAGMENT_SHADER,
		".comp": GL.GL_COMPUTE_SHADER,
		
		".vs": GL.GL_VERTEX_SHADER,
		".tcs": GL.GL_TESS_CONTROL_SHADER,
		".tes": GL.GL_TESS_EVALUATION_SHADER,
		".gs": GL.GL_GEOMETRY_SHADER,
		".fs": GL.GL_FRAGMENT_SHADER,
		".cs": GL.GL_COMPUTE_SHADER,

		GL.GL_VERTEX_SHADER: ".vert",
		GL.GL_TESS_CONTROL_SHADER: ".tesc",
		GL.GL_TESS_EVALUATION_SHADER: ".tese",
		GL.GL_GEOMETRY_SHADER: ".geom",
		GL.GL_FRAGMENT_SHADER: ".frag",
		GL.GL_COMPUTE_SHADER: ".comp"
	}

	primitive_type_map = \
	{
		"points": [GL.GL_POINTS],
		"lines": [GL.GL_LINES, GL.GL_LINE_STRIP, GL.GL_LINE_LOOP],
		"lines_adjacency": [GL.GL_LINES_ADJACENCY, GL.GL_LINE_STRIP_ADJACENCY],
		"triangles": [GL.GL_TRIANGLES, GL.GL_TRIANGLE_STRIP, GL.GL_TRIANGLE_FAN],
		"triangles_adjacency": [GL.GL_TRIANGLES_ADJACENCY, GL.GL_TRIANGLE_STRIP_ADJACENCY]
	}

	polygon_modes = [GL.GL_FILL, GL.GL_LINE, GL.GL_POINT]

	depth_funcs = [GL.GL_ALWAYS, GL.GL_NEVER, GL.GL_LESS, GL.GL_EQUAL, GL.GL_LEQUAL, GL.GL_GREATER, GL.GL_NOTEQUAL, GL.GL_GEQUAL]

	depth_func_strs = ["always", "never", "<", "==", "<=", ">", "!=", ">="]

	stencil_funcs = [GL.GL_ALWAYS, GL.GL_NEVER, GL.GL_LESS, GL.GL_EQUAL, GL.GL_LEQUAL, GL.GL_GREATER, GL.GL_NOTEQUAL, GL.GL_GEQUAL]

	stencil_func_strs = ["always", "never", "<", "==", "<=", ">", "!=", ">="]

	shader_types = [GL.GL_VERTEX_SHADER, GL.GL_FRAGMENT_SHADER, GL.GL_GEOMETRY_SHADER, GL.GL_TESS_CONTROL_SHADER, GL.GL_TESS_EVALUATION_SHADER, None]
	
	wrap_types = [GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT, GL.GL_CLAMP_TO_EDGE, GL.GL_CLAMP_TO_BORDER, GL.GL_MIRROR_CLAMP_TO_EDGE]
	
	filter_types = [GL.GL_NEAREST, GL.GL_LINEAR, None]
	
	none_color_attachment_types = [GL.GL_DEPTH_ATTACHMENT, GL.GL_STENCIL_ATTACHMENT, GL.GL_DEPTH_STENCIL_ATTACHMENT]
	
	draw_types = [GL.GL_STATIC_DRAW, GL.GL_DYNAMIC_DRAW, GL.GL_STREAM_DRAW, GL.GL_DYNAMIC_COPY]
	
	triangle_types = [GL.GL_TRIANGLES, GL.GL_TRIANGLE_STRIP, GL.GL_TRIANGLE_FAN]
	
	line_types = [GL.GL_LINES, GL.GL_LINE_LOOP, GL.GL_LINE_STRIP]
	
	primitive_types = [*triangle_types, *line_types, GL.GL_POINTS, GL.GL_PATCHES]
	
	cull_face_types = [GL.GL_BACK, GL.GL_FRONT, GL.GL_FRONT_AND_BACK, None]
	
	blend_equations = [GL.GL_FUNC_ADD, GL.GL_FUNC_SUBTRACT, GL.GL_FUNC_REVERSE_SUBTRACT]
	
	blend_funcs = \
	[
		GL.GL_ZERO, GL.GL_ONE,
		GL.GL_SRC_COLOR, GL.GL_ONE_MINUS_SRC_COLOR,
		GL.GL_DST_COLOR, GL.GL_ONE_MINUS_DST_COLOR,
		GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA,
		GL.GL_DST_ALPHA, GL.GL_ONE_MINUS_DST_ALPHA,
		GL.GL_CONSTANT_COLOR, GL.GL_ONE_MINUS_CONSTANT_COLOR,
		GL.GL_CONSTANT_ALPHA, GL.GL_ONE_MINUS_CONSTANT_ALPHA
	]

	attr_types = \
	(
		int, float,
		glm.vec2, glm.ivec2, glm.uvec2, glm.dvec2,
		glm.vec3, glm.ivec3, glm.uvec3, glm.dvec3,
		glm.vec4, glm.ivec4, glm.uvec4, glm.dvec4,

		glm.mat2x2, glm.mat2x3, glm.mat2x4,
		glm.mat3x2, glm.mat3x3, glm.mat3x4,
		glm.mat4x2, glm.mat4x3, glm.mat4x4,

		glm.dmat2x2, glm.dmat2x3, glm.dmat2x4,
		glm.dmat3x2, glm.dmat3x3, glm.dmat3x4,
		glm.dmat4x2, glm.dmat4x3, glm.dmat4x4,
	)

	int_types = [GL.GL_BYTE, GL.GL_UNSIGNED_BYTE, GL.GL_SHORT, GL.GL_UNSIGNED_SHORT, GL.GL_INT, GL.GL_UNSIGNED_INT]

	atom_type_names = \
	[
		"bool", "int", "uint", "uint64_t", "float", "double", "atomic_uint",

		"bvec2", "bvec3", "bvec4",
		"ivec2", "ivec3", "ivec4",
		"uvec2", "uvec3", "uvec4",
		"vec2", "vec3", "vec4",
		"dvec2", "dvec3", "dvec4",

		"mat2x2", "mat3x2", "mat4x2",
		"mat2x3", "mat3x3", "mat4x3",
		"mat2x4", "mat3x4", "mat4x4",
		"mat2", "mat3", "mat4",

		"dmat2x2", "dmat3x2", "dmat4x2",
		"dmat2x3", "dmat3x3", "dmat4x3",
		"dmat2x4", "dmat3x4", "dmat4x4",
		"dmat2", "dmat3", "dmat4",

		"sampler2D", "isampler2D", "usampler2D",
		"sampler2DMS", "isampler2DMS", "usampler2DMS",
		"sampler2DArray", "isampler2DArray", "usampler2DArray",
		"sampler2DMSArray", "isampler2DMSArray", "usampler2DMSArray",
		"samplerCube", "samplerCubeArray",
		"image2D", "iimage2D", "uimage2D"
	]

	atom_type_map = \
	{
		"bool":bool, "int":int, "uint":np.uint32, "uint64_t":np.uint64,
		"float":np.float32, "double":np.float64, "atomic_uint":np.uint32,

		"bvec2":glm.bvec2, "bvec3":glm.bvec3, "bvec4":glm.bvec4,
		"ivec2":glm.ivec2, "ivec3":glm.ivec3, "ivec4":glm.ivec4,
		"uvec2":glm.uvec2, "uvec3":glm.uvec3, "uvec4":glm.uvec4,
		"vec2":glm.vec2, "vec3":glm.vec3, "vec4":glm.vec4,
		"dvec2":glm.dvec2, "dvec3":glm.dvec3, "dvec4":glm.dvec4,

		"mat2x2":glm.mat2x2, "mat3x2":glm.mat3x2, "mat4x2":glm.mat4x2,
		"mat2x3":glm.mat2x3, "mat3x3":glm.mat3x3, "mat4x3":glm.mat4x3,
		"mat2x4":glm.mat2x4, "mat3x4":glm.mat3x4, "mat4x4":glm.mat4x4,
		"mat2":glm.mat2, "mat3":glm.mat3, "mat4":glm.mat4,

		"dmat2x2":glm.dmat2x2, "dmat3x2":glm.dmat3x2, "dmat4x2":glm.dmat4x2,
		"dmat2x3":glm.dmat2x3, "dmat3x3":glm.dmat3x3, "dmat4x3":glm.dmat4x3,
		"dmat2x4":glm.dmat2x4, "dmat3x4":glm.dmat3x4, "dmat4x4":glm.dmat4x4,
		"dmat2":glm.dmat2, "dmat3":glm.dmat3, "dmat4":glm.dmat4
	}

	memory_modifiers_to_internal_types_map = \
	{
		"r11f_g11f_b10f": GL.GL_R11F_G11F_B10F,
		"rgba16_snorm": GL.GL_RGBA16_SNORM,
		"rgba8_snorm": GL.GL_RGBA8_SNORM,
		"rg16_snorm": GL.GL_RG16_SNORM,
		"rgb10_a2ui": GL.GL_RGB10_A2UI,
		"rg8_snorm": GL.GL_RG8_SNORM,
		"r16_snorm": GL.GL_R16_SNORM,
		"r8_snorm": GL.GL_R8_SNORM,
		"rgb10_a2": GL.GL_RGB10_A2,
		"rgba32ui": GL.GL_RGBA32UI,
		"rgba16ui": GL.GL_RGBA16UI,
		"rgba8ui": GL.GL_RGBA8UI,
		"rgba32f": GL.GL_RGBA32F,
		"rgba16f": GL.GL_RGBA16F,
		"rgba32i": GL.GL_RGBA32UI,
		"rgba16i": GL.GL_RGBA16I,
		"rgba16": GL.GL_RGBA16,
		"rgba8i": GL.GL_RGBA8I,
		"rg32ui": GL.GL_RG32UI,
		"rg16ui": GL.GL_RG16UI,
		"rg8ui": GL.GL_RG8UI,
		"r32ui": GL.GL_R32UI,
		"r16ui": GL.GL_R16UI,
		"rg32i": GL.GL_RG32I,
		"rg16i": GL.GL_RG16I,
		"rg32f": GL.GL_RG32F,
		"rg16f": GL.GL_RG16F,
		"rgba8": GL.GL_RGBA8,
		"rg8i": GL.GL_RG8I,
		"r32i": GL.GL_R32I,
		"r16i": GL.GL_R16I,
		"r32f": GL.GL_R32F,
		"r16f": GL.GL_R16F,
		"rg16": GL.GL_RG16,
		"r8ui": GL.GL_R8UI,
		"r8i": GL.GL_R8I,
		"rg8": GL.GL_RG8,
		"r16": GL.GL_R16,
		"r8": GL.GL_R8
	}
	mipmap_filter_map = \
	{
		(GL.GL_NEAREST, GL.GL_NEAREST): GL.GL_NEAREST_MIPMAP_NEAREST,
		(GL.GL_NEAREST, GL.GL_LINEAR): GL.GL_NEAREST_MIPMAP_LINEAR,
		(GL.GL_LINEAR, GL.GL_NEAREST): GL.GL_LINEAR_MIPMAP_NEAREST,
		(GL.GL_LINEAR, GL.GL_LINEAR): GL.GL_LINEAR_MIPMAP_LINEAR
	}
	fbo_status_errors = \
	{
		GL.GL_FRAMEBUFFER_UNDEFINED: "default FBO does not exist",
		GL.GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT: "some attachments are incomplete",
		GL.GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT: "no attachments attached",
		GL.GL_FRAMEBUFFER_INCOMPLETE_DRAW_BUFFER: "all color attachments' GL_FRAMEBUFFER_ATTACHMENT_OBJECT_TYPE is GL_NONE",
		GL.GL_FRAMEBUFFER_INCOMPLETE_READ_BUFFER: "all read buffer color attachments' GL_FRAMEBUFFER_ATTACHMENT_OBJECT_TYPE is GL_NONE",
		GL.GL_FRAMEBUFFER_UNSUPPORTED: "the combination of attachments' internal formats violates an implementation-dependent set of restrictions",
		GL.GL_FRAMEBUFFER_INCOMPLETE_MULTISAMPLE: 
		[
			"GL_RENDERBUFFER_SAMPLES is not the same for all attached RBOs",
			"GL_TEXTURE_SAMPLES is the not same for all attached textures",
			"attachments are a mix of RBOs and textures, but GL_RENDERBUFFER_SAMPLES doesn't match GL_TEXTURE_SAMPLES",
			"GL_TEXTURE_FIXED_SAMPLE_LOCATIONS is not the same for all attached textures",
			"attachments are a mix of RBOs and textures, but GL_TEXTURE_FIXED_SAMPLE_LOCATIONS is not GL_TRUE for all attached textures",
		],
		GL.GL_FRAMEBUFFER_INCOMPLETE_LAYER_TARGETS:
		[
			"some attachments are layered, but some populated attachments are not layered",
			"all populated color attachments are not from textures of the same target"
		]
	}