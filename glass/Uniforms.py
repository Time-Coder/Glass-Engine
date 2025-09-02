from OpenGL import GL
import OpenGL.GL.ARB.gpu_shader_int64 as gsi64
import cgmath as cgm
import copy
from enum import Enum
from typing import Union, Dict, TYPE_CHECKING

from .utils import checktype, uint64_to_uvec2
from .CustomLiteral import CustomLiteral
from .sampler2D import sampler2D
from .image2D import image2D
from .FBOAttachment import FBOAttachment
from .usampler2D import usampler2D
from .isampler2D import isampler2D
from .uimage2D import uimage2D
from .iimage2D import iimage2D
from .sampler2DMS import sampler2DMS
from .isampler2DMS import isampler2DMS
from .usampler2DMS import usampler2DMS
from .samplerCube import samplerCube
from .sampler2DArray import sampler2DArray
from .ACBO import ACBO
from .GlassConfig import GlassConfig
from .UniformVar import UniformVar
from .ShaderParser import ShaderParser, SimpleVar, Var

if TYPE_CHECKING:
    from .ShaderProgram import ShaderProgram


class Uniforms:

    _set_atom_map = {}

    def __init__(self, shader_program:ShaderProgram):
        self._program:ShaderProgram = shader_program
        self.info:Dict[str, Var] = {}
        self.descendants:Dict[str, Var] = {}

        self._atoms_to_update = {}
        self._uniform_var_map:Dict[str, UniformVar] = {}
        self._texture_value_map = {}
        self._current_atom_name:str = ""

    @property
    def program(self)->ShaderProgram:
        return self._program
    
    def update_info(self, info:Dict[str, Var])->None:
        for var in info.values():
            self.descendants[var.name] = var
            self.descendants.update(var.descendants)

        self.info.update(info)

    def clear(self):
        self.info.clear()
        self.descendants.clear()
        self._atoms_to_update.clear()
        self._uniform_var_map.clear()
        self._texture_value_map.clear()
        self._current_atom_name:str = ""

    def __getitem__(self, name: str):
        program = self.program
        if GlassConfig.debug and name not in self.descendants:
            error_message = (
                f"uniform variable '{name}' is not defined in following files:\n"
            )
            error_message += "\n".join(program.related_files)
            raise NameError(error_message)

        if name not in self._uniform_var_map:
            self._uniform_var_map[name] = UniformVar(self, self.descendants[name])

        return self._uniform_var_map[name]

    def __setitem__(self, name: str, value):
        program = self.program
        if GlassConfig.debug and name not in self.descendants:
            error_message = (
                f"uniform variable '{name}' is not defined in following files:\n"
            )
            error_message += "\n".join(program.related_files)
            raise NameError(error_message)

        for atom in self.descendants[name].atoms:
            atom_value = ShaderParser.access(value, atom.access_chain)
            self._set_atom(atom, atom_value)

    @checktype
    def __contains__(self, name: str):
        return name in self.descendants

    @staticmethod
    def _copy(value):
        type_str = type(value).__name__
        if value is None or "sampler" in type_str or "image" in type_str:
            return value
        else:
            return copy.copy(value)

    def _set_atom(self, atom_info: SimpleVar, value):
        name:str = atom_info.name
        if GL.glGetUniformLocation:
            program = self.program
            program.use()

            atom_type = atom_info.type
            if atom_type != "atomic_uint":
                location = -1
                if atom_info.location == -2:
                    location = GL.glGetUniformLocation(program._id, name)
                    atom_info.location = location
                else:
                    location = atom_info.location

                if location == -1:
                    return

                self._current_atom_name = name
                func = getattr(self, "_set_" + atom_type)
                func(location, value)
            else:
                binding_point = atom_info.binding_point
                offset = atom_info.offset
                ACBO.set(binding=binding_point, offset=offset, value=value)
        else:
            self._atoms_to_update[name] = Uniforms._copy(value)

    def _set_bool(self, location: int, value):
        if not isinstance(value, int):
            value = int(value)

        GL.glUniform1i(location, value)

    def _set_int(self, location: int, value):
        if isinstance(value, Enum):
            value = int(value.value)

        if not isinstance(value, int):
            value = int(value)

        GL.glUniform1i(location, value)

    def _set_uint(self, location: int, value):
        if isinstance(value, Enum):
            value = int(value.value)

        if not isinstance(value, int):
            value = int(value)

        GL.glUniform1ui(location, value)

    def _set_uint64_t(self, location: int, value):
        if not isinstance(value, int):
            value = int(value)

        gsi64.glUniform1ui64ARB(location, value)

    def _set_float(self, location: int, value):
        if not isinstance(value, float):
            value = float(value)

        GL.glUniform1f(location, value)

    def _set_double(self, location: int, value):
        if not isinstance(value, float):
            value = float(value)

        GL.glUniform1d(location, value)

    def _set_bvec2(self, location: int, value: cgm.bvec2):
        if not isinstance(value, cgm.bvec2):
            value = cgm.bvec2(value)

        GL.glUniform2i(location, int(value.x), int(value.y))

    def _set_bvec3(self, location: int, value: cgm.bvec3):
        if not isinstance(value, cgm.bvec3):
            value = cgm.bvec3(value)

        GL.glUniform3i(location, int(value.x), int(value.y), int(value.z))

    def _set_bvec4(self, location: int, value: cgm.bvec4):
        if not isinstance(value, cgm.bvec4):
            value = cgm.bvec4(value)

        GL.glUniform4i(location, int(value.x), int(value.y), int(value.z), int(value.w))

    def _set_ivec2(self, location: int, value: cgm.ivec2):
        if not isinstance(value, cgm.ivec2):
            value = cgm.ivec2(value)

        GL.glUniform2i(location, value.x, value.y)

    def _set_ivec3(self, location: int, value: cgm.ivec3):
        if not isinstance(value, cgm.ivec3):
            value = cgm.ivec3(value)

        GL.glUniform3i(location, value.x, value.y, value.z)

    def _set_ivec4(self, location: int, value: cgm.ivec4):
        if not isinstance(value, cgm.ivec4):
            value = cgm.ivec4(value)

        GL.glUniform4i(location, value.x, value.y, value.z, value.w)

    def _set_uvec2(self, location: int, value: Union[cgm.uvec2, int]):
        if isinstance(value, cgm.uvec2):
            GL.glUniform2ui(location, value.x, value.y)
        else:
            if not isinstance(value, int):
                value = int(value)

            used_value = uint64_to_uvec2(value)
            GL.glUniform2ui(location, used_value.x, used_value.y)

    def _set_uvec3(self, location: int, value: cgm.uvec3):
        if not isinstance(value, cgm.uvec3):
            value = cgm.uvec3(value)

        GL.glUniform3ui(location, value.x, value.y, value.z)

    def _set_uvec4(self, location: int, value: cgm.uvec4):
        if not isinstance(value, cgm.uvec4):
            value = cgm.uvec4(value)

        GL.glUniform4ui(location, value.x, value.y, value.z, value.w)

    def _set_vec2(self, location: int, value: cgm.vec2):
        if not isinstance(value, cgm.vec2):
            value = cgm.vec2(value)

        GL.glUniform2f(location, value.x, value.y)

    def _set_vec3(self, location: int, value: cgm.vec3):
        if not isinstance(value, cgm.vec3):
            value = cgm.vec3(value)

        GL.glUniform3f(location, value.x, value.y, value.z)

    def _set_vec4(self, location: int, value: cgm.vec4):
        if not isinstance(value, cgm.vec4):
            value = cgm.vec4(value)

        GL.glUniform4f(location, value.x, value.y, value.z, value.w)

    def _set_dvec2(self, location: int, value: cgm.dvec2):
        if not isinstance(value, cgm.dvec2):
            value = cgm.dvec2(value)

        GL.glUniform2d(location, value.x, value.y)

    def _set_dvec3(self, location: int, value: cgm.dvec3):
        if not isinstance(value, cgm.dvec3):
            value = cgm.dvec3(value)

        GL.glUniform3d(location, value.x, value.y, value.z)

    def _set_dvec4(self, location: int, value: cgm.dvec4):
        if not isinstance(value, cgm.dvec4):
            value = cgm.dvec4(value)

        GL.glUniform4d(location, value.x, value.y, value.z, value.w)

    def _set_mat2(self, location: int, value: cgm.mat2):
        if not isinstance(value, cgm.mat2):
            value = cgm.mat2(value)

        GL.glUniformMatrix2fv(location, 1, False, cgm.value_ptr(value))

    def _set_mat3x2(self, location: int, value: cgm.mat3x2):
        if not isinstance(value, cgm.mat3x2):
            value = cgm.mat3x2(value)

        GL.glUniformMatrix3x2fv(location, 1, False, cgm.value_ptr(value))

    def _set_mat4x2(self, location: int, value: cgm.mat4x2):
        if not isinstance(value, cgm.mat4x2):
            value = cgm.mat4x2(value)

        GL.glUniformMatrix4x2fv(location, 1, False, cgm.value_ptr(value))

    def _set_mat2x3(self, location: int, value: cgm.mat2x3):
        if not isinstance(value, cgm.mat2x3):
            value = cgm.mat2x3(value)

        GL.glUniformMatrix2x3fv(location, 1, False, cgm.value_ptr(value))

    def _set_mat3(self, location: int, value: cgm.mat3x3):
        if not isinstance(value, cgm.mat3x3):
            value = cgm.mat3x3(value)

        GL.glUniformMatrix3fv(location, 1, False, cgm.value_ptr(value))

    def _set_mat4x3(self, location: int, value: cgm.mat4x3):
        if not isinstance(value, cgm.mat4x3):
            value = cgm.mat4x3(value)

        GL.glUniformMatrix4x3fv(location, 1, False, cgm.value_ptr(value))

    def _set_mat2x4(self, location: int, value: cgm.mat2x4):
        if not isinstance(value, cgm.mat2x4):
            value = cgm.mat2x4(value)

        GL.glUniformMatrix2x4fv(location, 1, False, cgm.value_ptr(value))

    def _set_mat3x4(self, location: int, value: cgm.mat3x4):
        if not isinstance(value, cgm.mat3x4):
            value = cgm.mat3x4(value)

        GL.glUniformMatrix3x4fv(location, 1, False, cgm.value_ptr(value))

    def _set_mat4(self, location: int, value: cgm.mat4x4):
        if not isinstance(value, cgm.mat4x4):
            value = cgm.mat4x4(value)

        GL.glUniformMatrix4fv(location, 1, False, cgm.value_ptr(value))

    def _set_mat2x2(self, location: int, value: cgm.mat2x2):
        if not isinstance(value, cgm.mat2x2):
            value = cgm.mat2x2(value)

        GL.glUniformMatrix2fv(location, 1, False, cgm.value_ptr(value))

    def _set_mat3x3(self, location: int, value: cgm.mat3x3):
        if not isinstance(value, cgm.mat3x3):
            value = cgm.mat3x3(value)

        GL.glUniformMatrix3fv(location, 1, False, cgm.value_ptr(value))

    def _set_mat4x4(self, location: int, value: cgm.mat4x4):
        if not isinstance(value, cgm.mat4x4):
            value = cgm.mat4x4(value)

        GL.glUniformMatrix4fv(location, 1, False, cgm.value_ptr(value))

    def _set_dmat2(self, location: int, value: cgm.dmat2):
        if not isinstance(value, cgm.dmat2):
            value = cgm.dmat2(value)

        GL.glUniformMatrix2dv(location, 1, False, cgm.value_ptr(value))

    def _set_dmat3x2(self, location: int, value: cgm.dmat3x2):
        if not isinstance(value, cgm.dmat3x2):
            value = cgm.dmat3x2(value)

        GL.glUniformMatrix3x2dv(location, 1, False, cgm.value_ptr(value))

    def _set_dmat4x2(self, location: int, value: cgm.dmat4x2):
        if not isinstance(value, cgm.dmat4x2):
            value = cgm.dmat4x2(value)

        GL.glUniformMatrix4x2dv(location, 1, False, cgm.value_ptr(value))

    def _set_dmat2x3(self, location: int, value: cgm.dmat2x3):
        if not isinstance(value, cgm.dmat2x3):
            value = cgm.dmat2x3(value)

        GL.glUniformMatrix2x3dv(location, 1, False, cgm.value_ptr(value))

    def _set_dmat3(self, location: int, value: cgm.dmat3x3):
        if not isinstance(value, cgm.dmat3x3):
            value = cgm.dmat3x3(value)

        GL.glUniformMatrix3dv(location, 1, False, cgm.value_ptr(value))

    def _set_dmat4x3(self, location: int, value: cgm.dmat4x3):
        if not isinstance(value, cgm.dmat4x3):
            value = cgm.dmat4x3(value)

        GL.glUniformMatrix4x3dv(location, 1, False, cgm.value_ptr(value))

    def _set_dmat2x4(self, location: int, value: cgm.dmat2x4):
        if not isinstance(value, cgm.dmat2x4):
            value = cgm.dmat2x4(value)

        GL.glUniformMatrix2x4dv(location, 1, False, cgm.value_ptr(value))

    def _set_dmat3x4(self, location: int, value: cgm.dmat3x4):
        if not isinstance(value, cgm.dmat3x4):
            value = cgm.dmat3x4(value)

        GL.glUniformMatrix3x4dv(location, 1, False, cgm.value_ptr(value))

    def _set_dmat4(self, location: int, value: cgm.dmat4):
        if not isinstance(value, cgm.dmat4):
            value = cgm.dmat4(value)

        GL.glUniformMatrix4dv(location, 1, False, cgm.value_ptr(value))

    def _set_dmat2x2(self, location: int, value: cgm.dmat2x2):
        if not isinstance(value, cgm.dmat2x2):
            value = cgm.dmat2x2(value)

        GL.glUniformMatrix2dv(location, 1, False, cgm.value_ptr(value))

    def _set_dmat3x3(self, location: int, value: cgm.dmat3x3):
        if not isinstance(value, cgm.dmat3x3):
            value = cgm.dmat3x3(value)

        GL.glUniformMatrix3dv(location, 1, False, cgm.value_ptr(value))

    def _set_dmat4x4(self, location: int, value: cgm.dmat4x4):
        if not isinstance(value, cgm.dmat4x4):
            value = cgm.dmat4x4(value)

        GL.glUniformMatrix4dv(location, 1, False, cgm.value_ptr(value))

    @checktype
    def _set_sampler2D(
        self,
        location: int,
        value: Union[sampler2D, str],
        sampler_type: CustomLiteral[sampler2D, isampler2D, usampler2D] = sampler2D,
    ):
        if isinstance(value, str):
            value = sampler_type.load(value)

        if value is not None:
            value.bind()

        program = self.program
        program._sampler_map[self._current_atom_name]["location"] = location
        program._sampler_map[self._current_atom_name]["sampler"] = value

    @checktype
    def _set_isampler2D(self, location: int, value: Union[isampler2D, str]):
        self._set_sampler2D(location, value, isampler2D)

    @checktype
    def _set_usampler2D(self, location: int, value: Union[usampler2D, str]):
        self._set_sampler2D(location, value, usampler2D)

    @checktype
    def _set_sampler2DMS(self, location: int, value: sampler2DMS):
        if value is not None:
            value.bind()

        program = self.program
        program._sampler_map[self._current_atom_name]["location"] = location
        program._sampler_map[self._current_atom_name]["sampler"] = value

    @checktype
    def _set_isampler2DMS(self, location: int, value: isampler2DMS):
        self._set_sampler2DMS(location, value)

    @checktype
    def _set_usampler2DMS(self, location: int, value: usampler2DMS):
        self._set_sampler2DMS(location, value)

    @checktype
    def _set_sampler2DArray(self, location: int, value: sampler2DArray):
        if value is not None:
            value.bind()

        program = self.program
        program._sampler_map[self._current_atom_name]["location"] = location
        program._sampler_map[self._current_atom_name]["sampler"] = value

    def __set_general_image2D(
        self,
        location: int,
        value: Union[image2D, iimage2D, uimage2D, str],
        image_type: CustomLiteral[image2D, iimage2D, uimage2D] = image2D,
    ):
        internal_format = self.descendants[self._current_atom_name].internal_format
        if isinstance(value, str):
            value = image_type.load(
                value, internal_format=internal_format
            )

        program = self.program
        access_mode = self.descendants[self._current_atom_name].access_mode
        if value is not None:
            if GlassConfig.debug and internal_format is not None and internal_format != value.internal_format:
                raise ValueError(
                    f"uniform image2D {self._current_atom_name} need format {internal_format}, {value.internal_format} were given"
                )

            value.bind()

        program._sampler_map[self._current_atom_name]["location"] = location
        program._sampler_map[self._current_atom_name]["access"] = access_mode
        program._sampler_map[self._current_atom_name]["sampler"] = value

    @checktype
    def _set_iimage2D(self, location: int, value: Union[iimage2D, str]):
        self.__set_general_image2D(location, value, image_type=iimage2D)

    @checktype
    def _set_uimage2D(self, location: int, value: Union[uimage2D, str]):
        self.__set_general_image2D(location, value, image_type=uimage2D)

    @checktype
    def _set_image2D(self, location: int, value: Union[image2D, str]):
        self.__set_general_image2D(location, value, image_type=image2D)

    @checktype
    def _set_samplerCube(self, location: int, value: samplerCube):
        if value is not None and not value.is_completed:
            raise RuntimeError("not completed samplerCube")

        if value is not None:
            value.bind()

        program = self.program
        program._sampler_map[self._current_atom_name]["sampler"] = value
        program._sampler_map[self._current_atom_name]["location"] = location
