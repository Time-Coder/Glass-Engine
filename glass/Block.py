from OpenGL import GL

class Block:

	class Variable:
		def __init__(self, block, name):
			self._block = block
			self._program = self._block._program
			self._name = name
			self._bound_var = None
			self._binding_point = 0

			atom_info_list = self._block._block_map[self._name]["atoms"]
			if not atom_info_list:
				return

			pos_point = atom_info_list[0]["name"].find(".")
			self._atom_info_map = {}

			structure_key_list = []
			for atom_info in atom_info_list:
				atom_name = atom_info["name"][pos_point+1:]
				self._atom_info_map[atom_name] = atom_info
				structure_key_list.append("(" + atom_info["type"] + ", " + atom_name + ")")
			self._structure_key = ", ".join(structure_key_list)

		def bind(self, var):
			if var is self._bound_var:
				return

			if var is None:
				self.unbind()
				return

			self.unbind()

			cls = self._block.__class__
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

		def unbind(self):
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

		def __del__(self):
			try:
				self.unbind()
			except:
				pass

		def __hash__(self):
			return id(self)
		
		def __eq__(self, other):
			return (id(self) == id(other))

		def bind_to_point(self, binding_point:int)->None:
			if self._binding_point == binding_point:
				return

			cls_name = self._block.__class__.__name__
			if cls_name == "UniformBlock":
				GL.glUniformBlockBinding(self._program._id, self._block._blocks_info[self._name]["index"], binding_point)
			elif cls_name == "ShaderStorageBlock":
				GL.glShaderStorageBlockBinding(self._program._id, self._block._blocks_info[self._name]["index"], binding_point)

			self._binding_point = binding_point

		def upload(self, force_upload:bool=False):
			if self._bound_var is None:
				return

			cls = self._block.__class__
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
		self._program = program
		self._block_var_map = {}
		self._auto_upload = True

	@property
	def auto_upload(self):
		return self._auto_upload
	
	@auto_upload.setter
	def auto_upload(self, flag:bool):
		self._auto_upload = flag

	def upload(self, force_upload:bool=False):
		for block_var in self._block_var_map.values():
			block_var.upload(force_upload)

	@classmethod
	def upload_var(cls, var, force_upload:bool=False):
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
	
	def __setitem__(self, name:str, var):
		self[name].bind(var)

	@property
	def _block_map(self):
		if self.__class__.__name__ == "UniformBlock":
			return self._program._uniform_block_map
		elif self.__class__.__name__ == "ShaderStorageBlock":
			return self._program._shader_storage_block_map

	@property
	def _blocks_info(self):
		if self.__class__.__name__ == "UniformBlock":
			return self._program._uniform_blocks_info
		elif self.__class__.__name__ == "ShaderStorageBlock":
			return self._program._shader_storage_blocks_info
