from .PostProcessEffect import PostProcessEffect
from ..Frame import Frame

from glass import FBO, sampler2D, ShaderProgram, GLConfig
from glass.utils import checktype

from OpenGL import GL
import os

class BloomEffect(PostProcessEffect):

    @checktype
    def __init__(self):
        PostProcessEffect.__init__(self)
        
        self._src_width = 0
        self._src_height = 0

        self._bloom_down_fbo_list = []
        
        self._down_program = None
        self._up_program = None
        self._mix_fbo = None
        self._mix_program = None

        self.strength:float = 0.5
        self.threshold:float = 1
        self.blur_times:int = 6

    def need_pos_info(self)->bool:
        return False

    @property
    def down_program(self):
        if self._down_program is None:
            self._down_program = ShaderProgram()
            self._down_program.compile(Frame.draw_frame_vs)
            self._down_program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/PostProcessEffects/bloom_downsampling.fs")
        
        return self._down_program
    
    @property
    def up_program(self):
        if self._up_program is None:
            self._up_program = ShaderProgram()
            self._up_program.compile(Frame.draw_frame_vs)
            self._up_program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/PostProcessEffects/bloom_upsampling.fs")
        
        return self._up_program
    
    @property
    def mix_fbo(self):
        if self._mix_fbo is None:
            self._mix_fbo = FBO()
            self._mix_fbo.attach(0, sampler2D)
        
        return self._mix_fbo
    
    @property
    def mix_program(self):
        if self._mix_program is None:
            self._mix_program = ShaderProgram()
            self._mix_program.compile(Frame.draw_frame_vs)
            self._mix_program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/PostProcessEffects/bloom_mix.fs")
        
        return self._mix_program
    
    def bloom_down_fbo(self, i:int)->FBO:
        if i < len(self._bloom_down_fbo_list):
            return self._bloom_down_fbo_list[i]
        else:
            return None

    def __get_bloom_image(self, screen_image:sampler2D):
        self.__update_fbo_list(screen_image.width, screen_image.height)
        
        with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):
            current_index = 0
            for i in range(self.blur_times):
                down_fbo = self.bloom_down_fbo(i)
                if down_fbo is None:
                    break

                with down_fbo:
                    GLConfig.clear_buffers()
                    self.down_program["threshold"] = self.threshold
                    self.down_program["mip_level"] = i
                    self.down_program["screen_image"] = screen_image
                    self.down_program.draw_triangles(Frame.vertices, Frame.indices)
                screen_image = down_fbo.color_attachment(0)
                current_index = i

            with GLConfig.LocalConfig(blend=True,
                blend_src_rgb=GL.GL_ONE, blend_dest_rgb=GL.GL_ONE,
                blend_src_alpha=GL.GL_ONE, blend_dest_alpha=GL.GL_ONE):
                for i in range(current_index, -1, -1):
                    down_fbo = self.bloom_down_fbo(i)
                    with down_fbo:
                        self.up_program["filter_radius"] = 0.02 * self.strength
                        self.up_program["screen_image"] = screen_image
                        self.up_program.draw_triangles(Frame.vertices, Frame.indices)
                    screen_image = down_fbo.color_attachment(0)

        return screen_image

    def draw_to_active(self, screen_image:sampler2D)->None:
        bloom_image = self.__get_bloom_image(screen_image)
        with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):
            self.mix_program["screen_image"] = screen_image
            self.mix_program["bloom_image"] = bloom_image
            self.mix_program.draw_triangles(Frame.vertices, Frame.indices)

    def apply(self, screen_image:sampler2D)->sampler2D:
        bloom_image = self.__get_bloom_image(screen_image)
        self.mix_fbo.resize(screen_image.width, screen_image.height)
        with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):
            with self.mix_fbo:
                self.mix_program["screen_image"] = screen_image
                self.mix_program["bloom_image"] = bloom_image
                self.mix_program.draw_triangles(Frame.vertices, Frame.indices)
        return self.mix_fbo.color_attachment(0)

    def __update_fbo_list(self, src_width:int, src_height:int):
        if src_width == self._src_width and \
           src_height == self._src_height:
            return
        
        dest_width = 8
        dest_height = int(dest_width / src_width * src_height)

        width_list, height_list = [], []
        width, height = src_width, src_height

        is_width_down = (src_width > dest_width)
        scale = 0.5 if is_width_down else 2
        while (width > dest_width) == is_width_down:
            width = int(width * scale)
            width_list.append(width)

        is_height_down = (height > dest_height)
        scale = 0.5 if is_height_down else 2
        while (height > dest_height) == is_height_down:
            height = int(height * scale)
            height_list.append(height)

        len_width_list = len(width_list)
        len_height_list = len(height_list)
        delta_len = len_height_list - len_width_list

        if delta_len > 0:
            width_list.extend([width_list[-1]]*delta_len)
            len_width_list += delta_len
        elif delta_len < 0:
            height_list.extend([height_list[-1]]*(-delta_len))
            len_height_list -= delta_len

        len_bloom_down_fbo_list = len(self._bloom_down_fbo_list)
        while len_bloom_down_fbo_list < len_width_list:
            fbo = FBO()
            fbo.auto_clear = False
            fbo.attach(0, sampler2D)
            self._bloom_down_fbo_list.append(fbo)
            len_bloom_down_fbo_list += 1

        self.used_length = len_width_list

        for i in range(len_width_list):
            bloom_down_fbo = self._bloom_down_fbo_list[i]

            width = width_list[i]
            height = height_list[i]

            bloom_down_fbo.resize(width, height)

        self._src_width = src_width
        self._src_height = src_height
