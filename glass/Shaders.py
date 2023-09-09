import os

from OpenGL import GL
import re
import copy
import warnings

from .utils import delete, md5s, modify_time, load_var, save_var, cat, relative_path
from .GlassConfig import GlassConfig
from .GLObject import GLObject
from .ShaderParser import ShaderParser
from .GPUProgram import CompileError, CompileWarning

class BaseShader(GLObject):

	__message_prefix1 = re.compile(r"^0\((?P<line_number>\d+)\) : (?P<message_type>\w+) ", flags=re.M)
	__message_prefix2 = re.compile(r"^(?P<message_type>\w+): 0:(?P<line_number>\d+): ", flags=re.M)
	__message_prefix3 = re.compile(r"^(?P<message_type>\w+): ([a-zA-Z]:[/\\]+)?[/\\]*([^<>:\"/\\|?*]+[/\\]+)*([^<>:\"/\\|?*]+)?:(?P<line_number>\d+): ", flags=re.M)
	_basic_info = \
	{
		"gen_func": GL.glCreateShader,
		"bind_func": None,
		"del_func": GL.glDeleteShader,
		"target_type": None,
		"binding_type": None,
		"need_number": False,
	}

	def __init__(self, shader_type):
		GLObject.__init__(self)
		self._type = shader_type
		self._code = ""
		self._clean_code = ""
		self._comments_set = set()
		self._line_message_map = {}
		self._file_name = ""
		self._include_paths = [""]
		self._predefines = {}
		self._compiled_but_not_applied = False
		self._should_recompile = True

		self.attributes_info = {}
		self.geometry_in = ""
		self.uniforms_info = {}
		self.uniform_blocks_info = {}
		self.shader_storage_blocks_info = {}
		self.structs_info = {}
		self.outs_info = {}
		self.work_group_size = tuple()
		self.related_files = []

	@delete
	def clear(self):
		pass

	@delete
	def bind(self):
		pass

	@delete
	def unbind(self):
		pass

	@delete
	def is_bound(self):
		pass

	@classmethod
	def load(cls, file_name:str, include_paths:list=None):
		if include_paths is None:
			include_paths = []
		
		if not os.path.isfile(file_name):
			raise FileNotFoundError(file_name)
		
		file_name = os.path.abspath(file_name).replace("\\", "/")
		if file_name in cls._shader_map:
			return cls._shader_map[file_name]
		else:
			shader = cls()
			for include_path in include_paths:
				shader.add_include_path(include_path)
				
			shader.compile(file_name)
			cls._shader_map[file_name] = shader
			return shader

	@property
	def type(self):
		return self._type

	@property
	def is_compiled(self):
		return bool(self._code)

	@property
	def file_name(self):
		return self._file_name

	@property
	def code(self):
		return self._code

	@property
	def clean_code(self):
		return self._clean_code

	def _apply(self):
		if not self._compiled_but_not_applied:
			return
		
		if self._id == 0:
			self._id = GL.glCreateShader(self._type)
			if self._id == 0:
				raise MemoryError("Failed to create Shader!")
			
		if GlassConfig.print:
			print(f"compiling shader: {self.file_name} ", end="", flush=True)

		GL.glShaderSource(self._id, self._code)
		GL.glCompileShader(self._id)

		message_bytes = GL.glGetShaderInfoLog(self._id)
		message = message_bytes
		if isinstance(message_bytes, bytes):
			message = str(message_bytes, encoding="utf-8")

		error_messages, warning_messages = self._format_error_warning(message)
		if warning_messages and GlassConfig.warning:
			warning_message = f"\nWarning when compiling: {self._file_name}:\n" + "\n".join(warning_messages)
			warnings.warn(warning_message, category=CompileWarning)

		if error_messages:
			error_message = f"\nError when compiling: {self._file_name}:\n" + "\n".join(error_messages)
			raise CompileError(error_message)
		
		success = GL.glGetShaderiv(self._id, GL.GL_COMPILE_STATUS)
		if success != GL.GL_TRUE:
			raise CompileError(message)
		
		meta_info = {}
		meta_info["related_files"] = self.related_files
		meta_info["code"] = self._code
		meta_info["clean_code"] = self._clean_code
		meta_info["line_message_map"] = self._line_message_map
		meta_info["attributes_info"] = self.attributes_info
		meta_info["geometry_in"] = self.geometry_in
		meta_info["uniforms_info"] = self.uniforms_info
		meta_info["uniform_blocks_info"] = self.uniform_blocks_info
		meta_info["shader_storage_blocks_info"] = self.shader_storage_blocks_info
		meta_info["structs_info"] = self.structs_info
		meta_info["outs_info"] = self.outs_info
		meta_info["work_group_size"] = self.work_group_size
		save_var(meta_info, self._meta_file_name)
		
		self._compiled_but_not_applied = False

		if GlassConfig.print:
			print("done")

	def _test_should_recompile(self):
		meta_mtime = modify_time(self._meta_file_name)
		self._max_modify_time = 0

		if meta_mtime == 0:
			self._should_recompile = True
			return True
		
		meta_info = load_var(self._meta_file_name)
		related_files = meta_info["related_files"]
		should_recompile = False
		for file_name in related_files:			
			mtime = modify_time(file_name)
			if mtime == 0 or mtime > meta_mtime:
				should_recompile = True

			if mtime > self._max_modify_time:
				self._max_modify_time = mtime

		if should_recompile:
			self._should_recompile = True
			return True
		
		self._code = meta_info["code"]
		self._clean_code = meta_info["clean_code"]
		self._line_message_map = meta_info["line_message_map"]
		self.attributes_info = meta_info["attributes_info"]
		self.geometry_in = meta_info["geometry_in"]
		self.uniforms_info = meta_info["uniforms_info"]
		self.uniform_blocks_info = meta_info["uniform_blocks_info"]
		self.shader_storage_blocks_info = meta_info["shader_storage_blocks_info"]
		self.structs_info = meta_info["structs_info"]
		self.outs_info = meta_info["outs_info"]
		self.work_group_size = meta_info["work_group_size"]
		self.related_files = related_files

		self._should_recompile = False
		return False

	def _predefine_shader_type(self):
		if self._type == GL.GL_VERTEX_SHADER:
			self.predefine("VERTEX_SHADER")
		elif self._type == GL.GL_TESS_CONTROL_SHADER:
			self.predefine("TESS_CONTROL_SHADER")
		elif self._type == GL.GL_TESS_EVALUATION_SHADER:
			self.predefine("TESS_EVALUATION_SHADER")
		elif self._type == GL.GL_GEOMETRY_SHADER:
			self.predefine("GEOMETRY_SHADER")
		elif self._type == GL.GL_FRAGMENT_SHADER:
			self.predefine("FRAGMENT_SHADER")
		elif self._type == GL.GL_COMPUTE_SHADER:
			self.predefine("COMPUTE_SHADER")

	def compile(self, file_name):
		if self.is_compiled and not self._compiled_but_not_applied:
			raise RuntimeError("compiled shader cannot compile other files")

		if not os.path.isfile(file_name):
			raise FileNotFoundError(file_name)
		
		rel_name = relative_path(file_name)
		abs_name = os.path.abspath(file_name).replace("\\", "/")
		used_name = rel_name if len(rel_name) < len(abs_name) else abs_name
		self._file_name = used_name
		base_name = os.path.basename(abs_name)
		self._meta_file_name = GlassConfig.cache_folder + "/" + base_name + "_" + md5s(abs_name) + ".meta"

		if self._test_should_recompile():
			self._code = cat(file_name)
			self.related_files = [abs_name]
			self.add_include_path(".")
			self._predefine_shader_type()
			include_path = os.path.dirname(abs_name)
			if not os.path.isabs(file_name):
				include_path = relative_path(include_path)
			self.add_include_path(include_path)
			self.related_files.extend(self._replace_includes())

			self._clean_code = ShaderParser.delete_C_comments(self._code)
			self.attributes_info = {}
			self.geometry_in = ""
			self.uniforms_info = {}
			self.uniform_blocks_info = {}
			self.shader_storage_blocks_info = {}
			self.structs_info = {}
			self.outs_info = {}
			self.work_group_size = tuple()

			

			self.uniforms_info = ShaderParser.find_uniforms(self._clean_code)
			self.uniform_blocks_info = ShaderParser.find_uniform_blocks(self._clean_code)
			self.shader_storage_blocks_info = ShaderParser.find_shader_storage_blocks(self._clean_code)
			self.structs_info = ShaderParser.find_structs(self._clean_code)

			if self._type == GL.GL_VERTEX_SHADER:
				self.attributes_info = ShaderParser.find_attributes(self._clean_code)

			if self._type == GL.GL_GEOMETRY_SHADER:
				self.geometry_in = ShaderParser.find_geometry_in(self._clean_code)

			if self._type == GL.GL_FRAGMENT_SHADER:
				self.outs_info = ShaderParser.find_outs(self._clean_code)

			if self._type == GL.GL_COMPUTE_SHADER:
				self.work_group_size = ShaderParser.find_work_group_size(self._clean_code)

		self._compiled_but_not_applied = True

	def add_include_path(self, include_path):
		self._include_paths.insert(0, include_path)

	def predefine(self, name:str, value=None):
		self._predefines[name] = value

	def _find_comments(self):
		self._comments_set.clear()
		pos_start = 0
		pos_end = 0
		should_break = False
		len_code = len(self._code)
		while True:
			pos_start = self._code.find("/*", pos_end)
			if pos_start == -1:
				break

			pos_end = self._code.find("*/", pos_start+2)
			if pos_end == -1:
				pos_end = len_code - 2
				should_break = True
			pos_end += 2

			self._comments_set.update(set(range(pos_start, pos_end)))
			if should_break:
				break

		pos_start = 0
		pos_end = 0
		should_break = False
		while True:
			pos_start = self._code.find("//", pos_end)	
			if pos_start == -1:
				break

			pos_end = self._code.find("\n", pos_start+2)

			if pos_end == -1:
				pos_end = len_code
				should_break = True

			self._comments_set.update(set(range(pos_start, pos_end)))
			if should_break:
				break

	def _replace_includes(self):
		predefine_str = ""
		for name, value in self._predefines.items():
			if value is None:
				predefine_str += f"#define {name}\n"
			else:
				predefine_str += f"#define {name} {value}\n"
		lines_of_predefine_str = ShaderParser.lines(predefine_str)
		
		len_version = len("#version")
		self._find_comments()
		pos_version = 0
		while True:
			pos_version = self._code.find("#version", pos_version)
			if pos_version == -1:
				if predefine_str:
					self._code = predefine_str + self._code
				break
			elif pos_version in self._comments_set:
				pos_version += len_version
				continue
			else:
				pos_endl = self._code.find("\n", pos_version)
				if predefine_str:
					if pos_endl == -1:
						self._code = self._code + "\n" + predefine_str
					else:
						self._code = self._code[:pos_endl+1] + predefine_str + self._code[pos_endl+1:]
				break
		line_num_version = ShaderParser.line_of(self._code, pos_version)

		pos_include_start = 0
		pos_filename_start = 0
		pos_include_end = 0
		pos_filename_end = 0
		n_lines = ShaderParser.lines(self._code)
		self._line_message_map[0] = self._file_name + ": {message_type}: "
		for i in range(1, n_lines+1):
			if i <= line_num_version:
				self._line_message_map[i] = self._file_name + ":" + str(i) + ": {message_type}: "
			elif i < line_num_version + lines_of_predefine_str:
				self._line_message_map[i] = self._file_name + ":" + str(line_num_version) + ": {message_type}: "
			else:
				self._line_message_map[i] = self._file_name + ":" + str(i-lines_of_predefine_str+1) + ": {message_type}: "

		included_files = set()
		should_find_comments = False
		len_include = len("#include")
		while True:
			if should_find_comments:
				self._find_comments()

			pos_include_start = 0
			while True:
				pos_include_start = self._code.find("#include", pos_include_start)
				if pos_include_start == -1:
					return included_files

				if pos_include_start in self._comments_set:
					pos_include_start += len_include
				else:
					break

			pos_filename_start = pos_include_start + len_include
			pos_filename_start = ShaderParser.skip_space(self._code, pos_filename_start)
			if self._code[pos_filename_start] != '<' and self._code[pos_filename_start] != '"':
				line_num = ShaderParser.line_of(self._code, pos_filename_start)
				raise CompileError("\n" + self._line_message_map[line_num].format(message_type="error") + '#include file name must be enveloped by <...> or "..."')
			
			start_char = self._code[pos_filename_start]
			end_char = ('>' if start_char == '<' else '"')
			pos_filename_start += 1
			pos_filename_start = ShaderParser.skip_space(self._code, pos_filename_start)
			pos_filename_end = self._code.find(end_char, pos_filename_start)
			if pos_filename_end == -1:
				line_num = ShaderParser.line_of(self._code, pos_filename_start)
				raise CompileError("\n" + self._line_message_map[line_num].format(message_type="error") + '#include file name must be enveloped by <...> or "..."')
			
			pos_include_end = pos_filename_end + 1
			pos_filename_end -= 1
			pos_filename_end = ShaderParser.skip_space_reverse(self._code, pos_filename_end)
			include_filename = self._code[pos_filename_start : pos_filename_end+1]
			found = False

			for include_path in self._include_paths:
				if include_path and not os.path.isdir(include_path):
					continue

				full_name = include_filename
				if include_path:
					full_name = include_path + "/" + include_filename

				if not os.path.isfile(full_name):
					continue

				rel_name = relative_path(full_name)
				abs_name = os.path.abspath(full_name).replace("\\", "/")
				used_name = rel_name if len(rel_name) < len(abs_name) else abs_name

				include_content = ""
				if abs_name not in included_files:
					include_content = cat(abs_name)
					included_files.add(abs_name)

				self._code = self._code[:pos_include_start] + include_content + self._code[pos_include_end:]
				if include_content:
					include_line_num = ShaderParser.line_of(self._code, pos_include_start)
					include_lines = ShaderParser.lines(include_content)
					include_line_end = include_line_num + include_lines
					n_lines = ShaderParser.lines(self._code)

					old_line_message_map = copy.deepcopy(self._line_message_map)
					for i in range(include_line_end, n_lines+1):
						self._line_message_map[i] = old_line_message_map[i - include_lines + 1]

					for i in range(include_line_num, include_line_end):
						self._line_message_map[i] = used_name + ":" + str(i-include_line_num+1) + ": {message_type}: "
				
					self._include_paths.insert(0, os.path.dirname(full_name))
					should_find_comments = True
				else:
					should_find_comments = False

				found = True
				break
				
			if not found:
				line_num = ShaderParser.line_of(self._code, pos_filename_start)
				raise CompileError("\n" + self._line_message_map[line_num].format(message_type="error") + f'File "{include_filename}" not exists.')

		return included_files

	def _format_error_warning(self, message):
		def _replace_message(match):
			message_type = match.group('message_type').lower()
			line_number = int(match.group('line_number'))
			return self._line_message_map[line_number].format(message_type=message_type)

		message = BaseShader.__message_prefix1.sub(_replace_message, message)
		message = BaseShader.__message_prefix2.sub(_replace_message, message)
		message = BaseShader.__message_prefix3.sub(_replace_message, message)
		message = message.replace("syntax error syntax error", "syntax error")
		message = message.strip(" \t\n\r")

		warning_messages = []
		error_messages = []
		last = ""

		lines = message.split("\n")
		for line in lines:
			line = line.strip(" \t\n\r")
			if not line:
				continue

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

class VertexShader(BaseShader):

	_shader_map = {}

	def __init__(self):
		BaseShader.__init__(self, GL.GL_VERTEX_SHADER)

class FragmentShader(BaseShader):

	_shader_map = {}

	def __init__(self):
		BaseShader.__init__(self, GL.GL_FRAGMENT_SHADER)

class GeometryShader(BaseShader):

	_shader_map = {}

	def __init__(self):
		BaseShader.__init__(self, GL.GL_GEOMETRY_SHADER)

class ComputeShader(BaseShader):

	_shader_map = {}

	def __init__(self):
		BaseShader.__init__(self, GL.GL_COMPUTE_SHADER)

class TessControlShader(BaseShader):

	_shader_map = {}

	def __init__(self):
		BaseShader.__init__(self, GL.GL_TESS_CONTROL_SHADER)

class TessEvaluationShader(BaseShader):

	_shader_map = {}

	def __init__(self):
		BaseShader.__init__(self, GL.GL_TESS_EVALUATION_SHADER)