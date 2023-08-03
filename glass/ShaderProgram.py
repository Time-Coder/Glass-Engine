import os

from OpenGL import GL
import pathlib
import inspect
import warnings
import struct
import sys
import copy

from .Uniform import Uniform
from .GPUProgram import GPUProgram, LinkError, LinkWarning
from .Shaders import VertexShader, FragmentShader, GeometryShader, TessControlShader, TessEvaluationShader
from .Vertices import Vertices
from .Indices import Indices
from .Instances import Instances
from .utils import checktype, id_to_var, subscript, md5s, modify_time, save_var, load_var
from .GLInfo import GLInfo
from .GLConfig import GLConfig
from .TextureUnits import TextureUnits
from .ImageUnits import ImageUnits
from .VAO import VAO
from .VBO import VBO
from .EBO import EBO

class ShaderProgram(GPUProgram):

    def __init__(self):
        GPUProgram.__init__(self)
        self.vertex_shader = VertexShader()
        self.fragment_shader = FragmentShader()
        self.geometry_shader = GeometryShader()
        self.tess_ctrl_shader = TessControlShader()
        self.tess_eval_shader = TessEvaluationShader()
        self._binary_file_name = ""
        self._meta_file_name = ""
        self._patch_vertices = 0
        self._context = 0
        self._include_paths = []

    @staticmethod
    def __update_dict(dest_dict, src_dict):
        for key, value in src_dict.items():
            dest_dict[key] = copy.copy(value)

    @checktype
    def add_include_path(self, include_path:str):
        self._include_paths.insert(0, include_path)

    @checktype
    def compile(self, file_name:str, shader_type:GLInfo.shader_types=None):
        if self._is_linked:
            raise RuntimeError("linked shader program cannot compile other shaders")

        if not os.path.isfile(file_name):
            current_frame = inspect.currentframe().f_back.f_back
            calling_path = os.path.dirname(current_frame.f_code.co_filename)
            calling_path = calling_path.replace("\\", "/")
            file_name = calling_path + "/" + file_name
        
        if not os.path.isfile(file_name):
            raise FileNotFoundError(file_name)

        if shader_type is None:
            extention = pathlib.Path(file_name).suffix.lower()
            if extention in GLInfo.shader_ext_map:
                shader_type = GLInfo.shader_ext_map[extention]
            else:
                raise RuntimeError("Not support file type " + extention)

        shader = None
        if shader_type == GL.GL_VERTEX_SHADER:
            shader = VertexShader.load(file_name, include_paths=self._include_paths)
            self.vertex_shader = shader
        elif shader_type == GL.GL_FRAGMENT_SHADER:
            shader = FragmentShader.load(file_name, include_paths=self._include_paths)
            self.fragment_shader = shader
        elif shader_type == GL.GL_GEOMETRY_SHADER:
            shader = GeometryShader.load(file_name, include_paths=self._include_paths)
            self.geometry_shader = shader
        elif shader_type == GL.GL_TESS_CONTROL_SHADER:
            shader = TessControlShader.load(file_name, include_paths=self._include_paths)
            self.tess_ctrl_shader = shader
        elif shader_type == GL.GL_TESS_EVALUATION_SHADER:
            shader = TessEvaluationShader.load(file_name, include_paths=self._include_paths)
            self.tess_eval_shader = shader

        self._attributes_info.update(shader.attributes_info)
        self.__update_dict(self._uniforms_info, shader.uniforms_info)
        self.__update_dict(self._uniform_blocks_info, shader.uniform_blocks_info)
        self.__update_dict(self._shader_storage_blocks_info, shader.shader_storage_blocks_info)
        self._structs_info.update(shader.structs_info)
        self._outs_info.update(shader.outs_info)
        self._is_linked = False

    def _reapply(self):
        self.vertex_shader._apply()
        self.fragment_shader._apply()
        if self.geometry_shader.is_compiled:
            self.geometry_shader._apply()
        if self.tess_ctrl_shader.is_compiled:
            self.tess_ctrl_shader._apply()
        if self.tess_eval_shader.is_compiled:
            self.tess_eval_shader._apply()

        GL.glAttachShader(self._id, self.vertex_shader._id)
        if self.geometry_shader.is_compiled:
            GL.glAttachShader(self._id, self.geometry_shader._id)
        if self.tess_ctrl_shader.is_compiled:
            GL.glAttachShader(self._id, self.tess_ctrl_shader._id)
        if self.tess_eval_shader.is_compiled:
            GL.glAttachShader(self._id, self.tess_eval_shader._id)
        GL.glAttachShader(self._id, self.fragment_shader._id)

        GL.glProgramParameteri(self._id, GL.GL_PROGRAM_BINARY_RETRIEVABLE_HINT, GL.GL_TRUE)
        GL.glLinkProgram(self._id)

        if GLConfig.debug:
            message_bytes = GL.glGetProgramInfoLog(self._id)
            message = message_bytes
            if isinstance(message_bytes, bytes):
                message = str(message_bytes, encoding="utf-8")

            error_messages, warning_messages = self._format_error_warning(message)
            if warning_messages:
                warning_message = "Warning when linking following files:\n  " + \
                                  "\n  ".join(self._get_compiled_files()) + "\n" + \
                                  "\n".join(warning_messages)
                warnings.warn(warning_message, category=LinkWarning)

            if error_messages:
                error_message = "Error when linking following files:\n  " + \
                                "\n  ".join(self._get_compiled_files()) + "\n" + \
                                "\n".join(error_messages)
                raise LinkError(error_message)
            
            status = GL.glGetProgramiv(self._id, GL.GL_LINK_STATUS)
            if status != GL.GL_TRUE:
                raise LinkError(message)
            
        binary_length = int(GL.glGetProgramiv(self._id, GL.GL_PROGRAM_BINARY_LENGTH))
        length = GL.GLsizei()
        binary_format = GL.GLenum()
        binary_data = bytearray(binary_length)
        GL.glGetProgramBinary(self._id, binary_length, length, binary_format, binary_data)
        out_file = open(self._binary_file_name, "wb")
        out_file.write(struct.pack('i', int(binary_format.value)))
        out_file.write(struct.pack('i', binary_length))
        out_file.write(binary_data)
        out_file.close()

        self._apply_uniform_blocks()
        self._apply_shader_storage_blocks()

        meta_info = {}
        meta_info["attributes_info"] = self._attributes_info
        meta_info["uniforms_info"] = self._uniforms_info
        meta_info["uniform_blocks_info"] = self._uniform_blocks_info
        meta_info["shader_storage_blocks_info"] = self._shader_storage_blocks_info
        meta_info["structs_info"] = self._structs_info
        meta_info["outs_info"] = self._outs_info
        meta_info["sampler_map"] = self._sampler_map
        meta_info["uniform_map"] = self._uniform_map
        meta_info["uniform_block_map"] = self._uniform_block_map
        meta_info["shader_storage_block_map"] = self._shader_storage_block_map
        meta_info["include_paths"] = self._include_paths
        save_var(meta_info, self._meta_file_name)

    def _apply(self):
        if not self._linked_but_not_applied:
            return
        
        if self._id == 0:
            self._id = GL.glCreateProgram()
            if self._id == 0:
                raise MemoryError("failed to create ShaderProgram")

        if not self._should_relink:
            in_file = open(self._binary_file_name, "rb")
            binary_format = struct.unpack('i', in_file.read(4))[0]
            binary_length = struct.unpack('i', in_file.read(4))[0]
            binary_data = in_file.read(binary_length)
            in_file.close()

            GL.glProgramBinary(self._id, binary_format, binary_data, binary_length)
            status = GL.glGetProgramiv(self._id, GL.GL_LINK_STATUS)
            if GL.GL_TRUE != status:
                self._reapply()
        else:
            self._reapply()

        self._linked_but_not_applied = False

    def _test_should_relink(self):
        max_compiled_time = 0
        shader_should_recompile = False

        binary_name = os.path.basename(self.vertex_shader.file_name)
        abs_file_names = os.path.abspath(self.vertex_shader.file_name)
        shader_should_recompile = shader_should_recompile or self.vertex_shader._should_recompile
        if self.vertex_shader._meta_mtime > max_compiled_time:
            max_compiled_time = self.vertex_shader._meta_mtime

        if self.geometry_shader.is_compiled:
            binary_name += ("+" + os.path.basename(self.geometry_shader.file_name))
            abs_file_names += ("+" + os.path.abspath(self.geometry_shader.file_name))
            shader_should_recompile = shader_should_recompile or self.geometry_shader._should_recompile
            if self.geometry_shader._meta_mtime > max_compiled_time:
                max_compiled_time = self.geometry_shader._meta_mtime

        if self.tess_ctrl_shader.is_compiled:
            binary_name += ("+" + os.path.basename(self.tess_ctrl_shader.file_name))
            abs_file_names += ("+" + os.path.abspath(self.tess_ctrl_shader.file_name))
            shader_should_recompile = shader_should_recompile or self.tess_ctrl_shader._should_recompile
            if self.tess_ctrl_shader._meta_mtime > max_compiled_time:
                max_compiled_time = self.tess_ctrl_shader._meta_mtime

        if self.tess_eval_shader.is_compiled:
            binary_name += ("+" + os.path.basename(self.tess_eval_shader.file_name))
            abs_file_names += ("+" + os.path.abspath(self.tess_eval_shader.file_name))
            shader_should_recompile = shader_should_recompile or self.tess_eval_shader._should_recompile
            if self.tess_eval_shader._meta_mtime > max_compiled_time:
                max_compiled_time = self.tess_eval_shader._meta_mtime

        binary_name += ("+" + os.path.basename(self.fragment_shader.file_name))
        abs_file_names += ("+" + os.path.abspath(self.fragment_shader.file_name))
        shader_should_recompile = shader_should_recompile or self.fragment_shader._should_recompile
        if self.fragment_shader._meta_mtime > max_compiled_time:
            max_compiled_time = self.fragment_shader._meta_mtime

        file_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        cache_folder = file_dir + "/__glcache__"
        if not os.path.isdir(cache_folder):
            os.makedirs(cache_folder)

        base = cache_folder + "/" + binary_name + "_" + md5s(abs_file_names)
        self._binary_file_name = base + ".bin"
        self._meta_file_name = base + ".meta"

        bin_mtime = modify_time(self._binary_file_name)
        meta_mtime = modify_time(self._meta_file_name)
        if not shader_should_recompile and \
           bin_mtime > 0 and meta_mtime > 0 and \
           max_compiled_time < bin_mtime and \
           max_compiled_time < meta_mtime:
            meta_info = load_var(self._meta_file_name)
            self._attributes_info = meta_info["attributes_info"]
            self._uniforms_info = meta_info["uniforms_info"]
            self._uniform_blocks_info = meta_info["uniform_blocks_info"]
            self._shader_storage_blocks_info = meta_info["shader_storage_blocks_info"]
            self._structs_info = meta_info["structs_info"]
            self._outs_info = meta_info["outs_info"]
            self._sampler_map = meta_info["sampler_map"]
            self._uniform_map = meta_info["uniform_map"]
            self._uniform_block_map = meta_info["uniform_block_map"]
            self._shader_storage_block_map = meta_info["shader_storage_block_map"]
            self._include_paths = meta_info["include_paths"]
            self._should_relink = False
        else:
            self._should_relink = True

        return self._should_relink

    def _link(self):
        if self._is_linked:
            return

        if not self.vertex_shader.is_compiled:
            raise RuntimeError("should compile vertex shader before link")

        if not self.fragment_shader.is_compiled:
            raise RuntimeError("should compile fragment shader before link")

        if self._test_should_relink():
            self._resolve_uniforms()
            self._resolve_uniform_blocks()
            self._resolve_shader_storage_blocks()

            keys = list(self._attributes_info.keys())
            for key in keys:
                if "location" not in self._attributes_info[key]:
                    location = GL.glGetAttribLocation(self._id, self._attributes_info[key]["name"])
                    self._attributes_info[key]["location"] = location
                    self._attributes_info[location] = self._attributes_info[key]

        self._is_linked = True
        self._linked_but_not_applied = True
        if GL.glCreateProgram:
            self._apply()

    def __check_vertices(self, vertices, start_index, total):
        len_vertices = len(vertices)
        if not GLConfig.debug:
            if vertices is not None and total is None:
                total = len_vertices - start_index
            return total

        if vertices is not None and vertices:
            if start_index < 0 or (start_index >= len_vertices and vertices):
                raise IndexError("start index is out of range [0, " + str(len_vertices) + "]")

            if total is None:
                total = len_vertices - start_index

            if total < 0:
                raise IndexError("total number should be positive")

            if start_index + total > len_vertices:
                raise IndexError("end index is larger than array size")

        if not vertices:
            total = 0

        return total
    
    def __check_indices(self, indices, total):
        three_len_indices = 3 * len(indices)
        if not GLConfig.debug:
            if indices is not None and total is None:
                total = three_len_indices
            return total

        if indices is not None and three_len_indices > 0:
            if total is None:
                total = three_len_indices

            if total < 0:
                raise IndexError("total number should be positive")

            if total > three_len_indices:
                raise IndexError("end index is larger than elements size")

        if three_len_indices == 0:
            total = 0

        return total

    def __update_uniforms(self):
        for uniform_var in self._uniform._uniform_var_map.values():
            if uniform_var._bound_var is None:
                continue

            var = None
            id_var = uniform_var._bound_var_id
            try:
                var = id_to_var(id_var)
            except:
                continue
            
            for atom_name, atom_info in Uniform._bound_vars[id_var].items():
                # atom_value = eval("var" + atom_info["suffix"])
                atom_value = subscript(var, atom_info["subscript_chain"])
                self._uniform._set_atom(atom_name, atom_value)

        for atom_name, atom_value in self._uniform._should_update_atoms.items():
            self._uniform._set_atom(atom_name, atom_value)

        self._uniform._should_update_atoms.clear()

        # 绑定所有纹理
        self.use()
        self_used_texture_units = set()
        self_used_image_units = set()
        not_set_samplers = []
        not_set_images = []
        for sampler_info in self._sampler_map.values():
            location = sampler_info["location"]
            if location < 0:
                continue

            target_type = sampler_info["target_type"]
            texture_id = 0
            if sampler_info["sampler"] is not None:
                texture_id = sampler_info["sampler"].id

            texture_unit = None
            if "access" not in sampler_info:
                texture_unit = TextureUnits.unit_of_texture((target_type, texture_id))
                if texture_unit is None:
                    texture_unit = TextureUnits.available_unit
                    if texture_unit is None:
                        not_set_samplers.append(sampler_info)
                        continue
                    GLConfig.active_texture_unit = texture_unit
                    GL.glBindTexture(target_type, texture_id)
                    TextureUnits[texture_unit] = (target_type, texture_id)
                self_used_texture_units.add(texture_unit)
            else:
                texture_unit = ImageUnits.unit_of_image((target_type, texture_id))
                if texture_unit is None:
                    texture_unit = ImageUnits.available_unit
                    if texture_unit is None:
                        not_set_images.append(sampler_info)
                        continue
                
                access = sampler_info["access"]
                internal_format = sampler_info["sampler"].internal_format
                GL.glBindImageTexture(texture_unit, texture_id, 0, GL.GL_FALSE, 0, access, internal_format)
                ImageUnits[texture_unit] = (target_type, texture_id)
                self_used_image_units.add(texture_unit)

            if location not in self.uniform._texture_value_map or \
               self.uniform._texture_value_map[location] != texture_unit:
                GL.glUniform1i(location, texture_unit)
                self.uniform._texture_value_map[location] = texture_unit

        if not_set_samplers:
            available_units = GLConfig.available_texture_units - self_used_texture_units
            it_available_units = iter(available_units)
            for sampler_info in not_set_samplers:
                texture_id = 0
                if sampler_info["sampler"] is not None:
                    texture_id = sampler_info["sampler"].id
                texture_unit = next(it_available_units)
                target_type = sampler_info["target_type"]
                GLConfig.active_texture_unit = texture_unit
                GL.glBindTexture(target_type, texture_id)
                TextureUnits[texture_unit] = (target_type, texture_id)

        if not_set_images:
            available_units = GLConfig.available_image_units - self_used_image_units
            it_available_units = iter(available_units)
            for sampler_info in not_set_images:
                texture_id = 0
                if sampler_info["sampler"] is not None:
                    texture_id = sampler_info["sampler"].id

                texture_unit = next(it_available_units)
                target_type = sampler_info["target_type"]
                access = sampler_info["access"]
                internal_format = sampler_info["sampler"].internal_format
                GL.glBindImageTexture(texture_unit, texture_id, 0, False, 0, access, internal_format)
                ImageUnits[texture_unit] = (target_type, texture_id)

        if self._uniform_not_set_warning and GLConfig.debug:
            not_set_uniforms = []
            for name, uniform_info in self._uniform_map.items():
                if name not in self._uniform._atom_value_map and \
                   "location" not in uniform_info:
                    location = GL.glGetUniformLocation(self._id, name)
                    uniform_info["location"] = location
                    if location != -1:
                        not_set_uniforms.append(name)
                        
            if not_set_uniforms:
                warning_message = "in shader program:\n(\n  "
                warning_message += "\n  ".join(self._get_compiled_files())
                warning_message += "\n): "
                if len(not_set_uniforms) == 1:
                    warning_message += f"uniform variable '{not_set_uniforms[0]}' is not set but used"
                else:
                    warning_message += f"following uniform variables are not set but used:\n"
                    warning_message += "\n".join(not_set_uniforms)
                    
                warnings.warn(warning_message, category=RuntimeWarning)

    def __preprocess_before_draw(self, vertices, indices, instances, start_index, total, times, is_patch):
        if GLConfig.debug:
            if is_patch:
                if not self.tess_ctrl_shader.is_compiled:
                    raise RuntimeError("only shader program that with a tessilation shader can use draw_patches")

                if self._patch_vertices == 0:
                    raise RuntimeError("patch_vertices is not set before call draw_patches")
            else:
                if self.tess_ctrl_shader.is_compiled:
                    raise RuntimeError("shader program with a tessilation shader can only use draw_patches")
        
        if indices is None:
            total = self.__check_vertices(vertices, start_index, total)
        else:
            total = self.__check_indices(indices, total)

        if times is None and instances is not None:
            times = int(len(instances) / instances.divisor)

        self.use()
        self.__update_uniforms()
        if self._uniform_block.auto_upload:
            self._uniform_block.upload()
        if self._shader_storage_block.auto_upload:
            self._shader_storage_block.upload()

        if vertices is not None:
            vertices._apply(self, instances)

        if indices is not None:
            indices._apply()
            if vertices is not None:
                current_context = GLConfig.buffered_current_context
                if (current_context, self, instances) in vertices.vao_map:
                    vertices.vao_map[current_context, self, instances].setEBO(indices.ebo)
                else:
                    total = 0

        return total, times

    @property
    def patch_vertices(self):
        return self._patch_vertices

    @patch_vertices.setter
    @checktype
    def patch_vertices(self, value:int):
        self._patch_vertices = value

    def draw_patches(self,
          vertices:Vertices=None, indices:Indices=None, instances:Instances=None,
          start_index:int=0, total:int=None, times:int=None):

        total, times = self.__preprocess_before_draw(
            vertices, indices, instances,
            start_index, total, times, True)
        
        if (total is not None and total <= 0) or \
           (times is not None and times <= 0):
            return

        GL.glPatchParameteri(GL.GL_PATCH_VERTICES, self._patch_vertices)

        self.use()
        if indices is not None:
            if times is None:
                GL.glDrawElements(GL.GL_PATCHES, total, GL.GL_UNSIGNED_INT, None)
            else:
                GL.glDrawElementsInstanced(GL.GL_PATCHES, total, GL.GL_UNSIGNED_INT, None, times)
        else:
            if total is None:
                total = self._patch_vertices
            if times is None:
                GL.glDrawArrays(GL.GL_PATCHES, start_index, total)
            else:
                GL.glDrawArraysInstanced(GL.GL_PATCHES, start_index, total, times)

    def draw_triangles(self,
            vertices:Vertices=None, indices:Indices=None, instances:Instances=None,
            element_type:GLInfo.triangle_types=GL.GL_TRIANGLES,
            start_index:int=0, total:int=None, times:int=None):

        total, times = self.__preprocess_before_draw(
            vertices, indices, instances,
            start_index, total, times, False)
        
        if (total is not None and total <= 0) or \
           (times is not None and times <= 0):
            return
        
        self.use()
        if indices is not None:
            if times is None:
                GL.glDrawElements(element_type, total, GL.GL_UNSIGNED_INT, None)
            else:
                GL.glDrawElementsInstanced(element_type, total, GL.GL_UNSIGNED_INT, None, times)
        else:
            if times is None:
                GL.glDrawArrays(element_type, start_index, total)
            else:
                GL.glDrawArraysInstanced(element_type, start_index, total, times)

    def draw_points(self,
        vertices:Vertices=None, instances:Instances=None,
        start_index:int=0, total:int=None, times:int=None):

        total, times = self.__preprocess_before_draw(
            vertices, None, instances,
            start_index, total, times, False)
        
        if (total is not None and total <= 0) or \
           (times is not None and times <= 0):
            return
        
        GL.glEnable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)

        self.use()
        if times is None:
            GL.glDrawArrays(GL.GL_POINTS, start_index, total)
        else:
            GL.glDrawArraysInstanced(GL.GL_POINTS, start_index, total, times)

    def draw_lines(self,
        vertices:Vertices=None, indices:Indices=None, instances:Instances=None,
        element_type:GLInfo.line_types=GL.GL_LINE_STRIP,
        start_index:int=0, total:int=None, times:int=None):

        total, times = self.__preprocess_before_draw(
            vertices, indices, instances,
            start_index, total, times, False)
        
        if (total is not None and total <= 0) or \
           (times is not None and times <= 0):
            return
    
        self.use()
        if indices is not None:
            if times is None:
                GL.glDrawElements(element_type, total, GL.GL_UNSIGNED_INT, None)
            else:
                GL.glDrawElementsInstanced(element_type, total, GL.GL_UNSIGNED_INT, None, times)
        else:
            if times is None:
                GL.glDrawArrays(element_type, start_index, total)
            else:
                GL.glDrawArraysInstanced(element_type, start_index, total, times)

    def _get_compiled_files(self):
        result = []

        if self.vertex_shader._file_name:
            result.append(self.vertex_shader._file_name)
        if self.tess_ctrl_shader._file_name:
            result.append(self.tess_ctrl_shader._file_name)
        if self.tess_eval_shader._file_name:
            result.append(self.tess_eval_shader._file_name)
        if self.geometry_shader._file_name:
            result.append(self.geometry_shader._file_name)
        if self.fragment_shader._file_name:
            result.append(self.fragment_shader._file_name)

        return result
