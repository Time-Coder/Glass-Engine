import glm
import numpy as np
import struct
from OpenGL import GL
from enum import Enum

from .GLConfig import GLConfig
from .GLInfo import GLInfo
from .BO import BO
from .utils import checktype, capacity_of, subscript
from .helper import sizeof, type_from_str

class BindingPointsPool:
	def __init__(self, start, end, error_message=""):
		self._start = start
		self._end = end
		self._used_id = set()
		self._error_message = error_message

	@checktype
	def get(self, index:int=None):
		if index is None:
			for i in range(self._start, self._end):
				if i not in self._used_id:
					self._used_id.add(i)
					return i
		else:
			if index not in self._used_id:
				self._used_id.add(index)
				return index

		raise ValueError(self._error_message)

	def put_back(self, i):
		if i in self._used_id:
			self._used_id.remove(i)

class SSUBO(BO):

	_get_set_atom_map = {}

	@classmethod
	def _get_binding_point(cls):
		if cls._binding_points_pool is None:
			max_bindings = 0
			if cls.__name__ == "UBO":
				max_bindings = GLConfig.max_uniform_buffer_bindings
			elif cls.__name__ == "SSBO":
				max_bindings = GLConfig.max_shader_storage_buffer_bindings

			cls._binding_points_pool = BindingPointsPool(1, max_bindings)

		return cls._binding_points_pool.get()

	@classmethod
	def _put_back_binding_point(cls, point:int):
		if cls._binding_points_pool is not None:
			cls._binding_points_pool.put_back(point)

	def __init__(self):
		BO.__init__(self)
		self._bound_var = None
		self._buffer = bytearray()
		self._atom_info_map = {}
		self._binding_points = {}
		self._bound_block_vars = set()
		self._len_array = None
		self._force_upload = False

	def __del__(self):
		for bind_range in self._binding_points:
			self.__class__._put_back_binding_point(self._binding_points[bind_range])
		BO.__del__(self)

	def malloc(self, nbytes, draw_type:GLInfo.draw_types=GL.GL_STATIC_DRAW):
		BO.malloc(self, nbytes, draw_type)
		self._buffer = bytearray(b'\0'*nbytes)

	def bufferSubData(self, start:int, nbytes:int, value_array):
		if not isinstance(value_array, np.ndarray):
			value_array = np.array(value_array)

		value_bytes = value_array.tobytes()[:nbytes]
		if not self._force_upload and self._buffer[start:start+nbytes] == value_bytes:
			return

		BO.bufferSubData(self, start, nbytes, value_array)
		self._buffer[start:start+nbytes] = bytearray(value_bytes)

	@classmethod
	def makeCurrent(cls):
		current_context = GLConfig.buffered_current_context
		if cls._current_context == current_context:
			return
		cls._current_context = current_context

		for inst in cls.all_instances:
			binding_point = inst.bind_to_point()
			for block in inst._bound_block_vars:
				block.bind_to_point(binding_point)

	def upload(self, force_upload:bool=False):
		self._force_upload = force_upload

		max_size = self._get_size()
		buffer_type = self.__class__._basic_info["target_type"]
		if max_size != self.nbytes:
			self.bind()
			for binding_range, binding_point in self._binding_points.items():
				self.__class__._put_back_binding_point(binding_point)
				GL.glBindBufferRange(buffer_type, 0, self._id, binding_range[0], binding_range[1])
			self._binding_points.clear()
			self.malloc(max_size)

		for atom_name, atom_info in self._atom_info_map.items():
			atom_type = atom_info["type"]
			atom_offset = atom_info["offset"]
			atom_subscript_chain = atom_info["subscript_chain"]
			set_func = SSUBO._set_atom_func(atom_type)
			if "[{0}]" not in atom_name:
				# value = eval("self._bound_var." + atom_name)
				# eval("self._set_" + atom_type)(atom_offset, value)

				value = subscript(self._bound_var, atom_subscript_chain)
				set_func(self, atom_offset, value)
			else:
				stride = atom_info["stride"]
				for i in range(self._len_array):
					# value = eval("self._bound_var." + atom_name.format(i))
					# eval("self._set_" + atom_type)(atom_offset + i*stride, value)

					value = subscript(self._bound_var, atom_subscript_chain, i)
					set_func(self, atom_offset + i*stride, value)

		binding_point = self.bind_to_point()
		for block in self._bound_block_vars:
			block.bind_to_point(binding_point)

	@staticmethod
	def _get_atom_func(atom_type):
		SSUBO.__init_get_set_map()
		return SSUBO._get_set_atom_map[atom_type][0]
	
	@staticmethod
	def _set_atom_func(atom_type):
		SSUBO.__init_get_set_map()
		return SSUBO._get_set_atom_map[atom_type][1]

	@staticmethod
	def __init_get_set_map():
		if SSUBO._get_set_atom_map:
			return
		
		SSUBO._get_set_atom_map = \
		{
			"bool": (SSUBO._get_bool, SSUBO._set_bool),
			"int": (SSUBO._get_int, SSUBO._set_int),
			"uint": (SSUBO._get_uint, SSUBO._set_uint),
			"uint64_t": (SSUBO._get_uint64_t, SSUBO._set_uint64_t),
			"float": (SSUBO._get_float, SSUBO._set_float),
			"double": (SSUBO._get_double, SSUBO._set_double),
			"bvec2": (SSUBO._get_bvec2, SSUBO._set_bvec2),
			"bvec3": (SSUBO._get_bvec3, SSUBO._set_bvec3),
			"bvec4": (SSUBO._get_bvec4, SSUBO._set_bvec4),
			"ivec2": (SSUBO._get_ivec2, SSUBO._set_ivec2),
			"ivec3": (SSUBO._get_ivec3, SSUBO._set_ivec3),
			"ivec4": (SSUBO._get_ivec4, SSUBO._set_ivec4),
			"uvec2": (SSUBO._get_uvec2, SSUBO._set_uvec2),
			"uvec3": (SSUBO._get_uvec3, SSUBO._set_uvec3),
			"uvec4": (SSUBO._get_uvec4, SSUBO._set_uvec4),
			"vec2": (SSUBO._get_vec2, SSUBO._set_vec2),
			"vec3": (SSUBO._get_vec3, SSUBO._set_vec3),
			"vec4": (SSUBO._get_vec4, SSUBO._set_vec4),
			"dvec2": (SSUBO._get_dvec2, SSUBO._set_dvec2),
			"dvec3": (SSUBO._get_dvec3, SSUBO._set_dvec3),
			"dvec4": (SSUBO._get_dvec4, SSUBO._set_dvec4),
			"mat2": (SSUBO._get_mat2, SSUBO._set_mat2),
			"mat3x2": (SSUBO._get_mat3x2, SSUBO._set_mat3x2),
			"mat4x2": (SSUBO._get_mat4x2, SSUBO._set_mat4x2),
			"mat2x3": (SSUBO._get_mat2x3, SSUBO._set_mat2x3),
			"mat3": (SSUBO._get_mat3, SSUBO._set_mat3),
			"mat4x3": (SSUBO._get_mat4x3, SSUBO._set_mat4x3),
			"mat2x4": (SSUBO._get_mat2x4, SSUBO._set_mat2x4),
			"mat3x4": (SSUBO._get_mat3x4, SSUBO._set_mat3x4),
			"mat4": (SSUBO._get_mat4, SSUBO._set_mat4),
			"mat2x2": (SSUBO._get_mat2x2, SSUBO._set_mat2x2),
			"mat3x3": (SSUBO._get_mat3x3, SSUBO._set_mat3x3),
			"mat4x4": (SSUBO._get_mat4x4, SSUBO._set_mat4x4),
			"dmat2": (SSUBO._get_dmat2, SSUBO._set_dmat2),
			"dmat3x2": (SSUBO._get_dmat3x2, SSUBO._set_dmat3x2),
			"dmat4x2": (SSUBO._get_dmat4x2, SSUBO._set_dmat4x2),
			"dmat2x3": (SSUBO._get_dmat2x3, SSUBO._set_dmat2x3),
			"dmat3": (SSUBO._get_dmat3, SSUBO._set_dmat3),
			"dmat4x3": (SSUBO._get_dmat4x3, SSUBO._set_dmat4x3),
			"dmat2x4": (SSUBO._get_dmat2x4, SSUBO._set_dmat2x4),
			"dmat3x4": (SSUBO._get_dmat3x4, SSUBO._set_dmat3x4),
			"dmat4": (SSUBO._get_dmat4, SSUBO._set_dmat4),
			"dmat2x2": (SSUBO._get_dmat2x2, SSUBO._set_dmat2x2),
			"dmat3x3": (SSUBO._get_dmat3x3, SSUBO._set_dmat3x3),
			"dmat4x4": (SSUBO._get_dmat4x4, SSUBO._set_dmat4x4),
			"sampler2D": (SSUBO._get_sampler2D, SSUBO._set_sampler2D),
			"isampler2D": (SSUBO._get_isampler2D, SSUBO._set_isampler2D),
			"usampler2D": (SSUBO._get_usampler2D, SSUBO._set_usampler2D),
			"sampler2DMS": (SSUBO._get_sampler2DMS, SSUBO._set_sampler2DMS),
			"isampler2DMS": (SSUBO._get_isampler2DMS, SSUBO._set_isampler2DMS),
			"usampler2DMS": (SSUBO._get_usampler2DMS, SSUBO._set_usampler2DMS),
			"samplerCube": (SSUBO._get_samplerCube, SSUBO._set_samplerCube)
		}

	def _get_size(self):
		max_size = 0
		self._len_array = None
		for atom_name, atom_info in self._atom_info_map.items():
			current_type = type_from_str(atom_info["type"])
			current_size = atom_info["offset"] + sizeof(current_type)
			if "[{0}]" in atom_name:
				if self._len_array is None:
					# pos_array_end = atom_name.find("[{0}]")
					# variable_length_array = eval("self._bound_var." + atom_name[:pos_array_end])
					
					subscript_chain = atom_info["subscript_chain"]
					pos_array_end = subscript_chain.index(("getitem", "{0}"))
					variable_length_array = subscript(self._bound_var, subscript_chain[:pos_array_end])
					
					self._len_array = len(variable_length_array)
				stride = atom_info["stride"]
				current_size += capacity_of(self._len_array) * stride

			if current_size > max_size:
				max_size = current_size

		return max_size

	def _name_to_range(self, start_name:str, end_name:str):
		start_offset = self._atom_info_map[start_name]["offset"]
		end_info = self._atom_info_map[end_name]
		end_type = type_from_str(end_info["type"])
		nbytes = end_info["offset"] + sizeof(end_type) - start_offset
		if "[{0}]" in end_name:
			# pos_array_end = end_name.find("[{0}]")
			# len_array = len(eval("self._bound_var." + end_name[:pos_array_end]))

			subscript_chain = end_info["subscript_chain"]
			pos_array_end = subscript_chain.index(("getitem", "{0}"))
			variable_length_array = subscript(self._bound_var, subscript_chain[:pos_array_end])
			len_array = len(variable_length_array)

			nbytes += len_array * end_info["stride"]

		return start_offset, nbytes

	def bind_to_point(self, start:int=0, nbytes:int=None, force_bind:bool=True):
		if nbytes is None:
			nbytes = self.nbytes

		if nbytes <= 0:
			return -1

		self.bind()
		if (start, nbytes) not in self._binding_points:
			self._binding_points[start, nbytes] = self.__class__._get_binding_point()
		elif not force_bind:
			return self._binding_points[start, nbytes]
		
		binding_point = self._binding_points[start, nbytes]
		target_type = self.__class__._basic_info["target_type"]
		GL.glBindBufferRange(target_type, binding_point, self._id, start, nbytes)

		return binding_point

	def unbind_from_point(self, start:int, nbytes:int):
		if (start, nbytes) not in self._binding_points:
			return
		
		self.__class__._put_back_binding_point(self._binding_points[(start, nbytes)])
		del self._binding_points[(start, nbytes)]
		self.bind()
		GL.glBindBufferRange(self.__class__._basic_info["target_type"], 0, self._id, start, nbytes)

	def _set_bool(self, offset:int, value:bool):
		if not isinstance(value, int):
			value = int(value)

		self.bufferSubData(offset, 4, np.array([value], dtype=np.int32))

	def _set_int(self, offset:int, value:int):
		if isinstance(value, Enum):
			value = int(value.value)

		if not isinstance(value, int):
			value = int(value)

		self.bufferSubData(offset, 4, np.array([value], dtype=np.int32))

	def _set_uint(self, offset:int, value:int):
		if isinstance(value, Enum):
			value = int(value.value)

		if not isinstance(value, int):
			value = int(value)

		self.bufferSubData(offset, 4, np.array([value], dtype=np.uint32))

	def _set_uint64_t(self, offset:int, value:int):
		if not isinstance(value, int):
			value = int(value)

		self.bufferSubData(offset, 8, np.array([value], dtype=np.uint64))

	def _set_float(self, offset:int, value:float):
		if not isinstance(value, float):
			value = float(value)

		self.bufferSubData(offset, 4, np.array([value], dtype=np.float32))

	def _set_double(self, offset:int, value:float):
		if not isinstance(value, float):
			value = float(value)

		self.bufferSubData(offset, 8, np.array([value], dtype=np.float64))
	
	def _set_bvec2(self, offset:int, value:glm.bvec2):
		if not isinstance(value, glm.bvec2):
			value = glm.bvec2(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.int32))
	
	def _set_bvec3(self, offset:int, value:glm.bvec3):
		if not isinstance(value, glm.bvec3):
			value = glm.bvec3(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.int32))
	
	def _set_bvec4(self, offset:int, value:glm.bvec4):
		if not isinstance(value, glm.bvec4):
			value = glm.bvec4(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.int32))
	
	def _set_ivec2(self, offset:int, value:glm.ivec2):
		if not isinstance(value, glm.ivec2):
			value = glm.ivec2(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.int32))
	
	def _set_ivec3(self, offset:int, value:glm.ivec3):
		if not isinstance(value, glm.ivec3):
			value = glm.ivec3(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.int32))
	
	def _set_ivec4(self, offset:int, value:glm.ivec4):
		if not isinstance(value, glm.ivec4):
			value = glm.ivec4(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.int32))
	
	def _set_uvec2(self, offset:int, value:(glm.uvec2,int)):
		if isinstance(value, glm.uvec2):
			self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.uint32))
		else:
			if not isinstance(value, int):
				value = int(value)

			self.bufferSubData(offset, 8, np.array([value], dtype=np.uint64))
	
	def _set_uvec3(self, offset:int, value:glm.uvec3):
		if not isinstance(value, glm.uvec3):
			value = glm.uvec3(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.uint32))
	
	def _set_uvec4(self, offset:int, value:glm.uvec4):
		if not isinstance(value, glm.uvec4):
			value = glm.uvec4(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.uint32))
	
	def _set_vec2(self, offset:int, value:glm.vec2):
		if not isinstance(value, glm.vec2):
			value = glm.vec2(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float32))

	def _set_vec3(self, offset:int, value:glm.vec3):
		if not isinstance(value, glm.vec3):
			value = glm.vec3(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float32))
	
	def _set_vec4(self, offset:int, value:glm.vec4):
		if not isinstance(value, glm.vec4):
			value = glm.vec4(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float32))

	def _set_dvec2(self, offset:int, value:glm.dvec2):
		if not isinstance(value, glm.dvec2):
			value = glm.dvec2(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float64))

	def _set_dvec3(self, offset:int, value:glm.dvec3):
		if not isinstance(value, glm.dvec3):
			value = glm.dvec3(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float64))
	
	def _set_dvec4(self, offset:int, value:glm.dvec4):
		if not isinstance(value, glm.dvec4):
			value = glm.dvec4(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float64))
	
	def _set_mat2(self, offset:int, value:glm.mat2):
		if not isinstance(value, glm.mat2):
			value = glm.mat2(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float32))
	
	def _set_mat3x2(self, offset:int, value:glm.mat3x2):
		if not isinstance(value, glm.mat3x2):
			value = glm.mat3x2(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float32))

	def _set_mat4x2(self, offset:int, value:glm.mat4x2):
		if not isinstance(value, glm.mat4x2):
			value = glm.mat4x2(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float32))

	def _set_mat2x3(self, offset:int, value:glm.mat2x3):
		if not isinstance(value, glm.mat2x3):
			value = glm.mat2x3(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float32))
	
	def _set_mat3(self, offset:int, value:glm.mat3x3):
		if not isinstance(value, glm.mat3x3):
			value = glm.mat3x3(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float32))
	
	def _set_mat4x3(self, offset:int, value:glm.mat4x3):
		if not isinstance(value, glm.mat4x3):
			value = glm.mat4x3(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float32))
	
	def _set_mat2x4(self, offset:int, value:glm.mat2x4):
		if not isinstance(value, glm.mat2x4):
			value = glm.mat2x4(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float32))
	
	def _set_mat3x4(self, offset:int, value:glm.mat3x4):
		if not isinstance(value, glm.mat3x4):
			value = glm.mat3x4(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float32))
	
	def _set_mat4(self, offset:int, value:glm.mat4x4):
		if not isinstance(value, glm.mat4x4):
			value = glm.mat4x4(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float32))

	def _set_mat2x2(self, offset:int, value:glm.mat2x2):
		if not isinstance(value, glm.mat2x2):
			value = glm.mat2x2(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float32))

	def _set_mat3x3(self, offset:int, value:glm.mat3x3):
		if not isinstance(value, glm.mat3x3):
			value = glm.mat3x3(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float32))

	def _set_mat4x4(self, offset:int, value:glm.mat4x4):
		if not isinstance(value, glm.mat4x4):
			value = glm.mat4x4(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float32))

	def _set_dmat2(self, offset:int, value:glm.mat2x2):
		if not isinstance(value, glm.mat2x2):
			value = glm.mat2x2(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float64))
	
	def _set_dmat3x2(self, offset:int, value:glm.mat3x2):
		if not isinstance(value, glm.mat3x2):
			value = glm.mat3x2(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float64))

	def _set_dmat4x2(self, offset:int, value:glm.mat4x2):
		if not isinstance(value, glm.mat4x2):
			value = glm.mat4x2(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float64))

	def _set_dmat2x3(self, offset:int, value:glm.mat2x3):
		if not isinstance(value, glm.mat2x3):
			value = glm.mat2x3(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float64))
	
	def _set_dmat3(self, offset:int, value:glm.mat3x3):
		if not isinstance(value, glm.mat3x3):
			value = glm.mat3x3(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float64))
	
	def _set_dmat4x3(self, offset:int, value:glm.mat4x3):
		if not isinstance(value, glm.mat4x3):
			value = glm.mat4x3(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float64))
	
	def _set_dmat2x4(self, offset:int, value:glm.mat2x4):
		if not isinstance(value, glm.mat2x4):
			value = glm.mat2x4(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float64))
	
	def _set_dmat3x4(self, offset:int, value:glm.mat3x4):
		if not isinstance(value, glm.mat3x4):
			value = glm.mat3x4(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float64))
	
	def _set_dmat4(self, offset:int, value:glm.mat4x4):
		if not isinstance(value, glm.mat4x4):
			value = glm.mat4x4(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float64))

	def _set_dmat2x2(self, offset:int, value:glm.dmat2x2):
		if not isinstance(value, glm.dmat2x2):
			value = glm.dmat2x2(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float64))

	def _set_dmat3x3(self, offset:int, value:glm.dmat3x3):
		if not isinstance(value, glm.dmat3x3):
			value = glm.dmat3x3(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float64))

	def _set_dmat4x4(self, offset:int, value:glm.dmat4x4):
		if not isinstance(value, glm.dmat4x4):
			value = glm.dmat4x4(value)

		self.bufferSubData(offset, sizeof(value), np.array(value, dtype=np.float64))

	@checktype
	def _set_sampler2D(self, offset:int, value:int):
		self.bufferSubData(offset, 8, np.array(value, dtype=np.uint64))

	@checktype
	def _set_isampler2D(self, offset:int, value:int):
		self.bufferSubData(offset, 8, np.array(value, dtype=np.uint64))

	@checktype
	def _set_usampler2D(self, offset:int, value:int):
		self.bufferSubData(offset, 8, np.array(value, dtype=np.uint64))

	@checktype
	def _set_sampler2DMS(self, offset:int, value:int):
		self.bufferSubData(offset, 8, np.array(value, dtype=np.uint64))

	@checktype
	def _set_isampler2DMS(self, offset:int, value:int):
		self.bufferSubData(offset, 8, np.array(value, dtype=np.uint64))

	@checktype
	def _set_usampler2DMS(self, offset:int, value:int):
		self.bufferSubData(offset, 8, np.array(value, dtype=np.uint64))

	@checktype
	def _set_samplerCube(self, offset:int, value:int):
		self.bufferSubData(offset, 8, np.array(value, dtype=np.uint64))

	def _get_bool(self, offset:int)->bool:
		value = int.from_bytes(self._buffer[offset:offset+4], signed=False)
		return (value != 0)

	def _get_int(self, offset:int)->int:
		return int.from_bytes(self._buffer[offset:offset+4], signed=True)

	def _get_uint(self, offset:int)->int:
		return int.from_bytes(self._buffer[offset:offset+4], signed=False)
	
	def _get_uint64_t(self, offset:int)->int:
		return int.from_bytes(self._buffer[offset:offset+8], signed=False)

	def _get_float(self, offset:int)->float:
		return struct.unpack('f', self._buffer[offset:offset+4])[0]

	def _get_double(self, offset:int)->float:
		return struct.unpack('lf', self._buffer[offset:offset+4])[0]

	def _get_bvec2(self, offset:int)->glm.bvec2:
		return glm.bvec2.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.bvec2)]))

	def _get_bvec3(self, offset:int)->glm.bvec3:
		return glm.bvec3.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.bvec3)]))

	def _get_bvec4(self, offset:int)->glm.bvec4:
		return glm.bvec4.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.bvec4)]))

	def _get_ivec2(self, offset:int)->glm.ivec2:
		return glm.ivec2.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.ivec2)]))

	def _get_ivec3(self, offset:int)->glm.ivec3:
		return glm.ivec3.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.ivec3)]))

	def _get_ivec4(self, offset:int)->glm.ivec4:
		return glm.ivec4.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.ivec4)]))
	
	def _get_uvec2(self, offset:int)->glm.uvec2:
		return glm.uvec2.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.uvec2)]))
	
	def _get_uvec3(self, offset:int)->glm.uvec3:
		return glm.uvec3.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.uvec3)]))
	
	def _get_uvec4(self, offset:int)->glm.uvec4:
		return glm.uvec4.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.uvec4)]))
	
	def _get_vec2(self, offset:int)->glm.vec2:
		return glm.vec2.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.vec2)]))

	def _get_vec3(self, offset:int)->glm.vec3:
		return glm.vec3.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.vec3)]))
	
	def _get_vec4(self, offset:int)->glm.vec4:
		return glm.vec4.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.vec4)]))

	def _get_dvec2(self, offset:int)->glm.dvec2:
		return glm.dvec2.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.dvec2)]))

	def _get_dvec3(self, offset:int)->glm.dvec3:
		return glm.dvec3.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.dvec3)]))
	
	def _get_dvec4(self, offset:int)->glm.dvec4:
		return glm.dvec4.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.dvec4)]))
	
	def _get_mat2(self, offset:int)->glm.mat2x2:
		return glm.mat2.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.mat2)]))
	
	def _get_mat3x2(self, offset:int)->glm.mat3x2:
		return glm.mat3x2.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.mat3x2)]))

	def _get_mat4x2(self, offset:int)->glm.mat4x2:
		return glm.mat4x2.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.mat4x2)]))

	def _get_mat2x3(self, offset:int)->glm.mat2x3:
		return glm.mat2x3.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.mat2x3)]))
	
	def _get_mat3(self, offset:int)->glm.mat3x3:
		return glm.mat3.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.mat3)]))
	
	def _get_mat4x3(self, offset:int)->glm.mat4x3:
		return glm.mat4x3.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.mat4x3)]))
	
	def _get_mat2x4(self, offset:int)->glm.mat2x4:
		return glm.mat2x4.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.mat2x4)]))
	
	def _get_mat3x4(self, offset:int)->glm.mat3x4:
		return glm.mat3x4.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.mat3x4)]))
	
	def _get_mat4(self, offset:int)->glm.mat4x4:
		return glm.mat4.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.mat4)]))

	def _get_mat2x2(self, offset:int)->glm.mat2x2:
		return glm.mat2x2.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.mat2x2)]))

	def _get_mat3x3(self, offset:int)->glm.mat3x3:
		return glm.mat3x3.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.mat3x3)]))

	def _get_mat4x4(self, offset:int)->glm.mat4x4:
		return glm.mat4x4.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.mat4x4)]))

	def _get_dmat2(self, offset:int)->glm.mat2x2:
		return glm.dmat2.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.dmat2)]))
	
	def _get_dmat3x2(self, offset:int)->glm.mat3x2:
		return glm.dmat3x2.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.dmat3x2)]))

	def _get_dmat4x2(self, offset:int)->glm.mat4x2:
		return glm.dmat4x2.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.dmat4x2)]))

	def _get_dmat2x3(self, offset:int)->glm.mat2x3:
		return glm.dmat2x3.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.dmat2x3)]))
	
	def _get_dmat3(self, offset:int)->glm.mat3x3:
		return glm.dmat3.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.dmat3)]))
	
	def _get_dmat4x3(self, offset:int)->glm.mat4x3:
		return glm.dmat4x3.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.dmat4x3)]))
	
	def _get_dmat2x4(self, offset:int)->glm.mat2x4:
		return glm.dmat2x4.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.dmat2x4)]))
	
	def _get_dmat3x4(self, offset:int)->glm.mat3x4:
		return glm.dmat3x4.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.dmat3x4)]))
	
	def _get_dmat4(self, offset:int)->glm.mat4x4:
		return glm.dmat4.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.dmat4)]))

	def _get_dmat2x2(self, offset:int)->glm.dmat2x2:
		return glm.dmat2x2.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.dmat2x2)]))

	def _get_dmat3x3(self, offset:int)->glm.dmat3x3:
		return glm.dmat3x3.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.dmat3x3)]))

	def _get_dmat4x4(self, offset:int)->glm.dmat4x4:
		return glm.dmat4x4.from_bytes(bytes(self._buffer[offset:offset+glm.sizeof(glm.dmat4x4)]))

	def _get_sampler2D(self, offset:int)->int:
		return int.from_bytes(self._buffer[offset:offset+8], signed=False)

	def _get_isampler2D(self, offset:int)->int:
		return int.from_bytes(self._buffer[offset:offset+8], signed=False)

	def _get_usampler2D(self, offset:int)->int:
		return int.from_bytes(self._buffer[offset:offset+8], signed=False)

	def _get_sampler2DMS(self, offset:int)->int:
		return int.from_bytes(self._buffer[offset:offset+8], signed=False)

	def _get_isampler2DMS(self, offset:int)->int:
		return int.from_bytes(self._buffer[offset:offset+8], signed=False)

	def _get_usampler2DMS(self, offset:int)->int:
		return int.from_bytes(self._buffer[offset:offset+8], signed=False)

	def _get_samplerCube(self, offset:int)->int:
		return int.from_bytes(self._buffer[offset:offset+8], signed=False)