from OpenGL import GL
import OpenGL.GL.ARB.gpu_shader_int64 as gsi64
import glm
import copy
from enum import Enum

from .utils import checktype, get_subscript_chain, uint64_to_uvec2, di
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
from .utils import subscript

class Uniform:
    
    _bound_vars = {}
    # {
    #     "<id_normal_var>":
    #     {
    #         "<atom_name>":
    #         {
    #             "suffix": "<suffix>"
    #             "uniforms": set()
    #         }
    #     }
    # }

    _set_atom_map = {}

    class Variable:
        _all_attrs = {"__init__", "__getitem__", "__setitem__", "__getattr__", "__setattr__",
                      "_uniform_id", "_name", "_bound_var",
                      "bind", "unbind", "location"}

        def __init__(self, uniform_id, name):
            self._uniform_id = uniform_id
            self._name = name
            self._bound_var = None

        @property
        def uniform(self):
            return di(self._uniform_id)

        def __del__(self):
            self.unbind()

        def __hash__(self):
            return id(self)
        
        def __eq__(self, other):
            return (id(self) == id(other))

        @property
        def location(self):
            program = self.uniform.program
            if "location" not in program._uniform_map[self._name]:
                program.use()
                location = GL.glGetUniformLocation(program._id, self._name)
                program._uniform_map[self._name]["location"] = location
                return location
            else:
                return program._uniform_map[self._name]["location"]

        def bind(self, var):
            if var is self._bound_var:
                return

            if var is None:
                self.unbind()
                return

            if isinstance(var, (bool, int, float)):
                raise ValueError("cannot bind to " + var.__class__.__name__ + " value")

            self.unbind()

            id_var = id(var)
            if id_var not in Uniform._bound_vars:
                Uniform._bound_vars[id_var] = {}

            len_name = len(self._name)
            for atom in self.uniform.program._uniform_map[self._name]["atoms"]:
                atom_name = atom["name"]
                atom_suffix = atom["name"][len_name:]
                subscript_chain = get_subscript_chain(atom_suffix)
                subscript(var, subscript_chain)
                if atom_name not in Uniform._bound_vars[id_var]:
                    Uniform._bound_vars[id_var][atom_name] = {}

                atom_info = Uniform._bound_vars[id_var][atom_name]
                atom_info["suffix"] = atom_suffix
                atom_info["subscript_chain"] = subscript_chain
                if "uniforms" not in atom_info:
                    atom_info["uniforms"] = set()
                atom_info["uniforms"].add(self._uniform_id)

            self._bound_var = var

        def unbind(self):
            if self._bound_var is None:
                return

            id_var = id(self._bound_var)
            if id_var in Uniform._bound_vars:
                var_info = Uniform._bound_vars[id_var]
                should_remove_atoms = []
                for atom_name, info in var_info.items():
                    if self._uniform_id in info["uniforms"]:
                        info["uniforms"].remove(self._uniform_id)
                    if not info["uniforms"]:
                        should_remove_atoms.append(atom_name)
                for atom_name in should_remove_atoms:
                    del var_info[atom_name]
                if not var_info:
                    del Uniform._bound_vars[id_var]
            
            self._bound_var = None

        def __contains__(self, name:(str, int)):
            full_name = self._name
            if isinstance(name, str):
                full_name += ("." + name)
            elif isinstance(name, int):
                full_name += "[" + str(name) + "]"

            return (full_name in self.uniform.program._uniform_map)

        def __getitem__(self, name:(str, int)):
            full_name = self._name
            if isinstance(name, str):
                full_name += ("." + name)
            elif isinstance(name, int):
                full_name += "[" + str(name) + "]"

            uniform = self.uniform
            program = uniform.program
            if GlassConfig.debug and full_name not in program._uniform_map:
                error_message = "uniform variable '" + full_name + "' is not defined in following files:\n"
                error_message += "\n".join(program.related_files)
                raise NameError(error_message)
            
            if full_name not in uniform._uniform_var_map:
                uniform._uniform_var_map[full_name] = Uniform.Variable(self._uniform_id, full_name)

            return uniform._uniform_var_map[full_name]

        @checktype
        def __setitem__(self, name:(str, int), value):
            full_name = self._name
            if isinstance(name, str):
                full_name += ("." + name)
            elif isinstance(name, int):
                full_name += "[" + str(name) + "]"

            uniform = self.uniform
            program = uniform.program
            if GlassConfig.debug and full_name not in program._uniform_map:
                error_message = "uniform variable '" + full_name + "' is not defined in following files:\n"
                error_message += "\n".join(program.related_files)
                raise NameError(error_message)

            uniform[full_name] = value

        def __getattr__(self, name:str):
            if name in Uniform.Variable._all_attrs:
                return super().__getattr__(name)

            return self.__getitem__(name)

        def __setattr__(self, name:str, value):
            if name in Uniform.Variable._all_attrs:
                return super().__setattr__(name, value)

            self.__setitem__(name, value)

    def __init__(self, shader_program):
        self._program_id = id(shader_program)
        self._atoms_to_update = {}
        self._uniform_var_map = {}
        self._atom_value_map = {}
        self._texture_value_map = {}
        self._current_atom_name = ""

    @property
    def program(self):
        return di(self._program_id)

    def __getitem__(self, name:str):
        program = self.program
        if GlassConfig.debug and name not in program._uniform_map:
            error_message = f"uniform variable '{name}' is not defined in following files:\n"
            error_message += "\n".join(program.related_files)
            raise NameError(error_message)

        if name not in self._uniform_var_map:
            self._uniform_var_map[name] = Uniform.Variable(id(self), name)

        return self._uniform_var_map[name]

    def __setitem__(self, name:str, value):
        program = self.program
        if GlassConfig.debug and name not in program._uniform_map:
            error_message = f"uniform variable '{name}' is not defined in following files:\n"
            error_message += "\n".join(program.related_files)
            raise NameError(error_message)

        for atom in program._uniform_map[name]["atoms"]:
            atom_value = subscript(value, atom["subscript_chain"])
            self._set_atom(atom["name"], atom_value)

    @checktype
    def __contains__(self, name:str):
        return (name in self.program._uniform_map)

    @staticmethod
    def _copy(value):
        type_str = type(value).__name__
        if "sampler" in type_str or "image" in type_str:
            return value
        else:
            return copy.copy(value)

    def _set_atom(self, name:str, value):
        if name in self._atom_value_map and self._atom_value_map[name] == value:
            if isinstance(value, FBOAttachment):
                value.bind()
            return
        
        if GL.glGetUniformLocation:
            program = self.program
            program.use()

            uniform_info = program._uniform_map[name]
            uniform_type = uniform_info["type"]
            if uniform_type != "atomic_uint":
                location = -1
                if "location" not in uniform_info:
                    location = GL.glGetUniformLocation(program._id, name)
                    uniform_info["location"] = location
                else:
                    location = uniform_info["location"]

                if location == -1:
                    return
                
                self._current_atom_name = name
                func = Uniform._set_atom_func(uniform_type)
                func(self, location, value)
                self._atom_value_map[name] = Uniform._copy(value)
            else:
                binding_point = uniform_info["binding_point"]
                offset = uniform_info["offset"]
                ACBO.set(binding=binding_point, offset=offset, value=value)
        else:
            self._atoms_to_update[name] = Uniform._copy(value)

    @staticmethod
    def _set_atom_func(atom_type):
        if not Uniform._set_atom_map:
            Uniform._set_atom_map = \
            {
                "bool": Uniform._set_bool, "int": Uniform._set_int, "uint": Uniform._set_uint,
                "uint64_t": Uniform._set_uint64_t, "float": Uniform._set_float, "double": Uniform._set_double,
                "bvec2": Uniform._set_bvec2, "bvec3": Uniform._set_bvec3, "bvec4": Uniform._set_bvec4,
                "ivec2": Uniform._set_ivec2, "ivec3": Uniform._set_ivec3, "ivec4": Uniform._set_ivec4,
                "uvec2": Uniform._set_uvec2, "uvec3": Uniform._set_uvec3, "uvec4": Uniform._set_uvec4,
                "vec2": Uniform._set_vec2, "vec3": Uniform._set_vec3, "vec4": Uniform._set_vec4,
                "dvec2": Uniform._set_dvec2, "dvec3": Uniform._set_dvec3, "dvec4": Uniform._set_dvec4,
                "mat2": Uniform._set_mat2, "mat3": Uniform._set_mat3, "mat4": Uniform._set_mat4,
                "dmat2": Uniform._set_dmat2, "dmat3": Uniform._set_dmat3, "dmat4": Uniform._set_dmat4,
                "mat2x2": Uniform._set_mat2x2, "mat2x3": Uniform._set_mat2x3, "mat2x4": Uniform._set_mat2x4,
                "mat3x2": Uniform._set_mat3x2, "mat3x3": Uniform._set_mat3x3, "mat3x4": Uniform._set_mat3x4,
                "mat4x2": Uniform._set_mat4x2, "mat4x3": Uniform._set_mat4x3, "mat4x4": Uniform._set_mat4x4,
                "dmat2x2": Uniform._set_dmat2x2, "dmat2x3": Uniform._set_dmat2x3, "dmat2x4": Uniform._set_dmat2x4,
                "dmat3x2": Uniform._set_dmat3x2, "dmat3x3": Uniform._set_dmat3x3, "dmat3x4": Uniform._set_dmat3x4,
                "dmat4x2": Uniform._set_dmat4x2, "dmat4x3": Uniform._set_dmat4x3, "dmat4x4": Uniform._set_dmat4x4,
            
                "sampler2D": Uniform._set_sampler2D, "isampler2D": Uniform._set_isampler2D, "usampler2D": Uniform._set_usampler2D,
                "image2D": Uniform._set_image2D, "iimage2D": Uniform._set_iimage2D, "uimage2D": Uniform._set_uimage2D,
                "sampler2DMS": Uniform._set_sampler2DMS, "isampler2DMS": Uniform._set_isampler2DMS, "usampler2DMS": Uniform._set_usampler2DMS,
                "samplerCube": Uniform._set_samplerCube, "sampler2DArray": Uniform._set_sampler2DArray
            }
        return Uniform._set_atom_map[atom_type]

    def _set_bool(self, location:int, value):
        if not isinstance(value, int):
            value = int(value)

        GL.glUniform1i(location, value)

    def _set_int(self, location:int, value):
        if isinstance(value, Enum):
            value = int(value.value)

        if not isinstance(value, int):
            value = int(value)

        GL.glUniform1i(location, value)

    def _set_uint(self, location:int, value):
        if isinstance(value, Enum):
            value = int(value.value)

        if not isinstance(value, int):
            value = int(value)
            
        GL.glUniform1ui(location, value)

    def _set_uint64_t(self, location:int, value):
        if not isinstance(value, int):
            value = int(value)

        gsi64.glUniform1ui64ARB(location, value)

    def _set_float(self, location:int, value):
        if not isinstance(value, float):
            value = float(value)

        GL.glUniform1f(location, value)

    def _set_double(self, location:int, value):
        if not isinstance(value, float):
            value = float(value)

        GL.glUniform1d(location, value)

    def _set_bvec2(self, location:int, value:glm.bvec2):
        if not isinstance(value, glm.bvec2):
            value = glm.bvec2(value)

        GL.glUniform2i(location, int(value.x), int(value.y))

    def _set_bvec3(self, location:int, value:glm.bvec3):
        if not isinstance(value, glm.bvec3):
            value = glm.bvec3(value)

        GL.glUniform3i(location, int(value.x), int(value.y), int(value.z))

    def _set_bvec4(self, location:int, value:glm.bvec4):
        if not isinstance(value, glm.bvec4):
            value = glm.bvec4(value)

        GL.glUniform4i(location, int(value.x), int(value.y), int(value.z), int(value.w))

    def _set_ivec2(self, location:int, value:glm.ivec2):
        if not isinstance(value, glm.ivec2):
            value = glm.ivec2(value)

        GL.glUniform2i(location, value.x, value.y)
        
    def _set_ivec3(self, location:int, value:glm.ivec3):
        if not isinstance(value, glm.ivec3):
            value = glm.ivec3(value)

        GL.glUniform3i(location, value.x, value.y, value.z)
        
    def _set_ivec4(self, location:int, value:glm.ivec4):
        if not isinstance(value, glm.ivec4):
            value = glm.ivec4(value)

        GL.glUniform4i(location, value.x, value.y, value.z, value.w)
            
    def _set_uvec2(self, location:int, value:(glm.uvec2,int)):
        if isinstance(value, glm.uvec2):
            GL.glUniform2ui(location, value.x, value.y)
        else:
            if not isinstance(value, int):
                value = int(value)

            used_value = uint64_to_uvec2(value)
            GL.glUniform2ui(location, used_value.x, used_value.y)
            
    def _set_uvec3(self, location:int, value:glm.uvec3):
        if not isinstance(value, glm.uvec3):
            value = glm.uvec3(value)

        GL.glUniform3ui(location, value.x, value.y, value.z)
            
    def _set_uvec4(self, location:int, value:glm.uvec4):
        if not isinstance(value, glm.uvec4):
            value = glm.uvec4(value)

        GL.glUniform4ui(location, value.x, value.y, value.z, value.w)
            
    def _set_vec2(self, location:int, value:glm.vec2):
        if not isinstance(value, glm.vec2):
            value = glm.vec2(value)

        GL.glUniform2f(location, value.x, value.y)
        
    def _set_vec3(self, location:int, value:glm.vec3):
        if not isinstance(value, glm.vec3):
            value = glm.vec3(value)

        GL.glUniform3f(location, value.x, value.y, value.z)
            
    def _set_vec4(self, location:int, value:glm.vec4):
        if not isinstance(value, glm.vec4):
            value = glm.vec4(value)

        GL.glUniform4f(location, value.x, value.y, value.z, value.w)
        
    def _set_dvec2(self, location:int, value:glm.dvec2):
        if not isinstance(value, glm.dvec2):
            value = glm.dvec2(value)

        GL.glUniform2d(location, value.x, value.y)
        
    def _set_dvec3(self, location:int, value:glm.dvec3):
        if not isinstance(value, glm.dvec3):
            value = glm.dvec3(value)

        GL.glUniform3d(location, value.x, value.y, value.z)
            
    def _set_dvec4(self, location:int, value:glm.dvec4):
        if not isinstance(value, glm.dvec4):
            value = glm.dvec4(value)

        GL.glUniform4d(location, value.x, value.y, value.z, value.w)
            
    def _set_mat2(self, location:int, value:glm.mat2):
        if not isinstance(value, glm.mat2):
            value = glm.mat2(value)

        GL.glUniformMatrix2fv(location, 1, False, glm.value_ptr(value))
            
    def _set_mat3x2(self, location:int, value:glm.mat3x2):
        if not isinstance(value, glm.mat3x2):
            value = glm.mat3x2(value)

        GL.glUniformMatrix3x2fv(location, 1, False, glm.value_ptr(value))
        
    def _set_mat4x2(self, location:int, value:glm.mat4x2):
        if not isinstance(value, glm.mat4x2):
            value = glm.mat4x2(value)

        GL.glUniformMatrix4x2fv(location, 1, False, glm.value_ptr(value))
        
    def _set_mat2x3(self, location:int, value:glm.mat2x3):
        if not isinstance(value, glm.mat2x3):
            value = glm.mat2x3(value)

        GL.glUniformMatrix2x3fv(location, 1, False, glm.value_ptr(value))
            
    def _set_mat3(self, location:int, value:glm.mat3x3):
        if not isinstance(value, glm.mat3x3):
            value = glm.mat3x3(value)

        GL.glUniformMatrix3fv(location, 1, False, glm.value_ptr(value))
            
    def _set_mat4x3(self, location:int, value:glm.mat4x3):
        if not isinstance(value, glm.mat4x3):
            value = glm.mat4x3(value)

        GL.glUniformMatrix4x3fv(location, 1, False, glm.value_ptr(value))
            
    def _set_mat2x4(self, location:int, value:glm.mat2x4):
        if not isinstance(value, glm.mat2x4):
            value = glm.mat2x4(value)

        GL.glUniformMatrix2x4fv(location, 1, False, glm.value_ptr(value))
            
    def _set_mat3x4(self, location:int, value:glm.mat3x4):
        if not isinstance(value, glm.mat3x4):
            value = glm.mat3x4(value)

        GL.glUniformMatrix3x4fv(location, 1, False, glm.value_ptr(value))
            
    def _set_mat4(self, location:int, value:glm.mat4x4):
        if not isinstance(value, glm.mat4x4):
            value = glm.mat4x4(value)

        GL.glUniformMatrix4fv(location, 1, False, glm.value_ptr(value))
        
    def _set_mat2x2(self, location:int, value:glm.mat2x2):
        if not isinstance(value, glm.mat2x2):
            value = glm.mat2x2(value)

        GL.glUniformMatrix2fv(location, 1, False, glm.value_ptr(value))
        
    def _set_mat3x3(self, location:int, value:glm.mat3x3):
        if not isinstance(value, glm.mat3x3):
            value = glm.mat3x3(value)

        GL.glUniformMatrix3fv(location, 1, False, glm.value_ptr(value))
        
    def _set_mat4x4(self, location:int, value:glm.mat4x4):
        if not isinstance(value, glm.mat4x4):
            value = glm.mat4x4(value)

        GL.glUniformMatrix4fv(location, 1, False, glm.value_ptr(value))
        
    def _set_dmat2(self, location:int, value:glm.dmat2):
        if not isinstance(value, glm.dmat2):
            value = glm.dmat2(value)

        GL.glUniformMatrix2dv(location, 1, False, glm.value_ptr(value))
            
    def _set_dmat3x2(self, location:int, value:glm.dmat3x2):
        if not isinstance(value, glm.dmat3x2):
            value = glm.dmat3x2(value)

        GL.glUniformMatrix3x2dv(location, 1, False, glm.value_ptr(value))
        
    def _set_dmat4x2(self, location:int, value:glm.dmat4x2):
        if not isinstance(value, glm.dmat4x2):
            value = glm.dmat4x2(value)

        GL.glUniformMatrix4x2dv(location, 1, False, glm.value_ptr(value))
        
    def _set_dmat2x3(self, location:int, value:glm.dmat2x3):
        if not isinstance(value, glm.dmat2x3):
            value = glm.dmat2x3(value)

        GL.glUniformMatrix2x3dv(location, 1, False, glm.value_ptr(value))
            
    def _set_dmat3(self, location:int, value:glm.dmat3x3):
        if not isinstance(value, glm.dmat3x3):
            value = glm.dmat3x3(value)

        GL.glUniformMatrix3dv(location, 1, False, glm.value_ptr(value))
            
    def _set_dmat4x3(self, location:int, value:glm.dmat4x3):
        if not isinstance(value, glm.dmat4x3):
            value = glm.dmat4x3(value)

        GL.glUniformMatrix4x3dv(location, 1, False, glm.value_ptr(value))
            
    def _set_dmat2x4(self, location:int, value:glm.dmat2x4):
        if not isinstance(value, glm.dmat2x4):
            value = glm.dmat2x4(value)

        GL.glUniformMatrix2x4dv(location, 1, False, glm.value_ptr(value))
            
    def _set_dmat3x4(self, location:int, value:glm.dmat3x4):
        if not isinstance(value, glm.dmat3x4):
            value = glm.dmat3x4(value)

        GL.glUniformMatrix3x4dv(location, 1, False, glm.value_ptr(value))
            
    def _set_dmat4(self, location:int, value:glm.dmat4):
        if not isinstance(value, glm.dmat4):
            value = glm.dmat4(value)

        GL.glUniformMatrix4dv(location, 1, False, glm.value_ptr(value))
        
    def _set_dmat2x2(self, location:int, value:glm.dmat2x2):
        if not isinstance(value, glm.dmat2x2):
            value = glm.dmat2x2(value)

        GL.glUniformMatrix2dv(location, 1, False, glm.value_ptr(value))
        
    def _set_dmat3x3(self, location:int, value:glm.dmat3x3):
        if not isinstance(value, glm.dmat3x3):
            value = glm.dmat3x3(value)

        GL.glUniformMatrix3dv(location, 1, False, glm.value_ptr(value))
        
    def _set_dmat4x4(self, location:int, value:glm.dmat4x4):
        if not isinstance(value, glm.dmat4x4):
            value = glm.dmat4x4(value)

        GL.glUniformMatrix4dv(location, 1, False, glm.value_ptr(value))
        
    @checktype
    def _set_sampler2D(self, location:int, value:(sampler2D,str), sampler_type:[sampler2D,isampler2D,usampler2D]=sampler2D):
        if isinstance(value, str):
            value = sampler_type.load(value)

        if value is not None:
            value.bind()

        program = self.program
        program._sampler_map[self._current_atom_name]["location"] = location
        program._sampler_map[self._current_atom_name]["sampler"] = value
        
    @checktype
    def _set_isampler2D(self, location:int, value:(isampler2D,str)):
        self._set_sampler2D(location, value, isampler2D)
        
    @checktype
    def _set_usampler2D(self, location:int, value:(usampler2D,str)):
        self._set_sampler2D(location, value, usampler2D)
        
    @checktype
    def _set_sampler2DMS(self, location:int, value:sampler2DMS):
        if value is not None:
            value.bind()

        program = self.program
        program._sampler_map[self._current_atom_name]["location"] = location
        program._sampler_map[self._current_atom_name]["sampler"] = value
        
    @checktype
    def _set_isampler2DMS(self, location:int, value:isampler2DMS):
        self._set_sampler2DMS(location, value)
        
    @checktype
    def _set_usampler2DMS(self, location:int, value:usampler2DMS):
        self._set_sampler2DMS(location, value)
        
    @checktype
    def _set_sampler2DArray(self, location:int, value:sampler2DArray):
        if value is not None:
            value.bind()

        program = self.program
        program._sampler_map[self._current_atom_name]["location"] = location
        program._sampler_map[self._current_atom_name]["sampler"] = value

    def __set_general_image2D(self, location:int, value:(image2D,iimage2D,uimage2D,str), image_type:[image2D,iimage2D,uimage2D]=image2D):
        if isinstance(value, str):
            value = image_type.load(value, internal_format=self._current_internal_format)

        access = GL.GL_READ_WRITE
        program = self.program
        memory_qualifiers = program._uniform_map[self._current_atom_name]["memory_qualifiers"]
        internal_format = program._uniform_map[self._current_atom_name]["internal_format"]
        if value is not None:
            if GlassConfig.debug and internal_format != value.internal_format:
                raise ValueError(f"uniform image2D {self._current_atom_name} need format {internal_format}, {value.internal_format} were given")

            access = GL.GL_READ_WRITE
            if "readonly" in memory_qualifiers:
                access = GL.GL_READ_ONLY
            elif "writeonly" in memory_qualifiers:
                access = GL.GL_WRITE_ONLY
            
            value.bind()
            
        program._sampler_map[self._current_atom_name]["location"] = location
        program._sampler_map[self._current_atom_name]["access"] = access
        program._sampler_map[self._current_atom_name]["sampler"] = value
        
    @checktype
    def _set_iimage2D(self, location:int, value:(iimage2D,str)):
        self.__set_general_image2D(location, value, image_type=iimage2D)
        
    @checktype
    def _set_uimage2D(self, location:int, value:(uimage2D,str)):
        self.__set_general_image2D(location, value, image_type=uimage2D)
        
    @checktype
    def _set_image2D(self, location:int, value:(image2D,str)):
        self.__set_general_image2D(location, value, image_type=image2D)
        
    @checktype
    def _set_samplerCube(self, location:int, value:samplerCube):
        if value is not None and not value.is_completed:
            raise RuntimeError("not completed samplerCube")

        if value is not None:
            value.bind()

        program = self.program
        program._sampler_map[self._current_atom_name]["sampler"] = value
        program._sampler_map[self._current_atom_name]["location"] = location
