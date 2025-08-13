from OpenGL import GL
import numpy as np
import re
from ctypes import c_int, pointer
from typing import Dict

from .GLObject import GLObject
from .Uniforms import Uniforms
from .UniformBlocks import UniformBlocks
from .ShaderStorageBlocks import ShaderStorageBlocks
from .ShaderParser import ShaderParser, Var, Attribute, Struct
from .utils import LP_LP_c_char, delete, checktype


_target_type_map = {
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
    "uimage2D": GL.GL_TEXTURE_2D,
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

    _basic_info = {
        "gen_func": GL.glCreateProgram,
        "bind_func": GL.glUseProgram,
        "del_func": GL.glDeleteProgram,
        "target_type": None,
        "binding_type": GL.GL_CURRENT_PROGRAM,
        "need_number": False,
    }

    __message_prefix1 = re.compile(
        r"(?P<shader_type>\w+) info\n-{4,}\n0?\((?P<line_number>\d+)\) : (?P<message_type>\w+) "
    )
    __message_prefix2 = re.compile(
        r"(?P<shader_type>\w+) info\n-{4,}\n(?P<message_type>\w+): "
    )
    __message_prefix3 = re.compile(
        r"\n0?\((?P<line_number>\d+)\) : (?P<message_type>\w+) "
    )

    def __init__(self):
        GLObject.__init__(self)

        self._attributes_info:Dict[str, Attribute] = {}
        self._acceptable_primitives = []
        self._structs_info:Dict[str, Struct] = {}
        self._outs_info:Dict[str, Var] = {}
        self._sampler_map = {}

        self._uniforms:Uniforms = Uniforms(self)
        self._uniform_blocks:UniformBlocks = UniformBlocks(self)
        self._shader_storage_blocks:ShaderStorageBlocks = ShaderStorageBlocks(self)

        self._is_collected:bool = False
        self._is_linked:bool = False
        self._uniform_not_set_warning:bool = True

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return id(self) == id(other)

    @delete
    def bind(self):
        pass

    @delete
    def unbind(self):
        pass

    @delete
    def is_bound(self):
        pass

    def __getitem__(self, name: str):
        self.collect_info()
        if name in self._uniforms.info:
            return self._uniforms[name]
        elif name in self._shader_storage_blocks.info:
            return self._shader_storage_blocks[name]
        elif name in self._uniform_blocks.info:
            return self._uniform_blocks[name]
        else:
            error_message = f"'{name}' is not defined in following files:\n"
            error_message += "\n".join(self.related_files)
            raise NameError(error_message)

    def __setitem__(self, name: str, value):
        self.collect_info()
        if name in self._uniforms.info:
            self._uniforms[name] = value
        elif name in self._shader_storage_blocks.info:
            self._shader_storage_blocks[name] = value
        elif name in self._uniform_blocks.info:
            self._uniform_blocks[name] = value
        else:
            error_message = f"'{name}' is not defined in following files:\n"
            error_message += "\n".join(self.related_files)
            raise NameError(error_message)

    def __contains__(self, name: str):
        self.collect_info()
        return (
            name in self._uniforms.info
            or name in self._uniform_blocks.info
            or name in self._shader_storage_blocks.info
        )

    @property
    def uniforms_info(self):
        self.collect_info()
        return self._uniforms.info

    @property
    def uniform(self):
        self.collect_info()
        return self._uniforms

    @property
    def uniform_block(self):
        self.collect_info()
        return self._uniform_blocks

    @property
    def buffer(self):
        self.collect_info()
        return self._shader_storage_blocks

    def download(self, var):
        id_var = id(var)
        if id_var not in ShaderStorageBlocks._bound_vars:
            raise ValueError(f"{var} is not bound with any shader storage blocks")

        for block_var in self._shader_storage_block._block_var_map.values():
            if block_var._bound_var is var:
                for ssbo in ShaderStorageBlocks._bound_vars[id_var].values():
                    if block_var in ssbo._bound_block_vars:
                        ssbo.download()

    def _relink(self, binary_file_name: str):
        pass

    def _link(self):
        pass

    def collect_info(self):
        pass

    def use(self):
        self.collect_info()
        self._link()

        GL.glUseProgram(self._id)

    def stop_using(self):
        if not self.is_using:
            return

        GL.glUseProgram(0)

    @property
    def is_using(self):
        return self._id != 0 and GPUProgram.active_id == self._id

    @property
    def uniform_not_set_warning(self):
        return self._uniform_not_set_warning

    @uniform_not_set_warning.setter
    @checktype
    def uniform_not_set_warning(self, flag: bool):
        self._uniform_not_set_warning = flag

    @property
    def related_files(self):
        return []

    def _format_error_warning(self, message):
        used_shaders = []

        def _replace_message1(match):
            message_type = match.group("message_type")
            shader_type = match.group("shader_type")
            line_number = int(match.group("line_number"))

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
                return (
                    used_shader._line_message_map[line_number]
                    .replace("\\", "/")
                    .replace("./", "")
                    .format(message_type=message_type)
                )
            else:
                return message_type + ": "

        def _replace_message2(match):
            message_type = match.group("message_type")
            return message_type + ": "

        def _replace_message3(match):
            message_type = match.group("message_type")
            line_number = int(match.group("line_number"))

            used_shader = None
            if used_shaders:
                used_shader = used_shaders[-1]

            if used_shader is not None:
                return "\n" + used_shader._line_message_map[line_number].replace(
                    "\\", "/"
                ).replace("./", "").format(message_type=message_type)

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

    def _resolve_uniforms(self):
        for uniform in self._uniforms.info.values():
            for atom in uniform.atoms:
                atom_type = atom.type
                atom_name = atom.name
                if "sampler" in atom_type or "image" in atom_type:
                    self._sampler_map[atom_name] = {
                        "location": -1,
                        "sampler": None,
                        "target_type": _target_type_map[atom_type],
                    }

    def _apply_uniform_blocks(self):
        backup_block_index = 0
        for block_name, block_info in self._uniform_blocks.info.items():
            atoms = self._uniform_blocks.info[block_name].atoms
            len_atoms = len(atoms)
            has_var_name = (block_info.name != block_info.type)

            atom_names = []
            for atom in atoms:
                atom_name = atom["name"]
                if has_var_name:
                    atom_name = block_name + "." + atom_name

                atom_names.append(atom_name)

            try:
                block_index = GL.glGetUniformBlockIndex(self._id, block_name)
            except GL.error.GLError:
                block_index = backup_block_index

            if block_index == 4294967295:  # -1
                raise ValueError(f"failed to get uniform block {block_name}'s index")

            block_size = np.array([0], dtype=int)
            GL.glGetActiveUniformBlockiv(
                self._id, block_index, GL.GL_UNIFORM_BLOCK_DATA_SIZE, block_size
            )
            block_size = block_size[0]
            block_info["size"] = block_size
            block_info["index"] = block_index

            atom_indices = np.array([0] * len_atoms, dtype=np.uint)
            GL.glGetUniformIndices(
                self._id, len_atoms, LP_LP_c_char(atom_names), atom_indices
            )

            for atom_name, atom_index in zip(atom_names, atom_indices):
                if atom_index == 4294967295:  # -1
                    raise ValueError(
                        f"failed to get uniform block variable {atom_name}'s index"
                    )

            atom_offsets = np.array([0] * len_atoms, dtype=int)
            GL.glGetActiveUniformsiv(
                self._id, len_atoms, atom_indices, GL.GL_UNIFORM_OFFSET, atom_offsets
            )

            array_strides = np.array([0] * len_atoms, dtype=int)
            GL.glGetActiveUniformsiv(
                self._id,
                len_atoms,
                atom_indices,
                GL.GL_UNIFORM_ARRAY_STRIDE,
                array_strides,
            )

            block_members = block_info.members
            for atom, array_stride, atom_offset in zip(
                atoms, array_strides, atom_offsets
            ):
                atom_name = atom.name
                member_name = ShaderParser.array_basename(atom_name)
                stride = int(array_stride)
                member_type = block_members[member_name].type
                offset = atom_offset + stride * ShaderParser.index_offset(
                    member_type, atom_name
                )
                atom.offset = int(offset)
                atom.stride = stride

            backup_block_index += 1

    def _apply_shader_storage_blocks(self):
        backup_block_index = 0
        for block_name, block_info in self._shader_storage_blocks.info.items():
            atoms = self._shader_storage_blocks.info[block_name].atoms

            try:
                block_index = GL.glGetProgramResourceIndex(
                    self._id, GL.GL_SHADER_STORAGE_BLOCK, block_name
                )
            except GL.error.GLError:
                block_index = backup_block_index

            if block_index == GL.GL_INVALID_INDEX:
                raise ValueError(f"failed to get {block_name} index")

            block_info.index = block_index
            has_var_name = (block_info.name != block_info.type)

            props = np.array(
                [GL.GL_OFFSET, GL.GL_ARRAY_STRIDE, GL.GL_TOP_LEVEL_ARRAY_STRIDE]
            )
            length = c_int()
            block_members = block_info.members
            for atom in atoms:
                atom_offset_stride = np.array([0, 0, 0], dtype=np.int32)
                atom_name = re.sub(r"\[\d+\]", "[0]", atom.name.format(0))
                used_atom_name = atom_name
                if has_var_name:
                    used_atom_name = block_name + "." + atom_name

                atom_index = GL.glGetProgramResourceIndex(
                    self._id, GL.GL_BUFFER_VARIABLE, used_atom_name
                )
                if atom_index == GL.GL_INVALID_INDEX:
                    raise ValueError(f"failed to get {used_atom_name} index")

                GL.glGetProgramResourceiv(
                    self._id,
                    GL.GL_BUFFER_VARIABLE,
                    atom_index,
                    3,
                    props,
                    atom_offset_stride.nbytes,
                    pointer(length),
                    atom_offset_stride,
                )
                atom_offset_stride = [int(x) for x in atom_offset_stride]

                member_name = ShaderParser.array_basename(atom_name)
                atom_offset = atom_offset_stride[0] + atom_offset_stride[
                    1
                ] * ShaderParser.index_offset(
                    block_members[member_name].type, atom_name
                )
                atom_stride = min(atom_offset_stride[1], atom_offset_stride[2])
                if atom_stride == 0:
                    atom_stride = max(atom_offset_stride[1], atom_offset_stride[2])

                atom.offset = int(atom_offset)
                atom.stride = int(atom_stride)

            backup_block_index += 1
