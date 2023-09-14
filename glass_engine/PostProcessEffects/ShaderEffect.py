from .PostProcessEffect import PostProcessEffect
from ..Frame import Frame

from glass.utils import checktype, cat, md5s, relative_path, modify_time
from glass import FBO, ShaderProgram, sampler2D, GLConfig, GlassConfig, GLInfo

from OpenGL import GL
import os
import time
import glm
from datetime import datetime

class ShaderEffect(PostProcessEffect):

    __template_content = ""
    __template_filename = os.path.dirname(os.path.abspath(__file__)) + "/../glsl/PostProcessEffects/shader_effect_template.glsl"

    @checktype
    def __init__(self, shader_path:str=None, internal_format:GLInfo.internal_formats=GL.GL_RGBA32F, generate_mipmap:bool=False):
        PostProcessEffect.__init__(self)
        
        self._dynamic = False
        self._internal_format = internal_format
        self._generate_mipmap = generate_mipmap

        self._fbo = None
        self._program = None
        self._fragment_filename = ""
        self._uniforms = {}

        self._shader_path = ""
        self._start_time = 0
        self._last_frame_time = 0
        self._frame_index = 0
        
        if shader_path is not None:
            self.shader_path = shader_path

    @property
    def fbo(self):
        if self._fbo is None:
            self._fbo = FBO()
            self._fbo.attach(0, sampler2D, self._internal_format)
        return self._fbo

    def __hash__(self):
        return id(self)

    @property
    def shader_path(self):
        return self._shader_path

    @shader_path.setter
    @checktype
    def shader_path(self, shader_path:str):
        current_file_path = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isfile(shader_path) and not os.path.isabs(shader_path):
            shader_path = current_file_path + "/" + shader_path

        if not os.path.isfile(shader_path):
            raise FileNotFoundError(shader_path)

        shader_path = os.path.abspath(shader_path).replace("\\", "/")
        if shader_path == self._shader_path:
            return
        
        file_base_name = os.path.basename(shader_path)
        dest_file_name = GlassConfig.cache_folder + "/" + file_base_name + "_" + md5s(shader_path) + ".glsl"
        if modify_time(ShaderEffect.__template_filename) > modify_time(dest_file_name):
            out_file = open(dest_file_name, "w")
            out_file.write(ShaderEffect.__template(shader_path))
            out_file.close()

        self._fragment_filename = dest_file_name
        self._shader_path = shader_path

    @property
    def program(self):
        if self._fragment_filename:
            self._program = ShaderProgram()
            self._program.compile(Frame.draw_frame_vs)
            self._program.compile(self._fragment_filename, GL.GL_FRAGMENT_SHADER)
            self._fragment_filename = ""

        if self._uniforms and self._program is not None:
            for name, value in self._uniforms.items():
                self._program[name] = value
            self._uniforms.clear()

        return self._program

    def draw(self, screen_image:sampler2D)->sampler2D:
        if self._generate_mipmap:
            screen_image.filter_mipmap = GL.GL_LINEAR

        if self.camera is not None:
            self.program["camera"] = self.camera
            
        self.program["depth_map"] = self.depth_map
        self.program["view_pos_map"] = self.view_pos_map
        self.program["view_normal_map"] = self.view_normal_map
        self.program["screen_image"] = screen_image
        self._dynamic = (self.program["iTime"].location != -1 or \
                         self.program["iTimeDelta"].location != -1 or \
                         self.program["iFrameRate"].location != -1 or \
                         self.program["iFrame"].location != -1 or \
                         self.program["iDate"].location != -1)

        if self._dynamic:
            current_time = time.time()
            now = datetime.now()

            if self._start_time == 0:
                self._start_time = current_time
            if self._last_frame_time == 0:
                self._last_frame_time = current_time
            
            time_delta = current_time - self._last_frame_time
            fps = 60
            if time_delta > 0:
                fps = 1/time_delta
            t = current_time - self._start_time
            
            self.program["iTime"] = t
            self.program["iTimeDelta"] = time_delta
            self.program["iFrameRate"] = fps
            self.program["iFrame"] = self._frame_index
            self.program["iDate"] = glm.vec4(now.year, now.month, now.day, now.second + now.microsecond/1000)
            
            self._last_frame_time = current_time
            self._frame_index += 1
            
        self.program.draw_triangles(Frame.vertices, Frame.indices)

    def draw_to_active(self, screen_image:sampler2D)->None:
        with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):
            self.draw(screen_image)

    def apply(self, screen_image:sampler2D)->sampler2D:
        self.fbo.resize(screen_image.width, screen_image.height)
        with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):
            with self.fbo:
                self.draw(screen_image)

        return self.fbo.color_attachment(0)
    
    def __getitem__(self, name:str):
        if self._program is None:
            return self._uniforms[name]
        else:
            return self._program[name]
    
    def __setitem__(self, name:str, value):
        if self._program is None:
            self._uniforms[name] = value
        else:
            self.program[name] = value

    @property
    def should_update(self):
        if not self.enabled:
            return False
        
        return (self._should_update or self._dynamic)
    
    @should_update.setter
    def should_update(self, flag:bool):
        self._should_update = flag

    def need_pos_info(self)->bool:
        return (self.program["view_pos_map"].location >= 0 or \
                self.program["view_normal_map"].location >= 0 or \
                self.program["depth_map"].location >= 0)

    @staticmethod
    def __template(file_name):
        if not ShaderEffect.__template_content:
            ShaderEffect.__template_content = cat(ShaderEffect.__template_filename)
        
        rel_path = relative_path(file_name, GlassConfig.cache_folder)
        return ShaderEffect.__template_content.replace("{file_name}", rel_path)
