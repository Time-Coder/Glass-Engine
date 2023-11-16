import re
from OpenGL import GL
from .utils import has_valid
from .helper import sizeof, type_from_str
from .GLInfo import GLInfo

class ShaderParser:

	@staticmethod
	def lines(content):
		return len(content.split("\n"))

	@staticmethod
	def line_of(content, pos):
		content_size = len(content)
		size = min(content_size, pos+1)
		n_line = 1
		for i in range(size):
			if content[i] == '\n':
				n_line += 1

		return n_line

	@staticmethod
	def skip_space(content, i):
		len_content = len(content)
		if i < 0 or i >= len_content:
			return i

		while i < len_content and content[i] in ' \t\n':
			i += 1

		return i

	@staticmethod
	def skip_space_reverse(content, i):
		if i < 0 or i >= len(content):
			return i

		while i >= 0 and content[i] in ' \t\n':
			i -= 1

		return i

	@staticmethod
	def join_name(name_list):
		result = ""
		for name in name_list:
			if isinstance(name, str):
				result += ("." + name)
			elif isinstance(name, int):
				result += ("[" + str(name) + "]")
		return result

	@staticmethod
	def delete_C_comments(content:str)->str:
		result = ""
		n = len(content)
		in_str = False
		last_is_slash = False
		pos_start = 0
		i = 0
		while i < n:
			if content[i] == '"':
				last_is_slash = False
				if i-1 >= 0 and content[i-1] != '\\':
					in_str = not in_str
			elif content[i] == '/':
				if in_str:
					last_is_slash = False
					i += 1
					continue

				if last_is_slash:
					result += content[pos_start : i-1]
					last_is_slash = False
					i = content.find('\n', i)
					if i == -1:
						return result
					pos_start = i
				else:
					last_is_slash = True
			elif content[i] == '*':
				if in_str:
					last_is_slash = False
					i += 1
					continue

				if last_is_slash:
					result += content[pos_start : i-1]
					i += 1
					if i >= n:
						return result
					i = content.find("*/", i)
					if i == -1:
						return result
					i += 1
					pos_start = i + 1
				last_is_slash = False
				i += 1
				continue
			else:
				last_is_slash = False
			i += 1

		if pos_start < n:
			result += content[pos_start:]

		return re.sub(r"\\[ \t]*\n", "", result)

	@staticmethod
	def find_geometry_in(content):
		geometry_in = []
		regx = r"^\s*layout\s*\((?P<layout_qualifiers>[^\n]*?)\)\s*in\s*;"
		def append_geometry_in(match):
			layout_qualifiers = match.group("layout_qualifiers")
			args, kwargs = ShaderParser.get_layout_qualifiers(layout_qualifiers)
			acceptable_geometry_ins = ["points", "lines", "lines_adjacency", "triangles", "triangles_adjacency"]
			for arg in args:
				if arg in acceptable_geometry_ins:
					geometry_in.append(arg)
					return

		re.sub(regx, append_geometry_in, content, flags=re.M)
		
		if geometry_in:
			return geometry_in[0]
		else:
			return ""
		
	@staticmethod
	def find_attributes(content):
		attributes_info = {}
		def append_attribute(match):
			location = int(match.group("location"))
			var_type = match.group("type")
			python_type = type_from_str(var_type)
			size = sizeof(python_type)
			var_name = match.group("name")
			
			element_names = ShaderParser.resolve_array(var_name)
			for name in element_names:
				attribute = \
				{
					"name": name,
					"location": location,
					"type": var_type,
					"python_type": python_type,
					"size": size,
					"is_legacy": False
				}

				attributes_info[name] = attribute
				attributes_info[location] = attribute
				location += 1

			return ""

		def append_legacy_attribute(match):
			var_name = match.group("name")
			var_type = match.group("type")
			python_type = type_from_str(var_type)
			size = sizeof(python_type)

			if "[" in var_name:
				raise TypeError("not support attribute as array with legacy attribute format")
			
			attribute = \
			{
				"name": var_name,
				"type": var_type,
				"python_type": python_type,
				"size": size,
				"is_legacy": True
			}

			attributes_info[var_name] = attribute

			return ""

		re.sub(r"^\s*layout\s*\(\s*location\s*=\s*(?P<location>\d+)\)[\s\n]*in\s+(?P<type>[a-zA-Z_]\w*)\s+(?P<name>[a-zA-Z_]\w*(\s*\[\S+\]\s*)*)\s*;", append_attribute, content, flags=re.M)
		re.sub(r"^\s*attribute\s+(?P<type>[a-zA-Z_]\w*)\s+(?P<name>[a-zA-Z_]\w*(\s*\[\S+\]\s*)*)\s*;", append_legacy_attribute, content, flags=re.M)
		return attributes_info

	@staticmethod
	def resolve_name_type(var_name, var_type):
		pos_start = var_name.find('[')
		if pos_start == -1:
			return var_name, var_type
		var_type += var_name[pos_start:]
		return var_name[:pos_start].strip(" \t"), var_type

	@staticmethod
	def next_index(current_index, indices):
		i = -1
		try:
			while True:
				current_index[i] += 1
				if indices[i] != 0 and current_index[i] >= indices[i]:
					current_index[i] = 0
					i -= 1
				else:
					break
			return True
		except:
			return False

	@staticmethod
	def extract_array_indices(var_name):
		if "[" not in var_name:
			return []

		indices = []
		len_var_name = len(var_name)
		pos_start = len_var_name
		while True:
			pos_end = var_name.rfind("]", 0, pos_start)
			if pos_end == -1:
				break

			str_mid = var_name[pos_end+1:pos_start]
			if pos_end>=0 and pos_end < len_var_name and \
			   pos_start>=0 and pos_start < len_var_name and has_valid(str_mid):
				break

			pos_start = var_name.rfind("[", 0, pos_end)
			if pos_start == -1:
				break

			index = 0
			if pos_end - pos_start > 1:
				index = int(var_name[pos_start+1:pos_end].strip(" \t"))

			indices.insert(0, index)

		return indices

	@staticmethod
	def array_basename(name):
		pos_start = name.find("[")
		if pos_start == -1:
			return name
		else:
			return name[:pos_start].strip(" \t")

	@staticmethod
	def index_offset(total_index_str, current_index_str):
		total_index = ShaderParser.extract_array_indices(total_index_str)
		stop_index = ShaderParser.extract_array_indices(current_index_str)
		len_total_index = len(total_index)
		if len(stop_index) != len_total_index:
			raise ValueError("array should have same dimension")

		if not total_index:
			return 0

		current_index = [0]*len_total_index
		current_index[-1] = -1

		offset = 0
		while ShaderParser.next_index(current_index, total_index):
			if current_index == stop_index:
				break
			offset += 1

		return offset

	@staticmethod
	def resolve_array(var_name):
		if '[' not in var_name:
			return [var_name]
			
		indices = ShaderParser.extract_array_indices(var_name)
		base_name = ShaderParser.array_basename(var_name)

		element_names = []
		current_index = [0]*len(indices)
		current_index[-1] = -1
		while ShaderParser.next_index(current_index, indices):
			element_name = base_name
			for index in current_index:
				element_name += ("[" + str(index) + "]")
			element_names.append(element_name)

		return element_names

	@staticmethod
	def find_structs(content):
		structs_info = {}
		def append_struct(match):
			members = {}
			body = match.group("body")
			def append_member(match):
				var_name, var_type = ShaderParser.resolve_name_type(match.group("name"), match.group("type"))
				member = \
				{
					"type": var_type,
					"name": var_name
				}
				members[var_name] = member
				return ""

			re.sub(r"^\s*(?P<type>[a-zA-Z_]\w*(\s*\[\S+\]\s*)*)[\s\n]+(?P<name>[a-zA-Z_]\w*(\s*\[\S+\]\s*)*)[\s\n]*;", append_member, body, flags=re.M)
			structs_info[match.group("name")] = {"name": match.group("name"), "members": members}

		re.sub(r"^\s*struct[\s\n]+(?P<name>[a-zA-Z_]\w*)[\s\n]*\{(?P<body>.*?)\}", append_struct, content, flags=re.M|re.S)
		return structs_info

	@staticmethod
	def get_layout_qualifiers(content):
		if content is None:
			return [], {}

		items = content.split(",")
		args = []
		kwargs = {}
		for item in items:
			item = item.strip()
			if "=" in item:
				key_value = item.split("=")
				key = key_value[0].strip()
				value = key_value[1].strip()
				kwargs[key] = value
			else:
				args.append(item)

		return args, kwargs

	@staticmethod
	def get_memory_qualifiers(content):
		if content is None:
			return []

		result = []
		if "coherent" in content:
			result.append("coherent")

		if "volatile" in content:
			result.append("volatile")

		if "restrict" in content:
			result.append("restrict")

		if "readonly" in content:
			result.append("readonly")

		if "writeonly" in content:
			result.append("writeonly")

		if "readwrite" in content:
			result.append("readwrite")

		return result

	@staticmethod
	def get_internal_format(layout_args):
		for memory_qualifier, internel_format in GLInfo.memory_modifiers_to_internal_types_map.items():
			if memory_qualifier in layout_args:
				return internel_format
			
		return GL.GL_RGBA32F

	@staticmethod
	def find_uniforms(content):
		uniforms_info = {}
		atomic_offset = {}
		def append_uniform(match):
			var_name, var_type = ShaderParser.resolve_name_type(match.group("name"), match.group("type"))
			
			layout_args, layout_kwargs = [], {}
			internal_format = GL.GL_RGBA32F
			try:
				layout_qualifiers_str = match.group("layout_qualifiers")
				layout_args, layout_kwargs = ShaderParser.get_layout_qualifiers(layout_qualifiers_str)
				internal_format = ShaderParser.get_internal_format(layout_args)
			except IndexError:
				pass

			binding_point = -1
			if "binding" in layout_kwargs:
				binding_point = int(layout_kwargs["binding"])

			offset = 0
			if "offset" in layout_kwargs:
				offset = int(layout_kwargs["offset"])

			if binding_point != -1 and var_type == "atomic_uint":
				if offset == 0 and binding_point in atomic_offset:
					offset = atomic_offset[binding_point] + 4
				atomic_offset[binding_point] = offset

			memory_qualifiers = []
			try:
				memory_qualifiers_str = match.group("memory_qualifiers")
				memory_qualifiers = ShaderParser.get_memory_qualifiers(memory_qualifiers_str)
			except IndexError:
				pass

			uniforms_info[var_name] = \
			{
				"name": var_name,
				"type": var_type,
				"subscript_chain": [],
				"layout_qualifiers": (layout_args, layout_kwargs),
				"memory_qualifiers": memory_qualifiers,
				"internal_format": internal_format,
				"binding_point": binding_point,
				"offset": offset
			}
			return ""

		uniform_prefix = r"uniform[\s\n]+"
		uniform_regx = r"(?P<type>[a-zA-Z_]\w*(\s*\[\S+\]\s*)*)[\s\n]+(?P<name>[a-zA-Z_]\w*(\s*\[\S+\]\s*)*)[\s\n]*(=.*?)?;";
		layout_qualifiers_regx = r"(layout\s*\((?P<layout_qualifiers>[^\n]*?)\)[\s\n]*)?"
		memory_qualifiers_regx = r"(?P<memory_qualifiers>((coherent|volatile|restrict|readonly|writeonly|readwrite)[\s\n]+)+)?"
		re.sub(r"^\s*" + layout_qualifiers_regx + memory_qualifiers_regx + uniform_prefix + uniform_regx, append_uniform, content, flags=re.M|re.S)
		re.sub(r"^\s*" + uniform_prefix + layout_qualifiers_regx + memory_qualifiers_regx + uniform_regx, append_uniform, content, flags=re.M|re.S)
		return uniforms_info

	@staticmethod
	def find_uniform_blocks(content):
		uniform_blocks_info = {}
		def append_uniform_block(match):
			members = {}
			body = match.group("body")
			def append_member(match):
				var_name, var_type = ShaderParser.resolve_name_type(match.group("name"), match.group("type"))
				member = \
				{
					"type": var_type,
					"name": var_name
				}
				members[var_name] = member
				return ""

			re.sub(r"^\s*(?P<type>[a-zA-Z_]\w*(\s*\[\S+\]\s*)*)[\s\n]+(?P<name>[a-zA-Z_]\w*(\s*\[\S+\]\s*)*)[\s\n]*;", append_member, body, flags=re.M|re.S)
			var_name = ""
			try:
				var_name = match.group("var_name")
				if var_name is None:
					var_name = ""
			except:
				var_name = ""

			layout_args, layout_kwargs = [], {}
			internal_format = GL.GL_RGBA32F
			try:
				layout_qualifiers_str = match.group("layout_qualifiers")
				layout_args, layout_kwargs = ShaderParser.get_layout_qualifiers(layout_qualifiers_str)
				internal_format = ShaderParser.get_internal_format(layout_args)
			except IndexError:
				pass

			binding_point = -1
			if "binding" in layout_kwargs:
				binding_point = int(layout_kwargs["binding"])

			memory_qualifiers = []
			try:
				memory_qualifiers_str = match.group("memory_qualifiers")
				memory_qualifiers = ShaderParser.get_memory_qualifiers(memory_qualifiers_str)
			except IndexError:
				pass

			uniform_blocks_info[match.group("name")] = \
			{
				"name": match.group("name"),
				"members": members,
				"var_name": var_name,
				"layout_qualifiers": (layout_args, layout_kwargs),
				"memory_qualifiers": memory_qualifiers,
				"internal_format": internal_format,
				"binding_point": binding_point
			}
		
		uniform_prefix = r"uniform[\s\n]+"
		uniform_block_regx = r"(?P<name>[a-zA-Z_]\w*)[\s\n]*\{(?P<body>.*?)\}\s*((?P<var_name>[a-zA-Z_]\w*)\s*)?;"
		layout_qualifiers_regx = r"(layout\s*\((?P<layout_qualifiers>[^\n]*?)\)[\s\n]*)?"
		memory_qualifiers_regx = r"(?P<memory_qualifiers>((coherent|volatile|restrict|readonly|writeonly|readwrite)[\s\n]+)+)?"
		re.sub(r"^\s*" + layout_qualifiers_regx + memory_qualifiers_regx + uniform_prefix + uniform_block_regx, append_uniform_block, content, flags=re.M|re.S)
		re.sub(r"^\s*" + uniform_prefix + layout_qualifiers_regx + memory_qualifiers_regx + uniform_block_regx, append_uniform_block, content, flags=re.M|re.S)
		return uniform_blocks_info

	@staticmethod
	def find_shader_storage_blocks(content):
		shader_storage_blocks_info = {}
		def append_shader_storage_block(match):
			members = {}
			body = match.group("body")
			def append_member(match):
				var_name, var_type = ShaderParser.resolve_name_type(match.group("name"), match.group("type"))
				member = \
				{
					"type": var_type,
					"name": var_name
				}
				members[var_name] = member
				return ""

			re.sub(r"^\s*(?P<type>[a-zA-Z_]\w*(\s*\[.*\]\s*)*)[\s\n]+(?P<name>[a-zA-Z_]\w*(\s*\[.*\]\s*)*)[\s\n]*;", append_member, body, flags=re.M|re.S)
			var_name = ""
			try:
				var_name = match.group("var_name")
				if var_name is None:
					var_name = ""
			except:
				var_name = ""

			layout_args, layout_kwargs = [], {}
			internal_format = GL.GL_RGBA32F
			try:
				layout_qualifiers_str = match.group("layout_qualifiers")
				layout_args, layout_kwargs = ShaderParser.get_layout_qualifiers(layout_qualifiers_str)
				internal_format = ShaderParser.get_internal_format(layout_args)
			except IndexError:
				pass

			binding_point = -1
			if "binding" in layout_kwargs:
				binding_point = int(layout_kwargs["binding"])

			memory_qualifiers = []
			try:
				memory_qualifiers_str = match.group("memory_qualifiers")
				memory_qualifiers = ShaderParser.get_memory_qualifiers(memory_qualifiers_str)
			except IndexError:
				pass
			
			shader_storage_blocks_info[match.group("name")] = \
			{
				"name": match.group("name"),
				"members": members,
				"var_name": var_name,
				"layout_qualifiers": (layout_args, layout_kwargs),
				"memory_qualifiers": memory_qualifiers,
				"internal_format": internal_format,
				"binding_point": binding_point
			}
		
		buffer_prefix = r"buffer[\s\n]+"
		buffer_regx = r"(?P<name>[a-zA-Z_]\w*)[\s\n]*\{(?P<body>.*?)\}\s*((?P<var_name>[a-zA-Z_]\w*)\s*)?;"
		layout_qualifiers_regx = r"(layout\s*\((?P<layout_qualifiers>[^\n]*?)\)[\s\n]*)?"
		memory_qualifiers_regx = r"(?P<memory_qualifiers>((coherent|volatile|restrict|readonly|writeonly|readwrite)[\s\n]+)+)?"
		re.sub(r"^\s*" + layout_qualifiers_regx + memory_qualifiers_regx + buffer_prefix + buffer_regx, append_shader_storage_block, content, flags=re.M|re.S)
		re.sub(r"^\s*" + buffer_prefix + layout_qualifiers_regx + memory_qualifiers_regx + buffer_regx, append_shader_storage_block, content, flags=re.M|re.S)
		return shader_storage_blocks_info

	@staticmethod
	def find_outs(content):
		outs_info = {}
		def append_out(match):
			var_name, var_type = ShaderParser.resolve_name_type(match.group("name"), match.group("type"))
			outs_info[var_name] = {"name": var_name, "type": var_type}
			try:
				outs_info[var_name]["location"] = int(match.group("location"))
			except:
				outs_info[var_name]["location"] = 0

			return ""

		re.sub(r"^(\s*layout\s*\(\s*location\s*=\s*(?P<location>\d+)\))*[\s\n]*out[\s\n]+(?P<type>[a-zA-Z_]\w*(\s*\[\S+\]\s*)*)[\s\n]+(?P<name>[a-zA-Z_]\w*(\s*\[\S+\]\s*)*)[\s\n]*(=.*?)?;", append_out, content, flags=re.M|re.S)
		return outs_info

	@staticmethod
	def find_work_group_size(content):
		group_size = []

		def get_size3(match):
			group_size.append(int(match.group("local_size_x")))
			group_size.append(int(match.group("local_size_y")))
			group_size.append(int(match.group("local_size_z")))
			return ""

		def get_size2(match):
			group_size.append(int(match.group("local_size_x")))
			group_size.append(int(match.group("local_size_y")))
			group_size.append(1)
			return ""

		def get_size1(match):
			group_size.append(match.group("local_size_x"))
			group_size.append(1)
			group_size.append(1)
			return ""

		re.sub(r"^\s*layout\s*\(\s*local_size_x\s*=\s*(?P<local_size_x>\d+)\s*,\s*local_size_y\s*=\s*(?P<local_size_y>\d+)\s*,\s*local_size_z\s*=\s*(?P<local_size_z>\d+)\s*\)\s*in\s*;", get_size3, content, flags=re.M|re.S)
		if not group_size:
			re.sub(r"^\s*layout\s*\(\s*local_size_x\s*=\s*(?P<local_size_x>\d+)\s*,\s*local_size_y\s*=\s*(?P<local_size_y>\d+)\s*\)\s*in\s*;", get_size2, content, flags=re.M|re.S)
		
		if not group_size:
			re.sub(r"^\s*layout\s*\(\s*local_size_x\s*=\s*(?P<local_size_x>\d+)\s*\)\s*in\s*;", get_size1, content, flags=re.M|re.S)

		return tuple(group_size)