from OpenGL import GL
from .utils import di

class Block:

	class Variable:
		def __init__(self, block, name:str)->None:
			self._block_id:int = id(block)
			self._name:str = name
			self._bound_var:object = None
			self._binding_point:int = 0

			atom_info_list = block._block_map[self._name]["atoms"]
			if not atom_info_list:
				return

			self._atom_info_map = {}

			structure_key_list = []
			for atom_info in atom_info_list:
				atom_name = atom_info["name"]
				self._atom_info_map[atom_name] = atom_info
				structure_key_list.append("(" + atom_info["type"] + ", " + atom_name + ")")
			self._structure_key:str = ", ".join(structure_key_list)

		@property
		def block(self):
			return di(self._block_id)

		def bind(self, var:object)->None:
			if var is self._bound_var:
				return

			if var is None:
				self.unbind()
				return

			self.unbind()

			cls = self.block.__class__
			id_var = id(var)
			if id_var not in cls._bound_vars:
				cls._bound_vars[id_var] = {}

			if self._structure_key not in cls._bound_vars[id_var]:
				ssubo = cls.BO()
				ssubo._bound_var = var
				cls._bound_vars[id_var][self._structure_key] = ssubo
			ssubo = cls._bound_vars[id_var][self._structure_key]

			ssubo._atom_info_map = self._atom_info_map
			ssubo._bound_block_vars.add(self)

			self._bound_var = var

		def unbind(self)->None:
			if self._bound_var is None:
				return

			id_var = id(self._bound_var)
			cls = self._block.__class__
			
			if id_var not in cls._bound_vars or \
			   self._structure_key not in cls._bound_vars[id_var]:
				return

			ssubo = cls._bound_vars[id_var][self._structure_key]
			if self in ssubo._bound_block_vars:
				ssubo._bound_block_vars.remove(self)
			if not ssubo._bound_block_vars:
				ssubo.unbind_from_point()

			self._bound_var = None

		def binding_point(self)->int:
			return self._binding_point

		def __del__(self)->None:
			try:
				self.unbind()
			except:
				pass

		def __hash__(self)->int:
			return id(self)
		
		def __eq__(self, other)->bool:
			return (id(self) == id(other))

		def bind_to_point(self, binding_point:int)->None:
			if binding_point < 0:
				return

			if self._binding_point == binding_point:
				return

			block = self.block
			cls_name = block.__class__.__name__
			if cls_name == "UniformBlock":
				GL.glUniformBlockBinding(block.program.id, block._blocks_info[self._name]["index"], binding_point)
			elif cls_name == "ShaderStorageBlock":
				GL.glShaderStorageBlockBinding(block.program.id, block._blocks_info[self._name]["index"], binding_point)

			self._binding_point = binding_point

		def upload(self, force_upload:bool=False)->None:
			if self._bound_var is None:
				return

			cls = self.block.__class__
			id_var = id(self._bound_var)
			if id_var not in cls._bound_vars:
				return

			if self._structure_key not in cls._bound_vars[id_var]:
				return

			ssubo = cls._bound_vars[id_var][self._structure_key]
			assert self in ssubo._bound_block_vars

			if force_upload:
				ssubo.upload(force_upload)
			elif hasattr(self._bound_var, "upload"):
				self._bound_var.upload()

			binding_point = ssubo.bind_to_point(force_bind=False)
			self.bind_to_point(binding_point)

	def __init__(self, program):
		self._program_id = id(program)
		self._block_var_map = {}
		self._auto_upload = True

	@property
	def program(self):
		return di(self._program_id)

	@property
	def auto_upload(self)->bool:
		return self._auto_upload
	
	@auto_upload.setter
	def auto_upload(self, flag:bool)->None:
		self._auto_upload = flag

	def upload(self, force_upload:bool=False)->None:
		for block_var in self._block_var_map.values():
			block_var.upload(force_upload)

	@classmethod
	def upload_var(cls, var:object, force_upload:bool=False)->None:
		id_var = id(var)
		if id_var not in cls._bound_vars:
			return

		for ssubo in cls._bound_vars[id_var].values():
			ssubo.upload(force_upload)

	def __contains__(self, name:str)->bool:
		return (name in self._blocks_info)

	def __getitem__(self, name:str)->Variable:
		if name not in self._blocks_info:
			raise NameError(f"block '{name}' is not defined")

		if name not in self._block_var_map:
			self._block_var_map[name] = Block.Variable(self, name)

		return self._block_var_map[name]
	
	def __setitem__(self, name:str, var:object)->None:
		self[name].bind(var)

	@property
	def _block_map(self):
		if self.__class__.__name__ == "UniformBlock":
			return self.program._uniform_block_map
		elif self.__class__.__name__ == "ShaderStorageBlock":
			return self.program._shader_storage_block_map

	@property
	def _blocks_info(self):
		if self.__class__.__name__ == "UniformBlock":
			return self.program._uniform_blocks_info
		elif self.__class__.__name__ == "ShaderStorageBlock":
			return self.program._shader_storage_blocks_info
