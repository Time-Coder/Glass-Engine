from OpenGL import GL
import numpy as np
import re
from ctypes import c_int, pointer

from .GLObject import GLObject
from .GLInfo import GLInfo
from .GlassConfig import GlassConfig
from .GLConfig import GLConfig
from .Uniform import Uniform
from .UniformBlock import UniformBlock
from .ShaderStorageBlock import ShaderStorageBlock
from .ShaderParser import ShaderParser
from .utils import LP_LP_c_char, delete, checktype

_target_type_map = \
{
	"sampler2D": GL.GL_TEXTURE_2D,
	"isampler2D": GL.GL_TEXTURE_2D,
	"usampler2D": GL.GL_TEXTURE_2D,
	"sampler2DMS": GL.GL_TEXTURE_2D_MULTISAMPLE,
	"isampler2DMS": GL.GL_TEXTURE_2D_MULTISAMPLE,
	"usampler2DMS": GL.GL_TEXTURE_2D_MULTISAMPLE,

	"sampler2DArray": GL.GL_TEXTURE_2D_ARRAY,
	"isampler2DArray": GL.GL_TEXTURE_2D_ARRAY,
	"usampler2DArray": GL.GL_TEXTURE_2D_ARRAY,
	"sampler2DMSArray": GL.GL_TEXTURE_2D_MULTISAMPLE_ARRAY,
	"isampler2DMSArray": GL.GL_TEXTURE_2D_MULTISAMPLE_ARRAY,
	"usampler2DMSArray": GL.GL_TEXTURE_2D_MULTISAMPLE_ARRAY,

	"samplerCube": GL.GL_TEXTURE_CUBE_MAP,
	"samplerCubeArray": GL.GL_TEXTURE_CUBE_MAP_ARRAY,

	"image2D": GL.GL_TEXTURE_2D,
	"iimage2D": GL.GL_TEXTURE_2D,
	"uimage2D": GL.GL_TEXTURE_2D
}

class CompileError(Exception):
	pass

class CompileWarning(Warning):
	pass

class LinkError(Exception):
	pass

class LinkWarning(Warning):
	pass

