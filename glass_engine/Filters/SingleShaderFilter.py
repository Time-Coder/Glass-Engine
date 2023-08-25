from .Filters import Filter
from ..Frame import Frame

from glass.utils import checktype, cat, md5s, relative_path, modify_time
from glass import FBO, ShaderProgram, sampler2D, GLConfig, GlassConfig
from glass.WeakSet import WeakSet

from OpenGL import GL
import os
import time
import glm
from datetime import datetime

class SingleShaderFilter(Filter):

    __template_content = ""
    __template_filename = os.path.dirname(os.path.abspath(__file__)) + "/../glsl/Filters/single_shader_filter_template.glsl"

    _unknown_filters = WeakSet()
    _dynamic_filters = WeakSet()

    @checktype
    def __init__(self, shader_path:str=None):
        Filter.__init__(self)
        
        SingleShaderFilter._unknown_filters.add(self)

        self.fbo = FBO()
        self.fbo.attach(0, sampler2D, GL.GL_RGBA32F)

        self._shader_path = ""
        self._start_time = 0
        self._last_frame_time = 0
        self._frame_index = 0
        
        if shader_path is not None:
            self.shader_path = shader_path
    
    def __del__(self):
        if self in SingleShaderFilter._unknown_filters:
            SingleShaderFilter._unknown_filters.remove(self)

        if self in SingleShaderFilter._dynamic_filters:
            SingleShaderFilter._dynamic_filters.remove(self)

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
        if modify_time(SingleShaderFilter.__template_filename) > modify_time(dest_file_name):
            out_file = open(dest_file_name, "w")
            out_file.write(SingleShaderFilter.__template(shader_path))
            out_file.close()

        self.program = ShaderProgram()
        self.program.compile(Frame.draw_frame_vs)
        self.program.compile(dest_file_name, GL.GL_FRAGMENT_SHADER)

        self._shader_path = shader_path

    def draw(self, screen_image):
        self.program["screen_image"] = screen_image
        if self in SingleShaderFilter._unknown_filters:
            is_dynamic = (self.program["iTime"].location != -1 or \
                          self.program["iTimeDelta"].location != -1 or \
                          self.program["iFrameRate"].location != -1 or \
                          self.program["iFrame"].location != -1 or \
                          self.program["iDate"].location != -1)
            
            SingleShaderFilter._unknown_filters.remove(self)
            if is_dynamic:
                SingleShaderFilter._dynamic_filters.add(self)

        if self in SingleShaderFilter._dynamic_filters:
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

    def __call__(self, screen_image:sampler2D)->sampler2D:
        self.fbo.resize(screen_image.width, screen_image.height)
        with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):
            with self.fbo:
                self.draw(screen_image)

        return self.fbo.color_attachment(0)
    
    def __getitem__(self, name:str):
        return self.program[name]
    
    def __setitem__(self, name:str, value):
        self.program[name] = value

    @property
    def should_update(self):
        if not self.enabled:
            return False
        
        return (self._should_update or self in SingleShaderFilter._dynamic_filters)
    
    @should_update.setter
    @checktype
    def should_update(self, flag:bool):
        self._should_update = flag

    @staticmethod
    def __template(file_name):
        if not SingleShaderFilter.__template_content:
            SingleShaderFilter.__template_content = cat(SingleShaderFilter.__template_filename)
        
        rel_path = relative_path(file_name, GlassConfig.cache_folder)
        return SingleShaderFilter.__template_content.replace("{file_name}", rel_path)
