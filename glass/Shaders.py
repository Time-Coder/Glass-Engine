import os

from OpenGL import GL
import re
import warnings
import sys

from .utils import (
    defines_key,
    delete,
    md5s,
    modify_time,
    load_var,
    save_var,
    cat,
    relative_path,
    printable_path,
    printable_size,
)

from .GlassConfig import GlassConfig
from .GLConfig import GLConfig
from .GLObject import GLObject
from .ShaderParser import ShaderParser
from .GPUProgram import CompileError, CompileWarning
from .ShaderParser import ShaderParser


class BaseShader(GLObject):

    __message_prefix1 = re.compile(
        r"^0\((?P<line_number>\d+)\) : (?P<message_type>\w+) ", flags=re.M
    )
    __message_prefix2 = re.compile(
        r"^(?P<message_type>\w+): 0:(?P<line_number>\d+): ", flags=re.M
    )
    __message_prefix3 = re.compile(
        r"^(?P<message_type>\w+): ([a-zA-Z]:[/\\]+)?[/\\]*([^<>:\"/\\|?*]+[/\\]+)*([^<>:\"/\\|?*]+)?:(?P<line_number>\d+): ",
        flags=re.M,
    )
    _basic_info = {
        "gen_func": GL.glCreateShader,
        "bind_func": None,
        "del_func": GL.glDeleteShader,
        "target_type": None,
        "binding_type": None,
        "need_number": False,
    }
    _type = None

    def __init__(self, program):
        GLObject.__init__(self)
        self._program = program
        self._used_code: str = ""
        self._file_name: str = ""
        self._preprocessed_but_not_compiled: bool = False
        self._should_repreprocess: bool = True
        self._max_modify_time: int = 0

        self._include_paths: list = []
        self._defines: dict = {}
        self._shader_parser: ShaderParser = ShaderParser(self.__class__._type)

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
    def type(cls):
        return cls._type

    @property
    def is_compiled(self)->bool:
        return not self._shader_parser.is_empty

    @property
    def file_name(self)->str:
        return self._file_name

    def _apply_compile(self):
        if not self._preprocessed_but_not_compiled:
            return

        if self._id == 0:
            self._id = GL.glCreateShader(self.__class__._type)
            if self._id == 0:
                raise MemoryError("Failed to create Shader!")

        if not self._used_code:
            if not GlassConfig.debug:
                self._used_code = self._shader_parser.compress()
            else:
                self._used_code = self._shader_parser.clean_code

        version_pattern1 = r"#\s*version \d\d\d core"
        version_pattern2 = r"#\s*version \d\d\d"
        version_str = ""
        if (
            GLConfig.major_version > 3
            or GLConfig.major_version == 3
            and GLConfig.minor_version >= 3
        ):
            version_str = (
                f"#version {GLConfig.major_version}{GLConfig.minor_version}0 core"
            )
        else:
            if GLConfig.major_version == 3:
                if GLConfig.minor_version == 2:
                    version_str = "#version 150"
                elif GLConfig.minor_version == 1:
                    version_str = "#version 140"
                elif GLConfig.minor_version == 0:
                    version_str = "#version 130"
            elif GLConfig.major_version == 2:
                if GLConfig.minor_version == 1:
                    version_str = "#version 120"
                elif GLConfig.minor_version == 0:
                    version_str = "#version 110"

        if not version_str:
            raise RuntimeError(
                f"OpenGL version {GLConfig.major_version}.{GLConfig.minor_version} is not supported."
            )

        if re.search(version_pattern1, self._used_code):
            self._used_code = re.sub(version_pattern1, version_str, self._used_code)
        elif re.search(version_pattern2, self._used_code):
            self._used_code = re.sub(version_pattern2, version_str, self._used_code)

        if GlassConfig.print:
            print(
                f"compiling shader: {printable_path(self.file_name)} {printable_size(self._used_code)} ",
                end="",
                flush=True,
            )

        if GlassConfig.debug and GlassConfig.save_used_shaders:
            dest_folder = "used_shaders/" + os.path.basename(sys.argv[0])
            if not os.path.isdir(dest_folder):
                os.makedirs(dest_folder)

            out_file = open(dest_folder + "/" + os.path.basename(self.file_name), "w")
            out_file.write(self._used_code)
            out_file.close()

        GL.glShaderSource(self._id, self._used_code)
        GL.glCompileShader(self._id)

        message_bytes = GL.glGetShaderInfoLog(self._id)
        message = message_bytes
        if isinstance(message_bytes, bytes):
            message = str(message_bytes, encoding="utf-8")

        error_messages, warning_messages = self._format_error_warning(message)
        if warning_messages and GlassConfig.warning:
            warning_message = (
                f"\nWarning when compiling: {self._file_name}:\n"
                + "\n".join(warning_messages)
            )
            warnings.warn(warning_message, category=CompileWarning)

        if error_messages:
            error_message = f"\nError when compiling: {self._file_name}:\n" + "\n".join(
                error_messages
            )
            raise CompileError(error_message)

        success = GL.glGetShaderiv(self._id, GL.GL_COMPILE_STATUS)
        if success != GL.GL_TRUE:
            raise CompileError(message)

        save_var(self._shader_parser, self._shader_parser_file_name)
        self._preprocessed_but_not_compiled = False

        if GlassConfig.print:
            print("done")

    def _test_should_repreprocess(self):
        if GlassConfig.recompile:
            self._should_repreprocess = True
            return True

        meta_mtime = modify_time(self._shader_parser_file_name)
        self._max_modify_time = 0

        if meta_mtime == 0:
            self._should_repreprocess = True
            return True

        self._shader_parser = load_var(self._shader_parser_file_name)
        should_recompile = False
        for file_name in self._shader_parser.related_files:
            mtime = modify_time(file_name)
            if mtime == 0 or mtime > meta_mtime:
                should_recompile = True

            if mtime > self._max_modify_time:
                self._max_modify_time = mtime

        if should_recompile:
            self._should_repreprocess = True
            return True

        self._should_repreprocess = False
        return False

    def _define_shader_type(self):
        shader_type = self.__class__._type
        if shader_type == GL.GL_VERTEX_SHADER:
            self.define("VERTEX_SHADER")
        elif shader_type == GL.GL_TESS_CONTROL_SHADER:
            self.define("TESS_CONTROL_SHADER")
        elif shader_type == GL.GL_TESS_EVALUATION_SHADER:
            self.define("TESS_EVALUATION_SHADER")
        elif shader_type == GL.GL_GEOMETRY_SHADER:
            self.define("GEOMETRY_SHADER")
        elif shader_type == GL.GL_FRAGMENT_SHADER:
            self.define("FRAGMENT_SHADER")
        elif shader_type == GL.GL_COMPUTE_SHADER:
            self.define("COMPUTE_SHADER")

    def _collect_info(self, file_name):
        abs_name = os.path.abspath(file_name).replace("\\", "/")
        self._code = cat(abs_name)
        self._parse_code()

    def compile(self, file_name: str):
        if self.is_compiled and not self._preprocessed_but_not_compiled:
            self.delete()

        abs_name = os.path.abspath(file_name).replace("\\", "/")

        if not os.path.isfile(abs_name):
            raise FileNotFoundError(file_name)

        rel_name = relative_path(file_name)
        used_name = rel_name if len(rel_name) < len(abs_name) else abs_name
        self._file_name = used_name
        base_name = os.path.basename(abs_name)

        md5_value = md5s(f"{abs_name}{defines_key(self.defines)}")
        self._shader_parser_file_name = (
            f"{GlassConfig.cache_folder}/{base_name}_{md5_value}.parser"
        )

        if self._test_should_repreprocess():
            self._collect_info(file_name)

        self._preprocessed_but_not_compiled = True

    def add_include_path(self, include_path: str):
        full_name = os.path.abspath(include_path).replace("\\", "/")
        if self._include_paths and self._include_paths[0] == full_name:
            return False

        self._include_paths.insert(0, full_name)
        return True

    def remove_include_path(self, include_path: str):
        full_name = os.path.abspath(include_path).replace("\\", "/")
        if full_name not in self._include_paths:
            return False

        while full_name in self._include_paths:
            self._include_paths.remove(full_name)

        return True

    @property
    def include_paths(self) -> list:
        return self._include_paths + self._program.include_paths

    def define(self, name: str, value=None) -> bool:
        if name in self._defines and self._defines[name] == value:
            return False

        self._defines[name] = value
        return True

    def undef(self, name: str) -> bool:
        if name not in self._defines:
            return False

        del self._defines[name]
        return True

    @property
    def defines(self) -> dict:
        defines = {}
        program = self._program
        defines.update(program.defines)
        defines.update(self._defines)
        return defines

    def _parse_code(self):
        self._define_shader_type()
        self._shader_parser.parse(self._file_name, self._include_paths, self.defines)

    def _format_error_warning(self, message):

        def _replace_message(match):
            message_type = match.group("message_type").lower()
            line_number = int(match.group("line_number"))
            file_name = self._line_map[line_number][0]
            new_line_number = self._line_map[line_number][1]
            return file_name + ":" + str(new_line_number) + ": " + message_type + ": "

        message = BaseShader.__message_prefix1.sub(_replace_message, message)
        message = BaseShader.__message_prefix2.sub(_replace_message, message)
        message = BaseShader.__message_prefix3.sub(_replace_message, message)
        message = message.replace("syntax error syntax error", "syntax error")
        message = message.replace("'' : ", "")
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
    _type = GL.GL_VERTEX_SHADER


class FragmentShader(BaseShader):
    _type = GL.GL_FRAGMENT_SHADER


class GeometryShader(BaseShader):
    _type = GL.GL_GEOMETRY_SHADER


class ComputeShader(BaseShader):
    _type = GL.GL_COMPUTE_SHADER


class TessControlShader(BaseShader):
    _type = GL.GL_TESS_CONTROL_SHADER


class TessEvaluationShader(BaseShader):
    _type = GL.GL_TESS_EVALUATION_SHADER