class GPUProgram(GLObject):

	_basic_info = \
	{
		"gen_func": GL.glCreateProgram,
		"bind_func": GL.glUseProgram,
		"del_func": GL.glDeleteProgram,
		"target_type": None,
		"binding_type": GL.GL_CURRENT_PROGRAM,
		"need_number": False,
	}

	__message_prefix1 = re.compile(r"(?P<shader_type>\w+) info\n-{4,}\n0?\((?P<line_number>\d+)\) : (?P<message_type>\w+) ")
	__message_prefix2 = re.compile(r"(?P<shader_type>\w+) info\n-{4,}\n(?P<message_type>\w+): ")
	__message_prefix3 = re.compile(r"\n0?\((?P<line_number>\d+)\) : (?P<message_type>\w+) ")
	__active_program = {}

	def __init__(self):
		GLObject.__init__(self)

		self._attributes_info = {}
		self._acceptable_primitives = []
		self._uniforms_info = {}
		self._uniform_blocks_info = {}
		self._shader_storage_blocks_info = {}
		self._structs_info = {}
		self._outs_info = {}

		self._sampler_map = {}
		self._uniform_map = {}
		self._uniform_block_map = {}
		self._shader_storage_block_map = {}

		self._uniform = Uniform(self)
		self._uniform_block = UniformBlock(self)
		self._shader_storage_block = ShaderStorageBlock(self)

		self._is_linked = False
		self._linked_but_not_applied = False
		self._uniform_not_set_warning = True

	def __hash__(self):
		return id(self)
	
	def __eq__(self, other):
		return (id(self) == id(other))

	@delete
	def bind(self):
		pass
	
	@delete
	def unbind(self):
		pass
	
	@delete
	def is_bound(self):
		pass

	def __getitem__(self, name:str):
		if not self._is_linked:
			self._link()

		if name in self._uniform_map:
			return self._uniform[name]
		elif name in self._shader_storage_block_map:
			return self._shader_storage_block[name]
		elif name in self._uniform_block_map:
			return self._uniform_block[name]
		else:
			error_message = "'" + name + "' is not defined in following files:\n"
			error_message += "\n".join(self.related_files)
			raise NameError(error_message)

	def __setitem__(self, name:str, value):
		if not self._is_linked:
			self._link()

		if name in self._uniform_map:
			self._uniform[name] = value
		elif name in self._shader_storage_block_map:
			self._shader_storage_block[name] = value
		elif name in self._uniform_block_map:
			self._uniform_block[name] = value
		else:
			error_message = "'" + name + "' is not defined in following files:\n"
			error_message += "\n".join(self.related_files)
			raise NameError(error_message)
		
	def __contains__(self, name:str):
		if not self._is_linked:
			self._link()

		return (name in self._uniform_map or \
			    name in self.buffer._blocks_info or \
			    name in self.uniform_block._blocks_info)

	@property
	def uniform(self):
		if not self._is_linked:
			self._link()
			
		return self._uniform

	@property
	def uniform_block(self):
		if not self._is_linked:
			self._link()
			
		return self._uniform_block

	@property
	def buffer(self):
		if not self._is_linked:
			self._link()

		return self._shader_storage_block
	
	def download(self, var):
		id_var = id(var)
		if id_var not in ShaderStorageBlock._bound_vars:
			raise ValueError(f"{var} is not bound with any shader storage blocks")

		for block_var in self._shader_storage_block._block_var_map.values():
			if block_var._bound_var is var:
				for ssbo in ShaderStorageBlock._bound_vars[id_var].values():
					if block_var in ssbo._bound_block_vars:
						ssbo.download()

	def compile(self, shader_type, file_name=None):
		pass

	def _apply(self):
		pass

	def _link(self):
		pass

	@property
	def is_linked(self):
		return self._is_linked

	def use(self):
		if not self._is_linked:
			self._link()
		if self._linked_but_not_applied:
			self._apply()

		current_context = GLConfig.buffered_current_context
		if current_context not in GPUProgram.__active_program or \
		   GPUProgram.__active_program[current_context] != self._id:
			GL.glUseProgram(self._id)
			GPUProgram.__active_program[current_context] = self._id

	def stop_using(self):
		if not self.is_using:
			return

		GL.glUseProgram(0)

	@property
	def is_using(self):
		return (self._id != 0 and GPUProgram.active_id == self._id)
	
	@property
	def uniform_not_set_warning(self):
		return self._uniform_not_set_warning
	
	@uniform_not_set_warning.setter
	@checktype
	def uniform_not_set_warning(self, flag:bool):
		self._uniform_not_set_warning = flag

	@property
	def related_files(self):
		return []
	
	def _format_error_warning(self, message):
		used_shaders = []
		def _replace_message1(match):
			message_type = match.group("message_type")
			shader_type = match.group("shader_type")
			line_number = int(match.group('line_number'))

			used_shader = None
			if shader_type == "Vertex":
				used_shader = self.vertex_shader
			elif shader_type == "Fragment":
				used_shader = self.fragment_shader
			elif shader_type == "Geometry":
				used_shader = self.geometry_shader
			elif shader_type == "Tessellation control":
				used_shader = self.tess_ctrl_shader
			elif shader_type == "Tessellation evaluation":
				used_shader = self.tess_eval_shader
			
			if used_shader is not None:
				used_shaders.append(used_shader)
				return used_shader._line_message_map[line_number].replace("\\", "/").replace("./", "").format(message_type=message_type)
			else:
				return message_type + ": "
		
		def _replace_message2(match):
			message_type = match.group("message_type")
			return message_type + ": "
		
		def _replace_message3(match):
			message_type = match.group("message_type")
			line_number = int(match.group('line_number'))

			used_shader = None
			if used_shaders:
				used_shader = used_shaders[-1]
			
			if used_shader is not None:
				return "\n" + used_shader._line_message_map[line_number].replace("\\", "/").replace("./", "").format(message_type=message_type)

		message = GPUProgram.__message_prefix1.sub(_replace_message1, message)
		message = GPUProgram.__message_prefix2.sub(_replace_message2, message)
		message = GPUProgram.__message_prefix3.sub(_replace_message3, message)
		lines = message.split("\n")
		warning_messages = []
		error_messages = []
		last = "error"
		for line in lines:
			line = line.strip(" \t\n\r")
			if not line:
				continue

			line = line.replace("no program defined", "no 'void main()' defined")

			if "error" in line.lower():
				error_messages.append(line)
				last = "error"
			elif "warning" in line.lower():
				warning_messages.append(line)
				last = "warning"
			elif last == "error":
				error_messages.append(line)
			elif last == "warning":
				warning_messages.append(line)

		return error_messages, warning_messages

	def _resolve_one_uniform(self, var, uniform_map):
		var_type = var["type"]
		var_name = var["name"]
		var_subscript_chain = var["subscript_chain"]
		if var_type in GLInfo.atom_type_names:
			var_atoms = [var]
			var["atoms"] = var_atoms
			# var["location"] = GL.glGetUniformLocation(self._id, var["name"])
			uniform_map[var_name] = var
			return var_atoms

		if "[" in var_type:
			pos_start = var_type.find("[")
			pos_end = var_type.find("]", pos_start)
			base_type = var_type[:pos_start]
			atom_type = base_type + var_type[pos_end+1:]
			
			var_atoms = []
			if pos_end - pos_start > 1:
				num = int(var_type[pos_start+1 : pos_end])
				for i in range(num):
					atom_info = \
					{
						"name": var_name + "[" + str(i) + "]",
						"type": atom_type,
						"subscript_chain": [*var_subscript_chain, ("getitem", i)]
					}
					var_atoms.extend( self._resolve_one_uniform(atom_info, self._uniform_map) )
			else:
				atom_info = \
				{
					"name": var_name + "[{0}]",
					"type": atom_type,
					"subscript_chain": [*var_subscript_chain, ("getitem", "{0}")]
				}
				var_atoms.extend( self._resolve_one_uniform(atom_info, self._uniform_map) )
			var["atoms"] = var_atoms
			uniform_map[var_name] = var

			return var_atoms

		if GlassConfig.debug and var_type not in self._structs_info:
			raise TypeError("type " + var_type + " is not defined in shader program")

		var_atoms = []
		for member in self._structs_info[var_type]["members"].values():
			member_name = member["name"]
			uniform_info = \
			{
				"name": var_name + "." + member_name,
				"type": member["type"],
				"subscript_chain": [*var_subscript_chain, ("getattr", member_name)]
			}
			var_atoms.extend( self._resolve_one_uniform(uniform_info, self._uniform_map) )
		var["atoms"] = var_atoms
		uniform_map[var_name] = var

		return var_atoms

	def _resolve_uniforms(self):
		for uniform_info in self._uniforms_info.values():
			self._resolve_one_uniform(uniform_info, self._uniform_map)

		for uniform in self._uniform_map.values():
			for atom in uniform["atoms"]:
				atom_type = atom["type"]
				atom_name = atom["name"]
				if "sampler" in atom_type or "image" in atom_type:
					self._sampler_map[atom_name] = \
					{
						"location": -1,
						"sampler": None,
						"target_type": _target_type_map[atom_type]
					}

	def _resolve_one_uniform_block(self, block_info):
		uniform_block = {}
		block_name = block_info["name"]
		block_var_name = block_info["var_name"]
		uniform_block["name"] = block_name
		uniform_block["atoms"] = []

		for member in block_info["members"].values():
			member_name = member["name"]
			if block_var_name:
				member_name = block_var_name + "." + member_name
			uniform_info = \
			{
				"name": member_name,
				"type": member["type"],
				"subscript_chain": [("getattr", member_name)]
			}
			uniform_block["atoms"].extend( self._resolve_one_uniform(uniform_info, self._uniform_block_map) )

		self._uniform_block_map[block_name] = uniform_block
		return uniform_block["atoms"]

	def _apply_uniform_blocks(self):
		for block_name, block_info in self._uniform_blocks_info.items():
			atoms = self._uniform_block_map[block_name]["atoms"]
			len_atoms = len(atoms)
			atom_names = []
			for atom in atoms:
				atom_names.append(atom["name"])

			block_index = GL.glGetUniformBlockIndex(self._id, block_name)
			len_var_name = len(block_info["var_name"])

			block_size = np.array([0], dtype=int)
			GL.glGetActiveUniformBlockiv(self._id, block_index, GL.GL_UNIFORM_BLOCK_DATA_SIZE, block_size)
			block_size = block_size[0]
			block_info["size"] = block_size
			block_info["index"] = block_index
			
			atom_indices = np.array([0]*len_atoms, dtype=np.uint)
			GL.glGetUniformIndices(self._id, len_atoms, LP_LP_c_char(atom_names), atom_indices)
			
			atom_offsets = np.array([0]*len_atoms, dtype=int)
			GL.glGetActiveUniformsiv(self._id, len_atoms, atom_indices, GL.GL_UNIFORM_OFFSET, atom_offsets)

			array_strides = np.array([0]*len_atoms, dtype=int)
			GL.glGetActiveUniformsiv(self._id, len_atoms, atom_indices, GL.GL_UNIFORM_ARRAY_STRIDE, array_strides)

			block_members = block_info["members"]
			for atom, array_stride, atom_offset in zip(atoms, array_strides, atom_offsets):
				atom_name = atom["name"]
				member_name = ShaderParser.array_basename(atom_name)
				if len_var_name > 0:
					member_name = member_name[len_var_name+1:]

				stride = int(array_stride)
				member_type = block_members[member_name]["type"]
				offset = atom_offset + stride * ShaderParser.index_offset(member_type, atom_name)
				atom["offset"] = int(offset)
				atom["stride"] = stride

	def _resolve_uniform_blocks(self):
		for block_info in self._uniform_blocks_info.values():
			self._resolve_one_uniform_block(block_info)
		
		blocks_with_var_name = {}

		for block_name, block_info in self._uniform_blocks_info.items():
			var_name = block_info["var_name"]
			if var_name:
				blocks_with_var_name[var_name] = block_name

		for var_name, block_name in blocks_with_var_name.items():
			self._uniform_blocks_info[var_name] = self._uniform_blocks_info[block_name]
			self._uniform_block_map[var_name] = self._uniform_block_map[block_name]

		# self._apply_uniform_blocks()

	def _resolve_one_shader_storage_block(self, block_info):
		shader_storage_block = {}
		block_name = block_info["name"]
		block_var_name = block_info["var_name"]

		shader_storage_block["name"] = block_name
		shader_storage_block["atoms"] = []

		for member in block_info["members"].values():
			member_name = member["name"]
			if block_var_name:
				member_name = block_var_name + "." + member_name
			uniform_info = \
			{
				"name": member_name,
				"type": member["type"],
				"subscript_chain": [("getattr", member_name)]
			}
			shader_storage_block["atoms"].extend( self._resolve_one_uniform(uniform_info, self._shader_storage_block_map) )

		self._shader_storage_block_map[block_name] = shader_storage_block
		if block_var_name:
			self._shader_storage_block_map[block_var_name] = shader_storage_block

		return shader_storage_block["atoms"]

	def _apply_shader_storage_blocks(self):
		for block_name, block_info in self._shader_storage_blocks_info.items():
			atoms = self._shader_storage_block_map[block_name]["atoms"]

			block_index = GL.glGetProgramResourceIndex(self._id, GL.GL_SHADER_STORAGE_BLOCK, block_name)
			block_info["index"] = block_index

			block_var_name = block_info["var_name"]
			len_var_name = len(block_var_name)
			if block_var_name:
				raise ValueError("Shader Storage Block with variable name is not supported")

			props = np.array([GL.GL_OFFSET, GL.GL_ARRAY_STRIDE, GL.GL_TOP_LEVEL_ARRAY_STRIDE])
			length = c_int()
			block_members = block_info["members"]
			for atom in atoms:
				atom_offset_stride = np.array([0,0,0], dtype=np.int32)
				atom_name = re.sub(r"\[\d+\]", "[0]", atom["name"].format(0))
				atom_index = GL.glGetProgramResourceIndex(self._id, GL.GL_BUFFER_VARIABLE, atom_name)
				GL.glGetProgramResourceiv(self._id, GL.GL_BUFFER_VARIABLE, atom_index, 3, props, atom_offset_stride.nbytes, pointer(length), atom_offset_stride)
				atom_offset_stride = [int(x) for x in atom_offset_stride]

				member_name = ShaderParser.array_basename(atom_name)
				# member_name = ShaderParser.array_basename(atom["name"])
				if block_var_name:
					member_name = member_name[len_var_name+1:]
				# atom_offset = atom_offset_stride[0] + atom_offset_stride[1] * ShaderParser.index_offset(block_members[member_name]["type"], atom["name"].format(0))
				atom_offset = atom_offset_stride[0] + atom_offset_stride[1] * ShaderParser.index_offset(block_members[member_name]["type"], atom_name)
				atom_stride = min(atom_offset_stride[1], atom_offset_stride[2])
				if atom_stride == 0:
					atom_stride = max(atom_offset_stride[1], atom_offset_stride[2])

				atom["offset"] = int(atom_offset)
				atom["stride"] = int(atom_stride)

	def _resolve_shader_storage_blocks(self):
		for block_info in self._shader_storage_blocks_info.values():
			self._resolve_one_shader_storage_block(block_info)

		blocks_with_var_name = {}
		for block_name, block_info in self._shader_storage_blocks_info.items():
			var_name = block_info["var_name"]
			if var_name:
				blocks_with_var_name[var_name] = block_name

		for var_name in blocks_with_var_name:
			self._shader_storage_blocks_info[var_name] = block_info
			self._shader_storage_block_map[var_name] = self._shader_storage_block_map[block_name]

		# self._apply_shader_storage_blocks()