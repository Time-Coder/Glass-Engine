import os

import cv2
import numpy as np
import glm
from OpenGL import GL
import OpenGL.GL.ARB.bindless_texture as bt
import time
from datetime import datetime

from .FBOAttachment import FBOAttachment
from .GLInfo import GLInfo
from .utils import checktype, cat, modify_time, md5s, relative_path, is_text_file
from .helper import get_external_format, width_adapt, get_dtype, get_channels
from .ImageLoader import ImageLoader
from .Indices import Indices
from .Vertices import Vertices, Vertex
from .GLConfig import GLConfig
from .GlassConfig import GlassConfig

class sampler2D(FBOAttachment):

    _default_internal_format = GL.GL_RGBA32F
    _default_filter_min = GL.GL_LINEAR
    _default_filter_mag = GL.GL_LINEAR
    _default_filter_mipmap = GL.GL_LINEAR

    _sampler2D_map = {}
    _should_update = False
    __shadertoy_template_content = ""
    __shadertoy_template_filename = os.path.dirname(os.path.abspath(__file__)) + "/glsl/shadertoy_template.glsl"

    _basic_info = \
    {
        "gen_func": GL.glGenTextures,
        "bind_func": GL.glBindTexture,
        "del_func": GL.glDeleteTextures,
        "target_type": GL.GL_TEXTURE_2D,
        "binding_type": GL.GL_TEXTURE_BINDING_2D,
        "need_number": True,
    }

    @checktype
    def __init__(self, image:(str,np.ndarray)=None, width:int=None, height:int=None, internal_format:GLInfo.internal_formats=None):
        FBOAttachment.__init__(self)
        
        self._handle = 0
        self._file_name = ""
        self._image = None
        self._width = 0
        self._height = 0
        self._internal_format = self.__class__._default_internal_format

        self._wrap_s = GL.GL_REPEAT
        self._wrap_t = GL.GL_REPEAT
        self._filter_min = self.__class__._default_filter_min
        self._filter_mag = self.__class__._default_filter_mag
        self._filter_mipmap = self.__class__._default_filter_mipmap
        self._border_color = glm.vec4(0, 0, 0, 1)

        self._image_changed = True
        self._wrap_s_changed = True
        self._wrap_t_changed = True
        self._filter_min_changed = True
        self._filter_mag_changed = True
        self._border_color_changed = False

        # shadertoy
        self._shadertoy_program = None
        self._shadertoy_path = None
        self._shadertoy_start_time = 0
        self._shadertoy_last_frame_time = 0
        self._shadertoy_frame_index = 0
        self._should_update_shadertoy = True
        self.__frame_vertices = None
        self.__frame_indices = None

        if image is not None:
            self.image = image

        if width is not None:
            self.width = width

        if height is not None:
            self.height = height

        if internal_format is not None:
            self.internal_format = internal_format

    def __hash__(self):
        return id(self)

    def __deepcopy__(self, memo):
        result = self.__class__()
        result._image = self._image
        result._width = self._width
        result._height = self._height
        result._internal_format = self._internal_format

        result._wrap_s = self._wrap_s
        result._wrap_t = self._wrap_t
        result._filter_min = self._filter_min
        result._filter_mag = self._filter_mag
        result._filter_mipmap = self._filter_mipmap
        result._border_color = self._border_color
        result._dynamic = self._dynamic

        result._shadertoy_program = None
        result._shadertoy_path = self._shadertoy_path
        result._shadertoy_start_time = self._shadertoy_start_time
        result._shadertoy_last_frame_time = self._shadertoy_last_frame_time
        result._shadertoy_frame_index = self._shadertoy_frame_index
        if self._shadertoy_program is not None:
            result.__init_shadertoy(self._shadertoy_path)

        return result

    def __del__(self):
        if self._handle != 0:
            self._handle = 0

        FBOAttachment.__del__(self)

    @property
    def is_shadertoy(self)->bool:
        return bool(self._shadertoy_path)

    @classmethod
    def load(cls, file_name:str, internal_format:GLInfo.internal_formats=None):
        if not os.path.isfile(file_name):
            raise FileNotFoundError("not a valid image file: " + file_name)
        
        file_name = os.path.abspath(file_name).replace("\\", "/")
        if file_name not in sampler2D._sampler2D_map:
            sampler = cls(file_name, internal_format=internal_format)
            sampler._dynamic = False
            sampler2D._sampler2D_map[file_name] = sampler

        return sampler2D._sampler2D_map[file_name]

    @property
    def handle(self):
        if not bt.glGetTextureHandleARB:
            return 0
        
        self.bind()
        if self._handle == 0:
            self._handle = bt.glGetTextureHandleARB(self._id)
            if self._handle == 0:
                raise RuntimeError(f"failed to create sampler2D {self._id}'s handle")
            bt.glMakeTextureHandleResidentARB(self._handle)            
            self._dynamic = False

        return self._handle

    def bind(self, update_fbo:bool=False, force_update_image:bool=False):
        if self._should_update_shadertoy and self._shadertoy_program is not None and (self.fbo.context == 0 or self.fbo.context == GLConfig.buffered_current_context):
            self.__update_shadertoy()

        FBOAttachment.bind(self, update_fbo)

        if self._wrap_s_changed:
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, self._wrap_s)
            self._wrap_s_changed = False
        if self._wrap_t_changed:
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, self._wrap_t)
            self._wrap_t_changed = False
        if self._border_color_changed:
            GL.glTexParameterfv(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_BORDER_COLOR, glm.value_ptr(self._border_color))
            self._border_color_changed = False

        if self._filter_min_changed:
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, self._get_filter_min())
            self._filter_min_changed = False
        if self._filter_mag_changed:
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, self._filter_mag)
            self._filter_mag_changed = False

        generated_mipmap = False
        if force_update_image or self._image_changed:
            external_format = get_external_format(self._internal_format)
            width_adapt(self._width)
            GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, self._internal_format,
                            self._width, self._height, 0, external_format, self.dtype, self._image)
            
            if not update_fbo and self._filter_mipmap is not None and self._image is not None:
                self.generate_mipmap()
                generated_mipmap = True

            self._image_changed = False

        if not update_fbo and not generated_mipmap and not self._fbo_image_generated_mipmap:
            if self._filter_mipmap is not None:
                self.generate_mipmap()

            self._fbo_image_generated_mipmap = True

    def generate_mipmap(self):
        FBOAttachment.bind(self)
        GL.glGenerateMipmap(GL.GL_TEXTURE_2D)

    def clear(self):
        if self._id == 0:
            return

        self.bind()
        external_format = get_external_format(self._internal_format)
        dtype = get_dtype(self._internal_format)
        GL.glClearTexImage(self._id, 0, external_format, dtype, None)

    @property
    def width(self):
        return self._width

    @width.setter
    @FBOAttachment.param_setter
    def width(self, width:int):
        self._width = width
        if self._image is not None:
            if len(self._image.shape) > 2:
                cv2.resize(self._image, (width, self._image.shape[0], self._image.shape[2]))
            else:
                cv2.resize(self._image, (width, self._image.shape[0]))

        self._image_changed = True

    @property
    def height(self):
        return self._height

    @height.setter
    @FBOAttachment.param_setter
    def height(self, height:int):
        self._height = height
        if self._image is not None:
            if len(self._image.shape) > 2:
                cv2.resize(self._image, (self._image.shape[1], height, self._image.shape[2]))
            else:
                cv2.resize(self._image, (self._image.shape[1], height))

        self._image_changed = True

    @property
    def dtype(self):
        return get_dtype(self._internal_format)

    @property
    def internal_format(self):
        return self._internal_format

    def _set_internal_format(self, internal_format):
        self._internal_format = internal_format

        if self._image is not None:
            old_channels = self._image.shape[2] if len(self._image.shape) > 2 else 1
            new_channels = get_channels(internal_format)
            convert_map = \
            {
                (1,3): cv2.COLOR_GRAY2RGB,
                (1,4): cv2.COLOR_GRAY2RGBA,
                (3,1): cv2.COLOR_RGB2GRAY,
                (3,4): cv2.COLOR_RGB2RGBA,
                (4,1): cv2.COLOR_RGBA2GRAY,
                (4,3): cv2.COLOR_RGBA2RGB
            }
            if (old_channels,new_channels) in convert_map:
                conversion = convert_map[(old_channels,new_channels)]
                self._image = cv2.cvtColor(self._image, conversion)
            elif old_channels == 1:
                if len(self._image.shape) == 2:
                    self._image = np.expand_dims(self._image, axis=2)
                self._image = self._image.repeat(new_channels, axis=2)
            elif new_channels > old_channels:
                self._image = np.append(self._image, np.zeros((self._image.shape[0], self._image.shape[1], new_channels-old_channels), dtype=self._image.dtype), axis=2)
            elif new_channels < old_channels:
                self._image = self._image[:, :, :new_channels]

        if self._image is not None:
            old_np_dtype = self._image.dtype
            new_np_dtype = GLInfo.dtype_map[get_dtype(self._internal_format)]
            if old_np_dtype != new_np_dtype:
                if "int" in str(old_np_dtype) and "float" in str(new_np_dtype):
                    self._image = (self._image / 255).astype(new_np_dtype)
                elif "float" in str(old_np_dtype) and "int" in str(new_np_dtype):
                    self._image = (self._image * 255).astype(new_np_dtype)
                else:
                    self._image = self._image.astype(new_np_dtype)

        self._image_changed = True

    @internal_format.setter
    @FBOAttachment.param_setter
    def internal_format(self, internal_format:GLInfo.internal_formats):
        self._set_internal_format(internal_format)

    @property
    def wrap_s(self):
        return self._wrap_s

    @wrap_s.setter
    @FBOAttachment.param_setter
    def wrap_s(self, wrap_type:GLInfo.wrap_types):
        self._wrap_s = wrap_type
        self._wrap_s_changed = True

    @property
    def wrap_t(self):
        return self._wrap_t

    @wrap_t.setter
    @FBOAttachment.param_setter
    def wrap_t(self, wrap_type:GLInfo.wrap_types):
        self._wrap_t = wrap_type
        self._wrap_t_changed = True

    @property
    def wrap(self):
        return self._wrap_s, self._wrap_t

    @wrap.setter
    @FBOAttachment.param_setter
    def wrap(self, wrap_type):
        if wrap_type in GLInfo.wrap_types:
            self.wrap_s = wrap_type
            self.wrap_t = wrap_type
        else:
            self.wrap_s = wrap_type[0]
            self.wrap_t = wrap_type[1]

    @property
    def filter_min(self):
        return self._filter_min

    @filter_min.setter
    @FBOAttachment.param_setter
    def filter_min(self, filter_type:GLInfo.filter_types):
        self._filter_min = filter_type
        self._filter_min_changed = True

    @property
    def filter_mag(self):
        return self._filter_mag

    @filter_mag.setter
    @FBOAttachment.param_setter
    def filter_mag(self, filter_type:GLInfo.filter_types):
        self._filter_mag = filter_type
        self._filter_mag_changed = True

    @property
    def filter_mipmap(self):
        return self._filter_mipmap

    @filter_mipmap.setter
    @FBOAttachment.param_setter
    def filter_mipmap(self, filter_type:GLInfo.filter_types):
        self._filter_mipmap = filter_type
        self._filter_min_changed = True
        self._filter_mag_changed = True

    def _get_filter_min(self):
        if self._filter_mipmap is None:
            return self._filter_min
        else:
            return GLInfo.mipmap_filter_map[(self._filter_min, self._filter_mipmap)]
        
    @property
    def filter(self):
        return self._filter_min, self._filter_mag, self._filter_mipmap

    @filter.setter
    @FBOAttachment.param_setter
    def filter(self, filter_type):
        if filter_type in GLInfo.filter_types:
            self.filter_min = filter_type
            self.filter_mag = filter_type
            self.filter_mipmap = filter_type
        else:
            self.filter_min = filter_type[0]
            self.filter_mag = filter_type[1]
            if len(filter_type) > 2:
                self.filter_mipmap = filter_type[2]

    @property
    def border_color(self):
        return self._border_color

    @border_color.setter
    @FBOAttachment.param_setter
    def border_color(self, color:(glm.vec3, glm.vec4)):
        if isinstance(color, glm.vec3):
            color = glm.vec4(color, 1)

        self._border_color = color
        self._border_color_changed = True

    @property
    def file_name(self):
        return self._file_name

    @property
    def image(self):
        if self._fbo_image_changed:
            self._image = self._fbo.data(self._fbo_attach_point)
            self._image_changed = False
            self._fbo_image_changed = False

        return self._image

    @image.setter
    @FBOAttachment.param_setter
    def image(self, image:(np.ndarray,str)):
        if isinstance(image, str):
            self._file_name = os.path.abspath(image).replace("\\", "/")
        else:
            self._file_name = ""

        is_shadertoy = False
        if isinstance(image, str):
            try:
                image = ImageLoader.load(image)
            except ValueError as e:
                if is_text_file(image):
                    is_shadertoy = True
                else:
                    raise e

        self._shadertoy_program = None
        self._shadertoy_path = None
        self._shadertoy_start_time = 0
        self._shadertoy_last_frame_time = 0
        self._shadertoy_frame_index = 0

        if not is_shadertoy:
            self._image = image
            self._width = self._image.shape[1]
            self._height = self._image.shape[0]

            channels = self._image.shape[2] if len(self._image.shape) > 2 else 1
            self._internal_format = GLInfo.internal_formats_map[self._image.dtype][channels]
            self._image_changed = True
        else:
            self.__init_shadertoy(image)

    @checktype
    def malloc(self, width:int, height:int, samples:int=None, layers:int=None, internal_format:GLInfo.internal_formats=None):        
        self.width = width
        self.height = height

        if internal_format is None:
            internal_format = self.internal_format

        if internal_format is None:
            internal_format = self.__class__._default_internal_format

        self.internal_format = internal_format

    @property
    def is_completed(self):
        return (self._width > 0 and self._height > 0)
    
    def __getitem__(self, name:str):
        if self._shadertoy_program is None:
            raise RuntimeError("not a shader defined sampler2D")
        
        return self._shadertoy_program[name]
    
    def __setitem__(self, name:str, value):
        if self._shadertoy_program is None:
            raise RuntimeError("not a shader defined sampler2D")
        
        self._shadertoy_program[name] = value

    @property
    def samples(self):
        return None
    
    @samples.setter
    def samples(self, samples:int):
        pass

    def __init_shadertoy(self, shader_path):
        from .ShaderProgram import ShaderProgram
        from .FBO import FBO

        if self._width == 0:
            self._width = 800
        if self._height == 0:
            self._height = 800

        self._shadertoy_path = shader_path
        if not os.path.isfile(shader_path):
            raise FileNotFoundError(shader_path)
        
        shader_path = os.path.abspath(shader_path).replace("\\", "/")
        base_name = os.path.basename(shader_path)
        out_file_name = GlassConfig.cache_folder + "/" + base_name + "_" + md5s(shader_path) + ".glsl"
        if modify_time(sampler2D.__shadertoy_template_filename) > modify_time(out_file_name):
            out_file = open(out_file_name, "w")
            out_file.write(sampler2D.__shadertoy_template(shader_path))
            out_file.close()

        program = ShaderProgram()
        program.compile(os.path.dirname(os.path.abspath(__file__)) + "/glsl/draw_frame.vs")
        program.compile(out_file_name, GL.GL_FRAGMENT_SHADER)

        fbo = FBO(self.width, self.height)
        fbo.attach(0, attachment=self)

        self._shadertoy_program = program

    @staticmethod
    def __shadertoy_template(file_name):
        if not sampler2D.__shadertoy_template_content:
            sampler2D.__shadertoy_template_content = cat(sampler2D.__shadertoy_template_filename)
        
        rel_path = relative_path(file_name, GlassConfig.cache_folder)
        return sampler2D.__shadertoy_template_content.replace("{file_name}", rel_path)

    @property
    def _frame_vertices(self):
        if self.__frame_vertices is None:
            self.__frame_vertices = Vertices()
            self.__frame_vertices[0] = Vertex(position=glm.vec2(-1, -1))
            self.__frame_vertices[1] = Vertex(position=glm.vec2(1, -1))
            self.__frame_vertices[2] = Vertex(position=glm.vec2(1, 1))
            self.__frame_vertices[3] = Vertex(position=glm.vec2(-1, 1))

        return self.__frame_vertices
    
    @property
    def _frame_indices(self):
        if self.__frame_indices is None:
            self.__frame_indices = Indices()
            self.__frame_indices[0] = glm.uvec3(0, 1, 2)
            self.__frame_indices[1] = glm.uvec3(0, 2, 3)

        return self.__frame_indices

    def __update_shadertoy(self):
        self._should_update_shadertoy = False

        is_dynamic = (self._shadertoy_program["iTime"].location != -1 or \
                      self._shadertoy_program["iTimeDelta"].location != -1 or \
                      self._shadertoy_program["iFrameRate"].location != -1 or \
                      self._shadertoy_program["iFrame"].location != -1 or \
                      self._shadertoy_program["iChannelTime"].location != -1 or \
                      self._shadertoy_program["iDate"].location != -1)
        if is_dynamic:
            sampler2D._should_update = True

        current_time = time.time()
        now = datetime.now()

        if self._shadertoy_start_time == 0:
            self._shadertoy_start_time = current_time
        if self._shadertoy_last_frame_time == 0:
            self._shadertoy_last_frame_time = current_time
        
        time_delta = current_time - self._shadertoy_last_frame_time
        fps = 60
        if time_delta > 0:
            fps = 1/time_delta
        t = current_time - self._shadertoy_start_time
        
        with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):
            with self.fbo:
                resolution = glm.vec3(self._width, self._height, 1)
                self._shadertoy_program["iResolution"] = resolution
                self._shadertoy_program["iChannelResolution"] = [resolution] * 4
                self._shadertoy_program["iTime"] = t
                self._shadertoy_program["iTimeDelta"] = time_delta
                self._shadertoy_program["iFrameRate"] = fps
                self._shadertoy_program["iFrame"] = self._shadertoy_frame_index
                self._shadertoy_program["iChannelTime"] = [t, t, t, t]
                self._shadertoy_program["iDate"] = glm.vec4(now.year, now.month, now.day, now.second + now.microsecond/1000)
                self._shadertoy_program["iSampleRate"] = 44100
                
                self._shadertoy_last_frame_time = current_time
                self._shadertoy_frame_index += 1
                self._shadertoy_program.draw_triangles(self._frame_vertices, self._frame_indices)
        
        self._should_update_shadertoy = True
